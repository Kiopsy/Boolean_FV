import random
from helpers import OPERATIONS
from circuit import Circuit
import numpy as np
from goal import Goal
from recorder import add_to_csv
import datetime

now = datetime.datetime.now()
FILE_PATH = f"data/data_{now.strftime('%H_%M')}.csv"

const = {
    "CHANGING_GOAL" : False,

    # Define the population individuals 
    "N_pop": 5000,

    # Define the length of the binary genome in bits 
    "B": 104,

    # Define the probability of genome crossover
    "Pc": 0.5,

    # Define the number of generations to evolve the population
    "L": 10**5,

    # Define the maximum number of gates in the circuit
    # From the paper, curcui]ts were composed of NAND gands
    "MAX_GATES": 12,

    # expected number of generations until the goal is changed
    "G": 20
}
# Define the probability of a gene mutation
const["Pm"] = 0.7 / const["B"]

# change the goal every E = 20 generations
def get_goal(goal):
    if random.random() < 1/const["G"] and const["CHANGING_GOAL"]:
        goal = Goal(g = random.choice(["XOR", "EQ"]), f = random.choice(["AND", "OR"]), h = random.choice(["XOR", "EQ"]))

    return goal

# Initialize population of circuits
def init_population(pop_size: int) -> list[Circuit]:
    population = []
    for i in range(pop_size):
        individual_binary = "".join([str(random.randint(0, 1)) for _ in range(const["B"])])
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
        if random.random() < const["Pm"]:
            int_genome[i] = 1 - int_genome[i]
    return "".join([str(i) for i in int_genome])

# Crossover and mutate
def reproduce(parents: list[Circuit]) -> list[Circuit]:
    if random.random() < const["Pc"]:
        crossover_point = random.randint(1, len(parents[0].binary_genome)-1)
        child1_genome = parents[0].binary_genome[:crossover_point] + parents[1].binary_genome[crossover_point:]
        child2_genome = parents[1].binary_genome[:crossover_point] + parents[0].binary_genome[crossover_point:]
        return [Circuit(mutate(child1_genome)), Circuit(mutate(child2_genome))]
    else:
        return parents


# Genetic algorithm
def genetic_algorithm():

    add_to_csv(FILE_PATH, [f"settings: {const}"])
    add_to_csv(FILE_PATH, ["Gen", "Max Fitness", "Average Fitness", "Max Fitness Genome"])

    population = init_population(const["N_pop"])
    current_goal = Goal(g = "XOR", f = "OR", h = "XOR")
    for l in range(const["L"]):
        current_goal = get_goal(current_goal)
        fitness_list = calculate_fitness(population, current_goal)

        _max = max(fitness_list)
        _avg = sum(fitness_list)/len(fitness_list)
        _max_genome = population[fitness_list.index(_max)].binary_genome

        print(f"Gen {l}: Max fitness = {_max}; Avg fitness = {_avg}")
        add_to_csv(FILE_PATH, [l, _max, _avg, _max_genome])

        selection_weights = calculate_selection_weights(fitness_list)
        new_population = []
        for i in range(const["N_pop"]//2):
            parents = select_parents(population, selection_weights)
            children = reproduce(parents)
            new_population.extend(children)
        population = new_population

