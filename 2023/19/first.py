import re

file_rules, file_parts = open("./input.txt").read().split("\n\n")

condition_regex = re.compile(
    r"(?P<leftside>\w+)(?P<operator>>|<)(?P<rightside>\w+):(?P<next>\w+)"
)


class Condition:
    def __init__(self, condition):
        if "leftside" not in condition:
            self.simple = True
            self.next = condition
        else:
            self.simple = False
            self.left_side = condition["leftside"]
            self.operator = condition["operator"]
            self.right_side = int(condition["rightside"])
            self.next = condition["next"]

    def evaluate(self, values: dict[str, int]):
        if self.simple:
            return True

        value = values[self.left_side]

        match self.operator:
            case ">":
                return value > self.right_side
            case "<":
                return value < self.right_side


rules: dict[str, list[Condition]] = {}
for rule in file_rules.splitlines():
    name = rule.split("{")[0]
    conditions = rule.split("{")[1].split("}")[0].split(",")

    rules[name] = []

    for condition in conditions:
        cmatch = condition_regex.match(condition)
        rules[name].append(Condition(cmatch.groupdict() if cmatch else condition))

parts: list[dict[str, int]] = []
for part in file_parts.splitlines():
    part = part[1:-1]
    variables = part.split(",")

    parts.append({})

    for variable in variables:
        name, value = variable.split("=")
        value = int(value)

        parts[-1][name] = value

count = 0

for part in parts:
    current = "in"

    while current not in "AR":
        rule = rules[current]
        for condition in rule:
            if condition.evaluate(part):
                current = condition.next
                break

    if current == "A":
        count += sum(part.values())

print(count)
