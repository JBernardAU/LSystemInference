from LSystemExtended import LSystemExtended

class UnknownLSystem_00001(LSystemExtended):
    def __init__(self):
        super().__init__()
        self.name = "Unknown L-System 00001"
        self.words.append("ABABBBABA")
        self.words.append("ABABBBABABBBBBBBBBABABBBABA")
        self.words.append("ABABBBABABBBBBBBBBABABBBABABBBBBBBBBBBBBBBBBBBBBBBBBBBABABBBABABBBBBBBBBABABBBABA")
        self.contextSize = (0,0)
        self.identities = list()
        self.forbidden = None
        super().InitalizeFromSelf()




