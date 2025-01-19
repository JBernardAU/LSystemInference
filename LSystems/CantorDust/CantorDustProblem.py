from LSystems.InferenceProblem import InferenceProblem


class CantorDustProblem(InferenceProblem):
    def __init__(self, lsystem=None):
        super().__init__(lsystem)

        self.strings = []
        self.strings.append("ABABBBABA")
        self.strings.append("ABABBBABABBBBBBBBBABABBBABA")
        self.strings.append("ABABBBABABBBBBBBBBABABBBABABBBBBBBBBBBBBBBBBBBBBBBBBBBABABBBABABBBBBBBBBABABBBABA")

