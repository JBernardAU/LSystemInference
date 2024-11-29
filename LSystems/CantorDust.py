from LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule

class CantorDust(LSystem):
    def __init__(self, N=3):
        super().__init__()
        self.Initialize("ABA", ["A", "B"], list(), list(), "Cantor Dust")
        # For SAC ("A", "*", "*")
        self.sacs.append(("A", "*", "*"))
        self.AddRules(DeterministicRule(["ABA"]))
        # For SAC ("B", "*", "*")
        self.sacs.append(("B", "*", "*"))
        self.AddRules(DeterministicRule(["BBB"]))
        self.IterateN(self.axiom, N)
