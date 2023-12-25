import networkx as nx

file = open("./input.txt").read().splitlines()

graph = nx.Graph()

for line in file:
    name, connections = line.split(":")
    name = name.strip()

    for connection in connections.strip().split(" "):
        graph.add_edge(name, connection)

graph.remove_edges_from(nx.minimum_edge_cut(graph))

first, second = nx.connected_components(graph)

print(len(first) * len(second))
