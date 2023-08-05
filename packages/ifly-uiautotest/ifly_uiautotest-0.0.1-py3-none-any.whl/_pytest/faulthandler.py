import io
import os
import sys
from typing import Generator
from typing import TextIO

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item
from _pytest.stash import StashKey


fault_handler_stderr_key = StashKey[TextIO]()
fault_handler_originally_enabled_key = StashKey[bool]()


def pytest_addoption(parser: Parser) -> None:
    help = (
        "Dump the traceback of all threads if a test takes "
        "more than TIMEOUT seconds to finish."
    )
    parser.addini("faulthandler_timeout", help, default=0.0)


def pytest_configure(config: Config) -> None:
    import faulthandler

    stderr_fd_copy = os.dup(get_stderr_fileno())
    config.stash[fault_handler_stderr_key] = open(stderr_fd_copy, "w")
    config.stash[fault_handler_originally_enabled_key] = faulthandler.is_enabled()
    faulthandler.enable(file=config.stash[fault_handler_stderr_key])


def pytest_unconfigure(config: Config) -> None:
    import faulthandler

    faulthandler.disable()
    # Close the dup file installed during pytest_configure.
    if fault_handler_stderr_key in config.stash:
        config.stash[fault_handler_stderr_key].close()
        del config.stash[fault_handler_stderr_key]
    if config.stash.get(fault_handler_originally_enabled_key, False):
        # Re-enable the faulthandler if it was originally enabled.
        faulthandler.enable(file=get_stderr_fileno())


def get_stderr_fileno() -> int:
    try:
        fileno = sys.stderr.fileno()
        # The Twisted Logger will return an invalid file descriptor since it is not backed
        # by an FD. So, let's also forward this to the same code path as with pytest-xdist.
        if fileno == -1:
            raise AttributeError()
        return fileno
    except (AttributeError, io.UnsupportedOperation):
        # pytest-xdist monkeypatches sys.stderr with an object that is not an actual file.
        # https://docs.python.org/3/library/faulthandler.html#issue-with-file-descriptors
        # This is potentially dangerous, but the best we can do.
        return sys.__stderr__.fileno()


def get_timeout_config_value(config: Config) -> float:
    return float(config.getini("faulthandler_timeout") or 0.0)


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_protocol(item: Item) -> Generator[None, None, None]:
    timeout = get_timeout_config_value(item.config)
    stderr = item.config.stash[fault_handler_stderr_key]
    if timeout > 0 and stderr is not None:
        import faulthandler

        faulthandler.dump_traceback_later(timeout, file=stderr)
        try:
            yield
        finally:
            faulthandler.cancel_dump_traceback_later()
    else:
        yield


@pytest.hookimpl(tryfirst=True)
def pytest_enter_pdb() -> None:
    """Cancel any traceback dumping due to timeout before entering pdb."""
    import faulthandler

    faulthandler.cancel_dump_traceback_later()


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact() -> None:
    """Cancel any traceback dumping due to an interactive exception being
    raised."""
    import faulthandler

    faulthandler.cancel_dump_traceback_later()
