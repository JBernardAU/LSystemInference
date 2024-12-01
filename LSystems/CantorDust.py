from LSystems.LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule

class CantorDust(LSystem):
    def __init__(self, N=3):
        super().__init__()
        self.Initialize("ABA", ["A", "B"], list(), list(), "Cantor Dust")
        # For * < A > *
        self.AddRules(("A", "*", "*"), DeterministicRule(["ABA"]))
        # For * < B > *
        self.AddRules(("B", "*", "*"), DeterministicRule(["BBB"]))
        self.IterateN(self.axiom, N)

