from collections import deque
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


def part_1(file: str = "input.txt") -> int:
    grid = [list(line) for line in open(file).read().splitlines()]
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

        for new_facing in (facing.clockwise(), facing.counterclockwise()):
            heappush(pq, (score + 1000, r, c, new_facing))

    return -1


def part_2(file: str = "input.txt") -> int:
    grid = [list(line) for line in open(file).read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")

    min_score = part_1(file)

    queue = deque([(0, start_row, start_col, Face.EAST, {(start_row, start_col)})])

    seen: dict[tuple[*Position, Face], float] = {}
    tiles: set[Position] = set({(start_row, start_col)})

    while queue:
        score, r, c, facing, path = queue.popleft()

        if score > min_score:
            continue

        if (r, c) == (end_row, end_col):
            tiles.update(path | {(r, c)})
            continue

        if seen.get((r, c, facing), float("inf")) < score:
            continue

        seen[(r, c, facing)] = score

        dr, dc = DIRECTION[facing]
        new_r, new_c = r + dr, c + dc
        if (
            0 <= new_r < len(grid)
            and 0 <= new_c < len(grid[0])
            and grid[new_r][new_c] != "#"
            and (new_r, new_c) not in path
        ):
            queue.append((score + 1, new_r, new_c, facing, path | {(new_r, new_c)}))

        for new_facing in (facing.clockwise(), facing.counterclockwise()):
            queue.append((score + 1000, r, c, new_facing, path))

    return len(tiles)
