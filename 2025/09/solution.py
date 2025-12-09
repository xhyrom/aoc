from itertools import combinations, pairwise
from typing import cast

Coord = tuple[int, int]
Edge = tuple[int, int, int]


def part_1() -> int:
    coords = [
        tuple(map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    return max(
        (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
        for a, b in combinations(coords, 2)
    )


def filter_red_corners(coords: list[Coord]) -> list[Coord]:
    n = len(coords)
    if n <= 2:
        return coords

    corners = []
    for i in range(n):
        prev = coords[(i - 1 + n) % n]
        curr = coords[i]
        next = coords[(i + 1) % n]

        is_straight_x = prev[0] == curr[0] == next[0]
        is_straight_y = prev[1] == curr[1] == next[1]

        if not (is_straight_x or is_straight_y):
            corners.append(curr)

    return corners


def classify_edges(poly: list[Coord]) -> tuple[list[Edge], list[Edge]]:
    v_edges, h_edges = [], []

    for (x1, y1), (x2, y2) in pairwise(poly):
        if x1 == x2:  # vertical
            v_edges.append((x1, min(y1, y2), max(y1, y2)))
        else:  # horizontal
            h_edges.append((y1, min(x1, x2), max(x1, x2)))

    return v_edges, h_edges


def is_rect_intruded(
    bounds: tuple[int, int, int, int],
    v_edges: list[Edge],
    h_edges: list[Edge],
) -> bool:
    min_x, max_x, min_y, max_y = bounds

    for vx, vy_min, vy_max in v_edges:
        if min_x < vx < max_x:
            if max(vy_min, min_y) < min(vy_max, max_y):
                return True

    for hy, hx_min, hx_max in h_edges:
        if min_y < hy < max_y:
            if max(hx_min, min_x) < min(hx_max, max_x):
                return True

    return False


def is_point_inside(test_point: tuple[float, float], poly: list[Coord]) -> bool:
    tx, ty = test_point
    inside = False

    for (x1, y1), (x2, y2) in pairwise(poly):
        if (y1 > ty) != (y2 > ty):
            intersect_x = (x2 - x1) * (ty - y1) / (y2 - y1) + x1
            if tx < intersect_x:
                inside = not inside

    return inside


def part_2() -> int:
    coords: list[Coord] = [
        cast(Coord, tuple(map(int, line.split(","))))
        for line in open("input.txt").read().splitlines()
    ]

    corners = filter_red_corners(coords)

    poly = corners + [corners[0]]
    v_edges, h_edges = classify_edges(poly)

    max_area = 0

    for a, b in combinations(corners, 2):
        min_x, max_x = min(a[0], b[0]), max(a[0], b[0])
        min_y, max_y = min(a[1], b[1]), max(a[1], b[1])

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        area = width * height

        if area <= max_area:
            continue

        if is_rect_intruded((min_x, max_x, min_y, max_y), v_edges, h_edges):
            continue

        center_point = (min_x + 0.5, min_y + 0.5)
        if not is_point_inside(center_point, poly):
            continue

        max_area = area

    return max_area
