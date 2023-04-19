from circuit import Circuit

if __name__ == '__main__':
    three_binary_genome = '0000000001000010001100010001010110' # '0000000001 | 0000100011 | 0001000101 | 0110'
    three_gate_circuit = Circuit(three_binary_genome)
    
    a = three_gate_circuit.run_circuit([1, 1, 0, 0])
    print(a)