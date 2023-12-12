from functools import cache

file = open("./input.txt").readlines()

records = []
for line in file:
    line = line.strip()
    pattern, counts = line.split()

    # make five times longer
    pattern = "?".join([pattern] * 5)
    counts = tuple(int(x) for x in counts.split(",")) * 5

    records.append((pattern, counts))


@cache
def calculate_arrangements(pattern: str, counts: tuple[int]) -> int:
    # base case
    if not pattern:
        return len(counts) == 0

    if not counts:
        return "#" not in pattern

    result = 0

    if pattern[0] in ".?":
        result += calculate_arrangements(pattern[1:], counts)

    if (
        pattern[0] in "#?"
        and counts[0] <= len(pattern)
        and "." not in pattern[: counts[0]]
        and (counts[0] == len(pattern) or pattern[counts[0]] != "#")
    ):
        result += calculate_arrangements(pattern[counts[0] + 1 :], counts[1:])

    return result


total = 0
for pattern, counts in records:
    total += calculate_arrangements(pattern, counts)

print(total)
