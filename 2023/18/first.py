file = open("./input.txt").readlines()

directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

dig_plan = [(0, 0)]
boundary_points = 0

for line in file:
    direction, distance, _ = line.split()

    dr, dc = directions[direction]
    distance = int(distance)

    row, col = dig_plan[-1]

    boundary_points += distance
    dig_plan.append((row + dr * distance, col + dc * distance))


# Calculate the area of the polygon using the Shoelace formula
# https://en.wikipedia.org/wiki/Shoelace_formula
area = 0

for i in range(len(dig_plan)):
    # Calculate the signed area contribution of the current segment and add it to the total area
    area += dig_plan[i][0] * (dig_plan[i - 1][1] - dig_plan[(i + 1) % len(dig_plan)][1])

# Normalize the area by taking the absolute value and dividing by 2
area = abs(area) // 2

# Use Pick's theorem to calculate the number of interior points
# https://en.wikipedia.org/wiki/Pick%27s_theorem
interior_points = area - boundary_points // 2 + 1

print(interior_points + boundary_points)
