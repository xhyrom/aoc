from typing import List

file = open("./input.txt").read().strip().split("\n\n")

seeds = [int(x) for x in file[0].replace("seeds: ", "").split(" ")]

# Map format: [[destination_range_start, source_range_start, range_length], ...]
maps = [
    [[int(y) for y in x.split(" ")] for x in file[i].splitlines()[1::]]
    for i in range(1, 8)
]


def x_to_y(step: int, m: List[List[int]]) -> int:
    for destination_range_start, source_range_start, range_length in m:
        if step >= source_range_start and step < source_range_start + range_length:
            step = destination_range_start + (step - source_range_start)
            break

    return step


r = float("inf")

for seed in seeds:
    for m in maps:
        seed = x_to_y(seed, m)
    r = min(r, seed)

print(r)
