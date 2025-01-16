from ProductionRules.Deprecated.ProductionRule import ProductionRule

UnitTest_DeterministicRule = False

"""
PROPERTIES:
- Successors. A list containing the replacement string.
METHODS:
"""

class DeterministicRuleOld(ProductionRule):
    def __init__(self, Succ):
        super().__init__(Succ)

    def Replace(self):
        return self.successors[0]