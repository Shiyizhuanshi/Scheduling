# pip3 install networkx matplotlib
import networkx as nx
import matplotlib.pyplot as plt

# Define the directed edges
edges = [
    (0, 30), (1, 0), (2, 7), (3, 2), (4, 1), (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
    (10, 0), (11, 4), (12, 11), (13, 12), (16, 14), (14, 10), (15, 4), (16, 15),
    (17, 16), (19, 18), (20, 19), (21, 18), (22, 21), (23, 22), (24, 5), (25, 24),
    (26, 25), (27, 26), (28, 26), (29, 27), (29, 28), (30, 4), (30, 10), (30, 14),
    (30, 20), (30, 23), (30, 29), (18, 17), (19, 18), (20, 17), (21, 20), (22, 21),
    (23, 4), (24, 23), (25, 24), (26, 25), (27, 25), (28, 26), (28, 27), (29, 3),
    (29, 9), (29, 13), (29, 19), (29, 22), (29, 28)
]

# Create a directed graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Plot the DAG
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # Position the nodes

# Draw nodes and edges
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=edges, arrowstyle='->', arrowsize=15)

# Display the plot
plt.title("Directed Acyclic Graph (DAG)")
plt.show()
