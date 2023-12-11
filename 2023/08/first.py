import re

file = open("./input.txt").readlines()

instructions = list(file[0].strip())
nodes = {
    x[1]: (x[2], x[3])
    for x in (re.match(r"(\w+)\s*=\s*\((\w+), (\w+)\)", line) for line in file[2:])
}

next_node = "AAA"
required_node = "ZZZ"

i = 0
steps = 0

while next_node != required_node:
    if i >= len(instructions):
        i = 0

    instruction = instructions[i]
    cur_node = nodes[next_node]
    next_node = cur_node[instruction == "R"]

    steps += 1
    i += 1

print(steps)
