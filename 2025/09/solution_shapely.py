from itertools import combinations

from shapely.geometry import Polygon, box
from shapely.prepared import prep


def part_1() -> int:
    coords = [
        tuple(map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    return max(
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        for a, b in combinations(coords, 2)
    )


def part_2() -> int:
    coords = [
        tuple(map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    candidates = []
    for (x1, y1), (x2, y2) in combinations(coords, 2):
        min_x, max_x = (x1, x2) if x1 < x2 else (x2, x1)
        min_y, max_y = (y1, y2) if y1 < y2 else (y2, y1)

        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        candidates.append((area, min_x, min_y, max_x, max_y))

    candidates.sort(key=lambda x: x[0], reverse=True)

    poly = prep(Polygon(coords).simplify(0))

    for area, min_x, min_y, max_x, max_y in candidates:
        if poly.covers(box(min_x, min_y, max_x, max_y)):
            return area

    return -1
