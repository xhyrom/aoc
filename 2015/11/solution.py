"""
Day 11: Corporate Policy

The problem involves generating valid passwords according to specific rules:
1. Passwords must be exactly eight lowercase letters
2. Must include one increasing straight of at least three letters (e.g., abc)
3. Cannot contain letters i, o, or l
4. Must contain at least two different, non-overlapping pairs of letters

Key approach:
1. Convert password to ascii values and increment like a counter (right to left)
2. Skip invalid sequences by jumping ahead when hitting forbidden letters
3. Check each generated password against the rules until finding a valid one

Time complexity: O(n) for each password increment where n is password length
Space complexity: O(n) for storing password and pairs
"""

from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class Password:
    ords: list[int] = field(init=False)

    def __init__(self, password: str) -> None:
        self.ords = [ord(c) for c in password]

        for i in range(len(self.ords)):
            if self._skip_invalid_chars(i):
                break

    def _skip_invalid_chars(self, i: int) -> bool:
        if self.ords[i] in [ord("i"), ord("o"), ord("l")]:
            self.ords[i] += 1
            self.ords[i + 1 :] = [ord("a")] * len(self.ords[i + 1 :])
            return True

        return False

    def _generate(self) -> Iterator[None]:
        while True:
            self._increment_password()

            if self.meet():
                yield None

    def _increment_password(self) -> None:
        for i in range(len(self.ords) - 1, -1, -1):
            self.ords[i] += 1

            if self.ords[i] > ord("z"):
                self.ords[i] = ord("a")
            else:
                self._skip_invalid_chars(i)
                break

    def meet(self) -> bool:
        for i in range(len(self.ords) - 2):
            if (
                self.ords[i] + 1 == self.ords[i + 1]
                and self.ords[i] + 2 == self.ords[i + 2]
            ):
                break
        else:
            return False

        pairs = set()
        for i in range(len(self.ords) - 1):
            if self.ords[i] == self.ords[i + 1]:
                pairs.add(self.ords[i])
                if len(pairs) >= 2:
                    return True

        return False

    def next_valid(self) -> None:
        next(self._generate())

    def __str__(self) -> str:
        return "".join(map(chr, self.ords))


def part_1() -> Password:
    password = Password(open("input.txt").read().strip())
    password.next_valid()

    return password


def part_2() -> Password:
    password = part_1()
    password.next_valid()

    return password
