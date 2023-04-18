import random
from itertools import chain, product
from collections import deque

# Define the allowed operations
operations = {"XOR": lambda x, y: not (x or y), 
              "NAND": lambda x, y: not (x and y),
			  "EQ": lambda x, y: x == y, 
			  "AND": lambda x, y: x and y,
			  "OR": lambda x, y: x or y}

# Define the population individuals 
pop_size = 5000

# Define the length of the binary genome in bits 
gene_length = 104

# Define the probability of genome crossover
crossover_rate = 0.5

# Define the probability of a gene mutation
mutation_rate = 0.7 / gene_length

# Define the number of generations to evolve the population
max_generations = 10**5

# Define the maximum number of gates in the circuit
# From the paper, curcuits were composed of NAND gands
MAX_GATES = 12

# Define the input and output variables
circuit_inputs = ["x", "y", "w", "z"]
output = "u"

# A logic circuit
class Circuit:

    def __init__(self, binary_genome) -> None:
        self.binary_genome = binary_genome
        self.gates = [] # list of gates [(gate type, input1_addr, input2_addr)...]
        self.output_gene = None

    # Parse the genome according to https://www.pnas.org/doi/suppl/10.1073/pnas.0503610102/suppl_file/03610fig6.pdf
    def parse_genome(self):
        for i in range(0, len(self.binary_genome)-4, 10):
            gate_type = self.binary_genome[i:i+2]
            input1_addr = int(self.binary_genome[i+2:i+6], 2)
            input2_addr = int(self.binary_genome[i+6:i+10], 2)
            self.gates.append((gate_type, input1_addr, input2_addr))
        self.output_gene = int(self.binary_genome[-4:], 2)

    def run_circuit(self, input): # x, y, w, z = input
        # Initialize the gate values memo
        gate_values = {i: None for i in range(len(self.gates))}

        def dfs(i):
            # Indices 0-3 correspond to input values x, y, w, and z
            if i < 4:
                return input[i]
            
            # Indices 4-15 correspond to each gate (1, ..., 12)
            gate_idx = i - 4

            # Handle gate values
            if gate_values[gate_idx] is not None:
                return gate_values[gate_idx]
            
            gate_type, input1_addr, input2_addr = self.gates[gate_idx]

            # Compute the input values recursively
            input1_val = dfs(input1_addr)
            input2_val = dfs(input2_addr)

            # Accounting for unsolvable circuits
            if input1_val == -1 or input2_val == -1:
                return -1
            
            # NAND gate properties (if any input is zero, result is 1)
            if input1_val == 0 or input2_val == 0:
                return 1
            
            output_val = operations[gate_type](input1_val, input2_val)
            gate_values[gate_idx] = output_val
            return output_val
        
        # Run DFS by starting from the output then solving the circuit inwards
        return dfs(self.output_gene)
         
    # Fitness of a circuit to a goal function
    def fitness(self, goal):
        # TODO: Set an extra penalty for non-effective (no direct path to output) gates (https://pubmed.ncbi.nlm.nih.gov/16174729/)
        input_values = list(product([0, 1], repeat=len(circuit_inputs)))
        eval_score = 0

        # Fitness defined as the fraction of correct outputs over all possible inputs (https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000206&type=printable)
        for input in input_values:
            goal_output = goal(input)
            circuit_output = self.run_circuit(input)
            eval_score += (goal_output == circuit_output)

        return eval_score / len(input_values)

binary_genome = "00010101110001010111"
"""

# Define the possible values for the inputs and outputs
values = [0, 1]

# Define the function to generate a random circuit
def generate_circuit():
    circuit = []
    for i in range(random.randint(1, MAX_GATES)):
        gate = (random.choice(list(operations.keys())), random.randint(0, 3), random.randint(0, 3))
        circuit.append(gate)
    return circuit

# Define the function to evaluate a circuit
def evaluate_circuit(circuit, goal):
    num_correct = 0
    for x in values:
        for y in values:
            for w in values:
                for z in values:
                    inputs_dict = {"x": x, "y": y, "w": w, "z": z}
                    output_dict = {output: None}
                    for gate in circuit:
                        op, in1, in2 = gate
                        val1 = inputs_dict[inputs[in1]]
                        val2 = inputs_dict[inputs[in2]]
                        if op == "XOR":
                            output_dict[gate] = int(not (val1 or val2))
                        elif op == "EQ":
                            output_dict[gate] = int(val1 == val2)
                        elif op == "AND":
                            output_dict[gate] = int(val1 and val2)
                        elif op == "OR":
                            output_dict[gate] = int(val1 or val2)
                        inputs_dict[gate] = output_dict[gate]
                    if output_dict[output] == goal(x, y, w, z):
                        num_correct += 1
    return float(num_correct) / (len(values) ** 4)

# Define the goals as specified
def g(x, y):
    return random.choice([operations["XOR"], operations["EQ"]])(x, y)

def h(w, z):
    return random.choice([operations["XOR"], operations["EQ"]])(w, z)

def f(a, b):
    return random.choice([operations["AND"], operations["OR"]])(a, b)

# Define the function to generate a new goal every E generations
def get_goal(t):
    if t % 20 == 0:
        return lambda x, y, w, z: f(g(x, y), h(w, z))
    else:
        return current_goal

# Initialize the current goal and circuit
current_goal = lambda x, y, w, z: f(g(x, y), h(w, z))
current_circuit = generate_circuit()

# Evaluate the fitness of the circuit
fitness = evaluate_circuit(current_circuit, current_goal)

# Print the results
print("Current circuit: ", current_circuit)
print("Current fitness: ", fitness)
"""