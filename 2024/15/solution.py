from typing import Generator

Grid = list[list[str]]
Position = tuple[int, int]

DIRECTIONS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}


def find_robot(grid: Grid) -> Position:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@":
                return row, col

    raise ValueError("No robot found")


def find_box(grid: Grid) -> Generator[Position, None, None]:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] in ["O", "["]:
                yield row, col


def is_valid(grid: Grid, row: int, col: int) -> bool:
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != "#"


def check_movable(grid: Grid, row: int, col: int, dr: int, dc: int, seen: set) -> bool:
    if (row, col) in seen:
        return True
    seen.add((row, col))

    nr, nc = row + dr, col + dc
    match grid[nr][nc]:
        case "#":
            return False
        case "[":
            return check_movable(grid, nr, nc, dr, dc, seen) and check_movable(
                grid, nr, nc + 1, dr, dc, seen
            )
        case "]":
            return check_movable(grid, nr, nc, dr, dc, seen) and check_movable(
                grid, nr, nc - 1, dr, dc, seen
            )
        case "O":
            return check_movable(grid, nr, nc, dr, dc, seen)
    return True


def process_instruction(grid: Grid, row: int, col: int, instruction: str) -> Position:
    dr, dc = DIRECTIONS[instruction]

    nr, nc = row + dr, col + dc

    if not is_valid(grid, nr, nc):
        return row, col

    if grid[nr][nc] in ["[", "]", "O"]:
        seen = set()

        if not check_movable(grid, row, col, dr, dc, seen):
            return row, col

        while len(seen) > 0:
            for r, c in seen.copy():
                nr2, nc2 = r + dr, c + dc
                if (nr2, nc2) not in seen:
                    if grid[nr2][nc2] != "@" and grid[r][c] != "@":
                        grid[nr2][nc2] = grid[r][c]
                        grid[r][c] = "."

                    seen.remove((r, c))

        grid[row][col], grid[nr][nc] = grid[nr][nc], grid[row][col]
        return nr, nc

    grid[row][col], grid[nr][nc] = grid[nr][nc], grid[row][col]
    return nr, nc


def gps(grid: Grid) -> int:
    return sum(100 * box[0] + box[1] for box in find_box(grid))


def part_1() -> int:
    file = open("input.txt", "r").read()
    grid = [[char for char in line] for line in file.split("\n\n")[0].split("\n")]
    instructions = "".join(file.split("\n\n")[1].strip().split("\n"))

    row, col = find_robot(grid)
    for instruction in instructions:
        row, col = process_instruction(grid, row, col, instruction)

    return gps(grid)


def part_2() -> int:
    file = open("input.txt", "r").read()
    initial_grid = [
        [char for char in line] for line in file.split("\n\n")[0].split("\n")
    ]
    grid = []

    instructions = "".join(file.split("\n\n")[1].strip().split("\n"))

    # expand the grid
    for row in range(len(initial_grid)):
        if len(grid) <= row or row not in grid:
            grid.append([])

        for col in range(len(initial_grid[0])):
            match initial_grid[row][col]:
                case "#":
                    grid[row].extend(["#", "#"])
                case "O":
                    grid[row].extend(["[", "]"])
                case ".":
                    grid[row].extend([".", "."])
                case "@":
                    grid[row].extend(["@", "."])

    row, col = find_robot(grid)
    for instruction in instructions:
        row, col = process_instruction(grid, row, col, instruction)

    return gps(grid)
