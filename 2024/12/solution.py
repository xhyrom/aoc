from typing import Any

Grid = list[list[str]]
Position = tuple[int, int]
Region = set[Position]

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_valid(grid: Grid, row: int, col: int):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def find_region(
    grid: Grid,
    area: str,
    row: int,
    col: int,
    seen: set[Position],
) -> Region:
    if not is_valid(grid, row, col):
        return set()

    if grid[row][col] != area:
        return set()

    if (row, col) in seen:
        return set()

    seen.add((row, col))

    result = {(row, col)}

    for dx, dy in DIRECTIONS:
        new_row = row + dx
        new_col = col + dy

        if is_valid(grid, new_row, new_col) and (new_row, new_col) not in seen:
            result.update(find_region(grid, area, new_row, new_col, seen))

    return result


def find_all_regions(grid: Grid) -> list[Region]:
    seen = set()
    regions = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) not in seen:
                region = find_region(grid, grid[row][col], row, col, set())

                seen.update(region)
                regions.append(region)

    return regions


def part_1() -> Any:
    grid: Grid = [list(x) for x in open("input.txt").read().splitlines()]
    regions = find_all_regions(grid)

    result = 0

    for region in regions:
        area = len(region)
        perimeter = 0

        for row, col in region:
            for dx, dy in DIRECTIONS:
                new_row = row + dx
                new_col = col + dy

                if (new_row, new_col) not in region:
                    perimeter += 1

        result += area * perimeter

    return result


def part_2() -> Any:
    grid: Grid = [list(x) for x in open("input.txt").read().splitlines()]
    regions = find_all_regions(grid)

    result = 0

    for region in regions:
        area = len(region)

        seen = set()
        corners = 0

        for row, col in region:
            for dx, dy in [
                (-0.5, -0.5),
                (0.5, -0.5),
                (0.5, 0.5),
                (-0.5, 0.5),
            ]:
                new_row = row + dx
                new_col = col + dy

                if (new_row, new_col) in seen:
                    continue

                seen.add((new_row, new_col))

                adjacent = sum(
                    (new_row + r, new_col + c) in region
                    for r, c in [
                        (-0.5, -0.5),
                        (0.5, -0.5),
                        (0.5, 0.5),
                        (-0.5, 0.5),
                    ]
                )

                if adjacent == 1 or adjacent == 3:
                    corners += 1
                elif adjacent == 2:
                    # diagonal
                    pattern = [
                        (r, c) in region
                        for r, c in [
                            (new_row - 0.5, new_col - 0.5),
                            (new_row + 0.5, new_col + 0.5),
                        ]
                    ]

                    if pattern == [True, True] or pattern == [False, False]:
                        corners += 2

        result += area * corners

    return result
