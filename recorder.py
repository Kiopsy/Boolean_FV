import csv
import networkx as nx
import matplotlib.pyplot as plt
from circuit import Circuit


def create_graph(gates, output):
    # Create a graph
    G = nx.DiGraph()



    # Add nodes
    nodes = ["x", "y", "z", "w"] + [(f"NAND_{i}" if gate else f"X{i}") for i, gate in enumerate(gates)]
    G.add_nodes_from(nodes)

    # Add edges
    edge_list = []
    for i, (gate, input1_address, input2_address) in enumerate(gates):

        edge_list.append((nodes[input1_address], nodes[i+4]))
        edge_list.append((nodes[input2_address], nodes[i+4]))

    G.add_edges_from(edge_list)

    # Plot the graph
    nx.draw(G, with_labels=True, node_color=['blue' if n != 3 else 'red' for n in G.nodes()])
    plt.show()