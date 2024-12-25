from re import findall
from typing import Type

import numpy as np

Instruction = tuple[str, str, str, str, str]


def instructions_lights(
    file_name: str, dtype: Type[np.generic]
) -> tuple[list[Instruction], np.ndarray]:
    instructions = findall(
        r"(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)",
        open("input.txt").read(),
    )
    lights = np.zeros((1000, 1000), dtype=dtype)

    return instructions, lights


def part_1() -> int:
    instructions, lights = instructions_lights("input.txt", dtype=np.bool)

    for instruction in instructions:
        operation, x1, y1, x2, y2 = instruction
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if operation == "toggle":
            lights[x1 : x2 + 1, y1 : y2 + 1] = ~lights[x1 : x2 + 1, y1 : y2 + 1]
        elif operation == "turn on":
            lights[x1 : x2 + 1, y1 : y2 + 1] = True
        else:
            lights[x1 : x2 + 1, y1 : y2 + 1] = False

    return np.sum(lights)


def part_2() -> int:
    instructions, lights = instructions_lights("input.txt", dtype=np.int64)

    for instruction in instructions:
        operation, x1, y1, x2, y2 = instruction
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if operation == "toggle":
            lights[x1 : x2 + 1, y1 : y2 + 1] += 2
        elif operation == "turn on":
            lights[x1 : x2 + 1, y1 : y2 + 1] += 1
        else:
            lights[x1 : x2 + 1, y1 : y2 + 1] -= 1
            lights[lights < 0] = 0

    return np.sum(lights)
