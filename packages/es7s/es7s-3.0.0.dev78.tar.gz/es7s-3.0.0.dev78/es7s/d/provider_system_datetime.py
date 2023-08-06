# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime

from ._base import DataProvider
from ..shared import get_config


class SystemDatetimeProvider(DataProvider[None]):
    def _is_enabled(self) -> bool:
        date_enabled = get_config().getboolean('monitor.system-date', 'enable')
        time_enabled = get_config().getboolean('monitor.system-time', 'enable')
        return date_enabled or time_enabled

    def _get_socket_topic(self) -> str:
        return 'sys-datetime'

    def _collect(self) -> None:
        pass
