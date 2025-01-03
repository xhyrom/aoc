"""
Day 15: Science for Hungry People

This problem involves optimizing a cookie recipe by finding the perfect balance of ingredients.
Each ingredient contributes different properties to the cookie (capacity, durability, flavor,
texture, and calories), and we must use exactly 100 teaspoons total. The cookie's score is
calculated by multiplying the sums of each property across all ingredients, with negative
sums counted as zero. Part 2 adds an additional constraint that the cookie must have
exactly 500 calories.

Key approach:
1. Generate all valid combinations of 100 teaspoons split among 4 ingredients
2. Optimize by pruning combinations that can't yield positive scores
3. Calculate running sums of properties and precompute scores in generator
4. Track maximum score (with calorie filter for part 2)

Time complexity: O(n³) in worst case where n=100 (teaspoons), but typically better due to pruning
"""

import math
from re import findall
from typing import Any, Generator


def generate_combinations(
    ingredients: list[list[int]],
) -> Generator[tuple[tuple[int, int, int, int], int], None, None]:
    for a in range(101):
        first = [a * ingredients[0][i] for i in range(4)]

        for b in range(101 - a):
            second = [first[i] + b * ingredients[1][i] for i in range(4)]

            if any(
                n <= 0
                for n in (
                    second[i]
                    + max(ingredients[2][i], ingredients[3][i]) * (100 - a - b)
                    for i in range(4)
                )
            ):
                continue

            for c in range(101 - a - b):
                d = 100 - a - b - c
                third = [second[i] + c * ingredients[2][i] for i in range(4)]
                fourth = [third[i] + d * ingredients[3][i] for i in range(4)]

                yield (a, b, c, d), math.prod(max(i, 0) for i in fourth[:4])


def part_1() -> Any:
    ingredients = [
        [int(group) for group in findall(r"-?\d+", line)]
        for line in open("input.txt").read().splitlines()
    ]

    result = 0

    for _, score in generate_combinations(ingredients):
        result = max(result, score)

    return result


def part_2() -> Any:
    ingredients = [
        [int(group) for group in findall(r"-?\d+", line)]
        for line in open("input.txt").read().splitlines()
    ]

    result = 0

    for amounts, score in generate_combinations(ingredients):
        calories = sum(amounts[i] * ingredients[i][4] for i in range(len(ingredients)))
        if calories == 500:
            result = max(result, score)

    return result
