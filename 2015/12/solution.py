from json import loads
from re import findall


def part_1() -> int:
    data = open("input.txt").read().strip()
    return sum(int(num) for num in findall(r"\-?\d+", data))


def sum_numbers(data) -> int:
    match data:
        case int():
            return data
        case dict() if "red" in data.values():
            return 0
        case dict():
            return sum(map(sum_numbers, data.values()))
        case list():
            return sum(map(sum_numbers, data))
        case _:
            return 0


def part_2() -> int:
    data = loads(open("input.txt").read().strip())
    return sum_numbers(data)
