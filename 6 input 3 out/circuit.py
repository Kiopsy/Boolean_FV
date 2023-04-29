import itertools
from constants import OPERATIONS, GATE_TYPE_SZ, GATE_ADDR_SZ, NUM_INPUTS, NUM_OUTPUTS
from goal import Goal

# A logic circuit
class Circuit:
	def __init__(self, binary_genome:str, silent=True) -> None:
		self.BINARY_GENOME: str = binary_genome
		self.gates = [] 
		self.SILENT = silent
		self.output_genes: list[int] = []
		self.parse_genome()

	def sprint(self, *args, **kwargs):
		if not self.SILENT:
			print(args, kwargs)
		
	def parse_genome(self) -> None:
		gate_genome_sz = GATE_TYPE_SZ + (2 * GATE_ADDR_SZ)

		for i in range(0, len(self.BINARY_GENOME)-GATE_ADDR_SZ*NUM_OUTPUTS, gate_genome_sz):
			gate_type = self.get_gate_type(self.BINARY_GENOME[i:i+GATE_TYPE_SZ])
			input1_start = i + GATE_TYPE_SZ
			input1_end = input1_start + GATE_ADDR_SZ
			input1_addr = int(self.BINARY_GENOME[input1_start:input1_end], 2)

			input2_start = input1_end
			input2_end = input2_start + GATE_ADDR_SZ
			input2_addr = int(self.BINARY_GENOME[input2_start:input2_end], 2)

			self.gates.append([gate_type, input1_addr, input2_addr])

		for i in range(NUM_OUTPUTS):
			self.output_genes.append(int(self.BINARY_GENOME[-GATE_ADDR_SZ:], 2))
	
	def get_gate_type(self, binary_string: str) -> str:
		if binary_string == "00":
			return "NAND"
		else:
			return None
			
	def run_circuit(self, inputs) -> int:
		addr_to_output = dict()
		for i, val in enumerate(inputs):
			addr_to_output[i] = [val]

		for i, gate in enumerate(self.gates):
			addr_to_output[i + len(inputs)] = gate

		self.sprint("Gates:", addr_to_output)
		self.sprint("Output Genes:", self.output_genes)

		visited = set()

		def dfs(gate_index) -> list[int]:

			# if we have been to this index, return -1, meaning that this circuit potentially does not work
			if gate_index in visited:
				raise Exception(f"Self loop")

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

			if gate:
				val = OPERATIONS[gate](input1_val, input2_val)
			else:
				raise Exception(f"No gate here")

			# memoization => set the gate to be its output value so no future computations are needed
			addr_to_output[gate_index] = [val]

			# return output
			visited.remove(gate_index)
			return int(val)

		outputs = []

		for output_gene in self.output_genes:
			try:
				output = dfs(output_gene)
			except Exception as e:
				self.sprint(e)
				output = None
			outputs.append(output)

		return outputs 
	
	# Returns the fitness of a circuit defined as the fraction of correct outputs over all possible inputs
    # Fitness defined in https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000206&type=self.sprintable
	def fitness(self, goal: Goal) -> float:
		# TODO: Set an extra penalty for non-effective (no direct path to output) gates
		inputs = list(itertools.product([0, 1], repeat=NUM_INPUTS)) #TODO
		eval_score = 0

		for input_set in inputs:
			goal_output, circuit_output = goal[input_set], self.run_circuit(input_set)
			eval_score += (goal_output == circuit_output)

		return eval_score / len(inputs)
	
	def get_truth_table(self) -> dict[tuple[NUM_INPUTS], int]:
		inputs = list(itertools.product([1, 0], repeat=NUM_INPUTS))
		table = dict()
		
		for input_set in inputs:
			table[input_set] = self.run_circuit(input_set)
		
		return table