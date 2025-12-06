import math
import re
from itertools import groupby, zip_longest
from typing import Generator

Chunk = list[tuple[str, ...]]


def chunks(filename: str = "e1.input.txt") -> Generator[Chunk, None, None]:
    lines = open(filename).read().splitlines()
    columns = list(zip_longest(*lines, fillvalue=" "))

    for empty, group in groupby(
        columns, key=lambda col: all(char.isspace() for char in col)
    ):
        if not empty:
            yield list(group)


def solve_math(numbers: list[int], operator: str) -> int:
    if not numbers:
        return 0

    match operator:
        case "+":
            return sum(numbers)
        case "*":
            return math.prod(numbers)

    return -1


def part_1() -> int:
    total = 0

    for chunk in chunks():
        rows = ["".join(col) for col in zip(*chunk)]
        block = "\n".join(rows)

        operator = next((char for char in block if char in "+*"))
        numbers = [int(n) for n in re.findall(r"\d+", block)]

        total += solve_math(numbers, operator)

    return total


def part_2() -> int:
    total = 0

    for chunk in chunks():
        numbers = []
        operator = None

        for col in chunk:
            for char in col:
                if char in "+*":
                    operator = char

            numbers.append(int("".join(char for char in col if char.isdigit())))

        assert operator
        total += solve_math(numbers, operator)

    return total
