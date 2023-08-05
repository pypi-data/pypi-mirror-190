"""Terminal reporting of the full testing process.

This is a good source for looking at the various reporting hooks.
"""
import argparse
import datetime
import inspect
import platform
import sys
import warnings
from collections import Counter
from functools import partial
from pathlib import Path
from typing import Any
from typing import Callable
from typing import cast
from typing import ClassVar
from typing import Dict
from typing import Generator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Set
from typing import TextIO
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

import attr
import pluggy

import _pytest._version
from _pytest import nodes
from _pytest import timing
from _pytest._code import ExceptionInfo
from _pytest._code.code import ExceptionRepr
from _pytest._io.wcwidth import wcswidth
from _pytest.compat import final
from _pytest.config import _PluggyPlugin
from _pytest.config import Config
from _pytest.config import ExitCode
from _pytest.config import hookimpl
from _pytest.config.argparsing import Parser
from _pytest.nodes import Item
from _pytest.nodes import Node
from _pytest.pathlib import absolutepath
from _pytest.pathlib import bestrelpath
from _pytest.reports import BaseReport
from _pytest.reports import CollectReport
from _pytest.reports import TestReport

if TYPE_CHECKING:
    from typing_extensions import Literal

    from _pytest.main import Session


REPORT_COLLECTING_RESOLUTION = 0.5

KNOWN_TYPES = (
    "failed",
    "passed",
    "skipped",
    "deselected",
    "xfailed",
    "xpassed",
    "warnings",
    "error",
)

_REPORTCHARS_DEFAULT = "fE"


class MoreQuietAction(argparse.Action):
    """A modified copy of the argparse count action which counts down and updates
    the legacy quiet attribute at the same time.

    Used to unify verbosity handling.
    """

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        default: object = None,
        required: bool = False,
        help: Optional[str] = None,
    ) -> None:
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            default=default,
            required=required,
            help=help,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[object], None],
        option_string: Optional[str] = None,
    ) -> None:
        new_count = getattr(namespace, self.dest, 0) - 1
        setattr(namespace, self.dest, new_count)
        # todo Deprecate config.quiet
        namespace.quiet = getattr(namespace, "quiet", 0) + 1


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group._addoption(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="increase verbosity.",
    )
    group._addoption(
        "--no-header",
        action="store_true",
        default=False,
        dest="no_header",
        help="disable header",
    )
    group._addoption(
        "--no-summary",
        action="store_true",
        default=False,
        dest="no_summary",
        help="disable summary",
    )
    group._addoption(
        "-q",
        "--quiet",
        action=MoreQuietAction,
        default=0,
        dest="verbose",
        help="decrease verbosity.",
    )
    group._addoption(
        "--verbosity",
        dest="verbose",
        type=int,
        default=0,
        help="set verbosity. Default is 0.",
    )
    group._addoption(
        "-r",
        action="store",
        dest="reportchars",
        default=_REPORTCHARS_DEFAULT,
        metavar="chars",
        help="show extra test summary info as specified by chars: (f)ailed, "
        "(E)rror, (s)kipped, (x)failed, (X)passed, "
        "(p)assed, (P)assed with output, (a)ll except passed (p/P), or (A)ll. "
        "(w)arnings are enabled by default (see --disable-warnings), "
        "'N' can be used to reset the list. (default: 'fE').",
    )
    group._addoption(
        "--disable-warnings",
        "--disable-pytest-warnings",
        default=False,
        dest="disable_warnings",
        action="store_true",
        help="disable warnings summary",
    )
    group._addoption(
        "-l",
        "--showlocals",
        action="store_true",
        dest="showlocals",
        default=False,
        help="show locals in tracebacks (disabled by default).",
    )
    group._addoption(
        "--tb",
        metavar="style",
        action="store",
        dest="tbstyle",
        default="auto",
        choices=["auto", "long", "short", "no", "line", "native"],
        help="traceback print mode (auto/long/short/line/native/no).",
    )
    group._addoption(
        "--show-capture",
        action="store",
        dest="showcapture",
        choices=["no", "stdout", "stderr", "log", "all"],
        default="all",
        help="Controls how captured stdout/stderr/log is shown on failed tests. "
        "Default is 'all'.",
    )
    group._addoption(
        "--fulltrace",
        "--full-trace",
        action="store_true",
        default=False,
        help="don't cut any tracebacks (default is to cut).",
    )
    group._addoption(
        "--color",
        metavar="color",
        action="store",
        dest="color",
        default="auto",
        choices=["yes", "no", "auto"],
        help="color terminal output (yes/no/auto).",
    )
    group._addoption(
        "--code-highlight",
        default="yes",
        choices=["yes", "no"],
        help="Whether code should be highlighted (only if --color is also enabled)",
    )

    parser.addini(
        "console_output_style",
        help='console output: "classic", or with additional progress information ("progress" (percentage) | "count").',
        default="progress",
    )


def pytest_configure(config: Config) -> None:
    reporter = TerminalReporter(config, sys.stdout)
    config.pluginmanager.register(reporter, "terminalreporter")
    if config.option.debug or config.option.traceconfig:

        def mywriter(tags, args):
            msg = " ".join(map(str, args))
            reporter.write_line("[traceconfig] " + msg)

        config.trace.root.setprocessor("pytest:config", mywriter)


def getreportopt(config: Config) -> str:
    reportchars: str = config.option.reportchars

    old_aliases = {"F", "S"}
    reportopts = ""
    for char in reportchars:
        if char in old_aliases:
            char = char.lower()
        if char == "a":
            reportopts = "sxXEf"
        elif char == "A":
            reportopts = "PpsxXEf"
        elif char == "N":
            reportopts = ""
        elif char not in reportopts:
            reportopts += char

    if not config.option.disable_warnings and "w" not in reportopts:
        reportopts = "w" + reportopts
    elif config.option.disable_warnings and "w" in reportopts:
        reportopts = reportopts.replace("w", "")

    return reportopts


@hookimpl(trylast=True)  # after _pytest.runner
def pytest_report_teststatus(report: BaseReport) -> Tuple[str, str, str]:
    letter = "F"
    if report.passed:
        letter = "."
    elif report.skipped:
        letter = "s"

    outcome: str = report.outcome
    if report.when in ("collect", "setup", "teardown") and outcome == "failed":
        outcome = "error"
        letter = "E"

    return outcome, letter, outcome.upper()


@attr.s(auto_attribs=True)
class WarningReport:
    """Simple structure to hold warnings information captured by ``pytest_warning_recorded``.

    :ivar str message:
        User friendly message about the warning.
    :ivar str|None nodeid:
        nodeid that generated the warning (see ``get_location``).
    :ivar tuple fslocation:
        File system location of the source of the warning (see ``get_location``).
    """

    message: str
    nodeid: Optional[str] = None
    fslocation: Optional[Tuple[str, int]] = None

    count_towards_summary: ClassVar = True

    def get_location(self, config: Config) -> Optional[str]:
        """Return the more user-friendly information about the location of a warning, or None."""
        if self.nodeid:
            return self.nodeid
        if self.fslocation:
            filename, linenum = self.fslocation
            relpath = bestrelpath(config.invocation_params.dir, absolutepath(filename))
            return f"{relpath}:{linenum}"
        return None


@final
class TerminalReporter:
    def __init__(self, config: Config, file: Optional[TextIO] = None) -> None:
        import _pytest.config

        self.config = config
        self._numcollected = 0
        self._session: Optional[Session] = None
        self._showfspath: Optional[bool] = None

        self.stats: Dict[str, List[Any]] = {}
        self._main_color: Optional[str] = None
        self._known_types: Optional[List[str]] = None
        self.startpath = config.invocation_params.dir
        if file is None:
            file = sys.stdout
        self._tw = _pytest.config.create_terminal_writer(config, file)
        self._screen_width = self._tw.fullwidth
        self.currentfspath: Union[None, Path, str, int] = None
        self.reportchars = getreportopt(config)
        self.hasmarkup = self._tw.hasmarkup
        self.isatty = file.isatty()
        self._progress_nodeids_reported: Set[str] = set()
        self._show_progress_info = self._determine_show_progress_info()
        self._collect_report_last_write: Optional[float] = None
        self._already_displayed_warnings: Optional[int] = None
        self._keyboardinterrupt_memo: Optional[ExceptionRepr] = None

    def _determine_show_progress_info(self) -> "Literal['progress', 'count', False]":
        """Return whether we should display progress information based on the current config."""
        # do not show progress if we are not capturing output (#3038)
        if self.config.getoption("capture", "no") == "no":
            return False
        # do not show progress if we are showing fixture setup/teardown
        if self.config.getoption("setupshow", False):
            return False
        cfg: str = self.config.getini("console_output_style")
        if cfg == "progress":
            return "progress"
        elif cfg == "count":
            return "count"
        else:
            return False

    @property
    def verbosity(self) -> int:
        verbosity: int = self.config.option.verbose
        return verbosity

    @property
    def showheader(self) -> bool:
        return self.verbosity >= 0

    @property
    def no_header(self) -> bool:
        return bool(self.config.option.no_header)

    @property
    def no_summary(self) -> bool:
        return bool(self.config.option.no_summary)

    @property
    def showfspath(self) -> bool:
        if self._showfspath is None:
            return self.verbosity >= 0
        return self._showfspath

    @showfspath.setter
    def showfspath(self, value: Optional[bool]) -> None:
        self._showfspath = value

    @property
    def showlongtestinfo(self) -> bool:
        return self.verbosity > 0

    def hasopt(self, char: str) -> bool:
        char = {"xfailed": "x", "skipped": "s"}.get(char, char)
        return char in self.reportchars

    def write_fspath_result(self, nodeid: str, res, **markup: bool) -> None:
        fspath = self.config.rootpath / nodeid.split("::")[0]
        if self.currentfspath is None or fspath != self.currentfspath:
            if self.currentfspath is not None and self._show_progress_info:
                self._write_progress_information_filling_space()
            self.currentfspath = fspath
            relfspath = bestrelpath(self.startpath, fspath)
            self._tw.line()
            self._tw.write(relfspath + " ")
        self._tw.write(res, flush=True, **markup)

    def write_ensure_prefix(self, prefix: str, extra: str = "", **kwargs) -> None:
        if self.currentfspath != prefix:
            self._tw.line()
            self.currentfspath = prefix
            self._tw.write(prefix)
        if extra:
            self._tw.write(extra, **kwargs)
            self.currentfspath = -2

    def ensure_newline(self) -> None:
        if self.currentfspath:
            self._tw.line()
            self.currentfspath = None

    def write(self, content: str, *, flush: bool = False, **markup: bool) -> None:
        self._tw.write(content, flush=flush, **markup)

    def flush(self) -> None:
        self._tw.flush()

    def write_line(self, line: Union[str, bytes], **markup: bool) -> None:
        if not isinstance(line, str):
            line = str(line, errors="replace")
        self.ensure_newline()
        self._tw.line(line, **markup)

    def rewrite(self, line: str, **markup: bool) -> None:
        """Rewinds the terminal cursor to the beginning and writes the given line.

        :param erase:
            If True, will also add spaces until the full terminal width to ensure
            previous lines are properly erased.

        The rest of the keyword arguments are markup instructions.
        """
        erase = markup.pop("erase", False)
        if erase:
            fill_count = self._tw.fullwidth - len(line) - 1
            fill = " " * fill_count
        else:
            fill = ""
        line = str(line)
        self._tw.write("\r" + line + fill, **markup)

    def write_sep(
        self,
        sep: str,
        title: Optional[str] = None,
        fullwidth: Optional[int] = None,
        **markup: bool,
    ) -> None:
        self.ensure_newline()
        self._tw.sep(sep, title, fullwidth, **markup)

    def section(self, title: str, sep: str = "=", **kw: bool) -> None:
        self._tw.sep(sep, title, **kw)

    def line(self, msg: str, **kw: bool) -> None:
        self._tw.line(msg, **kw)

    def _add_stats(self, category: str, items: Sequence[Any]) -> None:
        set_main_color = category not in self.stats
        self.stats.setdefault(category, []).extend(items)
        if set_main_color:
            self._set_main_color()

    def pytest_internalerror(self, excrepr: ExceptionRepr) -> bool:
        for line in str(excrepr).split("\n"):
            self.write_line("INTERNALERROR> " + line)
        return True

    def pytest_warning_recorded(
        self,
        warning_message: warnings.WarningMessage,
        nodeid: str,
    ) -> None:
        from _pytest.warnings import warning_record_to_str

        fslocation = warning_message.filename, warning_message.lineno
        message = warning_record_to_str(warning_message)

        warning_report = WarningReport(
            fslocation=fslocation, message=message, nodeid=nodeid
        )
        self._add_stats("warnings", [warning_report])

    def pytest_plugin_registered(self, plugin: _PluggyPlugin) -> None:
        if self.config.option.traceconfig:
            msg = f"PLUGIN registered: {plugin}"
            # XXX This event may happen during setup/teardown time
            #     which unfortunately captures our output here
            #     which garbles our output if we use self.write_line.
            self.write_line(msg)

    def pytest_deselected(self, items: Sequence[Item]) -> None:
        self._add_stats("deselected", items)

    def pytest_runtest_logstart(
        self, nodeid: str, location: Tuple[str, Optional[int], str]
    ) -> None:
        # Ensure that the path is printed before the
        # 1st test of a module starts running.
        if self.showlongtestinfo:
            line = self._locationline(nodeid, *location)
            self.write_ensure_prefix(line, "")
            self.flush()
        elif self.showfspath:
            self.write_fspath_result(nodeid, "")
            self.flush()

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        self._tests_ran = True
        rep = report
        res: Tuple[
            str, str, Union[str, Tuple[str, Mapping[str, bool]]]
        ] = self.config.hook.pytest_report_teststatus(report=rep, config=self.config)
        category, letter, word = res
        if not isinstance(word, tuple):
            markup = None
        else:
            word, markup = word
        self._add_stats(category, [rep])
        if not letter and not word:
            # Probably passed setup/teardown.
            return
        running_xdist = hasattr(rep, "node")
        if markup is None:
            was_xfail = hasattr(report, "wasxfail")
            if rep.passed and not was_xfail:
                markup = {"green": True}
            elif rep.passed and was_xfail:
                markup = {"yellow": True}
            elif rep.failed:
                markup = {"red": True}
            elif rep.skipped:
                markup = {"yellow": True}
            else:
                markup = {}
        if self.verbosity <= 0:
            self._tw.write(letter, **markup)
        else:
            self._progress_nodeids_reported.add(rep.nodeid)
            line = self._locationline(rep.nodeid, *rep.location)
            if not running_xdist:
                self.write_ensure_prefix(line, word, **markup)
                if rep.skipped or hasattr(report, "wasxfail"):
                    available_width = (
                        (self._tw.fullwidth - self._tw.width_of_current_line)
                        - len(" [100%]")
                        - 1
                    )
                    reason = _get_raw_skip_reason(rep)
                    reason_ = _format_trimmed(" ({})", reason, available_width)
                    if reason and reason_ is not None:
                        self._tw.write(reason_)
                if self._show_progress_info:
                    self._write_progress_information_filling_space()
            else:
                self.ensure_newline()
                self._tw.write("[%s]" % rep.node.gateway.id)
                if self._show_progress_info:
                    self._tw.write(
                        self._get_progress_information_message() + " ", cyan=True
                    )
                else:
                    self._tw.write(" ")
                self._tw.write(word, **markup)
                self._tw.write(" " + line)
                self.currentfspath = -2
        self.flush()

    @property
    def _is_last_item(self) -> bool:
        assert self._session is not None
        return len(self._progress_nodeids_reported) == self._session.testscollected

    def pytest_runtest_logfinish(self, nodeid: str) -> None:
        assert self._session
        if self.verbosity <= 0 and self._show_progress_info:
            if self._show_progress_info == "count":
                num_tests = self._session.testscollected
                progress_length = len(f" [{num_tests}/{num_tests}]")
            else:
                progress_length = len(" [100%]")

            self._progress_nodeids_reported.add(nodeid)

            if self._is_last_item:
                self._write_progress_information_filling_space()
            else:
                main_color, _ = self._get_main_color()
                w = self._width_of_current_line
                past_edge = w + progress_length + 1 >= self._screen_width
                if past_edge:
                    msg = self._get_progress_information_message()
                    self._tw.write(msg + "\n", **{main_color: True})

    def _get_progress_information_message(self) -> str:
        assert self._session
        collected = self._session.testscollected
        if self._show_progress_info == "count":
            if collected:
                progress = self._progress_nodeids_reported
                counter_format = f"{{:{len(str(collected))}d}}"
                format_string = f" [{counter_format}/{{}}]"
                return format_string.format(len(progress), collected)
            return f" [ {collected} / {collected} ]"
        else:
            if collected:
                return " [{:3d}%]".format(
                    len(self._progress_nodeids_reported) * 100 // collected
                )
            return " [100%]"

    def _write_progress_information_filling_space(self) -> None:
        color, _ = self._get_main_color()
        msg = self._get_progress_information_message()
        w = self._width_of_current_line
        fill = self._tw.fullwidth - w - 1
        self.write(msg.rjust(fill), flush=True, **{color: True})

    @property
    def _width_of_current_line(self) -> int:
        """Return the width of the current line."""
        return self._tw.width_of_current_line

    def pytest_collection(self) -> None:
        if self.isatty:
            if self.config.option.verbose >= 0:
                self.write("collecting ... ", flush=True, bold=True)
                self._collect_report_last_write = timing.time()
        elif self.config.option.verbose >= 1:
            self.write("collecting ... ", flush=True, bold=True)

    def pytest_collectreport(self, report: CollectReport) -> None:
        if report.failed:
            self._add_stats("error", [report])
        elif report.skipped:
            self._add_stats("skipped", [report])
        items = [x for x in report.result if isinstance(x, Item)]
        self._numcollected += len(items)
        if self.isatty:
            self.report_collect()

    def report_collect(self, final: bool = False) -> None:
        if self.config.option.verbose < 0:
            return

        if not final:
            # Only write "collecting" report every 0.5s.
            t = timing.time()
            if (
                self._collect_report_last_write is not None
                and self._collect_report_last_write > t - REPORT_COLLECTING_RESOLUTION
            ):
                return
            self._collect_report_last_write = t

        errors = len(self.stats.get("error", []))
        skipped = len(self.stats.get("skipped", []))
        deselected = len(self.stats.get("deselected", []))
        selected = self._numcollected - errors - skipped - deselected
        line = "collected " if final else "collecting "
        line += (
            str(self._numcollected) + " item" + ("" if self._numcollected == 1 else "s")
        )
        if errors:
            line += " / %d error%s" % (errors, "s" if errors != 1 else "")
        if deselected:
            line += " / %d deselected" % deselected
        if skipped:
            line += " / %d skipped" % skipped
        if self._numcollected > selected > 0:
            line += " / %d selected" % selected
        if self.isatty:
            self.rewrite(line, bold=True, erase=True)
            if final:
                self.write("\n")
        else:
            self.write_line(line)

    @hookimpl(trylast=True)
    def pytest_sessionstart(self, session: "Session") -> None:
        self._session = session
        self._sessionstarttime = timing.time()
        if not self.showheader:
            return
        self.write_sep("=", "test session starts", bold=True)
        verinfo = platform.python_version()
        if not self.no_header:
            msg = f"platform {sys.platform} -- Python {verinfo}"
            pypy_version_info = getattr(sys, "pypy_version_info", None)
            if pypy_version_info:
                verinfo = ".".join(map(str, pypy_version_info[:3]))
                msg += f"[pypy-{verinfo}-{pypy_version_info[3]}]"
            msg += ", pytest-{}, pluggy-{}".format(
                _pytest._version.version, pluggy.__version__
            )
            if (
                self.verbosity > 0
                or self.config.option.debug
                or getattr(self.config.option, "pastebin", None)
            ):
                msg += " -- " + str(sys.executable)
            self.write_line(msg)
            lines = self.config.hook.pytest_report_header(
                config=self.config, start_path=self.startpath
            )
            self._write_report_lines_from_hooks(lines)

    def _write_report_lines_from_hooks(
        self, lines: Sequence[Union[str, Sequence[str]]]
    ) -> None:
        for line_or_lines in reversed(lines):
            if isinstance(line_or_lines, str):
                self.write_line(line_or_lines)
            else:
                for line in line_or_lines:
                    self.write_line(line)

    def pytest_report_header(self, config: Config) -> List[str]:
        line = "rootdir: %s" % config.rootpath

        if config.inipath:
            line += ", configfile: " + bestrelpath(config.rootpath, config.inipath)

        testpaths: List[str] = config.getini("testpaths")
        if config.invocation_params.dir == config.rootpath and config.args == testpaths:
            line += ", testpaths: {}".format(", ".join(testpaths))

        result = [line]

        plugininfo = config.pluginmanager.list_plugin_distinfo()
        if plugininfo:
            result.append("plugins: %s" % ", ".join(_plugin_nameversions(plugininfo)))
        return result

    def pytest_collection_finish(self, session: "Session") -> None:
        self.report_collect(True)

        lines = self.config.hook.pytest_report_collectionfinish(
            config=self.config,
            start_path=self.startpath,
            items=session.items,
        )
        self._write_report_lines_from_hooks(lines)

        if self.config.getoption("collectonly"):
            if session.items:
                if self.config.option.verbose > -1:
                    self._tw.line("")
                self._printcollecteditems(session.items)

            failed = self.stats.get("failed")
            if failed:
                self._tw.sep("!", "collection failures")
                for rep in failed:
                    rep.toterminal(self._tw)

    def _printcollecteditems(self, items: Sequence[Item]) -> None:
        if self.config.option.verbose < 0:
            if self.config.option.verbose < -1:
                counts = Counter(item.nodeid.split("::", 1)[0] for item in items)
                for name, count in sorted(counts.items()):
                    self._tw.line("%s: %d" % (name, count))
            else:
                for item in items:
                    self._tw.line(item.nodeid)
            return
        stack: List[Node] = []
        indent = ""
        for item in items:
            needed_collectors = item.listchain()[1:]  # strip root node
            while stack:
                if stack == needed_collectors[: len(stack)]:
                    break
                stack.pop()
            for col in needed_collectors[len(stack) :]:
                stack.append(col)
                indent = (len(stack) - 1) * "  "
                self._tw.line(f"{indent}{col}")
                if self.config.option.verbose >= 1:
                    obj = getattr(col, "obj", None)
                    doc = inspect.getdoc(obj) if obj else None
                    if doc:
                        for line in doc.splitlines():
                            self._tw.line("{}{}".format(indent + "  ", line))

    @hookimpl(hookwrapper=True)
    def pytest_sessionfinish(
        self, session: "Session", exitstatus: Union[int, ExitCode]
    ):
        outcome = yield
        outcome.get_result()
        self._tw.line("")
        summary_exit_codes = (
            ExitCode.OK,
            ExitCode.TESTS_FAILED,
            ExitCode.INTERRUPTED,
            ExitCode.USAGE_ERROR,
            ExitCode.NO_TESTS_COLLECTED,
        )
        if exitstatus in summary_exit_codes and not self.no_summary:
            self.config.hook.pytest_terminal_summary(
                terminalreporter=self, exitstatus=exitstatus, config=self.config
            )
        if session.shouldfail:
            self.write_sep("!", str(session.shouldfail), red=True)
        if exitstatus == ExitCode.INTERRUPTED:
            self._report_keyboardinterrupt()
            self._keyboardinterrupt_memo = None
        elif session.shouldstop:
            self.write_sep("!", str(session.shouldstop), red=True)
        self.summary_stats()

    @hookimpl(hookwrapper=True)
    def pytest_terminal_summary(self) -> Generator[None, None, None]:
        self.summary_errors()
        self.summary_failures()
        self.summary_warnings()
        self.summary_passes()
        yield
        self.short_test_summary()
        # Display any extra warnings from teardown here (if any).
        self.summary_warnings()

    def pytest_keyboard_interrupt(self, excinfo: ExceptionInfo[BaseException]) -> None:
        self._keyboardinterrupt_memo = excinfo.getrepr(funcargs=True)

    def pytest_unconfigure(self) -> None:
        if self._keyboardinterrupt_memo is not None:
            self._report_keyboardinterrupt()

    def _report_keyboardinterrupt(self) -> None:
        excrepr = self._keyboardinterrupt_memo
        assert excrepr is not None
        assert excrepr.reprcrash is not None
        msg = excrepr.reprcrash.message
        self.write_sep("!", msg)
        if "KeyboardInterrupt" in msg:
            if self.config.option.fulltrace:
                excrepr.toterminal(self._tw)
            else:
                excrepr.reprcrash.toterminal(self._tw)
                self._tw.line(
                    "(to show a full traceback on KeyboardInterrupt use --full-trace)",
                    yellow=True,
                )

    def _locationline(
        self, nodeid: str, fspath: str, lineno: Optional[int], domain: str
    ) -> str:
        def mkrel(nodeid: str) -> str:
            line = self.config.cwd_relative_nodeid(nodeid)
            if domain and line.endswith(domain):
                line = line[: -len(domain)]
                values = domain.split("[")
                values[0] = values[0].replace(".", "::")  # don't replace '.' in params
                line += "[".join(values)
            return line

        # collect_fspath comes from testid which has a "/"-normalized path.
        if fspath:
            res = mkrel(nodeid)
            if self.verbosity >= 2 and nodeid.split("::")[0] != fspath.replace(
                "\\", nodes.SEP
            ):
                res += " <- " + bestrelpath(self.startpath, Path(fspath))
        else:
            res = "[location]"
        return res + " "

    def _getfailureheadline(self, rep):
        head_line = rep.head_line
        if head_line:
            return head_line
        return "test session"  # XXX?

    def _getcrashline(self, rep):
        try:
            return str(rep.longrepr.reprcrash)
        except AttributeError:
            try:
                return str(rep.longrepr)[:50]
            except AttributeError:
                return ""

    #
    # Summaries for sessionfinish.
    #
    def getreports(self, name: str):
        return [x for x in self.stats.get(name, ()) if not hasattr(x, "_pdbshown")]

    def summary_warnings(self) -> None:
        if self.hasopt("w"):
            all_warnings: Optional[List[WarningReport]] = self.stats.get("warnings")
            if not all_warnings:
                return

            final = self._already_displayed_warnings is not None
            if final:
                warning_reports = all_warnings[self._already_displayed_warnings :]
            else:
                warning_reports = all_warnings
            self._already_displayed_warnings = len(warning_reports)
            if not warning_reports:
                return

            reports_grouped_by_message: Dict[str, List[WarningReport]] = {}
            for wr in warning_reports:
                reports_grouped_by_message.setdefault(wr.message, []).append(wr)

            def collapsed_location_report(reports: List[WarningReport]) -> str:
                locations = []
                for w in reports:
                    location = w.get_location(self.config)
                    if location:
                        locations.append(location)

                if len(locations) < 10:
                    return "\n".join(map(str, locations))

                counts_by_filename = Counter(
                    str(loc).split("::", 1)[0] for loc in locations
                )
                return "\n".join(
                    "{}: {} warning{}".format(k, v, "s" if v > 1 else "")
                    for k, v in counts_by_filename.items()
                )

            title = "warnings summary (final)" if final else "warnings summary"
            self.write_sep("=", title, yellow=True, bold=False)
            for message, message_reports in reports_grouped_by_message.items():
                maybe_location = collapsed_location_report(message_reports)
                if maybe_location:
                    self._tw.line(maybe_location)
                    lines = message.splitlines()
                    indented = "\n".join("  " + x for x in lines)
                    message = indented.rstrip()
                else:
                    message = message.rstrip()
                self._tw.line(message)
                self._tw.line()
            self._tw.line(
                "-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html"
            )

    def summary_passes(self) -> None:
        if self.config.option.tbstyle != "no":
            if self.hasopt("P"):
                reports: List[TestReport] = self.getreports("passed")
                if not reports:
                    return
                self.write_sep("=", "PASSES")
                for rep in reports:
                    if rep.sections:
                        msg = self._getfailureheadline(rep)
                        self.write_sep("_", msg, green=True, bold=True)
                        self._outrep_summary(rep)
                    self._handle_teardown_sections(rep.nodeid)

    def _get_teardown_reports(self, nodeid: str) -> List[TestReport]:
        reports = self.getreports("")
        return [
            report
            for report in reports
            if report.when == "teardown" and report.nodeid == nodeid
        ]

    def _handle_teardown_sections(self, nodeid: str) -> None:
        for report in self._get_teardown_reports(nodeid):
            self.print_teardown_sections(report)

    def print_teardown_sections(self, rep: TestReport) -> None:
        showcapture = self.config.option.showcapture
        if showcapture == "no":
            return
        for secname, content in rep.sections:
            if showcapture != "all" and showcapture not in secname:
                continue
            if "teardown" in secname:
                self._tw.sep("-", secname)
                if content[-1:] == "\n":
                    content = content[:-1]
                self._tw.line(content)

    def summary_failures(self) -> None:
        if self.config.option.tbstyle != "no":
            reports: List[BaseReport] = self.getreports("failed")
            if not reports:
                return
            self.write_sep("=", "FAILURES")
            if self.config.option.tbstyle == "line":
                for rep in reports:
                    line = self._getcrashline(rep)
                    self.write_line(line)
            else:
                for rep in reports:
                    msg = self._getfailureheadline(rep)
                    self.write_sep("_", msg, red=True, bold=True)
                    self._outrep_summary(rep)
                    self._handle_teardown_sections(rep.nodeid)

    def summary_errors(self) -> None:
        if self.config.option.tbstyle != "no":
            reports: List[BaseReport] = self.getreports("error")
            if not reports:
                return
            self.write_sep("=", "ERRORS")
            for rep in self.stats["error"]:
                msg = self._getfailureheadline(rep)
                if rep.when == "collect":
                    msg = "ERROR collecting " + msg
                else:
                    msg = f"ERROR at {rep.when} of {msg}"
                self.write_sep("_", msg, red=True, bold=True)
                self._outrep_summary(rep)

    def _outrep_summary(self, rep: BaseReport) -> None:
        rep.toterminal(self._tw)
        showcapture = self.config.option.showcapture
        if showcapture == "no":
            return
        for secname, content in rep.sections:
            if showcapture != "all" and showcapture not in secname:
                continue
            self._tw.sep("-", secname)
            if content[-1:] == "\n":
                content = content[:-1]
            self._tw.line(content)

    def summary_stats(self) -> None:
        if self.verbosity < -1:
            return

        session_duration = timing.time() - self._sessionstarttime
        (parts, main_color) = self.build_summary_stats_line()
        line_parts = []

        display_sep = self.verbosity >= 0
        if display_sep:
            fullwidth = self._tw.fullwidth
        for text, markup in parts:
            with_markup = self._tw.markup(text, **markup)
            if display_sep:
                fullwidth += len(with_markup) - len(text)
            line_parts.append(with_markup)
        msg = ", ".join(line_parts)

        main_markup = {main_color: True}
        duration = f" in {format_session_duration(session_duration)}"
        duration_with_markup = self._tw.markup(duration, **main_markup)
        if display_sep:
            fullwidth += len(duration_with_markup) - len(duration)
        msg += duration_with_markup

        if display_sep:
            markup_for_end_sep = self._tw.markup("", **main_markup)
            if markup_for_end_sep.endswith("\x1b[0m"):
                markup_for_end_sep = markup_for_end_sep[:-4]
            fullwidth += len(markup_for_end_sep)
            msg += markup_for_end_sep

        if display_sep:
            self.write_sep("=", msg, fullwidth=fullwidth, **main_markup)
        else:
            self.write_line(msg, **main_markup)

    def short_test_summary(self) -> None:
        if not self.reportchars:
            return

        def show_simple(stat, lines: List[str]) -> None:
            failed = self.stats.get(stat, [])
            if not failed:
                return
            termwidth = self._tw.fullwidth
            config = self.config
            for rep in failed:
                line = _get_line_with_reprcrash_message(config, rep, termwidth)
                lines.append(line)

        def show_xfailed(lines: List[str]) -> None:
            xfailed = self.stats.get("xfailed", [])
            for rep in xfailed:
                verbose_word = rep._get_verbose_word(self.config)
                pos = _get_pos(self.config, rep)
                lines.append(f"{verbose_word} {pos}")
                reason = rep.wasxfail
                if reason:
                    lines.append("  " + str(reason))

        def show_xpassed(lines: List[str]) -> None:
            xpassed = self.stats.get("xpassed", [])
            for rep in xpassed:
                verbose_word = rep._get_verbose_word(self.config)
                pos = _get_pos(self.config, rep)
                reason = rep.wasxfail
                lines.append(f"{verbose_word} {pos} {reason}")

        def show_skipped(lines: List[str]) -> None:
            skipped: List[CollectReport] = self.stats.get("skipped", [])
            fskips = _folded_skips(self.startpath, skipped) if skipped else []
            if not fskips:
                return
            verbose_word = skipped[0]._get_verbose_word(self.config)
            for num, fspath, lineno, reason in fskips:
                if reason.startswith("Skipped: "):
                    reason = reason[9:]
                if lineno is not None:
                    lines.append(
                        "%s [%d] %s:%d: %s"
                        % (verbose_word, num, fspath, lineno, reason)
                    )
                else:
                    lines.append("%s [%d] %s: %s" % (verbose_word, num, fspath, reason))

        REPORTCHAR_ACTIONS: Mapping[str, Callable[[List[str]], None]] = {
            "x": show_xfailed,
            "X": show_xpassed,
            "f": partial(show_simple, "failed"),
            "s": show_skipped,
            "p": partial(show_simple, "passed"),
            "E": partial(show_simple, "error"),
        }

        lines: List[str] = []
        for char in self.reportchars:
            action = REPORTCHAR_ACTIONS.get(char)
            if action:  # skipping e.g. "P" (passed with output) here.
                action(lines)

        if lines:
            self.write_sep("=", "short test summary info")
            for line in lines:
                self.write_line(line)

    def _get_main_color(self) -> Tuple[str, List[str]]:
        if self._main_color is None or self._known_types is None or self._is_last_item:
            self._set_main_color()
            assert self._main_color
            assert self._known_types
        return self._main_color, self._known_types

    def _determine_main_color(self, unknown_type_seen: bool) -> str:
        stats = self.stats
        if "failed" in stats or "error" in stats:
            main_color = "red"
        elif "warnings" in stats or "xpassed" in stats or unknown_type_seen:
            main_color = "yellow"
        elif "passed" in stats or not self._is_last_item:
            main_color = "green"
        else:
            main_color = "yellow"
        return main_color

    def _set_main_color(self) -> None:
        unknown_types: List[str] = []
        for found_type in self.stats.keys():
            if found_type:  # setup/teardown reports have an empty key, ignore them
                if found_type not in KNOWN_TYPES and found_type not in unknown_types:
                    unknown_types.append(found_type)
        self._known_types = list(KNOWN_TYPES) + unknown_types
        self._main_color = self._determine_main_color(bool(unknown_types))

    def build_summary_stats_line(self) -> Tuple[List[Tuple[str, Dict[str, bool]]], str]:
        """
        Build the parts used in the last summary stats line.

        The summary stats line is the line shown at the end, "=== 12 passed, 2 errors in Xs===".

        This function builds a list of the "parts" that make up for the text in that line, in
        the example above it would be:

            [
                ("12 passed", {"green": True}),
                ("2 errors", {"red": True}
            ]

        That last dict for each line is a "markup dictionary", used by TerminalWriter to
        color output.

        The final color of the line is also determined by this function, and is the second
        element of the returned tuple.
        """
        if self.config.getoption("collectonly"):
            return self._build_collect_only_summary_stats_line()
        else:
            return self._build_normal_summary_stats_line()

    def _get_reports_to_display(self, key: str) -> List[Any]:
        """Get test/collection reports for the given status key, such as `passed` or `error`."""
        reports = self.stats.get(key, [])
        return [x for x in reports if getattr(x, "count_towards_summary", True)]

    def _build_normal_summary_stats_line(
        self,
    ) -> Tuple[List[Tuple[str, Dict[str, bool]]], str]:
        main_color, known_types = self._get_main_color()
        parts = []

        for key in known_types:
            reports = self._get_reports_to_display(key)
            if reports:
                count = len(reports)
                color = _color_for_type.get(key, _color_for_type_default)
                markup = {color: True, "bold": color == main_color}
                parts.append(("%d %s" % pluralize(count, key), markup))

        if not parts:
            parts = [("no tests ran", {_color_for_type_default: True})]

        return parts, main_color

    def _build_collect_only_summary_stats_line(
        self,
    ) -> Tuple[List[Tuple[str, Dict[str, bool]]], str]:
        deselected = len(self._get_reports_to_display("deselected"))
        errors = len(self._get_reports_to_display("error"))

        if self._numcollected == 0:
            parts = [("no tests collected", {"yellow": True})]
            main_color = "yellow"

        elif deselected == 0:
            main_color = "green"
            collected_output = "%d %s collected" % pluralize(self._numcollected, "test")
            parts = [(collected_output, {main_color: True})]
        else:
            all_tests_were_deselected = self._numcollected == deselected
            if all_tests_were_deselected:
                main_color = "yellow"
                collected_output = f"no tests collected ({deselected} deselected)"
            else:
                main_color = "green"
                selected = self._numcollected - deselected
                collected_output = f"{selected}/{self._numcollected} tests collected ({deselected} deselected)"

            parts = [(collected_output, {main_color: True})]

        if errors:
            main_color = _color_for_type["error"]
            parts += [("%d %s" % pluralize(errors, "error"), {main_color: True})]

        return parts, main_color


def _get_pos(config: Config, rep: BaseReport):
    nodeid = config.cwd_relative_nodeid(rep.nodeid)
    return nodeid


def _format_trimmed(format: str, msg: str, available_width: int) -> Optional[str]:
    """Format msg into format, ellipsizing it if doesn't fit in available_width.

    Returns None if even the ellipsis can't fit.
    """
    # Only use the first line.
    i = msg.find("\n")
    if i != -1:
        msg = msg[:i]

    ellipsis = "..."
    format_width = wcswidth(format.format(""))
    if format_width + len(ellipsis) > available_width:
        return None

    if format_width + wcswidth(msg) > available_width:
        available_width -= len(ellipsis)
        msg = msg[:available_width]
        while format_width + wcswidth(msg) > available_width:
            msg = msg[:-1]
        msg += ellipsis

    return format.format(msg)


def _get_line_with_reprcrash_message(
    config: Config, rep: BaseReport, termwidth: int
) -> str:
    """Get summary line for a report, trying to add reprcrash message."""
    verbose_word = rep._get_verbose_word(config)
    pos = _get_pos(config, rep)

    line = f"{verbose_word} {pos}"
    line_width = wcswidth(line)

    try:
        # Type ignored intentionally -- possible AttributeError expected.
        msg = rep.longrepr.reprcrash.message  # type: ignore[union-attr]
    except AttributeError:
        pass
    else:
        available_width = termwidth - line_width
        msg = _format_trimmed(" - {}", msg, available_width)
        if msg is not None:
            line += msg

    return line


def _folded_skips(
    startpath: Path,
    skipped: Sequence[CollectReport],
) -> List[Tuple[int, str, Optional[int], str]]:
    d: Dict[Tuple[str, Optional[int], str], List[CollectReport]] = {}
    for event in skipped:
        assert event.longrepr is not None
        assert isinstance(event.longrepr, tuple), (event, event.longrepr)
        assert len(event.longrepr) == 3, (event, event.longrepr)
        fspath, lineno, reason = event.longrepr
        # For consistency, report all fspaths in relative form.
        fspath = bestrelpath(startpath, Path(fspath))
        keywords = getattr(event, "keywords", {})
        # Folding reports with global pytestmark variable.
        # This is a workaround, because for now we cannot identify the scope of a skip marker
        # TODO: Revisit after marks scope would be fixed.
        if (
            event.when == "setup"
            and "skip" in keywords
            and "pytestmark" not in keywords
        ):
            key: Tuple[str, Optional[int], str] = (fspath, None, reason)
        else:
            key = (fspath, lineno, reason)
        d.setdefault(key, []).append(event)
    values: List[Tuple[int, str, Optional[int], str]] = []
    for key, events in d.items():
        values.append((len(events), *key))
    return values


_color_for_type = {
    "failed": "red",
    "error": "red",
    "warnings": "yellow",
    "passed": "green",
}
_color_for_type_default = "yellow"


def pluralize(count: int, noun: str) -> Tuple[int, str]:
    # No need to pluralize words such as `failed` or `passed`.
    if noun not in ["error", "warnings", "test"]:
        return count, noun

    # The `warnings` key is plural. To avoid API breakage, we keep it that way but
    # set it to singular here so we can determine plurality in the same way as we do
    # for `error`.
    noun = noun.replace("warnings", "warning")

    return count, noun + "s" if count != 1 else noun


def _plugin_nameversions(plugininfo) -> List[str]:
    values: List[str] = []
    for plugin, dist in plugininfo:
        # Gets us name and version!
        name = "{dist.project_name}-{dist.version}".format(dist=dist)
        # Questionable convenience, but it keeps things short.
        if name.startswith("pytest-"):
            name = name[7:]
        # We decided to print python package names they can have more than one plugin.
        if name not in values:
            values.append(name)
    return values


def format_session_duration(seconds: float) -> str:
    """Format the given seconds in a human readable manner to show in the final summary."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        dt = datetime.timedelta(seconds=int(seconds))
        return f"{seconds:.2f}s ({dt})"


def _get_raw_skip_reason(report: TestReport) -> str:
    """Get the reason string of a skip/xfail/xpass test report.

    The string is just the part given by the user.
    """
    if hasattr(report, "wasxfail"):
        reason = cast(str, report.wasxfail)
        if reason.startswith("reason: "):
            reason = reason[len("reason: ") :]
        return reason
    else:
        assert report.skipped
        assert isinstance(report.longrepr, tuple)
        _, _, reason = report.longrepr
        if reason.startswith("Skipped: "):
            reason = reason[len("Skipped: ") :]
        elif reason == "Skipped":
            reason = ""
        return reason
