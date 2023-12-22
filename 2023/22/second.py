from collections import defaultdict, deque

file = open("./input.txt").read().splitlines()

bricks = []
for line in file:
    line = line.replace("~", ",").split(",")

    bricks.append([int(item) for item in line])

bricks.sort(key=lambda brick: brick[2])


def intersects(a, b):
    start_a, start_b = a[0], b[0]
    end_a, end_b = a[3], b[3]

    start_a_z, start_b_z = a[1], b[1]
    end_a_z, end_b_z = a[4], b[4]

    return max(start_a, start_b) <= min(end_a, end_b) and max(
        start_a_z, start_b_z
    ) <= min(end_a_z, end_b_z)


for i, brick in enumerate(bricks):
    max_z = 1
    for previous_brick in bricks[:i]:
        if intersects(brick, previous_brick):
            max_z = max(max_z, previous_brick[5] + 1)

    brick[5] -= brick[2] - max_z
    brick[2] = max_z

a_supports_b = defaultdict(set)
b_supports_a = defaultdict(set)

for upper_index, upper in enumerate(bricks):
    for lower_index, lower in enumerate(bricks[:upper_index]):
        if intersects(lower, upper) and upper[2] == lower[5] + 1:
            a_supports_b[lower_index].add(upper_index)
            b_supports_a[upper_index].add(lower_index)

count = 0

for i in range(len(bricks)):
    queue = deque(
        item_index
        for item_index in a_supports_b[i]
        if len(b_supports_a[item_index]) == 1
    )
    visited = set(queue)

    while queue:
        j = queue.popleft()

        for k in a_supports_b[j] - visited:
            if b_supports_a[k] <= visited:
                queue.append(k)
                visited.add(k)

    count += len(visited)

print(count)
