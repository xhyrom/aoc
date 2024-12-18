from heapq import heappop, heappush
from typing import Any, TypeAlias

Position: TypeAlias = tuple[int, int]


def manhattan_distance(r1: int, c1: int, r2: int, c2: int) -> int:
    return abs(r1 - r2) + abs(c1 - c2)


def solve(rows: int, cols: int, obstructions: list[Position]):
    end_row, end_col = rows - 1, cols - 1

    start_h = manhattan_distance(0, 0, end_row, end_col)
    pq = [(start_h, 0, 0, 0)]  # score + manhattan distance, score, row, col

    seen: dict[Position, float] = {}

    while pq:
        _, score, r, c = heappop(pq)

        if (r, c) == (end_row, end_col):
            return score

        if score >= seen.get((r, c), float("inf")):
            continue

        seen[(r, c)] = score

        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            new_r, new_c = r + dr, c + dc
            if (
                0 <= new_r < rows
                and 0 <= new_c < cols
                and (new_r, new_c) not in obstructions
            ):
                new_score = score + 1
                new_h = manhattan_distance(new_r, new_c, end_row, end_col)

                heappush(pq, (new_score + new_h, new_score, new_r, new_c))

    return -1


def part_1() -> Any:
    obstructions: list[Position] = [
        Position(map(int, x.split(",")[::-1]))  # row, col
        for x in open("input.txt").read().splitlines()
    ]

    return solve(71, 71, obstructions[:1024])


def part_2() -> Any:
    obstructions: list[Position] = [
        Position(map(int, x.split(",")[::-1]))  # row, col
        for x in open("input.txt").read().splitlines()
    ]

    start_at = 1024

    initial = obstructions[:start_at]
    remaining = obstructions[start_at:]

    left, right = 0, len(obstructions) - 1
    last_working = start_at

    while left <= right:
        mid = (left + right) // 2
        current_obstructions = initial + remaining[: mid + 1]

        r = solve(71, 71, current_obstructions)

        if r != -1:
            left = mid + 1
            last_working = mid + start_at  # +start_at to get the correct index
        else:
            right = mid - 1

    row, col = obstructions[last_working + 1]
    return f"{col},{row}"
