import random

# Initialize population
def init_population(pop_size, gene_length):
    population = []
    for i in range(pop_size):
        individual = [random.randint(0, 1) for j in range(gene_length)]
        population.append(individual)
    return population

# Evaluate fitness
def fitness_logic_circuits(individual):
    # implement logic circuits fitness function here
    return fitness

def fitness_RNA(individual):
    # implement RNA fitness function here
    return fitness

# Select parents
def select_parents(population, fitness_func):
    fitnesses = [fitness_func(individual) for individual in population]
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
def genetic_algorithm(pop_size, gene_length, fitness_func, crossover_rate, mutation_rate, max_generations):
    population = init_population(pop_size, gene_length)
    for i in range(max_generations):
        parents = select_parents(population, fitness_func)
        children = crossover(parents, crossover_rate)
        new_population = [mutate(child, mutation_rate/gene_length) for child in children]
        population = new_population
    best_individual = max(population, key=fitness_func)
    return best_individual

# Example usage for logic circuits model
best_individual = genetic_algorithm(5000, 104, fitness_logic_circuits, 0.5, 0.7, 105)
print(best_individual)
