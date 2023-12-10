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

# print
for k, v in enumerate(lines):
    m = [str(dist[(x, k)]) if (x, k) in dist else str(v) for x, v in enumerate(v)]
    print("".join(m))

print(max(dist.values()))
