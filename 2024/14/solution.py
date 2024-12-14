from re import findall
from typing import Optional

Robot = tuple[list[int], list[int]]


def get_robots() -> list[Robot]:
    return [
        (
            [int(match[1]), int(match[0])],
            [int(match[3]), int(match[2])],
        )  # (row, col), (row_v, col_v)
        for match in findall(
            r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)",
            open("input.txt").read(),
        )
    ]


def is_valid(rows: int, cols: int, row: int, col: int):
    return 0 <= row < rows and 0 <= col < cols


def move_robots(
    robots: list[Robot],
    rows: int,
    cols: int,
    seen: Optional[set[tuple[int, int]]] = None,
) -> Optional[set[tuple[int, int]]]:
    for robot in robots:
        new_row = robot[0][0] + robot[1][0]
        new_col = robot[0][1] + robot[1][1]

        if not (0 <= new_row < rows):
            new_row = new_row % rows

        if not (0 <= new_col < cols):
            new_col = new_col % cols

        robot[0][0] = new_row
        robot[0][1] = new_col

        if seen is not None:
            seen.add((new_row, new_col))

    return seen


def quadrant_position(rows: int, cols: int, row: int, col: int) -> int:
    mid_row = rows // 2
    mid_col = cols // 2

    if (rows % 2 == 1 and row == mid_row) or (cols % 2 == 1 and col == mid_col):
        return -1

    if row < mid_row:
        if col < mid_col:
            return 0
        else:
            return 1
    else:
        if col < mid_col:
            return 2
        else:
            return 3


def part_1() -> int:
    robots = get_robots()

    rows = 103
    cols = 101

    for _ in range(100):
        move_robots(robots, rows, cols)

    quadrants = {}

    for robot in robots:
        pos = quadrant_position(rows, cols, *robot[0])
        quadrants[pos] = quadrants.get(pos, 0) + 1

    result = 1

    for key, count in quadrants.items():
        if key != -1:
            result *= count

    return result


def part_2() -> int:
    robots = get_robots()

    rows = 103
    cols = 101

    i = 0
    while True:
        seen = move_robots(robots, rows, cols, set())
        if seen is not None:
            if len(seen) == len(robots):
                return i + 1  # to seconds

        i += 1
