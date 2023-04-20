import random
import itertools
from collections import deque
from helpers import OPERATIONS
from goal import Goal

# A logic circuit
class Circuit:
	def __init__(self, binary_genome:str, silent=True) -> None:
		self.binary_genome: str = binary_genome
		self.gates = [] 
		self.SILENT = silent
		self.output_gene: int = None
		self.parse_genome()

	def sprint(self, *args, **kwargs):
		if not self.SILENT:
			print(args, kwargs)
		
	def parse_genome(self):
		for i in range(0, len(self.binary_genome)-4, 10):
			gate_type = self.get_gate_type(self.binary_genome[i:i+2])
			input1_addr = int(self.binary_genome[i+2:i+6], 2)
			input2_addr = int(self.binary_genome[i+6:i+10], 2)
			self.gates.append([gate_type, input1_addr, input2_addr])
		self.output_gene = int(self.binary_genome[-4:], 2)
	
	
	def get_gate_type(self, binary_string: str):
		if binary_string == "00":
			return "NAND"
		else:
			return None
			
	def run_circuit(self, inputs: tuple[bool, bool, bool, bool]) -> int:
		addr_to_output = dict()
		for i, val in enumerate(inputs):
			addr_to_output[i] = [val]

		for i, gate in enumerate(self.gates):
			addr_to_output[i + len(inputs)] = gate

		self.sprint("Gates:", addr_to_output)
		self.sprint("Output Gene:", self.output_gene)

		visited = set()

		def dfs(gate_index):

			# if we have been to this index, return -1, meaning that this circuit potentially does not work
			if gate_index in visited:
				return -1

			visited.add(gate_index)

			self.sprint("Look for gate:", gate_index)

			# try to unpack the gate list seen at this index if theres is a gate list
			try:
				x, *inputs_addresses = addr_to_output[gate_index]
				gate = val = x
			except KeyError as e:
				raise Exception(f"No gate with index {e}")

			# if there is only one single value there, just return that single value
			if len(inputs_addresses) == 0:
				visited.remove(gate_index)
				return val

			# if we are dealing with a gate, get the value of its inputs
			input1_val = dfs(inputs_addresses[0])
			input2_val = dfs(inputs_addresses[1])

			# if any of the inputs are 0, we know that the output of the gate will be 1
			if (input1_val * input2_val) == 0:
				val  = 1
			# if any of the inputs are -1 and not 0, we know there is a self loop
			elif (input1_val * input2_val) < 0:
				raise Exception(f"Self or feedback loop")
			# else, we have two actual outcomes and we should compute it
			# NOTE: not every gate should be a nand, some should be nothing right?
			else:
				if gate:
					val = OPERATIONS[gate](input1_val, input2_val)
				else:
					raise Exception(f"No gate here")

			# memoization => set the gate to be its output value so no future computations are needed
			addr_to_output[gate_index] = [val]

			# return output
			visited.remove(gate_index)
			return int(val)

		try:
			output = dfs(self.output_gene)
		except Exception as e:
			self.sprint(e)
			output = None

		return output 
	
	# Returns the fitness of a circuit defined as the fraction of correct outputs over all possible inputs
    # Fitness defined in https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000206&type=self.sprintable
	def fitness(self, goal: Goal) -> float:
		# TODO: Set an extra penalty for non-effective (no direct path to output) gates

		inputs = list(itertools.product([0, 1], repeat=4))
		eval_score = 0

		for input_set in inputs:
			goal_output, circuit_output = goal[input_set], self.run_circuit(input_set)
			eval_score += (goal_output == circuit_output)

		return eval_score / len(inputs)
	
	def get_truth_table(self) -> dict[tuple[int, int, int, int], int]:
		inputs = list(itertools.product([1, 0], repeat=4))
		table = dict()
		
		for input_set in inputs:
			table[input_set] = self.run_circuit(input_set)
		
		return table