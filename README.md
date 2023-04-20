# Boolean_FV
A recreation of the paper by Parter et al., [Facilitated Variation: How Evolution Learns from Past Envirionments To Generalize to New Environments](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000206). We evolve logic gate circuits to satisfy a boolean function goal.

## Overview
The goal of this project is to convert a binary genome into a logic circuit composed of up to 12 NAND gates, and use a standard genetic algorithm to modify the genome and learn to satisfy a goal boolean function.

To achieve this goal, we convert a binary genome into a NAND logic circuit using the following methodology:

<img src='/supplementals/binary_encoding.png' width='800'/>

## Installation and Setup
Python version 3.7+ is required: the latest version of Python can be installed [here](https://www.python.org/downloads/). The program relies on Python's standard libraries, as well as external libraries including numpy, matplotlib, and networkx. However, all the requirements are listed in the file `requirements.txt`. Download all requirements for this repository by running the following command:
```bash
pip install -r requirements.txt
```
f
## Instructions
### Learning Simulation
To conduct experiments and test the [Theory of Facilitated Variation](https://www.pnas.org/doi/10.1073/pnas.0701035104#:~:text=In%20answer%2C%20the%20theory%20of,variety%20of%20regulatory%20targets%20for), switch between **fixed goals (FG)** and **modularly varying goals (MVG)** by changing the constants in the `constants.py` file. To switch to MVG, set the constant `CHANGING_GOAL` to `True`. To run the simulation and learn logic circuits that fit the goal function, use the following command in the terminal:

```bash
python main.py
```

To load a saved file, drag the file from the saves folder into the loads folder. Then, use the following command in the terminal:
```bash
python main.py [filename]
```

### Binary Genome Testing
To test a binary genome, retrieve the genome from the CSV file with the respective test. Then, use the following command in the terminal:
```bash
python genome_testing.py
```

Paste the genome, followed by the desired goal function. For example, to test a sample genome against the XOR/OR/XOR goal, use the following command:
```bash
python .\genome_testing.py
Genome: 0011011111110110101100111010010001100110010111100000010000101000011100110001111000011110100011110000000011010000000100010111
G/F/H: XOR/OR/XOR
```
Press enter three times to see how the circuit's truth table compares to the goal functions, and view the outputted digraph of the circuit. Here's an example truth table for a perfect circuit:
```bash
CIRCUIT TRUTH TABLE: [enter]
(1, 1, 1, 1): 0   (1, 1, 1, 0): 0   (1, 1, 0, 1): 0   (1, 1, 0, 0): 1
(1, 0, 1, 1): 0   (1, 0, 1, 0): 0   (1, 0, 0, 1): 0   (1, 0, 0, 0): 1
(0, 1, 1, 1): 0   (0, 1, 1, 0): 0   (0, 1, 0, 1): 0   (0, 1, 0, 0): 1
(0, 0, 1, 1): 1   (0, 0, 1, 0): 1   (0, 0, 0, 1): 1   (0, 0, 0, 0): 1


GOAL [(x XOR y) OR (w XOR z)] TRUTH TABLE: [enter]
(1, 1, 1, 1): 0   (1, 1, 1, 0): 0   (1, 1, 0, 1): 0   (1, 1, 0, 0): 1
(1, 0, 1, 1): 0   (1, 0, 1, 0): 0   (1, 0, 0, 1): 0   (1, 0, 0, 0): 1
(0, 1, 1, 1): 0   (0, 1, 1, 0): 0   (0, 1, 0, 1): 0   (0, 1, 0, 0): 1
(0, 0, 1, 1): 1   (0, 0, 1, 0): 1   (0, 0, 0, 1): 1   (0, 0, 0, 0): 1
```

## Example
A perfectly learned logic circuit to the goal function g(x,y,z,w) = (x XOR y) OR (z XOR w).

Respective binary genome: 0011011111110110101100111010010001100110010111100000010000101000011100110001111000011110100011110000000011010000000100010111

<img src='/supplementals/perfect_fit_XOR_OR_XOR_circuit.PNG' width='1000' />
