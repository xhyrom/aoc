from typing import Any


def part_1() -> Any:
    position = 50
    zeros = 0

    for line in open("input.txt").readlines():
        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

        if position == 0:
            zeros += 1

    return zeros

def part_2() -> Any:
    position = 50
    zeros = 0

    for line in open("input.txt").readlines():
        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            count = (position - 1) // 100 - (position - distance - 1) // 100

            zeros += count
            position = (position - distance) % 100
        else:
            count = (position + distance) // 100 - position // 100

            zeros += count
            position = (position + distance) % 100

    return zeros
