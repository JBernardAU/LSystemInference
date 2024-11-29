from ProductionRules.ProductionRule import ProductionRule

class UnknownRule(ProductionRule):
    def __init__(self):
        super().__init__([None])

    def Replace(self):
        raise Exception("UnknownRule.Replace() cannot be called.")
