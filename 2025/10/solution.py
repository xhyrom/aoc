import re
from collections import deque

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def solve_bfs(target: int, buttons: list[int]) -> int:
    queue = deque([(0, 0)])
    seen = {0}

    while queue:
        state, cost = queue.popleft()
        if state == target:
            return cost

        for btn in buttons:
            next = state ^ btn

            if next not in seen:
                seen.add(next)
                queue.append((next, cost + 1))

    return 0


def solve_milp(target: np.ndarray, buttons: list[list[int]]) -> int:
    dim = len(target)
    n_buttons = len(buttons)

    A = np.zeros((dim, n_buttons))
    for col_idx, indices in enumerate(buttons):
        valid_indices = [i for i in indices if i < dim]
        A[valid_indices, col_idx] = 1

    res = milp(
        c=np.ones(n_buttons),
        constraints=LinearConstraint(A, lb=target, ub=target),
        bounds=Bounds(lb=0, ub=np.inf),
        integrality=np.ones(n_buttons),
    )

    return int(round(res.fun))


def part_1() -> int:
    lines = open("input.txt").read().splitlines()
    total = 0

    for line in lines:
        match = re.search(r"\[([.#]+)\]", line)
        if not match:
            continue

        total += solve_bfs(
            sum(1 << i for i, c in enumerate(match.group(1)) if c == "#"),
            [
                sum(1 << int(x) for x in b.split(","))
                for b in re.findall(r"\(([\d,]+)\)", line)
            ],
        )

    return total


def part_2() -> int:
    lines = open("input.txt").read().splitlines()
    total = 0

    for line in lines:
        match = re.search(r"\{([\d,]+)\}", line)
        if not match:
            continue

        total += solve_milp(
            np.fromstring(match.group(1), sep=",", dtype=int),
            [[int(x) for x in b.split(",")] for b in re.findall(r"\(([\d,]+)\)", line)],
        )

    return total
