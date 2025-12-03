from typing import Optional


def intervals() -> list[tuple[int, ...]]:
    return list(
        map(
            lambda x: tuple(map(int, x.split("-"))),
            open("input.txt").read().replace("\n", "").strip().split(","),
        )
    )


def mobius(n: int) -> int:
    """
    Computes the Möbius function μ(n) for a given integer n.

    Returns:
      1: If n is square-free and has an even number of prime factors.
     -1: If n is square-free and has an odd number of prime factors.
      0: If n has a squared prime factor.

    Reference:
    https://en.wikipedia.org/wiki/M%C3%B6bius_function
    """

    if n == 1:
        return 1

    d = 2
    p_count = 0
    temp = n

    if temp % 2 == 0:
        temp //= 2
        p_count += 1
        if temp % 2 == 0:
            return 0

    d = 3
    while d * d <= temp:
        if temp % d == 0:
            if temp % (d * d) == 0:
                return 0
            temp //= d
            p_count += 1
        else:
            d += 2

    if temp > 1:
        p_count += 1

    return -1 if p_count % 2 else 1


def sum_periodic(limit: int, r_fixed: Optional[int] = None) -> int:
    """
    Calculates the sum of valid periodic numbers <= limit.

    Concepts:
    1. Geometric Series: Constructs the pattern multiplier (e.g., 10101) using:
       (10^(L*r) - 1) / (10^L - 1).
    2. Arithmetic Progression: Sums the valid seeds in O(1) time using:
       Sum = Count * (Min_Seed + Max_Seed) / 2.
    3. Möbius Inversion: Handle overlaps between periods
       (e.g., distinguishing period-2 vs period-4 patterns).

    Reference:
    https://www.reddit.com/r/adventofcode/comments/1pcbgai/2025_day_2_day_2_should_be_easy_right_closed/
    """

    limit_len = len(str(limit))
    total_sum = 0

    r_start = 2 if r_fixed is None else r_fixed
    r_end = limit_len + 1 if r_fixed is None else r_fixed + 1

    for r in range(r_start, r_end):
        mu = -mobius(r)
        if mu == 0:
            continue

        inner_sum = 0
        j = 0

        while True:
            L = j + 1
            total_len = L * r

            if total_len > limit_len:
                break

            pow_L = 10**L
            multiplier = (10**total_len - 1) // (pow_L - 1)

            min_seed = 10**j

            if min_seed * multiplier > limit:
                break

            max_seed_by_val = limit // multiplier
            max_seed_by_len = pow_L - 1

            t = min(max_seed_by_val, max_seed_by_len)

            if t >= min_seed:
                count = t - min_seed + 1
                sum_seeds = count * (min_seed + t) // 2
                inner_sum += sum_seeds * multiplier

            j += 1

        total_sum += mu * inner_sum

    return total_sum


def part_1() -> int:
    result = 0
    for start, end in intervals():
        result += sum_periodic(end, r_fixed=2) - sum_periodic(start - 1, r_fixed=2)

    return result


def part_2() -> int:
    result = 0
    for start, end in intervals():
        result += sum_periodic(end) - sum_periodic(start - 1)

    return result
