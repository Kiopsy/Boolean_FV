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

    GOAL_STR = input("Goal (optional): ").strip()

    GOAL_TRUTH_TABLE = Goal(GOAL_STR).truth_table if GOAL_STR else None

    print()
    input("CIRCUIT TRUTH TABLE: [enter]")
    print_table(c.get_truth_table(), GOAL_TRUTH_TABLE)
    print("\n")
    
    input("CIRCUIT GATES: [enter]")
    N = NUM_INPUTS
    print({i: v for i,v in enumerate([chr(i) for i in range(ord('z') - N + 1, ord('z') + 1)] + c.gates)})
    print("\n")
    
    input("CIRCUIT GRAPH: [enter]")
    while True:
        create_graph(c.gates, c.output_gene, N)

        repeat = input("New graph? ").strip().lower()
        if "n" in repeat or "q" in repeat:
            break

if __name__ == "__main__":
    main()

"""
def print_table(table):
    for i, (k, v) in enumerate(table.items()):
        print(f"{k}: {v}   ", end = "" if (i+1) % len(k) else "\n")

def main():
    GENOME = input("Genome: ").strip()
    GOAL = input("Goal G/F/H (optional): ").strip().upper()

    c = Circuit(GENOME)

    print()
    input("CIRCUIT TRUTH TABLE: [enter]")
    print_table(c.get_truth_table())
    print("\n")

    if GOAL:
        goal = Goal(GOAL.split("/"))
        input(f"GOAL [{goal}] TRUTH TABLE: [enter]")
        print_table(goal.truth_table)
        print("\n")
    
    input("CIRCUIT GATES: [enter]")
    print({i: v for i,v in enumerate(["x", "y", "z", "w"] + c.gates)})
    print("\n")
    
    input("CIRCUIT GRAPH: [enter]")
    while True:
        create_graph(c.gates, c.output_gene)

        repeat = input("New graph? ").strip().lower()
        if "n" in repeat or "q" in repeat:
            break
"""