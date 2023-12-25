from itertools import combinations

file = open("./input.txt").read().splitlines()
RANGE = (200000000000000, 400000000000000)


class Hailstone:
    def __init__(self, px: int, py: int, pz: int, vx: int, vy: int, vz: int):
        self.px = px
        self.py = py
        self.pz = pz

        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.a = vy
        self.b = -vx
        self.c = vy * px - vx * py

    def __repr__(self):
        return f"Hailstone{{px={self.px}, py={self.py}, pz={self.pz}, vx={self.vx}, vy={self.vy}, vz={self.vz}, a={self.a}, b={self.b}, c={self.c}}}"


hailstones = []

for line in file:
    line = line.replace("@", ",").strip().split(",")
    line = [int(item) for item in line]

    hailstones.append(Hailstone(*line))

count = 0

for first, second in combinations(hailstones, 2):
    a1, b1, c1 = first.a, first.b, first.c
    a2, b2, c2 = second.a, second.b, second.c
    if a1 * b2 == b1 * a2:
        continue

    x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
    y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)

    if (
        RANGE[0] <= x <= RANGE[1]
        and RANGE[0] <= y <= RANGE[1]
        and all(
            (x - hs.px) * hs.vx >= 0 and (y - hs.py) * hs.vy >= 0
            for hs in (first, second)
        )
    ):
        count += 1

print(count)
