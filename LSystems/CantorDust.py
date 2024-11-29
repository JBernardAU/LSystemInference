from LSystem import LSystem
from DeterministicRule import DeterministicRule

class CantorDust(LSystem):
    def __init__(self, N=3):
        super().__init__()
        self.Initialize("ABA", ["A", "B"], list(), "Cantor Dust")

        # add rules
        # For symbol A
        predecessors = [("A", "*", "*")]
        successors = ["ABA"]
        self.AddRules(DeterministicRule(predecessors, successors))

        # For symbol B
        predecessors = [("B", "*", "*")]
        successors = ["BBB"]
        self.AddRules(DeterministicRule(predecessors, successors))

        self.IterateN(self.axiom, N)
