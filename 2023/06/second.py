file = open("./input.txt").readlines()

game = {"min": float("inf"), "max": 0}


for i, line in enumerate(file):
    line = line.split(":")[1]
    line = line.strip()
    number = int(line.replace(" ", ""))

    game["time" if i == 0 else "distance"] = number

for mpm in range(game["time"]):
    if mpm * (game["time"] - mpm) > game["distance"]:
        game["min"] = min(game["min"], mpm)
        game["max"] = max(game["max"], mpm)

count = game["max"] - game["min"] + 1
print(count)
