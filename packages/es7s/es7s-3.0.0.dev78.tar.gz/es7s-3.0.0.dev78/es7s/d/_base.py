# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime
import threading as th
import time
import typing as t
from collections import deque

from ..shared import get_logger, ShutdownableThread, SocketServer

T = t.TypeVar("T")


class DataProvider(ShutdownableThread, t.Generic[T]):
    def __init__(self):
        provider_name = f"{self._get_socket_topic()}-pv"
        super().__init__(command_name=provider_name, thread_name="collect")
        self._daemon_buf = deque[any](maxlen=1)
        self._network_req_event = th.Event()

        if not self._is_enabled():
            self.shutdown()
            self.start()
            return

        self._socket_server = SocketServer(
            self._daemon_buf,
            self._get_socket_topic(),
            provider_name,
            self._network_req_event,
        )
        self._socket_server.start()
        self.start()

    def run(self):
        super().run()
        logger = get_logger()
        wait_sec = 0

        while True:
            if self.is_shutting_down():
                self.destroy()
                break

            if 0 < wait_sec <= 1:
                time.sleep(wait_sec)
            elif wait_sec > 1:
                time.sleep(1)
                wait_sec -= 1
                continue

            try:
                data = self._collect()
                logger.debug(f"Collected data {data}")
                self._daemon_buf.append(data)
            except DataCollectionError:
                pass
            except Exception as e:
                logger.exception(e)

            wait_sec = self._get_poll_interval_sec()

    def _is_enabled(self) -> bool:
        return True

    def _get_socket_topic(self) -> str:
        raise NotImplementedError()

    def _get_poll_interval_sec(self) -> float:
        return 1.0

    def _collect(self) -> T:
        raise NotImplementedError()


class DataCollectionError(Exception):
    pass
