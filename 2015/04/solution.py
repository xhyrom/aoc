from hashlib import md5
from typing import Callable


def hash(text: str, num: int):
    return md5(f"{text}{num}".encode("utf-8")).hexdigest()


def find(code: str, early: Callable[[str], bool]):
    i = 1

    while not early(hash(code, i)):
        i += 1

    return i


def part_1() -> int:
    code = open("input.txt").read().strip()
    return find(code, lambda x: x.startswith("00000"))


def part_2() -> int:
    code = open("input.txt").read().strip()
    return find(code, lambda x: x.startswith("000000"))
