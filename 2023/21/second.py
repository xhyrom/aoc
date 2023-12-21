from collections import deque
import numpy as np

lines = open("./input.txt").read().splitlines()


def count(input_data, n):
    data = []
    for _ in range(5):
        for line in input_data:
            data.append(5 * line.replace("S", "."))
            
    width = len(data[0])
    height = len(data)

    starting_row, starting_col = width // 2, height // 2

    queue = deque([(starting_row, starting_col, 0)])
    plots = set()
    visited = set()

    while queue:
        row, col, steps = queue.popleft()

        if (row, col, steps) in visited:
            continue

        visited.add((row, col, steps))

        if steps == n:
            plots.add((row, col))
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < width and 0 <= new_col < height:
                if data[new_col][new_row] != "#":
                    queue.append((new_row, new_col, steps + 1))

    return len(plots)


# Polynomial extrapolation

a0 = count(lines, 65)  # Count with 65 steps
a1 = count(lines, 65 + 131)  # Count with 196 (65 + 131) steps
a2 = count(lines, 65 + 2 * 131)  # Count with 327 (65 + 2*131) steps

# Fit a polynomial of degree 2 to the counts at the three positions
# np.rint is used to round to the nearest integer
# The coefficients are then converted to integers and stored in a list
poly = (
    np.rint(np.polynomial.polynomial.polyfit([0, 1, 2], [a0, a1, a2], 2))
    .astype(int)
    .tolist()
)

n = (26501365 - 65) // 131

print(sum(poly[i] * n**i for i in range(3)))
