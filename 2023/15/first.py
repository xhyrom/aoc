file = open("./input.txt").read().split(",")


def hash(text: str) -> int:
    r = 0

    for char in text:
        r += ord(char)
        r *= 17
        r %= 256

    return r


count = 0

for step in file:
    count += hash(step)

print(count)
