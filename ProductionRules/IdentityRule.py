from ProductionRules.ProductionRule import ProductionRule

UnitTest_IdentityRule = False

class IdentityRule(ProductionRule):
    def __init__(self, Succ):
        super().__init__(Succ)

    def Replace(self):
        return self.successors[0]


if UnitTest_IdentityRule:
    r = IdentityRule(["+"])
    r.Display()





