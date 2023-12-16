from collections import deque
from typing import Set, Tuple

file = open("./input.txt").readlines()

grid = tuple(line.strip() for line in file)


def add(row: int, col: int, dr: int, dc: int, visited: set, queue: deque):
    if (row, col, dr, dc) not in visited:
        visited.add((row, col, dr, dc))
        queue.append((row, col, dr, dc))


def calculate(ir: int, ic: int, idr: int, idc: int) -> int:
    queue = deque([(ir, ic, idr, idc)])
    visited: Set[Tuple[int, int, int, int]] = set()

    while queue:
        row, col, dr, dc = queue.popleft()

        row += dr
        col += dc

        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[row]):
            continue

        char = grid[row][col]

        if char == "." or (dc != 0 and ("|-" in char)):
            add(row, col, dr, dc, visited, queue)

        elif char == "/":
            dr, dc = -dc, -dr  # rotate
            add(row, col, dr, dc, visited, queue)

        elif char == "\\":
            dr, dc = dc, dr  # rotate
            add(row, col, dr, dc, visited, queue)

        elif char == "|":
            for dr, dc in ((1, 0), (-1, 0)):  # down, up
                add(row, col, dr, dc, visited, queue)

        else:  # char == "-"
            for dr, dc in ((0, 1), (0, -1)):  # right, left
                add(row, col, dr, dc, visited, queue)

    coordinates = {(row, col) for row, col, _, _ in visited}
    return len(coordinates)


max_energized = 0

# can start from any corner
for row in range(len(grid)):
    max_energized = max(max_energized, calculate(row, -1, 0, 1))
    max_energized = max(max_energized, calculate(row, len(grid[row]), 0, -1))

for col in range(len(grid[0])):
    max_energized = max(max_energized, calculate(-1, col, 1, 0))
    max_energized = max(max_energized, calculate(len(grid), col, -1, 0))

print(max_energized)
