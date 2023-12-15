from collections import defaultdict

file = open("./input.txt").read().split(",")


def hash(text: str) -> int:
    r = 0

    for char in text:
        r += ord(char)
        r *= 17
        r %= 256

    return r


boxes = defaultdict(list)

for step in file:
    if "-" in step:
        label = step.split("-")[0]
        box = hash(label)

        for box_label, focal in boxes[box]:
            focal = int(focal)
            if box_label == label:
                boxes[box].remove((box_label, focal))

    else:
        label, focal = step.split("=")
        focal = int(focal)
        box = hash(label)

        for i, (box_label, _) in enumerate(boxes[box]):
            if box_label == label:
                boxes[box][i] = (box_label, focal)
                break
        else:
            boxes[box].append((label, focal))

count = 0

for box in range(256):
    for lens, (_, focal) in enumerate(boxes[box]):
        count += (box + 1) * (lens + 1) * focal

print(count)
