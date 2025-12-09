from itertools import combinations

from shapely.geometry import Polygon, box


def part_1() -> int:
    coords = [
        tuple(map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    return max(
        abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1) for a, b in combinations(coords, 2)
    )


def part_2() -> int:
    coords = [
        tuple(map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    poly = Polygon(coords)
    max_area = -1

    for a, b in combinations(coords, 2):
        min_x, max_x = min(a[0], b[0]), max(a[0], b[0])
        min_y, max_y = min(a[1], b[1]), max(a[1], b[1])
        area = (max_x - min_x + 1) * (max_y - min_y + 1)

        if area < max_area or not poly.covers(box(min_x, min_y, max_x, max_y)):
            continue

        max_area = area

    return max_area
