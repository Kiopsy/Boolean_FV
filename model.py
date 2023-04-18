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

# An individual gate of any operation type
class Gate:
    def __init__(self, gate_type, inputs):
        self.type = gate_type
        self.inputs = inputs
        self.output = None

    def evaluate(self):
        if self.output is not None:
            return self.output
        else:

            self.output = operations[self.type](self.inputs[0], self.inputs[1])

# A logic circuit (digraph)
class Circuit:
    def __init__(self, inputs = {i: 0 for i in circuit_inputs}, output=MAX_GATES - 1) -> None:
        self.inputs = inputs # Inputs to the circuit
        self.gates = [Gate("NAND", set()) for _ in range(MAX_GATES)] # TODO: switch to non-NAND ops here or pass 
        self.output = output # Output gate index

        curr_edge_count = 0
        start_nodes = list(chain(inputs.keys(), range(MAX_GATES)))
        self.edges = {i: None for i in start_nodes}

        # Connect each start_node once
        for start in start_nodes:
            # Skip over connecting output gate
            if start == self.output:
                continue

            # Ensure each gate has at most two inputs
            while len(self.edges[end]) < 2:
                end = random.randint(0, MAX_GATES)

            # Add to the gate's input
            self.gates[end].inputs.add(start)
            self.edges[start].add(end)
            curr_edge_count += 1

        # Ensure all inputs are connected...allow for self loops and feedback loops
        while curr_edge_count < 2 * MAX_GATES:
            # Choose a random starting node
            start = random.choice(start_nodes)

            # Connect it to an endpoint without two inputs
            end = random.choice([k for k, v in self.edges.items() if len(v) < 2])

            # Add to the gate's input
            self.gates[end].inputs.add(start)
            self.edges[start].add(end)
            curr_edge_count += 1

    # Runs the circuit based on a particular input
    def run_circuit(input):
        # A fitness penalty of 0.2 was given for every gate above apredefined number of effective gates 
        penalty = 0 # TODO How?!?!

        # BFS
        visited = set()
        queue = deque([start_vertex])
        visited[start_vertex] = True

        while queue:
            curr_vertex = queue.popleft()
            print(curr_vertex)

            for neighbor in self.adj_list[curr_vertex]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return penalty

    # Returns the fitness of a circuit defined as the fraction of correct outputs over all possible inputs
    def fitness(self, goal):
        # Set an extra penalty for non-effective (no direct path to output) gates

        input_values = list(product([0, 1], repeat=len(circuit_inputs)))
        eval_score = 0

        for input in input_values:
            goal_output = goal(input)
            circuit_output, penalty = self.run_circuit(input)

            eval_score += (goal_output == circuit_output) - penalty

        return eval_score / len(input_values)





def initialization():
















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