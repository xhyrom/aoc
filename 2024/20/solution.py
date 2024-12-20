from collections import deque
from typing import Generator

Grid = list[list[str]]
Position = tuple[int, int]
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def find_point(grid: Grid, type: str) -> Position:
    return next(find_points(grid, type))


def find_points(grid: Grid, type: str) -> Generator[Position, None, None]:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                yield row, col


def calculate_distances(
    grid: Grid,
    start_row: int,
    start_col: int,
    walls: set[Position],
) -> dict[Position, int]:
    distances: dict[Position, int] = {}
    queue = deque([(start_row, start_col, 0)])
    seen = set() | walls

    while queue:
        r, c, dist = queue.popleft()

        distances[(r, c)] = dist

        for dr, dc in DIRECTIONS:
            new_r, new_c = r + dr, c + dc

            if (
                0 <= new_r < len(grid)
                and 0 <= new_c < len(grid[0])
                and (new_r, new_c) not in seen
            ):
                seen.add((r, c))
                queue.append((new_r, new_c, dist + 1))

    return distances


def find_possible_shortcuts(
    grid: Grid,
    distances_from_start: dict[Position, int],
    distances_to_end: dict[Position, int],
    walls: set[Position],
    regular_time: int,
    max_cheat_time: int,
) -> list[int]:
    savings = []
    rows, cols = len(grid), len(grid[0])

    for start_r in range(rows):
        for start_c in range(cols):
            if (start_r, start_c) in walls:
                continue

            for end_r in range(
                max(0, start_r - max_cheat_time),
                min(rows, start_r + max_cheat_time + 1),
            ):
                for end_c in range(
                    max(0, start_c - max_cheat_time),
                    min(cols, start_c + max_cheat_time + 1),
                ):
                    if (end_r, end_c) in walls:
                        continue

                    manhattan_dist = abs(end_r - start_r) + abs(end_c - start_c)
                    if manhattan_dist > max_cheat_time:
                        continue

                    total_time = (
                        distances_from_start[(start_r, start_c)]
                        + manhattan_dist
                        + distances_to_end[(end_r, end_c)]
                    )

                    if total_time < regular_time:
                        savings.append(regular_time - total_time)

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
    distances_from_start = calculate_distances(grid, start_row, start_col, walls)
    distances_to_end = calculate_distances(grid, end_row, end_col, walls)

    regular_time = distances_from_start[(end_row, end_col)]

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
