"""
Day 9: All in a Single Night

The problem is essentially a variation of the Traveling Salesman Problem (TSP),
but without the requirement to return to the starting city.

Key approach:
1. Use dynamic programming with bitmask to solve the problem:
   - Bitmask keeps track of visited cities
   - For each state (visited cities, last city), try all possible next cities
   - Cache results to avoid recalculating same states
2. For part 1, find minimum distance path
3. For part 2, find maximum distance path using same algorithm but maximizing instead

Time complexity: O(n^2 * 2^n) where n is number of cities
Space complexity: O(n * 2^n) for memoization cache
"""


def distances_cities() -> tuple[dict[tuple[str, str], int], list[str]]:
    distances = {}
    cities = set()

    for distance in open("input.txt").read().strip().split("\n"):
        start, _, end, _, dist = distance.split()
        distances[(start, end)] = int(dist)
        distances[(end, start)] = int(dist)

        cities.add(start)
        cities.add(end)

    return distances, list(cities)


def get_optimal_path(
    mask: int,
    last: int,
    cities: list[str],
    distances: dict[tuple[str, str], int],
    find_longest: bool,
    cache: dict[tuple[int, int], int],
) -> int:
    """
    Recursive function to find optimal (shortest/longest) path using dynamic programming with bitmask.

    Time complexity: O(n^2 * 2^n) where n is number of cities
    Space complexity: O(n * 2^n) for memoization cache

    References:
    - https://en.wikipedia.org/wiki/Travelling_salesman_problem
    - https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming/
    """

    if (mask, last) in cache:
        return cache[(mask, last)]

    if mask == (1 << len(cities)) - 1:
        return 0

    result = float("-inf") if find_longest else float("inf")
    curr_city = cities[last]

    for idx in range(len(cities)):
        if not (mask & (1 << idx)):
            next_city = cities[idx]
            if (curr_city, next_city) in distances:
                cost = distances[(curr_city, next_city)]

                subproblem = get_optimal_path(
                    mask | (1 << idx),
                    idx,
                    cities,
                    distances,
                    find_longest,
                    cache,
                )

                if find_longest:
                    result = max(result, cost + subproblem)
                else:
                    result = min(result, cost + subproblem)

    result = int(result)
    cache[(mask, last)] = result
    return result


def solve(
    distances: dict[tuple[str, str], int], cities: list[str], find_longest: bool = False
) -> int:
    cache = {}
    result = float("-inf") if find_longest else float("inf")
    for start in range(len(cities)):
        distance = get_optimal_path(
            1 << start, start, cities, distances, find_longest, cache
        )

        if find_longest:
            result = max(result, distance)
        else:
            result = min(result, distance)

    return int(result)


def part_1() -> int:
    distances, cities = distances_cities()
    return solve(distances, cities)


def part_2() -> int:
    distances, cities = distances_cities()
    return solve(distances, cities, find_longest=True)
