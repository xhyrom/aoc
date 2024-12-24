from typing import Callable, TypeVar

T = TypeVar("T")


def process(
    instructions: str, early: Callable[[int, int], tuple[bool, T]] | None = None
) -> T | int:
    floor = 0

    for i, instruction in enumerate(instructions):
        if instruction == "(":
            floor += 1
        elif instruction == ")":
            floor -= 1

        if early is not None:
            met, value = early(floor, i)
            if met:
                return value

    return floor


def part_1() -> int:
    instructions = open("input.txt").read()
    return process(instructions)


def part_2() -> int:
    instructions = open("input.txt").read()
    return process(instructions, lambda current_floor, i: (current_floor == -1, i + 1))
