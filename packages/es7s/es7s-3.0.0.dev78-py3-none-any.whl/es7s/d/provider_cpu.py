# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from ._base import DataProvider
from ..shared import get_config


class CpuProvider(DataProvider[dict]):
    def _is_enabled(self) -> bool:
        return get_config().getboolean('monitor.cpu-load-avg', 'enable')

    def _get_socket_topic(self) -> str:
        return 'cpu'

    def _collect(self) -> dict:
        return {
            "freq_mhz": psutil.cpu_freq(),
            "load_perc": psutil.cpu_percent(),
            "load_avg": psutil.getloadavg(),
            "core_count": psutil.cpu_count(),
        }
