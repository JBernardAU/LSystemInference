from ProductionRule import ProductionRule

UnitTest_IdentityRule = False

class IdentityRule(ProductionRule):
    def __init__(self, Pred, Succ):
        super().__init__(Pred, Succ)

    def Initialize(self, S):
        super().__init__([(S, "*", "*")],[S])

    def Replace(self, S, L, R):
        result = ""
        # just confirm
        if S == self.predecessors[0][0]:
            result = S
        else:
            raise Exception("Symbol " + S + " does not match predecessor " + self.predecessors[0][0] + " in identity rule.")

        return result


if UnitTest_IdentityRule:
    r = IdentityRule([("+","*","*")],["+"])
    r.Display()





