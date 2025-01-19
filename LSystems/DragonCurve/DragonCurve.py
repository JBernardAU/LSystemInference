from LSystems.LSystem import LSystem
from ProductionRules.ProductionRule import DeterministicProductionRule
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC, ANY_SYMBOL_ID
from WordsAndSymbols.Word import Word

class DragonCurve(LSystem):
    def __init__(self):
        super().__init__(name="Dragon Curve", axiom="X", alphabet=Alphabet(mappings={"X": 0, "Y": 1}, identity_symbols={"F","+","-"}), k=0, l=0)
        ruleX = DeterministicProductionRule(
            SaC([ANY_SYMBOL_ID], self.alphabet.get_id("X"), [ANY_SYMBOL_ID]),
            Word.from_string("X+YF+", self.alphabet, self.k, self.l)
        )
        ruleY = DeterministicProductionRule(
            SaC([ANY_SYMBOL_ID], self.alphabet.get_id("Y"), [ANY_SYMBOL_ID]),
            Word.from_string(string="-FX-Y", alphabet=self.alphabet, k=self.k, l=self.l)
        )
        self.add_rule(ruleX.sac,ruleX)
        self.add_rule(ruleY.sac,ruleY)
        self.iterate(n=3)