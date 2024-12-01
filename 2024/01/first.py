left = []
right = []

with open("./input.txt") as file:
    for line in file:
        left_number, right_number = map(
            int, filter(lambda i: i, line.strip().split(" "))
        )
        left.append(left_number)
        right.append(right_number)

left.sort()
right.sort()

distance = 0

for i in range(len(left)):
    distance += abs(left[i] - right[i])

print(distance)
