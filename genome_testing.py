from circuit import Circuit
from goal import Goal
from recorder import create_graph

def print_table(table):
    for i, (k, v) in enumerate(table.items()):
        print(f"{k}: {v}   ", end = "" if (i+1) % len(k) else "\n")

def main():
    GENOME = input("Genome: ").strip()
    GOAL = input("F/G/H: ").strip().capitalize()

    c = Circuit(GENOME)

    print()
    input("CIRCUIT TRUTH TABLE: [enter]")
    print_table(c.get_truth_table())
    print("\n")

    if GOAL:
        f, g, h = GOAL.split("/")
        goal = Goal(g, f, h)
        input(f"GOAL [{goal}] TRUTH TABLE: [enter]")
        print_table(goal.truth_table)
        print("\n")

    input("CIRCUIT GRAPH: [enter]")
    create_graph(c.gates, c.output_gene)

if __name__ == "__main__":
    create_graph([], 0)
    #main()