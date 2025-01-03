from collections import defaultdict


def backtrack(
    containers: list[int],
    remaining: int,
    index: int = 0,
    used: int = 0,
    result: dict[int, int] | None = None,
):
    if result is None:
        result = defaultdict(int)

    if remaining == 0:
        result[used] += 1
        return result

    if remaining < 0 or index >= len(containers):
        return result

    backtrack(containers, remaining, index + 1, used, result)
    backtrack(containers, remaining - containers[index], index + 1, used + 1, result)

    return result


def part_1() -> int:
    containers = list(map(int, open("input.txt").read().splitlines()))
    combinations = backtrack(containers, remaining=150)
    return sum(combinations.values())


def part_2() -> int:
    containers = list(map(int, open("input.txt").read().splitlines()))
    combinations = backtrack(containers, remaining=150)
    min_containers = min(combinations.keys())
    return combinations[min_containers]
