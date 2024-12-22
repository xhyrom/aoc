from collections import deque
from typing import Any


def sequence(num: int) -> int:
    num = (num ^ (num * 64)) % 16777216
    num = (num ^ (num // 32)) % 16777216
    num = (num ^ (num * 2048)) % 16777216
    return num


def part_1() -> Any:
    buyers = map(int, open("input.txt").read().splitlines())
    result = []

    for buyer in buyers:
        for _ in range(2000):
            buyer = sequence(buyer)

        result.append(buyer)

    return sum(result)


def part_2() -> Any:
    buyers = map(int, open("input.txt").read().splitlines())
    delta = {}

    for buyer in buyers:
        diff = deque(maxlen=4)
        seen = set()

        for _ in range(2000):
            new_buyer = sequence(buyer)

            initial_last_digit = buyer % 10
            next_last_digit = new_buyer % 10
            diff.append(next_last_digit - initial_last_digit)

            if len(diff) == 4:
                pattern = tuple(diff)
                if pattern not in seen:
                    seen.add(pattern)

                    delta[pattern] = delta.get(pattern, 0) + next_last_digit

            buyer = new_buyer

    return max(delta.values())
