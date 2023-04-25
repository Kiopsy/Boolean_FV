import datetime
from helpers import consistent_hash

# Define possible boolean goal functions to run the simulation on
GOALS = {
    # 4-input goals
    "G1" : "(w XOR x) OR (y XOR z)",
    "G2" : "(w EQ x) OR (y XOR z)",
    "G3" : "(w XOR x) OR (y EQ z)",
    "G4" : "(w XOR x) AND (y XOR z)",
    # 6-input goals
    "G5" : "(u XOR v) OR (w XOR x) OR (y XOR z)",
    "G6" : "(u EQ v) OR (w XOR x) OR (y XOR z)",
    "G7" : "(u XOR v) OR (w XOR x) OR (y EQ z)"
}

# Define the allowed operations
OPERATIONS = {"XOR": lambda x, y: (x ^ y), 
              "NAND": lambda x, y: not (x and y),
			  "EQ": lambda x, y: x == y, 
			  "AND": lambda x, y: x and y,
			  "OR": lambda x, y: x or y}

# How often for the simulation to save itself
SAVE_FREQUENCY = 1000

# The number of inputs a circuit will take
NUM_INPUTS = 4

# The length of a gate address in binary
GATE_ADDR_SZ = 4

# The length of a gate type in binary
GATE_TYPE_SZ = 2

class SimulationSettings:
    # If the goal is being changed or not
    CHANGING_GOAL = True

    # Define the maximum number of gates in the circuit
    # From the paper, circuits were composed of NAND gands
    MAX_GATES = 12

    # Define the population individuals 
    N_pop = 5000

    # Define the length of the binary genome in bits 
    B = (GATE_TYPE_SZ + 2 * GATE_ADDR_SZ) * MAX_GATES + GATE_ADDR_SZ
    print("B", B)

    # Define the probability of genome crossover
    Pc = 0.5

    # Define the number of generations to evolve the population
    L = 10**5

    # expected number of generations until the goal is changed
    G = 20

    # Define the probability of a gene mutation
    Pm = 0.7 / B

    t = 30

    # Define the number of inputs to the goal function & circuit
    NUM_INPUTS = NUM_INPUTS # TODO: fix this

    # goals
    INIT_GOAL = GOALS["G1"]
    GOALS = [GOALS["G1"], GOALS["G2"], GOALS["G3"]]

    def __repr__(self):
        class_vars = {k: v for k, v in vars(SimulationSettings).items() if not k.startswith("__")}
        return str(class_vars)
    