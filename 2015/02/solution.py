def gifts() -> list[tuple[int, ...]]:
    return [
        tuple(map(int, gift.split("x")))
        for gift in open("input.txt").read().splitlines()
    ]


def part_1() -> int:
    result = 0

    for len, width, height in gifts():
        result += (
            2 * len * width
            + 2 * width * height
            + 2 * height * len
            + min(len * width, width * height, len * height)
        )

    return result


def part_2() -> int:
    result = 0

    for len, width, height in gifts():
        result += (
            min(2 * (len + width), 2 * (width + height), 2 * (height + len))
            + len * width * height
        )

    return result
