import random
from itertools import chain, product
from collections import deque
from helpers import OPERATIONS

# Define the input and output variables
circuit_inputs = ["x", "y", "w", "z"]
output = "u"

# A logic circuit
class Circuit:
	def __init__(self, binary_genome, silent=True) -> None:
		self.binary_genome = binary_genome
		self.gates = [] 
		self.output_gene = None
		self.parse_genome()
		
	def parse_genome(self):
		for i in range(0, len(self.binary_genome)-4, 10):
			gate_type = self.binary_genome[i:i+2]
			input1_addr = int(self.binary_genome[i+2:i+6], 2)
			input2_addr = int(self.binary_genome[i+6:i+10], 2)
			self.gates.append([gate_type, input1_addr, input2_addr])
		self.output_gene = int(self.binary_genome[-4:], 2)
			
	def run_circuit(self, inputs):
		addr_to_output = dict()
		for i, val in enumerate(inputs):
			addr_to_output[i] = [val]

		for i, gate in enumerate(self.gates):
			addr_to_output[i + len(inputs)] = gate

		print("Gates:", addr_to_output)
		print("Output Gene:", self.output_gene)

		visited = set()

		def dfs(gate_index):

			# if we have been to this index, return -1, meaning that this circuit potentially does not work
			if gate_index in visited:
				return -1

			visited.add(gate_index)

			print("Look for gate:", gate_index)

			# try to unpack the gate list seen at this index if theres is a gate list
			try:
				x, *inputs_addresses = addr_to_output[gate_index]
			except KeyError as e:
				raise Exception(f"No gate with index {e}")

			# if there is only one single value there, just return that single value
			if len(inputs_addresses) == 0:
				visited.remove(gate_index)
				return x

			# if we are dealing with a gate, get the value of its inputs
			input1_val = dfs(inputs_addresses[0])
			input2_val = dfs(inputs_addresses[1])

			# if any of the inputs are 0, we know that the output of the gate will be 1
			if (input1_val * input2_val) == 0:
				x  = 1
			# if any of the inputs are -1 and not 0, we know there is a self loop
			elif (input1_val * input2_val) < 0:
				raise Exception(f"Self or feedback loop")
			# else, we have two actual outcomes and we should compute it
			# NOTE: not every gate should be a nand, some should be nothing right?
			else:
				if True:
					x = OPERATIONS["NAND"](input1_val, input2_val)
				else:
					pass

			# memoization => set the gate to be its output value so no future computations are needed
			addr_to_output[gate_index] = [x]

			# return output
			visited.remove(gate_index)
			return int(x)

		try:
			output = dfs(self.output_gene)
		except Exception as e:
			print(e)
			output = None

		return output 
	
	# Returns the fitness of a circuit defined as the fraction of correct outputs over all possible inputs
    # Fitness defined in https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000206&type=printable
	def fitness(self, goal):
		# TODO: Set an extra penalty for non-effective (no direct path to output) gates

		input_values = list(product([0, 1], repeat=len(circuit_inputs)))
		eval_score = 0

		for input in input_values:
			goal_output = goal(input)
			circuit_output = self.run_circuit(input)

			eval_score += (goal_output == circuit_output)

		return eval_score / len(input_values)