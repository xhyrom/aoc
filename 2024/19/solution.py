from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end = True

    def search(self, word: str, start: int = 0) -> list[int]:
        result = []
        node = self.root

        for i in range(start, len(word)):
            char = word[i]
            if char not in node.children:
                break

            node = node.children[char]
            if node.is_end:
                result.append(i + 1)

        return result


def get_patterns_and_designs() -> tuple[Trie, list[str]]:
    patterns, designs = open("input.txt").read().split("\n\n")
    patterns = set(patterns.strip().split(", "))
    designs = designs.strip().split("\n")

    trie = Trie()
    for pattern in patterns:
        trie.insert(pattern)

    return trie, designs


def can_make(trie: Trie, design: str, memo: dict[int, bool], start: int = 0) -> bool:
    if start in memo:
        return memo[start]

    if start == len(design):
        return True

    matching_prefixes = trie.search(design, start)
    result = any(can_make(trie, design, memo, prefix) for prefix in matching_prefixes)

    memo[start] = result
    return result


def count_ways(trie: Trie, design: str, memo: dict[int, int], start: int = 0) -> int:
    if start in memo:
        return memo[start]

    if start == len(design):
        return 1

    matching_prefixes = trie.search(design, start)
    result = sum(count_ways(trie, design, memo, prefix) for prefix in matching_prefixes)

    memo[start] = result
    return result


def part_1() -> int:
    trie, designs = get_patterns_and_designs()

    return sum(can_make(trie, design, {}) for design in designs)


def part_2() -> int:
    trie, designs = get_patterns_and_designs()

    return sum(count_ways(trie, design, {}) for design in designs)
