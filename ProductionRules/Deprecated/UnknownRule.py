from ProductionRules.Deprecated.ProductionRule import ProductionRule

class UnknownRuleOld(ProductionRule):
    def __init__(self):
        super().__init__([None])

    def Replace(self):
        raise Exception("UnknownRule.Replace() cannot be called.")
