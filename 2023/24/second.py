import sympy

file = open("./input.txt").read().splitlines()


class Hailstone:
    def __init__(self, px: int, py: int, pz: int, vx: int, vy: int, vz: int):
        self.px = px
        self.py = py
        self.pz = pz

        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __repr__(self):
        return f"Hailstone{{px={self.px}, py={self.py}, pz={self.pz}, vx={self.vx}, vy={self.vy}, vz={self.vz}, a={self.a}, b={self.b}, c={self.c}}}"


hailstones = []

for line in file:
    line = line.replace("@", ",").strip().split(",")
    line = [int(item) for item in line]

    hailstones.append(Hailstone(*line))

xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")
equations = []

for i, hailstone in enumerate(hailstones):
    equations.append(
        (xr - hailstone.px) * (hailstone.vy - vyr)
        - (yr - hailstone.py) * (hailstone.vx - vxr)
    )
    equations.append(
        (yr - hailstone.py) * (hailstone.vz - vzr)
        - (zr - hailstone.pz) * (hailstone.vy - vyr)
    )

    if i < 2:
        continue

    ans = sympy.solve(equations)
    if all(x % 1 == 0 for solution in ans for x in solution.values()):
        ans = ans[0]
        print(ans[xr] + ans[yr] + ans[zr])

        break
