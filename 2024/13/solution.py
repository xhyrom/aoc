from fractions import Fraction
from re import findall


def buttons() -> list[list[int]]:
    return [
        [int(x) for x in match]
        for match in findall(
            r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
            open("input.txt").read(),
        )
    ]


def solve(ax, ay, bx, by, px, py) -> int:
    """
    Solves a 2x2 system of linear equations using matrix inversion method.

    The system of equations is:
        aa_x + bb_x = px
        aa_y + bb_y = py

    e. g.
        94a + 22b = 8400
        34a + 67b = 5400

        (a, b) = (80, 40)

    Reference:
    https://en.m.wikipedia.org/wiki/System_of_linear_equations#Matrix_solution
    """

    det = ax * by - ay * bx
    A_inverse = [
        [Fraction(by, det), Fraction(-bx, det)],
        [Fraction(-ay, det), Fraction(ax, det)],
    ]

    a = A_inverse[0][0] * px + A_inverse[0][1] * py
    b = A_inverse[1][0] * px + A_inverse[1][1] * py

    # check if a or b has denominator different than 1
    if a.denominator != 1 or b.denominator != 1:
        return 0

    return 3 * int(a) + 1 * int(b)


def part_1() -> int:
    result = 0

    for ax, ay, bx, by, px, py in buttons():
        result += solve(ax, ay, bx, by, px, py)

    return result


def part_2() -> int:
    result = 0

    for ax, ay, bx, by, px, py in buttons():
        result += solve(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)

    return result
