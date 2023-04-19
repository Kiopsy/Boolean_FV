from circuit import Circuit
from goal import Goal
from recorder import create_graph

def main():
    GENOME = input("Genome: ").strip()
    GOAL = input("F/G/H: ").strip()

    goal = None

    if GOAL:
        f, g, h = GOAL.split("/")
        goal = Goal(g, f, h)

    c = Circuit(GENOME)

    print("CIRCUIT TRUTH TABLE:")
    print(c.get_truth_table())
    print("\n\n")

    print(f"GOAL [{goal}] TRUTH TABLE:")
    print(goal.truth_table)
    print("\n\n")

    input("CIRCUIT GRAPH: [enter]")
    create_graph(c.gates, c.output_gene)

if __name__ == "__main__":
    main()