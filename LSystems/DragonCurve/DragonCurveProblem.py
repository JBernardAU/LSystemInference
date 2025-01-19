from LSystems.InferenceProblem import InferenceProblem


class DragonCurveProblem(InferenceProblem):
    def __init__(self, lsystem=None):
        super().__init__(lsystem)

        self.strings = []
        self.strings.append("X+YF+")
        self.strings.append("X+YF++-FX-YF+")
        self.strings.append("X+YF++-FX-YF++-FX+YF+--FX-YF+")

