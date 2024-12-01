from GlobalSettings import identityAlphabet2D
from LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule
from Word import Word


class DragonCurve(LSystem):
    def __init__(self, N=3):
        super().__init__()
        identities = ["F","+","-"]
        self.Initialize(W="FX+FX+", A=["X", "Y"], k=0,l=0, Identities=identities, Forbidden=identities, Name="Dragon Curve")
        self.AddSAC(("X", "*", "*"),DeterministicRule([Word(self.__alphabet.ConvertString2List("X+YF"))]))
        self.AddSAC(("Y", "*", "*"),DeterministicRule([Word(self.__alphabet.ConvertString2List("FX-Y"))]))
        self.AddIdentityRules()
        self.IterateN(self.GetAxiom(), 5)
