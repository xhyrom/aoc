from typing import List

file = open("./input.txt").read().strip().split("\n\n")

seeds = [int(x) for x in file[0].replace("seeds: ", "").split(" ")]
ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

# Map format: [[destination_range_start, source_range_start, range_length], ...]
maps = [
    [[int(y) for y in x.split(" ")] for x in file[i].splitlines()[1::]]
    for i in range(1, 8)
]

# Reverse the maps
maps = [[(end, start, range_length) for start, end, range_length in m] for m in maps][
    ::-1
]


def x_to_y(step: int, m: List[List[int]]) -> int:
    for destination_range_start, source_range_start, range_length in m:
        if step >= source_range_start and step < source_range_start + range_length:
            step = destination_range_start + (step - source_range_start)
            break

    return step


def find_location(seed):
    x = seed
    for m in maps:
        x = x_to_y(x, m)

    return x


def contains(seed):
    return any(start <= seed < end for start, end in ranges)


location = 0
while True:
    seed = find_location(location)
    if contains(seed):
        print(f"r: {location}")
        break

    location += 1

    # Print progress
    if location % 1_000_000 == 0:
        print(location)
