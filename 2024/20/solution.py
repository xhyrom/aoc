from collections import deque
from heapq import heappop, heappush
from typing import Generator

Grid = list[list[str]]
Position = tuple[int, int]
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def find_point(grid: Grid, type: str) -> Position:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                return row, col

    raise ValueError(f"Can't find point {type}")


def find_points(grid: Grid, type: str) -> Generator[Position, None, None]:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                yield row, col


def dijkstra(
    grid: Grid,
    start_row: int,
    start_col: int,
    end_row: int,
    end_col: int,
    walls: set[Position],
):
    pq = [(0, start_row, start_col)]

    seen: dict[Position, int] = {}

    while pq:
        dist, r, c = heappop(pq)

        if dist >= seen.get((r, c), float("inf")):
            continue

        seen[(r, c)] = dist

        if (r, c) == (end_row, end_col):
            return dist

        for dx, dy in DIRECTIONS:
            new_r = r + dx
            new_c = c + dy
            if (
                0 <= new_r < len(grid)
                and 0 <= new_c < len(grid[0])
                and (new_r, new_c) not in walls
            ):
                heappush(pq, (dist + 1, new_r, new_c))

    return -1


def calculate_distances(
    grid: Grid,
    start_row: int,
    start_col: int,
    walls: set[Position],
) -> dict[Position, int]:
    rows, cols = len(grid), len(grid[0])
    distances: dict[Position, int] = {}
    queue = deque([(0, start_row, start_col)])
    visited = set()

    while queue:
        dist, r, c = queue.popleft()
        if (r, c) in visited:
            continue

        visited.add((r, c))
        distances[(r, c)] = dist

        for dx, dy in DIRECTIONS:
            new_pos = (r + dx, c + dy)
            if (
                0 <= new_pos[0] < rows
                and 0 <= new_pos[1] < cols
                and new_pos not in walls
                and new_pos not in visited
            ):
                queue.append((dist + 1, new_pos[0], new_pos[1]))

    return distances


def find_possible_shortcuts(
    grid: Grid,
    distances_from_start: dict[Position, int],
    distances_to_end: dict[Position, int],
    walls: set[Position],
    regular_time: int,
    max_cheat_time: int,
) -> list[int]:
    rows, cols = len(grid), len(grid[0])
    savings = []

    for start_r in range(rows):
        for start_c in range(cols):
            if (start_r, start_c) in walls or (
                start_r,
                start_c,
            ) not in distances_from_start:
                continue

            queue = deque([(start_r, start_c, 0)])
            seen = set()

            while queue:
                r, c, steps = queue.popleft()

                if steps > max_cheat_time:
                    continue

                if (r, c) not in walls and (r, c) in distances_to_end:
                    total_time = (
                        distances_from_start[(start_r, start_c)]
                        + steps
                        + distances_to_end[(r, c)]
                    )

                    if total_time < regular_time:
                        savings.append(regular_time - total_time)

                if steps < max_cheat_time:
                    for dr, dc in DIRECTIONS:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                            seen.add((nr, nc))
                            queue.append((nr, nc, steps + 1))

    return savings


def find_cheats(
    grid: Grid,
    start_row: int,
    start_col: int,
    end_row: int,
    end_col: int,
    walls: set[Position],
    max_cheat_time: int = 2,
) -> list[int]:
    regular_time = dijkstra(grid, start_row, start_col, end_row, end_col, walls)

    distances_from_start = calculate_distances(grid, start_row, start_col, walls)
    distances_to_end = calculate_distances(grid, end_row, end_col, walls)

    return find_possible_shortcuts(
        grid,
        distances_from_start,
        distances_to_end,
        walls,
        regular_time,
        max_cheat_time,
    )


def part_1(file: str = "input.txt") -> int:
    grid = [list(line) for line in open(file).read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")
    walls = set(find_points(grid, "#"))

    savings = find_cheats(grid, start_row, start_col, end_row, end_col, walls)

    return sum(1 for saving in savings if saving >= 100)


def part_2(file: str = "input.txt") -> int:
    grid = [list(line) for line in open(file).read().splitlines()]
    start_row, start_col = find_point(grid, "S")
    end_row, end_col = find_point(grid, "E")
    walls = set(find_points(grid, "#"))

    savings = find_cheats(
        grid, start_row, start_col, end_row, end_col, walls, max_cheat_time=20
    )
    return sum(1 for saving in savings if saving >= 100)
