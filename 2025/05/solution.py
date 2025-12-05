from bisect import bisect_right
from typing import Sequence, cast

Interval = tuple[int, int]


class RangeSet:
    def __init__(self, intervals: Sequence[Interval]) -> None:
        intervals = sorted(intervals)

        self.merged: list[Interval] = []

        curr_start, curr_end = intervals[0]
        for start, end in intervals[1:]:
            if start <= curr_end:
                curr_end = max(curr_end, end)
            else:
                self.merged.append((curr_start, curr_end))
                curr_start, curr_end = start, end

            self.merged.append((curr_start, curr_end))

        self.starts = [iv[0] for iv in self.merged]

    def contains(self, point: int) -> bool:
        idx = bisect_right(self.starts, point)

        if idx == 0:
            return False

        return point <= self.merged[idx - 1][1]

    def total_length(self) -> int:
        return sum(end - start + 1 for start, end in self.merged)


def input():
    ranges, ids = open("input.txt").read().split("\n\n")
    ranges = list(
        cast(Interval, tuple(map(int, line.split("-")))) for line in ranges.splitlines()
    )
    ids = list(map(int, ids.splitlines()))

    return ranges, ids


def part_1() -> int:
    ranges, ids = input()

    tree = RangeSet(ranges)
    return sum(1 for id in ids if tree.contains(id))


def part_2() -> int:
    ranges, _ = input()

    tree = RangeSet(ranges)
    return tree.total_length()
