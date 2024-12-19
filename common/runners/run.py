from dataclasses import dataclass
from typing import Any

from common.format import format_time


@dataclass
class Run:
    func_name: str
    file_name: str

    def beauty_func_name(self) -> str:
        return self.func_name.replace("_", " ").capitalize()


@dataclass
class SimpleRun(Run):
    result: Any
    time_taken: float

    def time_taken_formatted(self) -> str:
        return format_time(self.time_taken)


@dataclass
class BenchRun(Run):
    times: list[float]

    def __post_init__(self):
        self.times = sorted(self.times)

    def min(self) -> float:
        return self.times[0]

    def max(self) -> float:
        return self.times[-1]

    def avg(self) -> float:
        return sum(self.times) / len(self.times)

    def p(self, p: float) -> float:
        return self.times[int(len(self.times) * p)]

    def format_time(self, time: float) -> str:
        return format_time(time)
