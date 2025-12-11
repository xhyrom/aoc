from math import prod
from typing import Any


def count_paths(node: str, target: str, graph: dict[str, list[str]], cache=None) -> int:
    if cache is None:
        cache = {}

    if (node, target) in cache:
        return cache[(node, target)]

    if node == target:
        return 1

    total = sum(
        count_paths(neighbor, target, graph, cache) for neighbor in graph.get(node, [])
    )
    cache[(node, target)] = total

    return total


def chain(graph: dict[str, list[str]], nodes: list[str]) -> int:
    cache = {}
    return prod(count_paths(a, b, graph, cache) for a, b in zip(nodes, nodes[1:]))


def part_1() -> Any:
    graph = {
        k: v.split()
        for k, v in (line.split(":") for line in open("input.txt").read().splitlines())
    }

    return count_paths("you", "out", graph)


def part_2() -> Any:
    graph = {
        k.strip(): v.split()
        for k, v in (line.split(":") for line in open("input.txt").read().splitlines())
    }

    return chain(graph, ["svr", "dac", "fft", "out"]) + chain(
        graph, ["svr", "fft", "dac", "out"]
    )
