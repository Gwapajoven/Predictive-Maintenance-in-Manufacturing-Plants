import matplotlib.pyplot as plt
import networkx as nx

# Create a simple weighted graph similar to the uploaded example
simple_graph = nx.Graph()

# Add nodes
simple_nodes = list(range(9))
simple_graph.add_nodes_from(simple_nodes)

# Add weighted edges to form a connected graph
simple_edges = [
    (0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11),
    (2, 3, 7), (2, 5, 4), (2, 8, 2), (3, 4, 9),
    (3, 5, 14), (4, 5, 10), (5, 6, 2), (6, 7, 1), (6, 8, 6), (7, 8, 7)
]
simple_graph.add_weighted_edges_from(simple_edges)

# Run Prim's algorithm to find the Minimum Spanning Tree (MST)
mst_edges = list(nx.minimum_spanning_edges(simple_graph, algorithm='prim', data=True))
mst_edges_list = [(u, v) for u, v, d in mst_edges]  # Convert to a simpler format

# Define layout for the graph
pos = nx.spring_layout(simple_graph, seed=42)  # Layout for a visually pleasing arrangement

# Draw the complete graph in light gray
plt.figure(figsize=(8, 6))
nx.draw(simple_graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=15, font_weight='bold', edge_color='lightgray', width=2)

# Highlight the MST edges in red
nx.draw_networkx_edges(simple_graph, pos, edgelist=mst_edges_list, width=4, edge_color='red')

# Draw edge labels for all edges
edge_labels = {(u, v): f"{d['weight']}" for u, v, d in simple_graph.edges(data=True)}
nx.draw_networkx_edge_labels(simple_graph, pos, edge_labels=edge_labels, font_size=12)

# Display the plot
plt.title("Minimum Spanning Tree Visualization (Prim's Algorithm)")
plt.show()
