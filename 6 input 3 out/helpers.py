import csv
import networkx as nx
import matplotlib.pyplot as plt
import hashlib
import itertools

def consistent_hash(string):
    num_buckets = 10**6
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex, 16)
    return hash_int % num_buckets

def add_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def create_graph(gates, outputs, N = 6):
    
    TARGET = "*"
    GATE = "n"

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
    inputs = [chr(i) for i in range(ord('z') - N + 1, ord('z') + 1)] # TODO 
    nodes = inputs + [f"{GATE}_{i+len(inputs)}" for i in range(len(gates))]
    for i, output in enumerate(outputs):
        nodes[output] = f"{TARGET}_{i}" # output is target node
    G.add_nodes_from(nodes)

    # Add edges
    edge_list = []
    for i, (gate, input1_address, input2_address) in enumerate(gates):
        try:
            edge_list.append((nodes[input1_address], nodes[i+len(inputs)]))
            edge_list.append((nodes[input2_address], nodes[i+len(inputs)]))
        except Exception as e:
            print(i, e)
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
    pos = None
    for _ in range(2):
        pos = nx.spring_layout(G, pos = pos)
        for node in inputs:
            try:
                pos[node] = (pos[node][0], 1)
            except Exception as e:
                print(f"No input {node}; {node} is an output: {e}")

        for i in range(len(outputs)):
            try:
                pos[f"{TARGET}_{i}"] = (pos[f"{TARGET}_{i}"][0], -1)
            except Exception as e:
                print(f"Output at index {i} overwrites a previous output")


    
    node_color, node_shape = style_nodes(nodes)

    nx.draw_networkx_nodes(G, pos, node_color=node_color)#, node_shape=node_shape)
    nx.draw_networkx_edges(G, pos)#, edge_color=edge_color)
    nx.draw_networkx_labels(G, pos)
    plt.axis('off')
    plt.show()

def circuit_to_graph(c) -> nx.DiGraph:
    gates = c.gates
    outputs = c.output_genes

    N = 6
    TARGET = "*"
    GATE = "n"

    # Create a graph
    G = nx.DiGraph()

    # Add nodes
    inputs = [chr(i) for i in range(ord('z') - N + 1, ord('z') + 1)] # TODO 
    nodes = inputs + [f"{GATE}_{i+len(inputs)}" for i in range(len(gates))]
    for i, output in enumerate(outputs):
        nodes[output] = f"{TARGET}_{i}" # output is target node
    G.add_nodes_from(nodes)

    # Add edges
    edge_list = []
    for i, (gate, input1_address, input2_address) in enumerate(gates):
        try:
            edge_list.append((nodes[input1_address], nodes[i+len(inputs)]))
            edge_list.append((nodes[input2_address], nodes[i+len(inputs)]))
        except Exception as e:
            pass
    G.add_edges_from(edge_list)

    # Remove gates that should not exist
    for i, (gate, _, _) in enumerate(gates):
        if gate != "NAND":
            try:
                G.remove_node(f"{GATE}_{i+len(inputs)}")
            except Exception as e:
                pass

    return G

def compute_q(c):
    try:
        G = circuit_to_graph(c)
        k = 6
        comp = girvan_newman(G)
        limited = itertools.takewhile(lambda c: len(c) <= k, comp)
        partitions = ()
        for communities in limited:
            partitions = tuple(sorted(c) for c in communities)
        q = compute_modularity(G, partitions)
        return q
    except:
        return 0

def compute_modularity(G, partitions):
    # Compute the number of edges in the graph
    L = G.number_of_edges()

    # Compute the modularity as the difference between the actual and expected fraction of intra-module edges
    q = 0
    for i in range(len(partitions)):
        # extract subgraph
        sub_G = G.subgraph(partitions[i])

        # count number of edges in subgraph
        ls = sub_G.number_of_edges()

        degrees = dict(G.degree())

        # sum the degrees of the nodes in the list
        ds = sum(degrees[node] for node in partitions[i])

        sub_quantity = ls/L - (ds/(2*L)) ** 2

        q += sub_quantity

    return q
def girvan_newman(G, most_valuable_edge=None):
    """Finds communities in a graph using the Girvan–Newman method."""
    # If the graph is already empty, simply return its connected
    # components.
    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return
    # If no function is provided for computing the most valuable edge,
    # use the edge betweenness centrality.
    if most_valuable_edge is None:

        def most_valuable_edge(G):
            """Returns the edge with the highest betweenness centrality
            in the graph `G`.

            """
            # We have guaranteed that the graph is non-empty, so this
            # dictionary will never be empty.
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)

    # The copy of G here must include the edge weight data.
    g = G.copy().to_undirected()
    # Self-loops must be removed because their removal has no effect on
    # the connected components of the graph.
    g.remove_edges_from(nx.selfloop_edges(g))
    while g.number_of_edges() > 0:
        yield _without_most_central_edges(g, most_valuable_edge)

def _without_most_central_edges(G, most_valuable_edge):
    """Returns the connected components of the graph that results from
    repeatedly removing the most "valuable" edge in the graph.

    `G` must be a non-empty graph. This function modifies the graph `G`
    in-place; that is, it removes edges on the graph `G`.

    `most_valuable_edge` is a function that takes the graph `G` as input
    (or a subgraph with one or more edges of `G` removed) and returns an
    edge. That edge will be removed and this process will be repeated
    until the number of connected components in the graph increases.

    """
    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    while num_new_components <= original_num_components:
        edge = most_valuable_edge(G)
        G.remove_edge(*edge)
        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
    return new_components