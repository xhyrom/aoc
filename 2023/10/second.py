from collections import deque
from typing import Dict, List, Tuple, Deque

file = open("./input.txt").readlines()

lines = [list(line.strip()) for line in file]

STARTING_POINT = "S"

pipe_to_direction_mappings = {
    "|": ["n", "s"],
    "-": ["w", "e"],
    "L": ["n", "e"],
    "J": ["n", "w"],
    "7": ["s", "w"],
    "F": ["s", "e"],
    STARTING_POINT: ["n", "s", "w", "e"],
}

directions_mapping = {
    "n": (0, -1, "s"),
    "s": (0, 1, "n"),
    "w": (-1, 0, "e"),
    "e": (1, 0, "w"),
}


def pipe_to_direction(con: str) -> List[tuple[int, int]]:
    """
    Maps a pipe to the directions.
    """
    possible_directions = pipe_to_direction_mappings[con]

    return [directions_mapping[pd][:2] for pd in possible_directions]


def find_starting_point(lines):
    """
    Finds the starting point of the maze.
    """
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == STARTING_POINT:
                return x, y

    assert False, "No starting point found."


def get_starting_point_piece_type(lines):
    """
    Finds the piece type of the starting point.
    """
    # Find the starting point of the maze.
    x, y = find_starting_point(lines)

    # Find the reachable directions from the starting point.
    reachable_directions = []
    for direction in directions_mapping:
        dx, dy, opposite = directions_mapping[direction]

        # Check if the target is in bounds.
        if y + dy < 0 or y + dy >= len(lines):
            continue
        if x + dx < 0 or x + dx >= len(lines[y + dy]):
            continue

        # Check if the target is a pipe piece.
        target = lines[y + dy][x + dx]
        if target not in pipe_to_direction_mappings:
            continue

        # Check if the target is reachable.
        target_directions = pipe_to_direction_mappings[target]
        if opposite in target_directions:
            reachable_directions.append(direction)

    # Check if there is a pipe piece that can be reached from all directions.
    for pipe_type in pipe_to_direction_mappings:
        if len(reachable_directions) == len(
            pipe_to_direction_mappings[pipe_type]
        ) and all(
            [
                direction in pipe_to_direction_mappings[pipe_type]
                for direction in reachable_directions
            ]
        ):
            return pipe_type

    return None


starting_point = find_starting_point(lines)
connections: Dict[Tuple[int, int], List[Tuple[int, int]]] = {
    (starting_point): [],
}

# Find all the connections.
for y, line in enumerate(lines):
    for x, con in enumerate(line):
        moves: List[Tuple[int, int]] = []
        if con not in pipe_to_direction_mappings:
            continue

        possible_directions = pipe_to_direction(con)
        moves = [(pd[0] + x, pd[1] + y) for pd in possible_directions]

        for move in moves:
            if starting_point == move:
                connections[starting_point].append((x, y))

        if starting_point != (x, y):
            connections[(x, y)] = moves


dist: Dict[Tuple[int, int], int] = {(starting_point): 0}
queue: Deque[Tuple[int, int]] = deque([starting_point])

# BFS - Breadth First Search
while queue:
    current = queue.popleft()
    for con in connections[current]:
        if con not in dist:
            dist[con] = dist[current] + 1
            queue.append(con)


# Replace the starting point with the correct pipe piece.
lines[starting_point[1]][starting_point[0]] = get_starting_point_piece_type(lines)

# Find pieces inside loops.
for i in range(len(lines)):
    norths = 0
    for j in range(len(lines[i])):
        con = lines[i][j]

        if (j, i) in dist:
            pipe_directions = pipe_to_direction_mappings[con]
            if "n" in pipe_directions:
                norths += 1
            continue

        if norths % 2 == 0:
            lines[i][j] = "O"
        else:
            lines[i][j] = "I"

print(sum([line.count("I") for line in lines]))
