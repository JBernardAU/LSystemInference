from LSystem import LSystem

class UnknownLSystem_00001(LSystem):
    def __init__(self):
        super().__init__()
        self.Initialize("ABA", [], list(),"Unknown")
        self.words.append("ABABBBABA")
        self.words.append("ABABBBABABBBBBBBBBABABBBABA")
        self.words.append("ABABBBABABBBBBBBBBABABBBABABBBBBBBBBBBBBBBBBBBBBBBBBBBABABBBABABBBBBBBBBABABBBABA")

        self.contextSize = (0,0)

