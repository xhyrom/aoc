from collections import Counter


left = []
right = []

with open("./input.txt") as file:
    for line in file:
        left_number, right_number = map(
            int, filter(lambda i: i, line.strip().split(" "))
        )

        left.append(left_number)
        right.append(right_number)

counter = Counter(right)
similarity = 0

for num in left:
    similarity += num * counter.get(num, 0)

print(similarity)
