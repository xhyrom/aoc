from dataclasses import dataclass, field

DIRECTIONS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


@dataclass
class Santa:
    row: int = 0
    col: int = 0
    seen: set[tuple[int, int]] = field(default_factory=set)

    def move(self, dr: int, dc: int):
        self.row += dr
        self.col += dc
        self.visit()

    def visit(self):
        self.seen.add((self.row, self.col))


def part_1() -> int:
    return part_2(1) + 1


def part_2(num_santas=2) -> int:
    moves = open("input.txt").read().strip()
    santas: list[Santa] = [Santa() for _ in range(num_santas)]

    for i, move in enumerate(moves):
        santa = santas[i % len(santas)]
        dr, dc = DIRECTIONS[move]
        santa.move(dr, dc)

    return len(set().union(*(santa.seen for santa in santas)))
