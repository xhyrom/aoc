from collections import defaultdict, deque
from typing import Any


def input():
    with open("input.txt") as f1:
        content = f1.read()
        splitted = content.split("\n\n")

        rules = {}
        for rule in splitted[0].split("\n"):
            before, after = map(int, rule.split("|"))
            if before not in rules:
                rules[before] = set()

            rules[before].add(after)

        updates = []
        for update in splitted[1].split("\n"):
            if update:
                updates.append([int(x) for x in update.split(',')])

        return rules, updates

def is_valid_order(pages, rules):
    page_positions = {page: i for i, page in enumerate(pages)}

    for before in rules:
        if before in page_positions:
            for after in rules[before]:
                if after in page_positions:
                    if page_positions[before] > page_positions[after]:
                        return False
    return True

def part_1() -> Any:
    rules, updates = input()
    result = 0

    for update in updates:
        if is_valid_order(update, rules):
            middle_idx = len(update) // 2
            result += update[middle_idx]

    return result

def topological_sort(pages, rules):
    """
    Topological sort using Kahn's algorithm

    wiki: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """

    adj = defaultdict(set)
    in_degree = {page: 0 for page in pages}

    for before in rules:
        if before in pages:
            for after in rules[before]:
                if after in pages:
                    adj[before].add(after)
                    in_degree[after] += 1

    queue = deque([page for page in pages if in_degree[page] == 0])
    result = []

    while queue:
        page = queue.popleft()
        result.append(page)

        for neighbor in adj[page]:
            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(pages) else None

def part_2() -> Any:
    rules, updates = input()
    result = 0

    for update in updates:
        if not is_valid_order(update, rules):
            pages = topological_sort(set(update), rules)

            if pages:
                middle_idx = len(pages) // 2
                result += pages[middle_idx]

    return result
