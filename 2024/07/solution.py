def concatenate(a: int, b: int) -> int:
    digits = 0
    temp = b
    while temp > 0:
        temp //= 10
        digits += 1
    return a * (10**digits) + b


def create_equation(line: str) -> tuple[list[int], int]:
    result, *numbers = line.split()
    return [int(x) for x in numbers], int(result[:-1])


def solve_equation(
    numbers: list[int],
    target: int,
    operators: list[str],
    index: int = 0,
    current_value: int = -1,
):
    if current_value == -1:
        current_value = numbers[0]
        index = 1

    if index == len(numbers):
        if current_value == target:
            yield []

        return

    if current_value > target:
        return

    for operator in operators:
        match operator:
            case "+":
                new_value = current_value + numbers[index]
            case "*":
                new_value = current_value * numbers[index]
            case "||":
                new_value = concatenate(current_value, numbers[index])
            case _:
                raise ValueError(f"Invalid operator: {operator}")

        for solution in solve_equation(
            numbers, target, operators, index + 1, new_value
        ):
            yield [operator] + solution


def part_1() -> int:
    equations = map(create_equation, open("input.txt").read().splitlines())
    total = 0

    for numbers, result in equations:
        for solution in solve_equation(numbers, result, ["+", "*"]):
            total += result
            break

    return total


def part_2() -> int:
    equations = map(create_equation, open("input.txt").read().splitlines())
    total = 0

    for numbers, result in equations:
        for solution in solve_equation(numbers, result, ["+", "*", "||"]):
            total += result
            break

    return total
