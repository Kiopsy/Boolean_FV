from circuit import Circuit
from goal import Goal
from helpers import create_graph
from constants import NUM_INPUTS


def print_table(table, table2 = None):
    for i, (k, v) in enumerate(table.items()):
        print(f"{k}: {v}{'*' if table2 and table2[k] != v else ''}   ", end = "" if (i+1) % len(k) else "\n")

def main():
    
    GENOME = input("Genome: ").strip()

    try:
        c = Circuit(GENOME)
    except Exception as e:
        print(e)
        exit(1)

    print(c.find_from_output())

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