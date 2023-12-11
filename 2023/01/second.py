import re

lines = []

with open("./input.txt") as file:
    for file_line in file:
        lines.append(file_line.strip())

count = 0

for line in lines:
    line = (
        line.replace("one", "o1e")
        .replace("two", "t2o")
        .replace("three", "t3e")
        .replace("four", "f4r")
        .replace("five", "f5e")
        .replace("six", "s6x")
        .replace("seven", "s7n")
        .replace("eight", "e8t")
        .replace("nine", "n9e")
    )
    numbers = re.findall(rf"\d", line)
    first_number = int(numbers[0])
    last_number = int(numbers[-1])

    count += first_number * 10 + last_number

print(count)
