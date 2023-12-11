import re

lines = []

with open("./input.txt") as file:
    for file_line in file:
        lines.append(file_line.strip())

count = 0

for line in lines:
    numbers = re.findall(r"\d", line)
    first_number = int(numbers[0])
    last_number = int(numbers[-1])

    count += first_number * 10 + last_number

# Part 1
print(count)
