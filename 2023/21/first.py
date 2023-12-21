from collections import deque

lines = open("./input.txt").read().splitlines()


def find_starting_point(lines):
    """
    Finds the starting point of the maze.
    """
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == "S":
                return x, y

    assert False, "No starting point found."


starting_row, starting_col = find_starting_point(lines)

plots = set()
visited = {(starting_row, starting_col)}
queue = deque([(starting_row, starting_col, 64)])

while queue:
    row, col, steps = queue.popleft()

    if steps % 2 == 0:
        plots.add((row, col))

    if steps == 0:
        continue


    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dx, col + dy
        if (
            new_row < 0
            or new_row >= len(lines)
            or new_col < 0
            or new_col >= len(lines[0])
            or (new_row, new_col) in visited
            or lines[new_row][new_col] == "#"
        ):
            continue

        visited.add((new_row, new_col))
        queue.append((new_row, new_col, steps - 1))

print(len(plots))
