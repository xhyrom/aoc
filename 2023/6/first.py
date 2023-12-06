import re

file = open("./input.txt").readlines()

games = []


for i, line in enumerate(file):
    line = line.split(":")[1]
    line = line.strip()
    numbers = [int(x) for x in line.split()]
    for y, num in enumerate(numbers):
        if len(games) <= y:
            games.append({
                "r": 0
            })

        games[y]["time" if i == 0 else "distance"] = num

for game in games:
    for mpm in range(game["time"]):
        if mpm * (game["time"] - mpm) > game["distance"]:
            game["r"] = game["r"] + 1

count = 1
for game in games:
    count *= game["r"]

print(count)