from itertools import product


def concatenate(a: int, b: int) -> int:
    digits = 0
    temp = b
    while temp > 0:
        temp //= 10
        digits += 1

    return a * (10 ** digits) + b

def create_equation(line: str) -> tuple[list[int], int]:
    result, *numbers = line.split()
    numbers = [int(x) for x in numbers]

    return numbers, int(result[0:-1])

def evaluate(numbers: list[int], operators: tuple[str, ...]) -> int:
    result = numbers[0]

    for i, operator in enumerate(operators):
        match operator:
            case "+":
                result += numbers[i + 1]
            case "*":
                result *= numbers[i + 1]
            case "||":
                result = concatenate(result, numbers[i + 1])

    return result

def part_1() -> int:
    equations = map(create_equation, open("input.txt").read().splitlines())

    total = 0
    for numbers, result in equations:
        for operators in product(["+", "*"], repeat=len(numbers) - 1):
            if evaluate(numbers, operators) == result:
                total += result
                break

    return total

def part_2() -> int:
    equations = map(create_equation, open("input.txt").read().splitlines())

    total = 0
    for numbers, result in equations:
        for operators in product(["+", "*", "||"], repeat=len(numbers) - 1):
            if evaluate(numbers, operators) == result:
                total += result
                break

    return total
