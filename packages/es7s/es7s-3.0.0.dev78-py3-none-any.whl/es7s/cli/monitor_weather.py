# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import re

import click
import pytermor as pt

from ._base import _catch_and_log_and_exit, _catch_and_print
from ._base_monitor import (
    CoreMonitor,
    MonitorCliCommand,
    GenericRenderer,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
    CoreMonitorState,
)
from ..shared import (
    WeatherInfo,
    get_config,
    Styles,
    get_logger,
    format_weather_icon,
    SocketMessage,
)


class _WeatherMonitorConfig(CoreMonitorConfig):
    wind_warn_threshold: float = 10.0
    weather_icon_set_id: int = 0

    def update_from_config(self):
        super().update_from_config()
        self.wind_warn_threshold = get_config().getfloat(
            self._config_section, "wind-speed-warn-threshold"
        )
        self.weather_icon_set_id = get_config().getint(
            self._config_section,
            "weather-icon-set-id",
        )


@click.command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current weather",
    output_examples=[
        "│` 流 -4 °C `│",
        "│`!↑ 6.1m/s `│^A^",
    ],
)
@click.pass_context
@_catch_and_log_and_exit
@_catch_and_print
class WeatherMonitor(CoreMonitor[WeatherInfo, _WeatherMonitorConfig]):
    """
    Indicator of current weather. Queries 'wttr.in' web-service.

    Output is a fixed string 10 chars wide: │`!Ic TTT°C `│, where Ic is the weather
    icon, and TTT is current centigrade temperature. Alternative output format
    is: │`!D WWWm/s `│ (width is the same), where D is the wind direction icon and
    WWW is the speed of the wind in meters per second. Exclamation mark in either
    of formats indicates dangerously high wind speed, which is greater than
    <monitor.weather.wind-speed-warn-threshold> [default: 10] in m/s. Additionally,
    the monitor will periodically switch between primary mode with the temperature
    and alt mode with the wind, but only when necessary.

    Weather icon can be customized with config var <monitor.weather.weather-icon-set-id>,
    which is an integer such as 0 <= set-id <= 4, where 0 is the original emoji
    icon set [this is a default] and 1-4 are icon sets requiring NerdFont-compatible
    font to be available. Set 4 additionally provides differing icons for nighttime
    and daytime. Use '--demo' option to compare the sets.
    """

    def _init_settings(self) -> CoreMonitorSettings:
        return CoreMonitorSettings[_WeatherMonitorConfig](
            socket_topic="weather",
            socket_receive_interval_sec=0.1,
            update_interval_sec=0.1,  # both for network activity indicator
            message_ttl=3600,  # 1 hour
            alt_mode=True,
            network_comm_indic=True,
            config=_WeatherMonitorConfig("monitor.weather"),
            renderer=WeatherRenderer,
            demo_composer=WeatherDemoComposer,
        )

    def get_output_width(self) -> int:
        return 11

    def _format_data_impl(self, msg: SocketMessage[WeatherInfo]) -> pt.Text:
        logger = get_logger()
        fields = msg.data.fields
        logger.trace(fields, "Message data")

        weather_icon_origin = fields[0].strip().removesuffix("\ufe0f")
        weather_icon, weather_icon_st = format_weather_icon(
            weather_icon_origin, self._setup.config.weather_icon_set_id
        )

        temperature_origin = fields[1]
        temperature_origin = temperature_origin.removesuffix("°C").strip()
        temperature_i = int(temperature_origin)
        temperature_str = f"{abs(temperature_i):<2d}"
        if temperature_i > 0:
            temperature_str = "+" + temperature_str
        elif temperature_i < 0:
            temperature_str = "-" + temperature_str
        temperature_unit = "°C"

        wind_origin = fields[2]
        wind_icon, wind_speed_origin, _ = re.split(r"([\d.]+)", wind_origin)
        wind_speed_f = float(wind_speed_origin)
        wind_speed_str = pt.format_auto_float(wind_speed_f, 3, False)
        wind_warning = wind_speed_f > self._setup.config.wind_warn_threshold
        show_wind = self._state.is_alt_mode
        warning_tx = pt.Text(" ")
        wind_unit = "m/s"

        if wind_warning:
            warning_tx = pt.Text("!", pt.Style(Styles.WARNING_ACCENT, bold=True))

        logger.debug(f"Using weather icon set #{self._setup.config.weather_icon_set_id}")
        logger.debug(f"Weather icon: {weather_icon_origin} -> {weather_icon}")
        logger.debug(f"Temp. value: {temperature_origin} -> {temperature_i} -> {temperature_str}")
        logger.debug(f"Wind speed: {wind_speed_origin} -> {wind_speed_f} -> {wind_speed_str}")

        if show_wind:
            wind_icon_st = pt.Style(Styles.TEXT_DEFAULT)
            wind_val_st = pt.Style(Styles.TEXT_MAIN_VALUE, italic=True)
            wind_unit_st = pt.Style(Styles.TEXT_AUXILIARY, italic=True)
            if wind_warning:
                wind_icon_st = pt.Style(Styles.WARNING)
                wind_val_st = pt.Style(Styles.WARNING, bold=True)
                wind_unit_st = pt.Style(Styles.WARNING, dim=True)
            return (
                warning_tx
                + pt.Fragment(wind_icon, wind_icon_st)
                + pt.Fragment((" " + wind_speed_str.strip()).rjust(4), wind_val_st)
                + pt.Fragment(" " + wind_unit.ljust(4), wind_unit_st)
            )

        return (
            warning_tx
            + pt.Fragment(weather_icon, weather_icon_st)
            + pt.Fragment(temperature_str.rjust(5), Styles.TEXT_MAIN_VALUE)
            + pt.Fragment(temperature_unit.ljust(3), Styles.TEXT_AUXILIARY)
        )


class WeatherRenderer(GenericRenderer):
    def __init__(
        self,
        output_width: int,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
    ):
        super().__init__(output_width, monitor_setup, monitor_state, pt.NOOP_STYLE)


class WeatherDemoComposer(GenericDemoComposer):
    def render(self):
        msg = SocketMessage[WeatherInfo](WeatherInfo("MSK", ["*", "11", "0.0"]))
        self._print_row(self._render_msg(msg))
