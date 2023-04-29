from circuit import Circuit
import numpy as np
from goal import Goal
from helpers import add_to_csv, consistent_hash
from constants import SimulationSettings, SAVE_FREQUENCY
import pickle, os, random, datetime

class Simulation:

    def __init__(self, checkpoint = None) -> None:
        self.CHECKPOINT = checkpoint
        self.SETTINGS: SimulationSettings = SimulationSettings() if checkpoint == None else checkpoint["settings"]
        self.SETTINGS_HASH = consistent_hash(str(self.SETTINGS))
        self.SAVES_DIR = f"./saves/{self.SETTINGS_HASH}"
        self.CSV_FILE = f"{self.SAVES_DIR}/data_{datetime.datetime.now().strftime('%H_%M')}.csv"
        self.CSV_HEADER = ["Gen", "Max Fitness", "Average Fitness", "Normalized Fitness", "Max Fitness Genome", "Goal"]
        
    # Change the goal every E = 20 generations
    def get_goal(self, goal):
        if self.SETTINGS.CHANGING_GOAL and random.random() < 1/self.SETTINGS.G:
            goals = [Goal(goal_str) for goal_str in self.SETTINGS.GOALS]
            goals.remove(goal)
            goal = random.choice(goals)
            print(f"Goal has changed to {goal}")
    
        return goal

    # Initialize population of circuits
    def init_population(self, pop_size: int) -> list[Circuit]:
        population = []
        for _ in range(pop_size):
            individual_binary = "".join([str(random.randint(0, 1)) for _ in range(self.SETTINGS.B)])
            population.append(Circuit(individual_binary))
        return population

    def calculate_fitness(self, population: list[Circuit], goal: Goal) -> list[float]:
        return [individual.fitness(goal) for individual in population]

    def calculate_selection_weights(self, fitness_list: list[float]) -> list[float]:
        exp_values = np.exp(np.array(fitness_list) * self.SETTINGS.t)
        return list(exp_values / np.sum(exp_values))

    def select_parents(self, population: list[Circuit], selection_weights: list[float]) -> list[str]:
        parents = random.choices(population, weights=selection_weights, k=2)
        return [p.BINARY_GENOME for p in parents]

    # Mutation
    def mutate(self, genome: str) -> str:
        int_genome = [int(c) for c in genome]
        for i in range(len(genome)):
            if random.random() < self.SETTINGS.Pm:
                int_genome[i] = 1 - int_genome[i]
        return "".join([str(i) for i in int_genome])

    # Crossover and mutate
    def reproduce(self, parent_genomes: list[str]) -> list[Circuit]:
        if random.random() < self.SETTINGS.Pc:
            crossover_point = random.randint(1, len(parent_genomes[0])-1)
            child1_genome = parent_genomes[0][:crossover_point] + parent_genomes[1][crossover_point:]
            child2_genome = parent_genomes[1][:crossover_point] + parent_genomes[0][crossover_point:]
            return [Circuit(self.mutate(child1_genome)), Circuit(self.mutate(child2_genome))]
        else:
            return [Circuit(self.mutate(p)) for p in parent_genomes]

    # Genetic algorithm
    def genetic_algorithm(self):
        
        if not os.path.exists(self.SAVES_DIR):
            os.makedirs(self.SAVES_DIR)

            with open(f"{self.SAVES_DIR}/settings.txt", mode="w") as f:
                f.write(str(self.SETTINGS))

        if self.CHECKPOINT == None:
            add_to_csv(self.CSV_FILE, [f"settings: {self.SETTINGS}"])
            add_to_csv(self.CSV_FILE, self.CSV_HEADER)
            population = self.init_population(self.SETTINGS.N_pop)
            current_goal = Goal(self.SETTINGS.INIT_GOAL)
            starting_gen = 0
        else:
            add_to_csv(self.CSV_FILE, [f"Picking up from loadfile from dir {self.SETTINGS_HASH}..."])
            add_to_csv(self.CSV_FILE, [f"settings: {self.SETTINGS}"])
            add_to_csv(self.CSV_FILE, self.CSV_HEADER)
            population = self.CHECKPOINT["population"]
            current_goal = Goal(self.CHECKPOINT["goal_str"])
            starting_gen = self.CHECKPOINT["generation"]

        for gen in range(starting_gen, self.SETTINGS.L):
        
            if gen % SAVE_FREQUENCY == 0:
                checkpoint = dict()
                checkpoint["population"] = population
                checkpoint["goal_str"] = current_goal.GOAL_STR
                checkpoint["generation"] = gen
                checkpoint["settings"] = self.SETTINGS
                
                if gen < 1000:
                    filename = f"{self.SETTINGS_HASH}_{gen}"
                else:
                    filename = f"{self.SETTINGS_HASH}_{gen // SAVE_FREQUENCY}k"

                with open(f"{self.SAVES_DIR}/{filename}.pkl", "wb") as f:
                    pickle.dump(checkpoint, f)

            current_goal = self.get_goal(current_goal)
            fitness_list = self.calculate_fitness(population, current_goal)

            _max = max(fitness_list)
            _avg = sum(fitness_list)/len(fitness_list)
            _norm = (_max - _avg) / (1 - _avg)
            _max_genome = population[fitness_list.index(_max)].BINARY_GENOME

            print(f"Gen {gen} of {self.SETTINGS_HASH}: max = {_max}, avg = {_avg}")
            add_to_csv(self.CSV_FILE, [gen, _max, _avg, _norm, _max_genome, current_goal.GOAL_STR])

            selection_weights = self.calculate_selection_weights(fitness_list)
            new_population = []
            for _ in range(self.SETTINGS.N_pop//2):
                parents = self.select_parents(population, selection_weights)
                children = self.reproduce(parents)
                new_population.extend(children)
            population = new_population