import csv
import networkx as nx
import matplotlib.pyplot as plt


def add_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def create_graph(gates, output):
    TARGET = "O"
    GATE = "NAND"

     # Create a graph
    G = nx.DiGraph()

    # Add nodes
    inputs = ["x", "y", "z", "w"]
    nodes = inputs + [f"{GATE}_{i+len(inputs)}" for i in range(len(gates))] + [14, 15]
    nodes[output] = TARGET # output is target node
    G.add_nodes_from(nodes)

    # Add edges
    edge_list = []
    for i, (gate, input1_address, input2_address) in enumerate(gates):
        edge_list.append((nodes[input1_address], nodes[i+len(inputs)]))
        edge_list.append((nodes[input2_address], nodes[i+len(inputs)]))
    G.add_edges_from(edge_list)

    # Remove gates that should not exist
    for i, gate in enumerate(gates):
        if gate != "NAND":
            G.remove_node(f"{GATE}_{i+len(inputs)}")
    
    # Find the set of nodes connected to the target node
    connected_nodes = set(nx.node_connected_component(G, TARGET))

    # Extract the subgraph containing only the connected nodes
    subgraph = G.subgraph(connected_nodes)

    # Remove all nodes in the original graph that are not in the subgraph
    G.remove_nodes_from(set(G.nodes()) - set(subgraph.nodes()))

    # Plot the graph
    nx.draw(G, with_labels=True, node_color=['blue' if n != TARGET else 'red' for n in G.nodes()])
    plt.show()