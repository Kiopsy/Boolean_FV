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

def create_graph(gates, output, n = 4):
    
    TARGET = "*"
    GATE = "NAND"

    def style_nodes(nodes):
        node_color = []
        node_shape = []

        for n in nodes:
            if GATE in n:
               node_color.append("#bfbfbf")
               node_shape.append("v")
            elif TARGET in n:
               node_color.append("r")
               node_shape.append("d")
            else:
                node_color.append("orange")
                node_shape.append("o")
        
        return node_color, node_shape

    # Create a graph
    G = nx.DiGraph()

    # Add nodes
    inputs = [chr(i) for i in range(ord('z') - n + 1, ord('z') + 1)] # TODO
    nodes = inputs + [f"{GATE}_{i+len(inputs)}" for i in range(len(gates))]
    nodes[output] = TARGET # output is target node
    G.add_nodes_from(nodes)

    # Add edges
    edge_list = []
    for i, (_, input1_address, input2_address) in enumerate(gates):
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
    nodes = list(G.nodes())
    

    # Draw the graph with the style options
    for _ in range(2):
        pos = nx.spring_layout(G)
        for node in inputs:
            pos[node] = (pos[node][0], 1)
        pos[TARGET] = (pos[TARGET][0], -1)

    
    node_color, node_shape = style_nodes(nodes)

    nx.draw_networkx_nodes(G, pos, node_color=node_color)#, node_shape=node_shape)
    nx.draw_networkx_edges(G, pos)#, edge_color=edge_color)
    nx.draw_networkx_labels(G, pos)
    plt.axis('off')
    plt.show()