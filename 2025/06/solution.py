import math
import re
from itertools import groupby, zip_longest
from typing import Generator

Chunk = list[tuple[str, ...]]


def chunks(filename: str = "input.txt") -> Generator[Chunk, None, None]:
    lines = open(filename).read().splitlines()
    columns = list(zip_longest(*lines, fillvalue=" "))

    for empty, group in groupby(
        columns, key=lambda col: all(char.isspace() for char in col)
    ):
        if not empty:
            yield list(group)


def solve(numbers: list[int], operator: str) -> int:
    if not numbers:
        return 0

    match operator:
        case "+":
            return sum(numbers)
        case "*":
            return math.prod(numbers)

    return -1


def part_1() -> int:
    return sum(
        solve(
            [
                int(n)
                for n in re.findall(r"\d+", "\n".join("".join(r) for r in zip(*chunk)))
            ],
            next(c for col in chunk for c in col if c in "+*"),
        )
        for chunk in chunks()
    )


def part_2() -> int:
    return sum(
        solve(
            [int(re.sub(r"\D", "", "".join(col))) for col in chunk],
            next(char for col in chunk for char in col if char in "+*"),
        )
        for chunk in chunks()
    )
