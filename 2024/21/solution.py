from functools import cache
from itertools import permutations
from typing import Optional

Position = tuple[int, int]

numeric_keypad = {
    "7": (0, 0),  # (row, col)
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

directional_keypad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}  # (row, col)

DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}  # (row, col)


@cache
def get_sequence(
    sequence: str,
    depth: int = 2,
    use_directional: bool = False,
    current: Optional[Position] = None,
) -> int:
    if not sequence:
        return 0

    keypad = directional_keypad if use_directional else numeric_keypad

    row, col = current or keypad["A"]
    target_row, target_col = keypad[sequence[0]]

    dr, dc = target_row - row, target_col - col
    moves = "v" * dr if dr > 0 else "^" * (-dr)
    moves += ">" * dc if dc > 0 else "<" * (-dc)

    if not depth:
        return (
            len(moves)
            + 1
            + get_sequence(
                sequence[1:], depth, use_directional, (target_row, target_col)
            )
        )

    candidates = []
    for permutation in set(permutations(moves)):
        row, col = current or keypad["A"]

        for move in permutation:
            dr, dc = DIRECTIONS[move]
            row, col = row + dr, col + dc

            if (row, col) not in keypad.values():
                break
        else:
            candidates.append(get_sequence("".join(permutation) + "A", depth - 1, True))

    min_len = min(candidates) if candidates else -1
    assert min_len > 0, f"Invalid sequence: {sequence}"

    return min_len + get_sequence(
        sequence[1:], depth, use_directional, (target_row, target_col)
    )


def solve(codes: list[str], depth: int) -> int:
    result = 0

    for code in codes:
        id = int("".join(c for c in code if c.isdigit()))
        sequence_length = get_sequence(code, depth=depth)
        result += id * sequence_length

    return result


def part_1() -> int:
    codes = open("input.txt").read().splitlines()

    return solve(codes, 2)


def part_2() -> int:
    codes = open("input.txt").read().splitlines()

    return solve(codes, 25)
