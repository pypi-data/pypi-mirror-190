# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import requests

from ._base import DataProvider, DataCollectionError
from ..shared import WeatherInfo, get_config, get_logger


class WeatherProvider(DataProvider[WeatherInfo]):
    URL_TEMPLATE = "https://wttr.in/%(loc)s?format=%(fmt)s"
    QUERY_FORMAT = "%c|%t|%w&M"

    def __init__(self):
        self._location = get_config().get('monitor.weather', 'location')
        super().__init__()

    def _is_enabled(self) -> bool:
        return get_config().getboolean('monitor.weather', 'enable')

    def _get_socket_topic(self) -> str:
        return 'weather'

    def _get_poll_interval_sec(self) -> float:
        return 30.0

    def _collect(self) -> WeatherInfo:
        logger = get_logger()
        result = WeatherInfo(self._location, [])
        url = self.URL_TEMPLATE % {'loc': self._location, 'fmt': self.QUERY_FORMAT}
        try:
            self._network_req_event.set()
            response = requests.get(url, timeout=self._get_poll_interval_sec() - 1)
            logger.log_http_request(response)
        except requests.exceptions.ConnectionError as e:
            logger.error(e)
            raise DataCollectionError()
        except requests.RequestException as e:
            logger.exception(e)
            raise DataCollectionError()
        finally:
            self._network_req_event.clear()

        if not response.ok:
            logger.warning(f"Weather fetching failed: HTTP {response.status_code}")
            raise DataCollectionError()
        else:
            logger.trace(response.text, "Remote service response")
            result.fields = response.text.split('|')
        return result
