import urllib.request
from os import getenv


def schematic(grid: list[str]) -> list[int]:
    return [
        sum(1 for row in range(len(grid)) if grid[row][col] == "#")
        for col in range(len(grid[0]))
    ]


def locks_keys(filename: str) -> tuple[list[list[int]], list[list[int]]]:
    data = [x.splitlines() for x in open(filename).read().split("\n\n")]

    locks = list(map(schematic, [d for d in data if d[0].count(".") == 0]))
    keys = list(map(schematic, [d for d in data if d[-1].count(".") == 0]))

    return locks, keys


def can_fit(lock: list[int], key: list[int]) -> bool:
    return all(l + k <= 7 for l, k in zip(lock, key))


def part_1() -> int:
    locks, keys = locks_keys("input.txt")
    return sum(1 for lock in locks for key in keys if can_fit(lock, key))


def part_2() -> str:
    headers = {"Cookie": f"session={getenv('AOC_SESSION')}"}
    request = urllib.request.Request(
        "https://adventofcode.com/2024/day/25/answer",
        headers=headers,
        method="POST",
        data="level=2&answer=0".encode("ascii"),
    )
    urllib.request.urlopen(request)

    return ":)"
