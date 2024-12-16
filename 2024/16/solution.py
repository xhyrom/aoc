from collections import defaultdict, deque
from enum import Enum
from typing import Any
from heapq import heappush, heappop

Grid = list[list[str]]
Position = tuple[int, int]


class Face(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def counterclockwise(self):
        return Face((self.value - 1) % 4)

    def clockwise(self):
        return Face((self.value + 1) % 4)


DIRECTION = {
    Face.NORTH: (-1, 0),
    Face.EAST: (0, 1),
    Face.SOUTH: (1, 0),
    Face.WEST: (0, -1),
}


def find_point(grid: Grid, type: str) -> Position:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                return row, col

    raise ValueError("No robot found")


def part_1() -> Any:
    grid = [list(line) for line in open("input.txt").read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")

    pq = [(0, start_row, start_col, Face.EAST.value)]
    best_scores = {}

    while pq:
        score, r, c, facing = heappop(pq)
        facing = Face(facing)

        if score >= best_scores.get((r, c, facing), float("inf")):
            continue

        best_scores[(r, c, facing)] = score

        if (r, c) == (end_row, end_col):
            return score

        dr, dc = DIRECTION[facing]
        new_r, new_c = r + dr, c + dc
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and grid[new_r][new_c] != "#"
        ):
            heappush(pq, (score + 1, new_r, new_c, facing.value))

        new_facing = facing.clockwise()
        heappush(pq, (score + 1000, r, c, new_facing.value))

        new_facing = facing.counterclockwise()
        heappush(pq, (score + 1000, r, c, new_facing.value))

    return -1


def part_2() -> Any:
    grid = [list(line) for line in open("input.txt").read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")

    pq = [(0, start_row, start_col, Face.EAST.value, [])]
    best_scores = {}
    min_end_score = float("inf")
    tiles = {}

    while pq:
        score, r, c, facing, path = heappop(pq)
        facing = Face(facing)

        if (r, c) == (end_row, end_col):
            if score <= min_end_score:
                min_end_score = score
                if min_end_score not in tiles:
                    tiles[min_end_score] = set()
                tiles[min_end_score].update(path)
            continue

        if best_scores.get((r, c, facing), float("inf")) < score:
            continue

        best_scores[(r, c, facing)] = score

        dr, dc = DIRECTION[facing]
        new_r, new_c = r + dr, c + dc
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and grid[new_r][new_c] != "#"
        ):
            heappush(pq, (score + 1, new_r, new_c, facing.value, path + [(r, c)]))

        new_facing = facing.clockwise()
        heappush(pq, (score + 1000, r, c, new_facing.value, path + [(r, c)]))

        new_facing = facing.counterclockwise()
        heappush(pq, (score + 1000, r, c, new_facing.value, path + [(r, c)]))

    return len(tiles[min_end_score]) + 1
