from enum import Enum
from heapq import heappop, heappush

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

    def __lt__(self, other):
        return self.value < other.value


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

    raise ValueError(f"Can't find point {type}")


def part_1() -> int:
    grid = [list(line) for line in open("input.txt").read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")

    pq = [(0, start_row, start_col, Face.EAST)]

    seen: dict[tuple[*Position, Face], float] = {}

    while pq:
        score, r, c, facing = heappop(pq)

        if score >= seen.get((r, c, facing), float("inf")):
            continue

        seen[(r, c, facing)] = score

        if (r, c) == (end_row, end_col):
            return score

        dr, dc = DIRECTION[facing]
        new_r, new_c = r + dr, c + dc
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and grid[new_r][new_c] != "#"
        ):
            heappush(pq, (score + 1, new_r, new_c, facing))

        new_facing = facing.clockwise()
        heappush(pq, (score + 1000, r, c, new_facing))

        new_facing = facing.counterclockwise()
        heappush(pq, (score + 1000, r, c, new_facing))

    return -1


def part_2() -> int:
    grid = [list(line) for line in open("input.txt").read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")

    pq = [(0, start_row, start_col, Face.EAST, [])]

    seen: dict[tuple[*Position, Face], float] = {}
    min_score = float("inf")
    tiles: dict[float, set[Position]] = {}

    while pq:
        score, r, c, facing, path = heappop(pq)

        if (r, c) == (end_row, end_col):
            if score <= min_score:
                min_score = score
                if min_score not in tiles:
                    tiles[min_score] = set()

                tiles[min_score].update(path + [(r, c)])

        if seen.get((r, c, facing), float("inf")) < score:
            continue

        seen[(r, c, facing)] = score

        dr, dc = DIRECTION[facing]
        new_r, new_c = r + dr, c + dc
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and grid[new_r][new_c] != "#"
        ):
            heappush(pq, (score + 1, new_r, new_c, facing, path + [(r, c)]))

        heappush(
            pq,
            (score + 1000, r, c, facing.clockwise(), path + [(r, c)]),
        )

        heappush(
            pq,
            (
                score + 1000,
                r,
                c,
                facing.counterclockwise(),
                path + [(r, c)],
            ),
        )

    return len(tiles[min_score])
