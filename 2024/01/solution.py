from typing import Any


def part_1() -> Any:
    left = []
    right = []

    with open("./input.txt") as file:
        for line in file:
            left_number, right_number = map(
                int, filter(lambda i: i, line.strip().split(" "))
            )
            left.append(left_number)
            right.append(right_number)

    left.sort()
    right.sort()

    distance = 0

    for i in range(len(left)):
        distance += abs(left[i] - right[i])

    return distance


def part_2() -> Any:
    from collections import Counter

    left = []
    right = []

    with open("./input.txt") as file:
        for line in file:
            left_number, right_number = map(
                int, filter(lambda i: i, line.strip().split(" "))
            )

            left.append(left_number)
            right.append(right_number)

    counter = Counter(right)
    similarity = 0

    for num in left:
        similarity += num * counter.get(num, 0)

    return similarity
