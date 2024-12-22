from collections import deque


def evolve(num: int) -> int:
    # equivalent to (num ^ (num * 64)) % 16777216
    num = (num ^ (num << 6)) & 0xFFFFFF

    # equivalent to (num ^ (num // 32)) % 16777216
    num = (num ^ (num >> 5)) & 0xFFFFFF

    # equivalent to (num ^ (num * 2048)) % 16777216
    num = (num ^ (num << 11)) & 0xFFFFFF
    return num


def part_1() -> int:
    buyers = map(int, open("input.txt").read().splitlines())
    result = 0

    for buyer in buyers:
        for _ in range(2000):
            buyer = evolve(buyer)

        result += buyer

    return result


def part_2() -> int:
    buyers = map(int, open("input.txt").read().splitlines())
    delta = {}

    for buyer in buyers:
        diff = deque(maxlen=4)
        seen = set()

        for _ in range(2000):
            new_buyer = evolve(buyer)

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
