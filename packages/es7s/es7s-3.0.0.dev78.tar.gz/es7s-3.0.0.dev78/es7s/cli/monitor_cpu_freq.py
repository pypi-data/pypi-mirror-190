# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from ._base import _catch_and_log_and_exit, _catch_and_print
from ._base_monitor import (
    CoreMonitor,
    GenericDemoComposer,
    CoreMonitorSettings,
    MonitorCliCommand,
    CoreMonitorConfig, RatioStyleMap, RatioStyle,
)
from ..shared import SocketMessage, Styles

OUTPUT_WIDTH = 8


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current CPU frequency",
    output_examples=[
        "│`2.55 GHz`│    current value",
        "│`max 5.1G`│^A^ max value",
        "│`min 800M`│^A^ min value",
    ],
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
class CpuFreqMonitor(CoreMonitor[dict, CoreMonitorConfig]):
    """
    ``
    """

    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self._formatter = pt.StaticBaseFormatter(
            pad=True,
            allow_negative=False,
            unit_separator=" ",
            unit="Hz",
            prefix_refpoint_shift=+2,
        )
        self._alt_formatter = pt.StaticBaseFormatter(
            self._formatter,
            max_value_len=3,
            unit_separator="",
            unit="",
        )
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(self) -> CoreMonitorSettings:
        return CoreMonitorSettings(
            socket_topic="cpu",
            socket_receive_interval_sec=2,
            alt_mode=True,
            ratio_styles_map=RatioStyleMap([
                RatioStyle(1.00, pt.Style(bg=pt.cv.GRAY_15)),
            ]),
            config=CoreMonitorConfig("monitor.cpu-freq"),
            demo_composer=CpuFreqDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[dict]) -> pt.RT|list[pt.RT]:
        freq_mhz = msg.data.get("freq_mhz")
        fmin, fcur, fmax = freq_mhz.min, freq_mhz.current, freq_mhz.max
        self._state.ratio = None
        if fmin and fcur and fmax:
            self._state.ratio = fcur/fmax  # (fcur - fmin) / (fmax - fmin)

        if self._state.is_alt_mode:
            val_and_prefix = "N/A".ljust(4)
            if self._state.tick_render_num % 2 == 1:
                if fmin:
                    val_and_prefix = self._alt_formatter.format(fmin)
                label = "min".rjust(4)
            else:
                if fmax:
                    val_and_prefix = self._alt_formatter.format(fmax)
                label = "max".rjust(4)
            val, prefix_unit = val_and_prefix[:-1], val_and_prefix[-1]
            # 3  1
        else:
            val, prefix_unit = self._formatter.format(fcur).rsplit(" ", 1)
            # 4  3
            prefix_unit = prefix_unit.rjust(4)
            label = ""

        result_parts = [
            pt.Fragment(val, Styles.TEXT_DEFAULT),
            pt.Fragment(prefix_unit, Styles.TEXT_AUXILIARY),
            pt.Fragment(label, Styles.TEXT_LABEL),
        ]
        if self._state.is_alt_mode:
            result = pt.Text()
            [result.append(rp) for rp in result_parts]
            return result
        return result_parts


class CpuFreqDemoComposer(GenericDemoComposer):
    def render(self):
        pass
