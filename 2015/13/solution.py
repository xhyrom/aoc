"""
Day 13: Knights of the Dinner Table

This problem is a variation of the Traveling Salesman Problem (TSP) with a circular
arrangement and bidirectional happiness values between adjacent pairs.

Key approach:
1. Use dynamic programming with bitmask to solve the problem:
   - Bitmask keeps track of seated guests
   - For each state (seated guests, current person, starting person), try all possible next guests
   - Cache results to avoid recalculating same states
   - Track starting person to properly close the circle
2. Handle happiness values:
   - Each pair contributes two happiness values (both directions)
   - Final arrangement needs to account for happiness between first and last person

Time complexity: O(n^2 * 2^n) where n is number of guests
Space complexity: O(n * 2^n) for memoization cache

This is more efficient than generating all permutations O(n!) and provides
significant performance improvement for larger inputs.

Example arrangement:
    A -> B (A gains x, B gains y)
    B -> C (B gains p, C gains q)
    C -> D (C gains m, D gains n)
    D -> A (D gains j, A gains k)

Total happiness = sum of all gains/losses between adjacent pairs
"""

from collections import defaultdict


def attendes() -> dict[str, dict[str, int]]:
    attendees = defaultdict(dict)

    for line in open("input.txt").read().splitlines():
        name, _, operation, amount, _, _, _, _, _, _, neighbour = line.split()
        amount = int(amount)
        neighbour = neighbour[:-1]  # remove dot

        attendees[name][neighbour] = amount if operation == "gain" else -amount

    return attendees


def get_optimal_happiness(
    mask: int,
    curr: int,
    start: int,
    people: list[str],
    happiness: dict[str, dict[str, int]],
    cache: dict[tuple[int, int, int], int],
) -> int:
    state = (mask, curr, start)
    if state in cache:
        return cache[state]

    if mask.bit_count() == len(people) - 1:
        for last in range(len(people)):
            if not (mask & (1 << last)):
                return (
                    happiness[people[curr]][people[last]]
                    + happiness[people[last]][people[curr]]
                    + happiness[people[last]][people[start]]
                    + happiness[people[start]][people[last]]
                )

    result = float("-inf")

    for idx in range(len(people)):
        if not (mask & (1 << idx)):
            gain = (
                happiness[people[curr]][people[idx]]
                + happiness[people[idx]][people[curr]]
            )

            subproblem = get_optimal_happiness(
                mask | (1 << idx), idx, start, people, happiness, cache
            )

            result = max(result, gain + subproblem)

    result = int(result)
    cache[state] = result
    return result


def solve(happiness: dict[str, dict[str, int]]) -> int:
    people = list(happiness.keys())

    cache = {}
    result = float("-inf")

    for start in range(len(people)):
        result = max(
            result,
            get_optimal_happiness(1 << start, start, start, people, happiness, cache),
        )

    return int(result)


def part_1() -> int:
    return solve(attendes())


def part_2() -> int:
    happiness = attendes()

    me = "me"
    happiness[me] = {}

    for name in list(happiness.keys()):
        happiness[name][me] = 0
        happiness[me][name] = 0

    return solve(happiness)
