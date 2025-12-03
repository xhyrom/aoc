from typing import Any


def banks() -> list[list[int]]:
    return list(
        map(lambda bank: list(map(int, bank.strip())), open("input.txt").readlines())
    )


def solve(removable: int) -> int:
    res = 0

    for batteries in banks():
        remove = len(batteries) - removable
        stack = []

        for digit in batteries:
            while remove > 0 and stack and stack[-1] < digit:
                stack.pop()
                remove -= 1

            stack.append(digit)

        val = int("".join(map(str, stack[:removable])))
        res += val

    return res


def part_1() -> int:
    return solve(2)


def part_2() -> Any:
    return solve(12)
