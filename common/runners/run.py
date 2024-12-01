from dataclasses import dataclass
from typing import Any


@dataclass
class Run:
    func_name: str
    file_name: str
    result: Any
    time_taken: float
    with_startup_time: bool = False

    def beauty_func_name(self) -> str:
        return self.func_name.replace("_", " ").capitalize()

    def time_taken_ms(self) -> float:
        return self.time_taken / 10**6
