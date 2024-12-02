from dataclasses import dataclass
from typing import Any


@dataclass
class Run:
    func_name: str
    file_name: str
    result: Any
    time_taken: float

    def beauty_func_name(self) -> str:
        return self.func_name.replace("_", " ").capitalize()

    def time_taken_ms(self) -> float:
        return self.time_taken / 10**6

    def time_taken_formatted(self) -> str:
        if self.time_taken < 1000:
            value = self.time_taken
            unit = "ns"
        elif self.time_taken < 1000000:
            value = self.time_taken / 1000
            unit = "µs"
        elif self.time_taken < 1000000000:
            value = self.time_taken / 1000000
            unit = "ms"
        elif self.time_taken < 60000000000:
            value = self.time_taken / 1000000000
            unit = "s"
        else:
            value = self.time_taken / (60 * 1000000000)
            unit = "min"

        if abs(value - round(value)) < 0.0001:
            return f"{int(round(value))} {unit}"

        return f"{value:.3f} {unit}"
