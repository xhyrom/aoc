def removable_rolls(grid: list[list[str]]) -> list[tuple[int, int]]:
    rows = len(grid)
    cols = len(grid[0])
    rolls = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                counter = 0

                for dr, dc in [
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                    (1, 1),
                    (1, -1),
                    (-1, 1),
                    (-1, -1),
                ]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == "@":
                            counter += 1

                if counter < 4:
                    rolls.append((r, c))

    return rolls


def part_1() -> int:
    grid = [list(line.strip()) for line in open("input.txt").readlines()]
    return len(removable_rolls(grid))


def part_2() -> int:
    grid = [list(line.strip()) for line in open("input.txt").readlines()]
    total = 0

    while True:
        rolls = removable_rolls(grid)
        if not rolls:
            break

        total += len(rolls)
        for r, c in rolls:
            grid[r][c] = "."

    return total
