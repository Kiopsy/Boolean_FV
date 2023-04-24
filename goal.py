from constants import OPERATIONS
import itertools

class Goal: 

    def __init__(self, goal_list: list[str]):
        self.goal_str_lst = goal_list
        self.truth_table = dict()

        # Allow for 4-input goal functions
        if len(goal_list) == 3:
            self.func = lambda w, x, y, z: OPERATIONS[goal_list[0]](OPERATIONS[goal_list[1]](x, y), OPERATIONS[goal_list[2]](w, z))
            self.str = f"(w {goal_list[0]} x) {goal_list[1]} (y {goal_list[2]} z)"

            inputs = list(itertools.product([1, 0], repeat=len(goal_list)+1))
            for input_set in inputs:
                w, x, y, z = input_set
                self.truth_table[(x, y, w, z)] = int(self.func(x, y, w, z))

        # Allow for 6-input goal functions
        elif len(goal_list) == 5:
            self.func = lambda t, u, x, y, w, z: OPERATIONS[goal_list[3]](OPERATIONS[goal_list[1]](OPERATIONS[goal_list[0]](t, u), OPERATIONS[goal_list[2]](w, x)), OPERATIONS[goal_list[4]](y, z))
            self.str = f"(t {goal_list[0]} u) {goal_list[1]} (w {goal_list[2]} x) {goal_list[3]} (y {goal_list[4]} z)"

            inputs = list(itertools.product([1, 0], repeat=len(goal_list)+1))
            for input_set in inputs:
                t, u, w, x, y, z = input_set
                self.truth_table[(t, u, x, y, w, z)] = int(self.func(t, u, x, y, w, z))

    def __repr__(self):
        return self.str

    def __getitem__(self, key):
        return self.truth_table.get(key, None)

    def __eq__(self, other):
        if isinstance(other, Goal):
            return self.str == other.str
        return False