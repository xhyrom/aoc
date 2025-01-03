from typing import Any
from re import findall


def aunts() -> list[tuple[int, dict[str, int]]]:
    aunts: list[tuple[int, dict[str, int]]] = []

    for line in open("input.txt").read().splitlines():
        matches = findall(r"Sue (\d+)|(\w+: \d+)", line)
        aunt_id = int(matches[0][0])
        attributes = {
            key: int(value)
            for _, attr in matches
            if attr
            for key, value in [attr.split(": ")]
        }

        aunts.append((aunt_id, attributes))

    return aunts


def solve(predicate) -> int:
    for id, compounds in aunts():
        for key, value in compounds.items():
            if not predicate(key, value):
                break
        else:
            return id

    return -1


def part_1() -> Any:
    return solve(
        lambda key, value: {
            "akitas": lambda v: v == 0,
            "vizslas": lambda v: v == 0,
            "perfumes": lambda v: v == 1,
            "samoyeds": lambda v: v == 2,
            "cars": lambda v: v == 2,
            "children": lambda v: v == 3,
            "pomeranians": lambda v: v == 3,
            "goldfish": lambda v: v == 5,
            "trees": lambda v: v == 3,
            "cats": lambda v: v == 7,
        }[key](value)
    )


def part_2() -> Any:
    return solve(
        lambda key, value: {
            "akitas": lambda v: v == 0,
            "vizslas": lambda v: v == 0,
            "perfumes": lambda v: v == 1,
            "samoyeds": lambda v: v == 2,
            "cars": lambda v: v == 2,
            "children": lambda v: v == 3,
            "pomeranians": lambda v: v < 3,
            "goldfish": lambda v: v < 5,
            "trees": lambda v: v > 3,
            "cats": lambda v: v > 7,
        }[key](value)
    )
