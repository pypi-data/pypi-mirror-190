# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing

import click
import pytermor as pt

from ._base import _catch_and_log_and_exit, _catch_and_print
from ._base_monitor import (
    CoreMonitor,
    CoreMonitorConfig,
    GenericDemoComposer,
    CoreMonitorSettings,
    RatioStyleMap,
    RatioStyle,
    MonitorCliCommand,
)
from ..shared import SocketMessage, Styles

OUTPUT_WIDTH = 6


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current CPU load",
    output_examples=[],
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
class CpuLoadMonitor(CoreMonitor[dict, CoreMonitorConfig]):
    """
    a
    """

    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(self) -> CoreMonitorSettings:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="cpu",
            alt_mode=True,
            ratio_styles_map=RatioStyleMap(
                [
                    RatioStyle(0.70, pt.Style(Styles.TEXT_DEFAULT, bg=pt.cv.GRAY_15)),
                    RatioStyle(0.75, pt.Style(fg=pt.cv.GRAY_7, bg=pt.Color256.get_by_code(94))),
                    RatioStyle(0.80, pt.Style(fg=pt.cv.GRAY_7, bg=pt.Color256.get_by_code(136))),
                    RatioStyle(0.85, pt.Style(fg=pt.cv.GRAY_7, bg=pt.Color256.get_by_code(172))),
                    RatioStyle(0.90, pt.Style(fg=pt.cv.GRAY_7, bg=pt.Color256.get_by_code(208))),
                    RatioStyle(0.95, pt.Style(fg=pt.cv.GRAY_7, bg=pt.Color256.get_by_code(202))),
                    RatioStyle(0.99, pt.Style(fg=pt.cv.GRAY_7, bg=pt.Color256.get_by_code(160))),
                    RatioStyle(1.00, Styles.CRITICAL_ACCENT),
                ]
            ),
            config=CoreMonitorConfig("monitor.cpu-load"),
            demo_composer=CpuLoadDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[dict]) -> list[pt.FrozenText]:
        na_fmtd = pt.FrozenText("N/A", width=OUTPUT_WIDTH, align="center")
        if self._state.is_alt_mode:
            core_count = msg.data.get("core_count", None)
            core_count_fmtd = pt.FrozenText(f"{core_count:>2d} ", Styles.TEXT_MAIN_VALUE)
            label_fmtd = pt.FrozenText("cpu", Styles.TEXT_LABEL)
            return [core_count_fmtd, label_fmtd]
        load_perc = msg.data.get("load_perc", None)
        if load_perc is None:
            self._state.ratio = 0
            return [na_fmtd]
        self._state.ratio = load_perc / 100
        pad_left = pt.FrozenText(" ")
        load_fmtd = pt.FrozenText(f"{round(load_perc):^3d}", Styles.TEXT_MAIN_VALUE)
        unit_fmtd = pt.FrozenText("% ", Styles.TEXT_UNITS)
        return [pad_left, load_fmtd, unit_fmtd]


class CpuLoadDemoComposer(GenericDemoComposer):
    def render(self):
        columns = 5
        total_width = columns * (OUTPUT_WIDTH) + (columns - 1)
        self._print_header([("CPU load (all cores)", total_width)], total_width)

        self._monitor._setup.config.drop_separators()
        load_base = -1
        while load_base < 100:
            row = []
            for _ in range(columns):
                c = 1
                if load_base >= 4:
                    c = 2
                if load_base >= 10:
                    c = 3
                if load_base >= 39:
                    c = 4
                if load_base >= 40:
                    c = 5
                load_base += c
                row.append(self._render_msg(SocketMessage({"load_perc": load_base})))
            self._print_row(*row)

        def _format_special(label: str, output: str) -> tuple[pt.RT, ...]:
            return self._format_row_label(label, total_width - OUTPUT_WIDTH - 1), output

        def _make_specials() -> typing.Iterable[tuple[pt.RT, ...]]:
            yield _format_special("Disabled", self._monitor._renderer.update_disabled())
            yield _format_special("Config reloading", self._monitor._renderer.update_busy())
            yield _format_special("Empty daemon data bus", self._monitor._renderer.update_no_data())
            yield _format_special("Critical failure", self._monitor._renderer.update_on_error())
            yield _format_special("Post-failure timeout", self._monitor._renderer.update_idle())
            self._monitor._state.alt_mode_timeout = 1
            yield _format_special("Alt mode", self._monitor._renderer.update_primary())
            self._monitor._state.alt_mode_timeout = 0
            yield _format_special("Initialzing", self._monitor._renderer.update_init())

        self._monitor._state.alt_mode_timeout = 0
        self._print_horiz_sep("Specials", total_width)
        self._print_rows(*_make_specials())
        self._print_footer(total_width)
