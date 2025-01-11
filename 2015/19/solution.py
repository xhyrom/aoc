from typing import Generator


def replacements_molecule(file_name: str) -> tuple[list[tuple[str, str]], str]:
    replacements, molecule = open(file_name).read().split("\n\n")
    replacements = [
        (a, b)
        for a, b in (
            replacement.split(" => ") for replacement in replacements.splitlines()
        )
    ]

    return replacements, molecule.strip()


def find_all_positions(text: str, pattern: str) -> Generator[int, None, None]:
    pos = 0

    while True:
        pos = text.find(pattern, pos)
        if pos == -1:
            break

        yield pos
        pos += 1


def part_1() -> int:
    replacements, molecule = replacements_molecule("input.txt")

    molecules = set()
    for pattern, replacement in replacements:
        for pos in find_all_positions(molecule, pattern):
            new_molecule = molecule[:pos] + replacement + molecule[pos + len(pattern) :]
            molecules.add(new_molecule)

    return len(molecules)


def part_2() -> int:
    replacements, molecule = replacements_molecule("input.txt")
    replacements = [(to, fro) for fro, to in replacements]

    current = molecule
    steps = 0

    while any(char != "e" for char in current):
        for pattern, replacement in replacements:
            if pattern not in current:
                continue

            current = current.replace(pattern, replacement, 1)
            steps += 1
            break

    return steps
