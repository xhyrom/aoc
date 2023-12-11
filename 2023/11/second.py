from itertools import combinations
from bisect import bisect

file = open("./input.txt").readlines()

grid = []
empty_rows = []

for i, line in enumerate(file):
    row = list(line.strip())
    grid.append(row)

    if "#" not in row:
        empty_rows.append(i)


# Find the empty columns.
empty_columns = [x for x in range(len(grid[0])) if all(row[x] != "#" for row in grid)]

# Find the galaxies.
galaxies = []

# 1 milion - 1 because we replace empty row or column
expand_by = 1_000_000 - 1
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if col != ".":
            dx = expand_by * bisect(empty_columns, x)
            dy = expand_by * bisect(empty_rows, y)
            galaxies.append((x + dx, y + dy))

pairs = list(combinations(galaxies, 2))

count = 0

for p1, p2 in pairs:
    # we don't need to do BFS - we can just use Manhattan distance (https://en.wikipedia.org/wiki/Taxicab_geometry)
    count += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

print(count)
