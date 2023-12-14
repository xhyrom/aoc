file = open("./input.txt").readlines()

reflector = tuple(line.strip() for line in file)


def transpose(matrix):
    return list(map("".join, zip(*matrix)))


def rotate():
    global reflector
    reflector = tuple(row[::-1] for row in reflector)


def sort():
    global reflector
    reflector = transpose(reflector)

    for i, row in enumerate(reflector):
        groups = []
        # sort reflector by splitting #
        for group in row.split("#"):
            new_group = sorted(tuple(group), reverse=True)
            groups.append("".join(new_group))

        reflector[i] = "#".join(groups)


def spin_cycle():
    global reflector

    for _ in range(4):
        sort()
        rotate()


seen = set(reflector)
indexes = [reflector]

i = 0

while True:
    i += 1
    spin_cycle()

    if reflector in seen:
        break

    seen.add(reflector)
    indexes.append(reflector)

first = indexes.index(reflector)

reflector = indexes[(1000000000 - first) % (i - first) + first]

count = 0

for i, row in enumerate(reversed(reflector)):
    count += row.count("O") * (i + 1)

print(count)
