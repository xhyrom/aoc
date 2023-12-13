file = open("./input.txt").read().split("\n\n")

NOTE = list[str]

notes: list[NOTE] = [x.splitlines() for x in file]


def reflects(note: NOTE, i: int = 0) -> bool:
    rows, cols = len(note), len(note[0])
    bad = 0

    for col in range(cols):
        for row in range(rows):
            second_row = i * 2 + 1 - row
            if (second_row < 0) or (second_row >= row):
                continue

            if note[row][col] != note[second_row][col]:
                bad += 1

    return bad == 1


def transpose(note: NOTE):
    return list(zip(*note))


total = 0

for note in notes:
    transposed_note = transpose(note)

    rows, cols = len(note), len(note[0])

    row = next((i for i in range(rows - 1) if reflects(note, i)), -1)
    total += (row + 1) * 100

    col = next((i for i in range(cols - 1) if reflects(transposed_note, i)), -1)
    total += col + 1


print(total)
