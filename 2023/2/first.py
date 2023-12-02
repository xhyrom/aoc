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

MAX_ALLOWED_RED_CUBES = 12
MAX_ALLOWED_GREEN_CUBES = 13
MAX_ALLOWED_BLUE_CUBES = 14

def is_fine(cube: Cube) -> bool:
  return cube[1] == "red" and cube[0] <= MAX_ALLOWED_RED_CUBES or \
    cube[1] == "green" and cube[0] <= MAX_ALLOWED_GREEN_CUBES or \
    cube[1] == "blue" and cube[0] <= MAX_ALLOWED_BLUE_CUBES

count = 0
invalid_games = set()

for game_id, cube_sets in games.items():
  for cube_set in cube_sets:
    for cube in cube_set:
      if not is_fine(cube):
        print(f"Game {game_id} is not fine")
        invalid_games.add(game_id)
        break

for game_id in games.keys():
  if game_id not in invalid_games:
    count += game_id

print(count)