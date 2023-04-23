from constants import OPERATIONS, NUM_INPUTS
import itertools

class Goal: 

    def __init__(self, goal_lst: list[str]):
        self.goal_str_lst = goal_lst
        self.truth_table = dict()

        # Allow for 4-input goal functions
        if NUM_INPUTS == 4:
            self.func = lambda w, x, y, z: OPERATIONS[goal_lst[0]](OPERATIONS[goal_lst[1]](x, y), OPERATIONS[goal_lst[2]](w, z))
            self.str = f"(w {goal_lst[0]} x) {goal_lst[1]} (y {goal_lst[2]} z)"

            inputs = list(itertools.product([1, 0], repeat=NUM_INPUTS))
            for input_set in inputs:
                w, x, y, z = input_set
                self.truth_table[(x, y, w, z)] = int(self.func(x, y, w, z))

        # Allow for 6-input goal functions
        elif NUM_INPUTS == 6:
            self.func = lambda t, u, x, y, w, z: OPERATIONS[goal_lst[3]](OPERATIONS[goal_lst[1]](OPERATIONS[goal_lst[0]](t, u), OPERATIONS[goal_lst[2]](w, x)), OPERATIONS[goal_lst[4]](y, z))
            self.str = f"(t {goal_lst[0]} u) {goal_lst[1]} (w {goal_lst[2]} x) {goal_lst[3]} (y {goal_lst[4]} z)"

            inputs = list(itertools.product([1, 0], repeat=NUM_INPUTS))
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