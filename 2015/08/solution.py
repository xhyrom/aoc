from codecs import decode
from json import dumps
from typing import Callable


def solve(literals: list[str], calculate: Callable[[str], int]) -> int:
    result = 0

    for literal in literals:
        code_len = len(literal)
        str_len = calculate(literal)
        result += code_len - str_len

    return result


def part_1() -> int:
    literals = [line.strip() for line in open("input.txt")]
    return solve(literals, lambda x: len(decode(x[1:-1], "unicode_escape")))


def part_2() -> int:
    literals = [line.strip() for line in open("input.txt")]
    return -solve(literals, lambda x: len(dumps(x)))
