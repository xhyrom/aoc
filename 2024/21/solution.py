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

DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}  # (row, col)


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
    dr, dc = end_row - start_row, end_col - start_col
    vertical_moves = "v" * dr if dr > 0 else "^" * (-dr)
    horizontal_moves = ">" * dc if dc > 0 else "<" * (-dc)

    candidates = []

    for path in (
        vertical_moves + horizontal_moves,
        horizontal_moves + vertical_moves,
    ):
        row, col = start_row, start_col
        for move in path:
            dr, dc = DIRECTIONS[move]
            row, col = row + dr, col + dc
            if grid[row][col] == "#":
                break
        else:
            candidates.append(path + "A")

    return candidates


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
