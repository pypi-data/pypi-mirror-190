# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime

import click
import pytermor as pt

from ._base import _catch_and_log_and_exit, _catch_and_print
from ._base_monitor import (
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    CoreMonitorConfig, GenericDemoComposer,
)
from ..shared import Styles, get_config, SocketMessage


class _SystemTimeMonitorConfig(CoreMonitorConfig):
    display_seconds: bool = False

    def update_from_config(self):
        super().update_from_config()
        self.display_seconds = get_config().getboolean(self._config_section, "display-seconds")


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current time",
    output_examples=[
        "│`21:27`│",
        "│`04:07:32`│",
    ],
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
class SystemTimeMonitor(CoreMonitor[None, _SystemTimeMonitorConfig]):
    """
    Output is a fixed string either 5 chars wide: │`HH·MM`│, where HH is hours and
    MM is minutes -- current system time, or 8 chars wide: │`HH·MM·SS`│ (same, but
    also includes seconds).

    Mode depends on config variable <monitor.system-time.display-seconds> [default: no].
    """

    def _init_settings(self) -> CoreMonitorSettings:
        return CoreMonitorSettings[_SystemTimeMonitorConfig](
            socket_topic="sys-datetime",
            cache_output=False,
            config=_SystemTimeMonitorConfig("monitor.system-time"),
            demo_composer=SystemTimeDemoComposer,
        )

    def get_output_width(self) -> int:
        display_seconds = self._setup.config.display_seconds
        return 6 + (3 if display_seconds else 0)

    def _format_data_impl(self, msg: SocketMessage[None]) -> str | pt.IRenderable:
        now = msg.timestamp
        now_dt: datetime = datetime.datetime.fromtimestamp(msg.timestamp)
        hours_st = Styles.TEXT_MAIN_VALUE
        minutes_st = Styles.TEXT_DEFAULT
        seconds_st = Styles.TEXT_LABEL
        sep_st = Styles.TEXT_LABEL

        hours = pt.Fragment(now_dt.strftime("%H"), hours_st)
        minutes = pt.Fragment(now_dt.strftime("%M"), minutes_st)
        seconds = pt.Fragment(now_dt.strftime("%S"), seconds_st)
        sep = pt.Fragment(self._get_colon_sep(now), sep_st)

        result = [hours, sep, minutes]
        if self._setup.config.display_seconds:
            result += [sep, seconds]
        return pt.Text().append(*result)

    def _get_colon_sep(self, now: int) -> str:
        return ":" if now % 2 == 0 else " "


class SystemTimeDemoComposer(GenericDemoComposer):
    pass
