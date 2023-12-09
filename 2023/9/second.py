from typing import List

file = open("./input.txt").readlines()

history: List[List[int]] = [
    [int(item) for item in entry]
    for entry in [x.split(" ") for x in (line.strip() for line in file)]
]

pyramids: List[List[List[int]]] = []


def get_sequence(entry: List[int]) -> List[int]:
    sequence = []
    for i, item in enumerate(entry):
        previous = entry[i - 1]
        sequence.append(item - previous)

    sequence.pop(0)
    return sequence


for entry in history:
    pyramids.append([])

    pyramids[-1].append(entry)
    sequence = get_sequence(entry)
    pyramids[-1].append(sequence)
    while not all(item == 0 for item in sequence):
        sequence = get_sequence(sequence)
        pyramids[-1].append(sequence)

for pyramid in pyramids:
    reversed_pyramid = list(reversed(pyramid))
    for i, row in enumerate(reversed_pyramid):
        if i == 0:
            row.insert(0, 0)

        next_row = reversed_pyramid[i + 1] if i + 1 < len(reversed_pyramid) else []
        next_row.insert(0, (next_row[0] if len(next_row) > 0 else 0) - row[0])

count = 0

for pyramid in pyramids:
    count += pyramid[0][0]

print(count)
