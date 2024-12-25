def count_digits(n: int):
    """
    Counts the number of digits in a given number.
    """

    count = 0
    while n > 0:
        n //= 10
        count += 1

    return count


def ends_with(number: int, ending: int):
    """
    Checks if the number ends with the digits of the ending number.
    """

    return number % (10 ** count_digits(ending)) == ending


def create_equation(line: str) -> tuple[list[int], int]:
    result, *numbers = line.split()
    return [int(x) for x in numbers], int(result[:-1])


def solvable(
    numbers: list[int], current_value: int, operators: list[str], index: int = -1
) -> bool:
    """
    Recursively checks if the equation is valid by working backwards from the target value. This approach is
    faster than trying all possible combinations of the operators, since we can eliminate many possibilities.

    Parameters:
    - numbers: A list of integers that we want to use in the equation.
    - current_value: The target value we want to reach by applying the operators to the numbers.
    - operators: A list of operators that can be used ('+', '*', '||').
    - index: The current index in the numbers list.

    The function works by applying the inverse of each operator to the current value and checking if the resulting
    value can be achieved with the remaining numbers:
    - For addition ('+'), we subtract the current number from the current value. We ensure that the current value
      is greater than or equal to the current number to avoid negative results.
    - For multiplication ('*'), we divide the current value by the current number. We check that the current value
      is exactly divisible by the current number to maintain integer results.
    - For concatenation ('||'), we check if the current value ends with the current number and then remove those digits.
      This ensures that the current value actually ends with the digits of the current number, making the operation valid.
    """

    if index == -1:  # set the index to the last element
        index = len(numbers) - 1

    if index == 0:
        return current_value == numbers[0]
    else:
        for operator in operators:
            match operator:
                case "+":
                    if current_value >= numbers[index] and solvable(
                        numbers, current_value - numbers[index], operators, index - 1
                    ):
                        return True
                case "*":
                    if current_value % numbers[index] == 0 and solvable(
                        numbers, current_value // numbers[index], operators, index - 1
                    ):
                        return True
                case "||":
                    if ends_with(current_value, numbers[index]) and solvable(
                        numbers,
                        current_value // 10 ** count_digits(numbers[index]),
                        operators,
                        index - 1,
                    ):
                        return True

        return False


def part_1() -> int:
    equations = map(create_equation, open("input.txt").read().splitlines())
    total = 0

    for numbers, result in equations:
        if solvable(numbers, result, ["+", "*"]):
            total += result

    return total


def part_2() -> int:
    equations = map(create_equation, open("input.txt").read().splitlines())
    total = 0

    for numbers, result in equations:
        if solvable(numbers, result, ["+", "*", "||"]):
            total += result

    return total
