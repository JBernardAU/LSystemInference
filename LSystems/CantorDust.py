from LSystems.LSystem import LSystem
from ProductionRules.ProductionRule import DeterministicProductionRule
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC, ANY_SYMBOL_ID
from WordsAndSymbols.Word import Word

class CantorDust(LSystem):
    def __init__(self):
        super().__init__(name="Cantor Dust", axiom="ABA", alphabet = Alphabet(mappings={"A": 1, "B": 2},identity_symbols={}))
        ruleA = DeterministicProductionRule(
            SaC([ANY_SYMBOL_ID], self.alphabet.get_id("A"), [ANY_SYMBOL_ID]),
            Word.from_string("ABA", self.alphabet.mappings, self.i, self.j)
        )
        ruleB = DeterministicProductionRule(
            SaC([ANY_SYMBOL_ID], self.alphabet.get_id("B"), [ANY_SYMBOL_ID]),
            Word.from_string("BBB", self.alphabet.mappings, self.i, self.j)
        )
        self.add_rule(ruleA.sac,ruleA)
        self.add_rule(ruleB.sac,ruleB)
        self.iterate(n=3)