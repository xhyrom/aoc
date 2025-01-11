import numpy as np


def simulate(grid: np.ndarray, steps: int, stuck_corners: bool = False) -> int:
    for _ in range(steps):
        padded = np.pad(grid, pad_width=1, mode="constant", constant_values=0)

        neighbors = (
            padded[:-2, :-2]
            + padded[:-2, 1:-1]
            + padded[:-2, 2:]
            + padded[1:-1, :-2]
            + padded[1:-1, 2:]
            + padded[2:, :-2]
            + padded[2:, 1:-1]
            + padded[2:, 2:]
        )

        grid = (
            ((grid == 1) & ((neighbors == 2) | (neighbors == 3)))
            | ((grid == 0) & (neighbors == 3))
        ).astype(np.int8)

        if stuck_corners:
            grid[0, 0] = grid[0, -1] = grid[-1, 0] = grid[-1, -1] = 1

    return np.sum(grid)


def part_1() -> int:
    grid = np.array(
        [[1 if c == "#" else 0 for c in line.strip()] for line in open("input.txt")],
        dtype=np.int8,
    )

    return simulate(grid, 100, False)


def part_2() -> int:
    grid = np.array(
        [[1 if c == "#" else 0 for c in line.strip()] for line in open("input.txt")],
        dtype=np.int8,
    )

    return simulate(grid, 100, True)
