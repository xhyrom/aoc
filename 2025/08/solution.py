import heapq
from collections import Counter
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    z: int


class UnionFind:
    def __init__(self, elements: list[Box]):
        self.parent = {e: e for e in elements}
        self.size = len(elements)

    def find(self, item: Box) -> Box:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])

        return self.parent[item]

    def union(self, a: Box, b: Box) -> bool:
        r1 = self.find(a)
        r2 = self.find(b)

        if r1 != r2:
            self.parent[r1] = r2
            self.size -= 1

            return True

        return False


def euclidean(a: Box, b: Box) -> int:
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2


def pair(boxes: list[Box], limit: Optional[int] = None) -> list[tuple[int, Box, Box]]:
    def generator():
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                dist = euclidean(boxes[i], boxes[j])
                yield (dist, boxes[i], boxes[j])

    if limit:
        return heapq.nsmallest(limit, generator(), key=lambda x: x[0])
    else:
        pairs = list(generator())
        pairs.sort(key=lambda x: x[0])
        return pairs


def part_1() -> int:
    boxes = [
        Box(*map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    pairs = pair(boxes, 1000)
    uf = UnionFind(boxes)

    for i in range(len(pairs)):
        dist, a, b = pairs[i]
        uf.union(a, b)

    sizes = Counter()
    for box in boxes:
        root = uf.find(box)
        sizes[root] += 1

    top = sizes.most_common(3)
    return top[0][1] * top[1][1] * top[2][1]


def part_2() -> int:
    boxes = [
        Box(*map(int, line.split(",")))
        for line in open("input.txt").read().splitlines()
    ]

    pairs = pair(boxes)
    uf = UnionFind(boxes)

    for dist, a, b in pairs:
        if uf.union(a, b) and uf.size == 1:
            return a.x * b.x

    return -1
