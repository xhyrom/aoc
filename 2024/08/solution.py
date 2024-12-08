from itertools import combinations
from typing import Any


def is_valid(r, c, grid) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def get_antennas(grid) -> dict[str, list[tuple[int, int]]]:
    antennas = {}

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                antennas[cell] = antennas.get(cell, []) + [(r, c)]

    return antennas


def part_1() -> Any:
    grid = [line.strip() for line in open("input.txt").read().splitlines()]
    antinodes = set()

    for positions in get_antennas(grid).values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            p1 = (2 * r2 - r1, 2 * c2 - c1)
            p2 = (2 * r1 - r2, 2 * c1 - c2)

            if is_valid(*p1, grid):
                antinodes.add(p1)

            if is_valid(*p2, grid):
                antinodes.add(p2)

    return len(antinodes)


def part_2() -> Any:
    grid = [line.strip() for line in open("input.txt").read().splitlines()]
    antinodes = set()

    for positions in get_antennas(grid).values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            directions = [(r2 - r1, c2 - c1, r1, c1), (r1 - r2, c1 - c2, r2, c2)]

            for dr, dc, r, c in directions:
                while is_valid(r, c, grid):
                    antinodes.add((r, c))
                    r += dr
                    c += dc

    return len(antinodes)
