import itertools

class Goal: 

    def __init__(self, goal_str: list[str]):
        self.goal_str = goal_str
        self.truth_table = dict()

        # evaluate truth table
        parts = goal_str.split()
        variables = list(set([part for part in parts if part.islower()]))

        self.NUM_INPUTS = len(variables)

        goal_str = goal_str.replace("AND", "&")
        goal_str = goal_str.replace("XOR", "^")
        goal_str = goal_str.replace("EQ", "==")
        goal_str = goal_str.replace("OR", "|")

        inputs = list(itertools.product([1, 0], repeat=self.NUM_INPUTS))
        for input_set in inputs:
            eval_str = goal_str

            for i in range(len(variables)):
                eval_str = eval_str.replace(variables[i], str(input_set[i]))
            
            self.truth_table[input_set] = eval(eval_str)
    
    def __repr__(self):
        return self.goal_str

    def __getitem__(self, key):
        return self.truth_table.get(key, None)

    def __eq__(self, other):
        if isinstance(other, Goal):
            return self.goal_str == other.goal_str
        return False