from itertools import combinations


def bron_kerbosch(
    R: set[str],
    P: set[str],
    X: set[str],
    graph: dict[str, set[str]],
    cliques: list[set[str]],
):
    """
    Uses the Bron-Kerbosch algorithm to find all maximal cliques in a graph.

    Args:
        R: A set of vertices in the current clique.
        P: A set of vertices that can be added to the current clique.
        X: A set of vertices that cannot be added to the current clique.
        graph: A dictionary of vertices and their neighbors.
        cliques: A list to store

    Reference: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    """

    if not P and not X:
        cliques.append(R)
        return

    u = next(iter(P | X))
    for v in P - graph[u]:
        bron_kerbosch(R | {v}, P & graph[v], X & graph[v], graph, cliques)
        P.remove(v)
        X.add(v)


def part_1() -> int:
    connections = {}
    for line in open("input.txt").read().splitlines():
        a, b = line.split("-")
        connections[a] = connections.get(a, set()) | {b}
        connections[b] = connections.get(b, set()) | {a}

    cliques = []
    bron_kerbosch(set(), set(connections.keys()), set(), connections, cliques)

    # fixes order of vertices in cliques, python sets are unordered
    cliques = [sorted(clique) for clique in cliques]

    candidates = set()
    for clique in cliques:
        if len(clique) >= 3:
            for comb in combinations(clique, 3):
                if any(vertex.startswith("t") for vertex in comb):
                    candidates.add(tuple(comb))

    return len(candidates)


def part_2() -> str:
    connections = {}
    for line in open("input.txt").read().splitlines():
        a, b = line.split("-")
        connections[a] = connections.get(a, set()) | {b}
        connections[b] = connections.get(b, set()) | {a}

    cliques = []
    bron_kerbosch(set(), set(connections.keys()), set(), connections, cliques)
    largest_clique = max(cliques, key=len)

    return ",".join(sorted(largest_clique))
