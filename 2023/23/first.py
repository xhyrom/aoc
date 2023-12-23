from collections import defaultdict, deque

grid = open("./input.txt").read().splitlines()

start_pos = (0, grid[0].index("."))
end_pos = (len(grid) - 1, grid[-1].index("."))

points = [start_pos, end_pos]

directions = {
    "^": [(-1, 0)],
    "v": [(1, 0)],
    "<": [(0, -1)],
    ">": [(0, 1)],
    ".": [(-1, 0), (1, 0), (0, -1), (0, 1)],
}


def fit(row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != "#"


for r, row in enumerate(grid):
    for c, col in enumerate(row):
        if col == "#":
            continue

        neighbors = 0
        for dr, dc in directions["."]:
            new_row = r + dr
            new_col = c + dc

            if fit(new_row, new_col):
                neighbors += 1

            if neighbors >= 3:
                points.append((r, c))

graph = defaultdict(dict)

for point_row, point_col in points:
    queue = deque([(0, point_row, point_col)])
    visited = {(point_row, point_col)}

    while queue:
        n, row, col = queue.popleft()

        if n != 0 and (row, col) in points:
            graph[(point_row, point_col)][(row, col)] = n
            continue

        for dr, dc in directions[grid[row][col]]:
            new_row = row + dr
            new_col = col + dc

            if fit(new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((n + 1, new_row, new_col))


def backtrack(point, visited):
    if point == end_pos:
        return 0

    path = 0

    visited.add(point)
    for new_point in graph[point]:
        if new_point not in visited:
            path = max(path, backtrack(new_point, visited) + graph[point][new_point])
    visited.remove(point)

    return path


print(backtrack(start_pos, set()))
