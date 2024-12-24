vowels = {"a", "e", "i", "o", "u"}
blocked = {"ab", "cd", "pq", "xy"}


def valid(text: str) -> bool:
    if len([char for char in text if char in vowels]) < 3:
        return False

    if any(b in text for b in blocked):
        return False

    for i, char in enumerate(text):
        if i + 1 >= len(text):
            continue

        if text[i + 1] == char:
            return True

    return False


def part_1() -> int:
    strings = open("input.txt").read().splitlines()
    result = 0

    for string in strings:
        if valid(string):
            result += 1

    return result
