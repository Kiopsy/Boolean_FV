import datetime
from helpers import consistent_hash

# Define possible boolean goal functions to run the simulation on
GOALS = {
 "G1" : "((x XOR y) OR (z XOR w); (x XOR y) AND (t XOR u); (z XOR w) AND (t XOR u))",
 "G2" : "((x XOR y) AND (z XOR w); (x XOR y) OR (t XOR u); (z XOR w) AND (t XOR u))",
 "G3" : "((x XOR y) AND (z XOR w); (x XOR y) AND (t XOR u); (z XOR w) OR (t XOR u))",
 "G4" : "((x XOR y) AND (z XOR w); (x XOR y) AND (t XOR u); (z XOR w) AND (t XOR u))",
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
NUM_INPUTS = 6

NUM_OUTPUTS = 3

# The length of a gate address in binary
GATE_ADDR_SZ = 5

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
    B = (GATE_TYPE_SZ + 2 * GATE_ADDR_SZ) * MAX_GATES + GATE_ADDR_SZ * NUM_OUTPUTS

    # Define the probability of genome crossover
    Pc = 0.5

    # Define the number of generations to evolve the population
    L = 10**5

    # expected number of generations until the goal is changed
    G = 5

    # Define the probability of a gene mutation
    Pm = 0.7 / B

    t = 30

    # Define the number of inputs to the goal function & circuit
    NUM_INPUTS = NUM_INPUTS # TODO: fix this

    # goals
    INIT_GOAL = GOALS["G2"]
    GOALS = [GOALS["G1"], GOALS["G2"], GOALS["G3"]]

    def __repr__(self):
        class_vars = {k: v for k, v in vars(SimulationSettings).items() if not k.startswith("__")}
        return str(class_vars)
    