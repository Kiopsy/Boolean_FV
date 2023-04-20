from circuit import Circuit
from goal import Goal
from helpers import create_graph

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
        g, f, h = GOAL.split("/")
        goal = Goal(g, f, h)
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



if __name__ == "__main__":
    # create_graph([], 0)
    main()