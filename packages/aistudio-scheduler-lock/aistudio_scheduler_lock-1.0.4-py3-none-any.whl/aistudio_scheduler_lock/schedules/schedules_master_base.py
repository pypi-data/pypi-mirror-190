from abc import ABC, abstractmethod
from typing import TypedDict


class ScheduleDict(TypedDict):
    func: callable
    trigger: str
    days: int
    hours: int
    minutes: int
    seconds: int
    name: str
    is_enabled: bool


class SchedulesDict(TypedDict):
    global_schedules: list[ScheduleDict]
    local_schedules: list[ScheduleDict]


class SchedulesMasterBase(ABC):
    @abstractmethod
    def get_all(self) -> SchedulesDict:
        raise NotImplementedError()
