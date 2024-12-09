from typing import Any


def part_1() -> Any:
    disk_map = open("input.txt").read().strip()
    blocks = []

    disk_id = 0
    for i in range(len(disk_map)):
        if i % 2 == 0:
            blocks.extend([disk_id] * int(disk_map[i]))

            disk_id += 1
        else:
            blocks.extend(["."] * int(disk_map[i]))

    for i in (i for i, x in enumerate(blocks) if x == "."):
        while blocks[-1] == ".":
            blocks.pop()

        if len(blocks) <= i:
            break

        blocks[i] = blocks.pop()

    return sum(i * int(x) for i, x in enumerate(blocks) if x != ".")


def part_2() -> Any:
    disk_map = open("input.txt").read().strip()
    free_space = []
    files = {}

    disk_id = 0
    position = 0

    for i in range(len(disk_map)):
        size = int(disk_map[i])
        if i % 2 == 0:
            files[disk_id] = (position, size)

            disk_id += 1
        else:
            if size > 0:
                free_space.append((position, size))

        position += size

    for disk_id in range(len(files) - 1, -1, -1):
        pos, size = files[disk_id]
        found = None

        for idx, (start, length) in enumerate(free_space):
            if start >= pos:
                free_space = free_space[:idx]
                found = None
                break

            if size <= length:
                found = (idx, start, length)
                break

        if found:
            idx, start, length = found
            files[disk_id] = (start, size)

            if size == length:
                free_space.pop(idx)
            else:
                free_space[idx] = (start + size, length - size)

    return sum(
        disk_id * x
        for disk_id, (pos, size) in files.items()
        for x in range(pos, pos + size)
    )
