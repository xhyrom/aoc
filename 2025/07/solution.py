from collections import defaultdict, deque
from typing import Any

Grid = list[list[str]]
Position = tuple[int, int]


def find_point(grid: Grid, type: str) -> Position:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == type:
                return row, col

    raise ValueError(f"Can't find point {type}")


def is_valid(grid: Grid, row: int, col: int) -> bool:
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def part_1() -> Any:
    grid: Grid = [list(x) for x in open("input.txt").read().splitlines()]
    start_row, start_col = find_point(grid, "S")

    result = 0

    queue = deque([(start_row, start_col)])
    seen = set()

    while queue:
        r, c = queue.popleft()

        if (r, c) in seen:
            continue

        seen.add((r, c))

        nr, nc = r + 1, c
        if not is_valid(grid, nr, nc):
            continue

        if grid[nr][nc] == "^":
            result += 1
            queue.append((nr, nc - 1))
            queue.append((nr, nc + 1))
        else:
            queue.append((nr, nc))

    return result


def part_2() -> Any:
    grid: Grid = [list(x) for x in open("input.txt").read().splitlines()]
    start_row, start_col = find_point(grid, "S")

    result = 0

    queue = deque([(start_row, start_col)])

    ways = defaultdict(int)
    ways[(start_row, start_col)] = 1

    queued = set([(start_row, start_col)])

    while queue:
        r, c = queue.popleft()
        queued.remove((r, c))

        nr, nc = r + 1, c
        if not is_valid(grid, nr, nc):
            result += ways[(r, c)]
            continue

        if grid[nr][nc] == "^":
            targets = [(nr, nc - 1), (nr, nc + 1)]
        else:
            targets = [(nr, nc)]

        for tr, tc in targets:
            if not is_valid(grid, tr, tc):
                result += ways[(r, c)]
                continue

            ways[(tr, tc)] += ways[(r, c)]
            if (tr, tc) not in queued:
                queue.append((tr, tc))
                queued.add((tr, tc))

    return result
