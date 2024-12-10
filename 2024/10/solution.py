from typing import Any

Grid = list[list[int]]


def is_valid(grid: Grid, row: int, col: int):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def dfs(
    grid: Grid,
    row: int,
    col: int,
    trail: list[tuple[int, int]],
    heads: dict[tuple[int, int], int],
    seen: set[tuple[int, int]] | None = None,
) -> None:
    current = grid[row][col]
    upcoming = current + 1

    if current == 9:
        if seen is None or (row, col) not in seen:
            heads[trail[0]] = heads.get(trail[0], 0) + 1

            if seen is not None:
                seen.add((row, col))

        return

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if not is_valid(grid, row + dr, col + dc):
            continue

        if grid[row + dr][col + dc] == upcoming:
            trail.append((row + dr, col + dc))
            dfs(grid, row + dr, col + dc, trail, heads, seen)
            trail.pop()


def solve(track_seen: bool = True) -> int:
    grid: Grid = [
        [int(char) for char in line] for line in open("input.txt").read().splitlines()
    ]

    trailheads = [
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[0]))
        if grid[row][col] == 0
    ]

    heads = {pos: 0 for pos in trailheads}
    seen = set() if track_seen else None

    for row, col in trailheads:
        dfs(grid, row, col, [], heads, seen)

    return sum(heads.values())


def part_1() -> Any:
    return solve()


def part_2() -> Any:
    return solve(track_seen=False)
