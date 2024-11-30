from GlobalSettings import identityAlphabet2D
from LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule

class DragonCurve(LSystem):
    def __init__(self, N=3):
        super().__init__()
        identities = ["F","+","-"]
        self.Initialize("FX+FX+", ["X", "Y"], identities, identities, "Dragon Curve")
        # For * < X > *
        self.AddRules(("X", "*", "*"), DeterministicRule(["X+YF"]))
        # For * < Y > *
        self.AddRules(("Y", "*", "*"), DeterministicRule(["FX-Y"]))
        self.AddIdentityRules()
        self.IterateN(self.axiom, 5)
