import re
from typing import List, Tuple

# Open the file and read the lines into a list
lines: List[str] = open("./input.txt").read().splitlines()


def is_symbol(char: str) -> bool:
    """
    Checks if a character is a symbol.

    Parameters:
    char (str): The character to check.

    Returns:
    bool: True if the character is a symbol, False otherwise.
    """
    return char != "." and not char.isdigit()


def get_parts() -> List[List[Tuple[int, int, int]]]:
    """
    Extracts the parts from the lines.

    Returns:
    List[List[Tuple[int, int, int]]]: A list of parts for each line.
    """
    parts: List[List[Tuple[int, int, int]]] = []
    for i, line in enumerate(lines):
        parts.append([])

        # Find all numbers in the line
        for match in re.finditer(r"\d+", line):
            start_index = match.start(0)
            end_index = match.end(0) - 1
            number = int(match.group(0))
            part = (start_index, end_index, number)
            parts[i].append(part)

    return parts


count = 0
parts: List[List[Tuple[int, int, int]]] = get_parts()

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char != "*":
            continue

        adjacent_parts: List[int] = []

        # Loop over the line above, the current line, and the line below
        for k in range(-1, 2):
            # Check if the line exists
            if i + k < 0 or i + k > len(lines):
                continue

            # Loop over each part in the line
            for start_index, end_index, number in parts[i + k]:
                if start_index - 1 <= j <= end_index + 1:
                    adjacent_parts.append(number)

        # If there are two adjacent parts, multiply them and add to the count
        if len(adjacent_parts) == 2:
            count += adjacent_parts[0] * adjacent_parts[1]

print(count)
