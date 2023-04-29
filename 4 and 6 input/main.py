from simulation import Simulation
import os, sys, pickle

# Create load/save directories if non-existant
for dir in [f"saves", "loads"]:
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':

    checkpoint = None

    # Allow for command-line args for loading checkpoints
    if len(sys.argv) > 1:
        load_file = sys.argv[1]
    
        with open(f"./loads/{load_file}", 'rb') as f:
            checkpoint = pickle.load(f)
            print(f"Loading data from file {load_file}")

    sim = Simulation(checkpoint)
    sim.genetic_algorithm()