# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
from math import isclose, nextafter

import click
import pytermor as pt

from ._base import _catch_and_log_and_exit, _catch_and_print
from ._base_monitor import (
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
)
from ..shared import Styles, SocketMessage

OUTPUT_WIDTH = 14


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="recent average system load",
    output_examples=[
        "│`0.43 0.24 0.16`│  # low system load",
        "│`3.11 2.67 2.41`│  # (relatively) high system load",
    ],
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
class CpuLoadAvgMonitor(CoreMonitor[dict, CoreMonitorConfig]):
    """
    Display number of processes in the system run queue averaged
    over the last 1, 5 and 15 minutes.

    Output is a fixed string 14 chars wide: │`FF01 FF05 FF15`│, where FFnn
    is an average amount of running processes over the last 1, 5 and 15 minutes,
    respectively.
    """

    STYLES = (
        [
            pt.Style(Styles.TEXT_DEFAULT, bold=True),
            pt.Style(Styles.TEXT_AUXILIARY, bold=True),
            Styles.TEXT_AUXILIARY,
        ],
    )

    def _init_settings(self) -> CoreMonitorSettings:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="cpu",
            alt_mode=True,
            config=CoreMonitorConfig("monitor.cpu-load-avg"),
            demo_composer=CpuLoadAvgDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[dict]) -> pt.Text:
        def format_value(val: float):
            if isclose(val, 0.0, abs_tol=1e-3):
                val = nextafter(1e-3, 0)
            return pt.format_auto_float(float(val), 4, allow_exp_form=False) + " "

        if self._state.is_alt_mode:
            return pt.Text("(1/5/15m) avgl", Styles.TEXT_LABEL)

        result = pt.Text()
        load_avg = msg.data.get("load_avg")
        load_avg_strs = [*map(format_value, load_avg)]
        load_avg_strs[-1] = load_avg_strs[-1].rstrip(" ")
        for (tx, st) in zip(load_avg_strs, *self.STYLES):
            result += pt.Fragment(tx, st)
        return result

    def _get_output_on_init(self) -> str | pt.IRenderable:
        return pt.distribute_padded(self.get_output_width(), " ...", " ...", " ...")


class CpuLoadAvgDemoComposer(GenericDemoComposer):
    def render(self):
        input_val_width = 7
        input_width = input_val_width * 3 + 2

        columns = [("CPU load average over", input_width), ("Results", OUTPUT_WIDTH)]
        total_width = sum(c[1] for c in columns) + 1
        self._print_header(columns, bline=False)

        def make_header_val_cells(cw):
            return ((v, cw) for v in ["1min", "5min", "15min"])

        self._print_header([*make_header_val_cells(7), *make_header_val_cells(4)])

        vals = [(v, v / 5, v / 15) for v in [math.pow(math.e, e) for e in range(-8, 6, 1)]]
        self._monitor._setup.config.drop_separators()
        for val in vals:
            inp = self._format_row_label(
                " ".join(f"{v:{input_val_width}.{'1e' if v < 1e-3 else '3f'}}" for v in val),
                input_width,
            )
            self._print_row(
                inp, self._render_msg(SocketMessage({"load_avg": [*val]}))
            )
        self._print_footer(total_width)
