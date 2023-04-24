import itertools

class Goal: 

    def __init__(self, goal_str: str):
        
        self.truth_table = dict()

        # properly format goal_str with lowercase variables and uppercase op names
        goal_str = goal_str.lower()
        replacements = [("and", "&"), ("xor", "^"), ("eq", "=="), ("or", "|")]
        for a, b in replacements:
            goal_str = goal_str.replace(a, b)

        # set formatted string to the constsant
        self.GOAL_STR = goal_str

        
        variables = list(set([char for char in goal_str if char.islower()]))
        variables.sort(key = lambda x: goal_str.find(x))

        self.NUM_INPUTS = len(variables)

        # evaluate truth table
        inputs = list(itertools.product([1, 0], repeat=self.NUM_INPUTS))
        for input_set in inputs:
            eval_str = goal_str

            for i in range(len(variables)):
                eval_str = eval_str.replace(variables[i], str(input_set[i]))
            
            self.truth_table[input_set] = eval(eval_str)
    
    def __repr__(self):
        return self.GOAL_STR

    def __getitem__(self, key):
        return self.truth_table.get(key, None)

    def __eq__(self, other):
        if isinstance(other, Goal):
            return self.GOAL_STR == other.GOAL_STR
        return False