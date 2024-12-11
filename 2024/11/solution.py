from typing import Any


def solve(iter: int) -> int:
    numbers = list(map(int, open("input.txt").read().split()))
    dict = {}  # key is the stone number, value is the count of the stones with that number

    for num in numbers:
        dict[num] = dict.get(num, 0) + 1

    for _ in range(iter):
        new_dict = {}

        for key, value in dict.items():
            if key == 0:
                new_dict[1] = new_dict.get(1, 0) + value
            elif len(str(key)) % 2 == 0:
                left_half = int(str(key)[: len(str(key)) // 2])
                right_half = int(str(key)[len(str(key)) // 2 :])

                new_dict[left_half] = new_dict.get(left_half, 0) + value
                new_dict[right_half] = new_dict.get(right_half, 0) + value
            else:
                new_dict[key * 2024] = new_dict.get(key * 2024, 0) + value

        dict = new_dict

    return sum(dict.values())


def part_1() -> Any:
    return solve(25)


def part_2() -> Any:
    return solve(75)
