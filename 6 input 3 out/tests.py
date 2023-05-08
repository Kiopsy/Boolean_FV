from circuit import Circuit
import networkx as nx
import matplotlib.pyplot as plt
import itertools


def circuit_to_graph(c : Circuit) -> nx.DiGraph:
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
            print(i, e)
    G.add_edges_from(edge_list)

    # Remove gates that should not exist
    for i, (gate, _, _) in enumerate(gates):
        if gate != "NAND":
            try:
                G.remove_node(f"{GATE}_{i+len(inputs)}")
            except Exception as e:
                print(e)

    return G

def compute_modularity(G, partitions):
    # Compute the number of edges in the graph
    L = G.number_of_edges()

    # # Compute the fraction of edges that connect nodes in the same partition
    # intra_edges = 0
    # for u, v in G.edges():
    #     if partition[u] == partition[v]:
    #         intra_edges += 1
    # q = intra_edges / m

    # # Compute the expected fraction of edges that connect nodes in the same partition
    # expected_q = 0
    # for i in set(partition.values()):
    #     # Compute the fraction of nodes in partition i
    #     nodes_in_i = [u for u in G.nodes() if partition[u] == i]
    #     frac_nodes_in_i = len(nodes_in_i) / G.number_of_nodes()

    #     # Compute the fraction of edges that connect nodes in partition i
    #     edges_in_i = G.subgraph(nodes_in_i).number_of_edges()
    #     frac_edges_in_i = edges_in_i / m

    #     expected_q += frac_edges_in_i**2 - (frac_nodes_in_i**2)

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

if __name__ == '__main__':
    # GENOME = "000110101100000010100100001110000010001000101010000111101000000111000000000011100100000011100101000000000001001110000011010001101100000101111111011011111101001011111001001110111001101111111111001110111101000101000110001110001010000101011000010000101110001100001101000001100010001000100110001100101001000000101110100111011011110"
    GENOME = "001111100001000000011111000011100110001100111100111101110001001000110001100001000000011000100111000001000011001111011100010101000010000010011111001000000001101010100101011010011100010100110001101111000110111010011010011110010000001001001111001100101101111101000101100001000110100001111110111110110111000010100100010110100001110"
    try:
        c = Circuit(GENOME)
    except Exception as e:
        print(e)
        exit(1)

    create_graph(c.gates, c.output_genes)

    G = circuit_to_graph(c)

    # k = 4
    # comp = girvan_newman(G)
    # limited = itertools.takewhile(lambda c: len(c) <= k, comp)
    # best_partition = max(limited, key=lambda p: compute_modularity(G, p))
    # partition = {node_label: community_label for node_label, community_label in best_partition.items()}
    # res = tuple(sorted(tuple(sorted(c)) for c in best_partition))

    # (x ^ y) & (z ^ w); (x ^ y) & (t ^ u); (z ^ w) & (t ^ u)

    k = 6
    comp = girvan_newman(G)
    limited = itertools.takewhile(lambda c: len(c) <= k, comp)
    # print(len(list(limited)))

    partitions = ()
    for communities in limited:
        partitions = tuple(sorted(c) for c in communities)

    print(partitions)

    q = compute_modularity(G, partitions)
    print(q)