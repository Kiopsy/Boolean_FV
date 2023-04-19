from helpers import OPERATIONS
import itertools

class Goal:

    def __init__(self, g:str, f:str, h:str):
        self.func = lambda x, y, w, z: OPERATIONS[f](OPERATIONS[g](x, y), OPERATIONS[h](w, z))
        self.str = f"(x {g} y) {f} (w {h} z)"
        self.truth_table = dict()

        inputs = list(itertools.product([1, 0], repeat=4))
        for input_set in inputs:
            x, y, w, z = input_set
            self.truth_table[(x, y, w, z)] = self.func(x, y, w, z)


    def __repr__(self):
        return self.str

    def __getitem__(self, key):
        return self.truth_table.get(key, None)