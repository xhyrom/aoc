from typing import Dict, List

Cube = tuple[int, str]

games: Dict[str, List[List[Cube]]] = {}

# load game
with open("./input.txt") as file:
  for line in file:
    line = line.strip()
    if line:
      line = line.split(":")
      game_id = int(line[0].split(" ")[1])
      games[game_id] = []

      cube_sets = line[1].strip().split(";")
      for set_cube in cube_sets:
        cubes = set_cube.split(",")
        games[game_id].append([])
        for cube in cubes:
          cube = cube.strip()
          count = cube.split(" ")[0]
          color = cube.split(" ")[1]
          games[game_id][-1].append((int(count), color))


def set_minimum_cubes(minimum_cubes: Dict[str, Cube], cube_set: List[Cube]):
  for cube in cube_set:
    if minimum_cubes.get(cube[1], 0) < cube[0]:
      minimum_cubes[cube[1]] = cube[0]

count = 0

for game_id, cube_sets in games.items():
  power_count = 1
  minimum_cubes = {}
  for cube_set in cube_sets:
    for cube in cube_set:
      set_minimum_cubes(minimum_cubes, cube_set)
  
  for required in minimum_cubes.values():
    power_count *= required

  count += power_count

print(count)