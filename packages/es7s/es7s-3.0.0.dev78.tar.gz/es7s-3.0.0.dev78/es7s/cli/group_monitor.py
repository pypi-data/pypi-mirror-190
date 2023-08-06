# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from . import (
    monitor_battery,
    monitor_docker,
    monitor_cpu_load,
    monitor_cpu_load_avg,
    monitor_cpu_freq,
    monitor_system_time,
    monitor_system_date,
    monitor_weather,
)
from ._base import CliGroup, _catch_and_log_and_exit


@click.group(
    name=__file__,
    cls=CliGroup,
    short_help="run system monitor",
)
@click.pass_context
@_catch_and_log_and_exit
def group(ctx: click.Context, **kwargs):
    """
    Launch one of es7s system monitors, or indicators. Mostly
    used by tmux.
    """


# noinspection PyTypeChecker
commands: list[click.Command] = [
    monitor_battery.BatteryMonitor,
    monitor_docker.DockerMonitor,
    monitor_cpu_load.CpuLoadMonitor,
    monitor_cpu_load_avg.CpuLoadAvgMonitor,
    monitor_cpu_freq.CpuFreqMonitor,
    monitor_system_date.SystemDateMonitor,
    monitor_system_time.SystemTimeMonitor,
    monitor_weather.WeatherMonitor,
]
for command in commands:
    group.add_command(command)
