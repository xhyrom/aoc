import numpy as np


def part_1():
    target = int(open("input.txt").read().strip())
    limit = target // 10

    houses = np.zeros(limit + 1, dtype=np.int32)

    for elf in range(1, limit + 1):
        houses[elf::elf] += elf * 10

        if houses[elf] >= target:
            return elf

    return -1


def part_2():
    target = int(open("input.txt").read().strip())
    limit = target // 10

    houses = np.zeros(limit + 1, dtype=np.int32)

    for elf in range(1, limit + 1):
        end = min(limit, elf * 50)
        houses[elf : end + 1 : elf] += elf * 11

        if houses[elf] >= target:
            return elf

    return -1
