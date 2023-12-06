import math

file = open("./input.txt").readlines()

game = {"min": float("inf"), "max": 0}


for i, line in enumerate(file):
    line = line.split(":")[1]
    line = line.strip()
    number = int(line.replace(" ", ""))

    game["time" if i == 0 else "distance"] = number

"""
This section explains the quadratic formula and how it relates to the problem.

mpm (or hold_time) is the number of milimeters per milisecond
race_time is the number of miliseconds
distance (or record) is the number of milimeters

We want to find the minimum hold time (mpm) that satisfies the following inequality:
mpm * (race_time - mpm) > distance

transformations:
mpm * race_time - mpm * mpm - distance > 0
(-1) * mpm ^ 2 + race_time * mpm + (-distance) > 0

where:
    a is -1
    b is race_time
    c is -distance

We can solve for mpm using the quadratic formula:
x = (-b ± √(b² - 4ac)) / (2a)
"""

a = -1
b = game["time"]
c = -game["distance"]


def solve_quadratic(a, b, c):
    # calculate the discriminant
    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        return None

    # ^0.5 is equivalent to square root
    x1 = (-b + discriminant**0.5) / (2 * a)
    x2 = (-b - discriminant**0.5) / (2 * a)

    return x1, x2


"""
This section explains why we need to floor the low one and ceil the high one.

The two solutions for mpm represent the minimum and maximum hold times that satisfy the inequality.

Therefore, we need to floor the low solution (x1) to get the minimum hold time.
This ensures that we only consider hold times that are greater than or equal to the minimum requirement.

Similarly, we need to ceil the high solution (x2) to get the maximum hold time.
This ensures that we only consider hold times that are less than or equal to the maximum possible value.
"""

solutions = solve_quadratic(a, b, c)

low = int(math.floor(solutions[0] + 1))
high = int(math.ceil(solutions[1] - 1))

print(high - low + 1)
