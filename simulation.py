import random
from helpers import OPERATIONS
from circuit import Circuit

# Define the population individuals 
N_pop = 5000

# Define the length of the binary genome in bits 
B = 104

# Define the probability of genome crossover
Pc = 0.5

# Define the probability of a gene mutation
Pm = 0.7 / B

# Define the number of generations to evolve the population
L = 10**5

# Define the maximum number of gates in the circuit
# From the paper, curcuits were composed of NAND gands
MAX_GATES = 12

GENOME_LENGTH = MAX_GATES * 6 + 4

# Define the goals as specified
def g(x, y):
    return random.choice([OPERATIONS["XOR"], OPERATIONS["EQ"]])(x, y)

def h(w, z):
    return random.choice([OPERATIONS["XOR"], OPERATIONS["EQ"]])(w, z)

def f(a, b):
    return random.choice([OPERATIONS["AND"], OPERATIONS["OR"]])(a, b)

# Define the function to generate a new goal every E generations
def get_goal(t):
    if t % 20 == 0:
        return lambda x, y, w, z: f(g(x, y), h(w, z))
    else:
        return current_goal

# Initialize the current goal and circuit
current_goal = lambda x, y, w, z: f(g(x, y), h(w, z))

# Initialize population of circuits
def init_population(pop_size):
    population = []
    for i in range(pop_size):
        individual_binary = "".join([str(random.randint(0, 1)) for _ in range(GENOME_LENGTH)])
        population.append(Circuit(individual_binary))
    return population

# Select parents
def select_parents(population, fitness_func):
    fitnesses = [individual.fitness(fitness_func) for individual in population]
    total_fitness = sum(fitnesses)
    probabilities = [fitness/total_fitness for fitness in fitnesses]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

# Crossover
def crossover(parents, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, len(parents[0])-1)
        child1 = parents[0][:crossover_point] + parents[1][crossover_point:]
        child2 = parents[1][:crossover_point] + parents[0][crossover_point:]
        return [child1, child2]
    else:
        return parents

# Mutation
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

# Genetic algorithm
def genetic_algorithm(pop_size, fitness_func, crossover_rate, mutation_rate, max_generations):
    population = init_population(pop_size)
    for i in range(max_generations):
        parents = select_parents(population, fitness_func)
        children = crossover(parents, crossover_rate)
        new_population = [mutate(child, mutation_rate/gene_length) for child in children]
        population = new_population
    best_individual = max(population, key=fitness_func)
    return best_individual

# Example usage for logic circuits model
best_individual = genetic_algorithm(N_pop, current_goal, Pc, Pm, L)
print(best_individual.gates)
