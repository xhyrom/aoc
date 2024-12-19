from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AhoCorasickNode:
    children: dict[str, "AhoCorasickNode"] = field(default_factory=dict)
    fail: Optional["AhoCorasickNode"] = None
    output: list[int] = field(default_factory=list)


class AhoCorasick:
    def __init__(self):
        self.root = AhoCorasickNode()

    def insert(self, pattern: str) -> None:
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]

        node.output.append(len(pattern))

    def build_failure_links(self) -> None:
        queue = deque()
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                queue.append(child)

                failure = current.fail
                while failure and char not in failure.children:
                    failure = failure.fail

                child.fail = (
                    failure.children.get(char, self.root) if failure else self.root
                )
                child.output += child.fail.output

    def find_all_matches(self, text: str) -> list[tuple[int, int]]:
        matches = []
        node = self.root

        for i, char in enumerate(text):
            while node and char not in node.children:
                node = node.fail

            if not node:
                node = self.root
                continue

            node = node.children.get(char, self.root)
            if node.output:
                for length in node.output:
                    matches.append((i - length + 1, i + 1))

        return matches


def get_patterns_and_designs() -> tuple[AhoCorasick, list[str]]:
    patterns, designs = open("input.txt").read().split("\n\n")
    patterns = set(patterns.strip().split(", "))
    designs = designs.strip().split("\n")

    automaton = AhoCorasick()
    for pattern in patterns:
        automaton.insert(pattern)

    automaton.build_failure_links()

    return automaton, designs


def can_make(automaton: AhoCorasick, design: str) -> bool:
    n = len(design)
    dp = [False] * (n + 1)
    dp[0] = True

    matches = automaton.find_all_matches(design)
    for start, end in matches:
        if dp[start]:
            dp[end] = True

    return dp[n]


def count_ways(automaton: AhoCorasick, design: str) -> int:
    n = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1

    matches = automaton.find_all_matches(design)
    for start, end in matches:
        if dp[start] > 0:
            dp[end] += dp[start]

    return dp[n]


def part_1() -> int:
    automaton, designs = get_patterns_and_designs()

    return sum(can_make(automaton, design) for design in designs)


def part_2() -> int:
    automaton, designs = get_patterns_and_designs()

    return sum(count_ways(automaton, design) for design in designs)
