from circuit import Circuit
import numpy as np
from goal import Goal
from aux import add_to_csv, consistent_hash
from constants import SimulationSettings, FILE_PATH, SAVE_FREQUENCY
import pickle, os, random

class Simulation:

    def __init__(self, checkpoint = None):
        self.checkpoint = checkpoint
        self.settings: SimulationSettings = SimulationSettings() if checkpoint == None else checkpoint["settings"]

    # Change the goal every E = 20 generations
    def get_goal(self, goal):
        if self.settings.CHANGING_GOAL and random.random() < 1/self.settings.G:
            goal = Goal(g = random.choice(["XOR", "EQ"]), f = random.choice(["AND", "OR"]), h = random.choice(["XOR", "EQ"]))

        return goal

    # Initialize population of circuits
    def init_population(self, pop_size: int) -> list[Circuit]:
        population = []
        for i in range(pop_size):
            individual_binary = "".join([str(random.randint(0, 1)) for _ in range(self.settings.B)])
            population.append(Circuit(individual_binary))
        return population

    def calculate_fitness(self, population: list[Circuit], goal: Goal) -> list[float]:
        return [individual.fitness(goal) for individual in population]

    def calculate_selection_weights(self, fitness_list: list[float]) -> list[float]:
        t = 30
        exp_values = np.exp(np.array(fitness_list) * t)
        return list(exp_values / np.sum(exp_values))

    def select_parents(self, population: list[Circuit], selection_weights: list[float]) -> list[Circuit]:
        parents = random.choices(population, weights=selection_weights, k=2)
        return parents

    # Mutation
    def mutate(self, genome: str) -> str:
        int_genome = [int(c) for c in genome]
        for i in range(len(genome)):
            if random.random() < self.settings.Pm:
                int_genome[i] = 1 - int_genome[i]
        return "".join([str(i) for i in int_genome])

    # Crossover and mutate
    def reproduce(self, parents: list[Circuit]) -> list[Circuit]:
        if random.random() < self.settings.Pc:
            crossover_point = random.randint(1, len(parents[0].binary_genome)-1)
            child1_genome = parents[0].binary_genome[:crossover_point] + parents[1].binary_genome[crossover_point:]
            child2_genome = parents[1].binary_genome[:crossover_point] + parents[0].binary_genome[crossover_point:]
            return [Circuit(self.mutate(child1_genome)), Circuit(self.mutate(child2_genome))]
        else:
            return parents

    # Genetic algorithm
    def genetic_algorithm(self):

        if self.checkpoint == None:
            add_to_csv(FILE_PATH, [f"settings: {self.settings}"])
            add_to_csv(FILE_PATH, ["Gen", "Max Fitness", "Average Fitness", "Normalized Fitness", "Max Fitness Genome"])

            population = self.init_population(self.settings.N_pop)
            current_goal = Goal(g = "XOR", f = "OR", h = "XOR")
            starting_gen = 0
        else:
            add_to_csv(FILE_PATH, [f"Picking up from load file..."])
            add_to_csv(FILE_PATH, [f"settings: {self.settings}"])
            add_to_csv(FILE_PATH, ["Gen", "Max Fitness", "Average Fitness", "Normalized Fitness", "Max Fitness Genome"])
            population = self.checkpoint["population"]
            starting_gen = self.checkpoint["generation"]
            current_goal = self.checkpoint["goal"]


        for l in range(starting_gen, self.settings.L):
        
            if starting_gen % SAVE_FREQUENCY == 0:
                checkpoint = dict()
                checkpoint["generations"] = l 
                checkpoint["settings"] = self.settings
                checkpoint["population"] = population
                checkpoint["goal"] = current_goal

                dir = f"./saves/{consistent_hash(str(self.settings))}"

                if not os.path.exists(dir):
                    os.makedirs(dir)

                    with open(f"{dir}/settings.txt", mode="w") as f:
                        f.write(str(self.settings))
                
                with open(f"{dir}/{l}.pkl", "wb") as f:
                    pickle.dump(checkpoint, f)

            current_goal = self.get_goal(current_goal)
            fitness_list = self.calculate_fitness(population, current_goal)

            _max = max(fitness_list)
            _avg = sum(fitness_list)/len(fitness_list)
            _norm = (_max - _avg) / (1 - _avg)
            _max_genome = population[fitness_list.index(_max)].binary_genome

            print(f"Gen {l}: max = {_max}, avg = {_avg}, norm = {_norm}")
            add_to_csv(FILE_PATH, [l, _max, _avg, _norm, _max_genome])

            selection_weights = self.calculate_selection_weights(fitness_list)
            new_population = []
            for _ in range(self.settings.N_pop//2):
                parents = self.select_parents(population, selection_weights)
                children = self.reproduce(parents)
                new_population.extend(children)
            population = new_population

