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


rules: dict[str, list[Condition]] = {}
for rule in file_rules.splitlines():
    name = rule.split("{")[0]
    conditions = rule.split("{")[1].split("}")[0].split(",")

    rules[name] = []

    for condition in conditions:
        cmatch = condition_regex.match(condition)
        rules[name].append(Condition(cmatch.groupdict() if cmatch else condition))


def count(
    current,
    ranges={"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)},
):
    if current == "R":
        return 0

    if current == "A":
        product = 1
        for lo, hi in ranges.values():
            product *= hi - lo + 1
        return product

    total = 0

    rule = rules[current]

    for condition in rule:
        if condition.simple:
            total += count(condition.next, ranges)
        else:
            new_range = dict(ranges)

            cur_range = ranges[condition.left_side]

            if cur_range[0] < condition.right_side < cur_range[1]:
                if condition.operator == "<":
                    new_range[condition.left_side] = (
                        cur_range[0],
                        condition.right_side - 1,
                    )
                    ranges[condition.left_side] = (condition.right_side, cur_range[1])
                else:
                    new_range[condition.left_side] = (
                        condition.right_side + 1,
                        cur_range[1],
                    )
                    ranges[condition.left_side] = (cur_range[0], condition.right_side)

                total += count(condition.next, new_range)

    return total


print(count("in"))
