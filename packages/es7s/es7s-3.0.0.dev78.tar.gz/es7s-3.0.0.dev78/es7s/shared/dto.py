# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import time
import typing as t
from dataclasses import dataclass, field

T = t.TypeVar("T")


def now() -> int:
    return int(time.time())


@dataclass
class SocketMessage(t.Generic[T]):
    data: T
    timestamp: int = field(default_factory=now)
    network_comm: bool = False



@dataclass
class BatteryInfo:
    MAX_LEVEL = 100

    level: int | float | None = None
    is_charging: bool | None = None
    remaining_sec: int | None = None

    @property
    def is_max(self) -> bool:
        return self.level is not None and round(self.level) >= self.MAX_LEVEL


@dataclass()
class DockerStatus:
    match_amount: int = 0
    container_names: list[str] = None
    updated_in_prev_tick: bool = False

    def __post_init__(self):
        if self.container_names is None:
            self.container_names = []


@dataclass()
class WeatherInfo:
    location: str
    fields: list[str]
