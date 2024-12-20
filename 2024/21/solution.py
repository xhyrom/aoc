from collections import deque
from enum import Enum
from functools import cache
from typing import Any, TypeAlias

Grid = list[list[str]]
Position: TypeAlias = tuple[int, int]


numeric_keypad: Grid = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["#", "0", "A"],
]
directional_keypad: Grid = [["#", "^", "A"], ["<", "v", ">"]]


class Face(Enum):
    NORTH = (0, "^")
    EAST = (1, ">")
    SOUTH = (2, "v")
    WEST = (3, "<")

    def symbol(self) -> str:
        return self.value[1]

    @classmethod
    def from_delta(cls, dr: int, dc: int) -> "Face":
        match (dr, dc):
            case (0, 1):
                return cls.EAST
            case (1, 0):
                return cls.SOUTH
            case (0, -1):
                return cls.WEST
            case (-1, 0):
                return cls.NORTH
            case _:
                raise ValueError(f"Invalid delta: ({dr}, {dc})")


def find_paths(
    grid: Grid,
    start_row: int,
    start_col: int,
    end_row: int,
    end_col: int,
):
    queue = deque([(start_row, start_col, Face.NORTH, [])])
    paths = []
    min_length = float("inf")

    while queue:
        r, c, face, path = queue.popleft()

        if len(path) > min_length:
            continue

        if (r, c) == (end_row, end_col):
            if len(path) <= min_length:
                min_length = len(path)
                paths.append("".join(p[2] for p in path) + "A")

            continue

        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            new_r, new_c = r + dr, c + dc
            if (
                0 <= new_r < len(grid)
                and 0 <= new_c < len(grid[0])
                and grid[new_r][new_c] != "#"
            ):
                face = Face.from_delta(dr, dc)

                new_path = path + [(new_r, new_c, face.symbol())]
                queue.append((new_r, new_c, face, new_path))

    return paths


@cache
def directional_path_length(sequence: str, depth: int) -> int:
    if depth == 0:
        return len(sequence)

    start_row, start_col = find_point(directional_keypad, "A")
    total = 0

    for char in sequence:
        end_row, end_col = find_point(directional_keypad, char)

        paths = find_paths(
            directional_keypad,
            start_row,
            start_col,
            end_row,
            end_col,
        )
        total += min(directional_path_length(path, depth - 1) for path in paths)

        start_row, start_col = end_row, end_col

    return total


def sequence_length(sequence: str, depth: int) -> int:
    start_row, start_col = find_point(numeric_keypad, "A")
    total = 0

    for char in sequence:
        end_row, end_col = find_point(numeric_keypad, char)

        paths = find_paths(numeric_keypad, start_row, start_col, end_row, end_col)
        total += min(directional_path_length(path, depth) for path in paths)

        start_row, start_col = end_row, end_col

    return total


def find_point(grid: Grid, type: str) -> Position:
    return next(find_points(grid, type))


def find_points(grid: Grid, type: str):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                yield row, col


def part_1() -> Any:
    codes = [line for line in open("input.txt").read().splitlines()]
    result = 0

    for code in codes:
        id = int("".join([char for char in code if char.isdigit()]))
        length = sequence_length(code, 2)

        result += id * length

    return result


def part_2() -> Any:
    codes = [line for line in open("input.txt").read().splitlines()]
    result = 0

    for code in codes:
        id = int("".join([char for char in code if char.isdigit()]))
        length = sequence_length(code, 25)

        result += id * length

    return result
