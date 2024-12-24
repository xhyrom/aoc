def valid(text: str) -> bool:
    pairs = {}
    for i in range(len(text) - 1):
        pair = text[i : i + 2]
        if pair in pairs:
            if i > pairs[pair] + 1:
                break
        else:
            pairs[pair] = i
    else:
        return False

    return any(text[i] == text[i + 2] for i in range(len(text) - 2))


def part_2() -> int:
    strings = open("input.txt").read().splitlines()
    result = 0

    for string in strings:
        if valid(string):
            result += 1

    return result
