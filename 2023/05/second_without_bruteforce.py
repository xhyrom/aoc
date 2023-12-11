file = open("./input.txt").read().strip().split("\n\n")

inputs = [int(x) for x in file[0].replace("seeds: ", "").split(" ")]

# Seeds format: [(start, end), ...]
seeds = [(inputs[i], inputs[i] + inputs[i + 1]) for i in range(0, len(inputs), 2)]

# Map format: [[destination_range_start, source_range_start, range_length], ...]
maps = [
    [[int(y) for y in x.split(" ")] for x in file[i].splitlines()[1::]]
    for i in range(1, 8)
]


def remap(start: int, end: int, new_seeds: list[tuple[int]], m: list[int]) -> int:
    for destination_range_start, source_range_start, range_length in m:
        # Check if the ranges overlap
        overlap_start = max(start, source_range_start)
        overlap_end = min(end, source_range_start + range_length)

        if overlap_start < overlap_end:
            new_seeds.append(
                (
                    destination_range_start + (overlap_start - source_range_start),
                    destination_range_start + (overlap_end - source_range_start),
                )
            )

            if start < overlap_start:
                seeds.append((start, overlap_start))

            if overlap_end < end:
                seeds.append((overlap_end, end))

            break
    else:
        # If no overlap, just add the original range to the new seeds
        new_seeds.append((start, end))


r = float("inf")

for m in maps:
    new_seeds = []
    while len(seeds) > 0:
        start, end = seeds.pop()
        remap(start, end, new_seeds, m)

    seeds = new_seeds

print(min(seeds)[0])
