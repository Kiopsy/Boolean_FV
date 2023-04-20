import datetime

class SimulationSettings:
    # If the goal is being changed or not
    CHANGING_GOAL = False

    # Define the population individuals 
    N_pop = 5000

    # Define the length of the binary genome in bits 
    B = 104

    # Define the probability of genome crossover
    Pc = 0.5

    # Define the number of generations to evolve the population
    L = 10**5

    # Define the maximum number of gates in the circuit
    # From the paper, circuits were composed of NAND gands
    MAX_GATES = 12

    # expected number of generations until the goal is changed
    G = 20

    # Define the probability of a gene mutation
    Pm = 0.7 / B



    def __repr__(self):
        class_vars = {k: v for k, v in vars(SimulationSettings).items() if not k.startswith("__")}
        return str(class_vars)

# Define the allowed operations
OPERATIONS = {"XOR": lambda x, y: not (x or y), 
              "NAND": lambda x, y: not (x and y),
			  "EQ": lambda x, y: x == y, 
			  "AND": lambda x, y: x and y,
			  "OR": lambda x, y: x or y}

# csv file path
FILE_PATH = f"data/data_{datetime.datetime.now().strftime('%H_%M')}.csv"

# How often for the simulation to save itself
SAVE_FREQUENCY = 1000