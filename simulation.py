import random
from helpers import OPERATIONS
from circuit import Circuit
import numpy as np
from goal import Goal
from recorder import add_to_csv
import datetime
from constants import Constants as c

now = datetime.datetime.now()
FILE_PATH = f"data/data_{now.strftime('%H_%M')}.csv"

# Define save variables
SAVE_FILE_PATH = ''
LOAD_FILE_PATH = ''
SAVE_ITERATIONS = 1000 # save every _ iterations


# Change the goal every E = 20 generations
def get_goal(goal):
    if c.CHANGING_GOAL and random.random() < 1/c.G:
        goal = Goal(g = random.choice(["XOR", "EQ"]), f = random.choice(["AND", "OR"]), h = random.choice(["XOR", "EQ"]))

    return goal

# Initialize population of circuits
def init_population(pop_size: int) -> list[Circuit]:
    population = []
    for i in range(pop_size):
        individual_binary = "".join([str(random.randint(0, 1)) for _ in range(c.B)])
        population.append(Circuit(individual_binary))
    return population

def calculate_fitness(population: list[Circuit], goal: Goal) -> list[float]:
    return [individual.fitness(goal) for individual in population]

def calculate_selection_weights(fitness_list: list[float]) -> list[float]:
    t = 30
    exp_values = np.exp(np.array(fitness_list) * t)
    return list(exp_values / np.sum(exp_values))

def select_parents(population: list[Circuit], selection_weights: list[float]) -> list[Circuit]:
    parents = random.choices(population, weights=selection_weights, k=2)
    return parents

# Mutation
def mutate(genome: str) -> str:
    int_genome = [int(c) for c in genome]
    for i in range(len(genome)):
        if random.random() < c.Pm:
            int_genome[i] = 1 - int_genome[i]
    return "".join([str(i) for i in int_genome])

# Crossover and mutate
def reproduce(parents: list[Circuit]) -> list[Circuit]:
    if random.random() < c.Pc:
        crossover_point = random.randint(1, len(parents[0].binary_genome)-1)
        child1_genome = parents[0].binary_genome[:crossover_point] + parents[1].binary_genome[crossover_point:]
        child2_genome = parents[1].binary_genome[:crossover_point] + parents[0].binary_genome[crossover_point:]
        return [Circuit(mutate(child1_genome)), Circuit(mutate(child2_genome))]
    else:
        return parents

# Genetic algorithm
def genetic_algorithm():

    add_to_csv(FILE_PATH, [f"settings: {c()}"])
    add_to_csv(FILE_PATH, ["Gen", "Max Fitness", "Average Fitness", "Normalized Fitness", "Max Fitness Genome"])

    population = init_population(c.N_pop)
    current_goal = Goal(g = "XOR", f = "OR", h = "XOR")
    for l in range(c.L):
        current_goal = get_goal(current_goal)
        fitness_list = calculate_fitness(population, current_goal)

        _max = max(fitness_list)
        _avg = sum(fitness_list)/len(fitness_list)
        _norm = (_max - _avg) / (1 - _avg)
        _max_genome = population[fitness_list.index(_max)].binary_genome

        print(f"Gen {l}: max = {_max}, avg = {_avg}, norm = {_norm}")
        add_to_csv(FILE_PATH, [l, _max, _avg, _norm, _max_genome])

        selection_weights = calculate_selection_weights(fitness_list)
        new_population = []
        for i in range(c.N_pop//2):
            parents = select_parents(population, selection_weights)
            children = reproduce(parents)
            new_population.extend(children)
        population = new_population

