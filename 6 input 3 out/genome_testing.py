from circuit import Circuit
from goal import Goal
from helpers import create_graph
from constants import NUM_INPUTS


def print_table(table, table2 = None):
    for i, (k, v) in enumerate(table.items()):
        print(f"{k}: {v}{'*' if table2 and table2[k] != v else ''}   ", end = "" if (i+1) % len(k) else "\n")

def main():
    
    GENOME = "100100010111001010111110001100011000101011111010101000001111110010001010010101010101010101110011011111100100011010001011000110011000011000010000100100110000000010100101001001100110001011011111101111101011001101001000000011010001010110001111100101101101010010010000010110010001010111000100001001101001100100010011001000010010011" #input("Genome: ").strip()

    try:
        c = Circuit(GENOME)
    except Exception as e:
        print(e)
        exit(1)

    GOAL_STR = "(x XOR y) OR (z XOR w); (x XOR y) AND (t XOR u); (z XOR w) AND (t XOR u)"# input("Goal (optional): ").strip()

    GOAL_TRUTH_TABLE = Goal(GOAL_STR).truth_table if GOAL_STR else None

    print("Goal truth table")
    print_table(GOAL_TRUTH_TABLE)

    print()
    input("CIRCUIT TRUTH TABLE: [enter]")
    print_table(c.get_truth_table(), GOAL_TRUTH_TABLE)
    print("\n")
    
    input("CIRCUIT GATES: [enter]")
    N = NUM_INPUTS
    print({i: v for i,v in enumerate([chr(i) for i in range(ord('z') - N + 1, ord('z') + 1)] + c.gates)})
    print(c.output_genes)
    print("\n")
    
    input("CIRCUIT GRAPH: [enter]")
    create_graph(c.gates, c.output_genes, N)
    
if __name__ == "__main__":
    main()