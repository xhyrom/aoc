from collections import deque
from typing import Set, Tuple

file = open("./input.txt").readlines()

grid = tuple(line.strip() for line in file)


def add(row: int, col: int, dr: int, dc: int, visited: set, queue: deque):
    if (row, col, dr, dc) not in visited:
        visited.add((row, col, dr, dc))
        queue.append((row, col, dr, dc))


# row, col, delta_row, delta_col
queue = deque([(0, -1, 0, 1)])
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

# grab row and col only
coordinates = {(row, col) for row, col, _, _ in visited}
energized = len(coordinates)

print(energized)
