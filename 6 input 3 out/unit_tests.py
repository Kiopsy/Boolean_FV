import unittest
from goal import Goal
import itertools

class TestGoals(unittest.TestCase):
    
    def test_set_4_input_goal(self):
        g = Goal("(x xor y) or (z eq w)")

        truth_table = dict()
        inputs = list(itertools.product([1, 0], repeat=4))
        for input_set in inputs:
            a, b, c, d = input_set
            truth_table[input_set] = int(((a ^ b)) or (c == d))

        self.assertEqual(g.truth_table, truth_table)
    
    def test_set_6_input_goal(self):
        g = Goal("(x xor y) or (z eq w) and (q xor p)")

        truth_table = dict()
        inputs = list(itertools.product([1, 0], repeat=6))
        for input_set in inputs:
            a, b, c, d, e, f = input_set
            truth_table[input_set] = int(((a ^ b)) or (c == d) and (e ^ f))

        self.assertEqual(g.truth_table, truth_table)

        
        
if __name__ == '__main__':
    unittest.main()
