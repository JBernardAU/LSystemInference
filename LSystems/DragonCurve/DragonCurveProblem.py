from LSystems.InferenceProblem import InferenceProblem


class DragonCurveProblem(InferenceProblem):
    def __init__(self, settings_file="\\DragonCurve\\settings.json", lsystem=None):
        super().__init__(settings_file, lsystem)

    def _load_strings(self):
        self.strings.append("X+YF+")
        self.strings.append("X+YF++-FX-YF+")
        self.strings.append("X+YF++-FX-YF++-FX+YF+--FX-YF+")

