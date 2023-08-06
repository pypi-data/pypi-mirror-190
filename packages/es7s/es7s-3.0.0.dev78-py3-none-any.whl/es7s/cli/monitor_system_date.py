# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime

import click
import pytermor as pt

from ._base_monitor import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig, \
    GenericDemoComposer
from ._base import _catch_and_log_and_exit, _catch_and_print
from ..shared import Styles, get_config, SocketMessage


class _SystemDateMonitorConfig(CoreMonitorConfig):
    display_year: bool = False

    def update_from_config(self):
        super().update_from_config()
        self.display_year = get_config().getboolean(self._config_section, "display-year")


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current date",
    output_examples=[
        "│`Wed 14 Dec`│",
        "│`Sun 27 Nov 2022`│",
    ],
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
class SystemDateMonitor(CoreMonitor[None, _SystemDateMonitorConfig]):
    """
    Output is a fixed string either 10 chars wide: │`DOW·DD·MMM`│, where DOW is
    current day of the week abbreviation, DD is current day, and MMM is current month,
    or 15 chars wide: │`DOW·DD·MMM·YYYY`│ (same, but also includes year -- YYYY).

    Mode depends on config variable <monitor.system-date.display-year> [default: no].
    """

    def _init_settings(self) -> CoreMonitorSettings[_SystemDateMonitorConfig]:
        return CoreMonitorSettings[_SystemDateMonitorConfig](
            socket_topic="sys-datetime",
            config=_SystemDateMonitorConfig("monitor.system-date"),
            demo_composer=SystemDateDemoComposer,
        )

    def get_output_width(self) -> int:
        display_year = self._setup.config.display_year
        return 10 + (5 if display_year else 0)

    def _format_data_impl(self, msg: SocketMessage[None]) -> pt.Text:
        now = datetime.datetime.fromtimestamp(msg.timestamp)
        day_st = Styles.TEXT_MAIN_VALUE
        mon_st = Styles.TEXT_DEFAULT
        dow_st = year_st = Styles.TEXT_LABEL

        dow = pt.Fragment(now.strftime("%a"), dow_st)
        day = pt.Fragment(now.strftime("%0e"), day_st)
        mon = pt.Fragment(now.strftime("%b"), mon_st)
        year = pt.Fragment(now.strftime("%Y"), year_st)
        sep = " "

        result = dow + sep + day + sep + mon
        if self._setup.config.display_year:
            result += sep + year

        return result


class SystemDateDemoComposer(GenericDemoComposer):
    pass
