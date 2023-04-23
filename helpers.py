import csv
import networkx as nx
import matplotlib.pyplot as plt
import hashlib

def consistent_hash(string):
    num_buckets = 10000
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex, 16)
    return hash_int % num_buckets

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
    inputs = ["x", "y", "z", "w"] # TODO
    nodes = inputs + [f"{GATE}_{i+len(inputs)}" for i in range(len(gates))]
    nodes[output] = TARGET # output is target node
    G.add_nodes_from(nodes)

    # Add edges
    edge_list = []
    for i, (gate, input1_address, input2_address) in enumerate(gates):
        edge_list.append((nodes[input1_address], nodes[i+len(inputs)]))
        edge_list.append((nodes[input2_address], nodes[i+len(inputs)]))
    G.add_edges_from(edge_list)

    # Remove gates that should not exist
    for i, (gate, _, _) in enumerate(gates):
        if gate != "NAND":
            try:
                G.remove_node(f"{GATE}_{i+len(inputs)}")
            except Exception as e:
                print(e)

    # Plot the graph
    nx.draw(G, with_labels=True)
    plt.show()