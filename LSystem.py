class LSystem:
    def __init__(self):
        self.name = ""
        self.axiom = ""
        self.alphabet = []
        self.rules = []
        self.strings = []

    def Display(self, WithRules=True):
        print("Lsystem " + self.name)
        print("Alphabet: ")
        sep = ""
        for s in self.alphabet:
            print(sep + s, end="")
            sep = ","
        print()
        print("Axiom: " + self.axiom)

        if WithRules:
            print("Rules: ")
            for r in self.rules:
                print(r)

        print("Strings: ")
        for st in self.strings:
            print(st)

    # This iterates a generation from a word
    def Iterate(self, W):
        #print("Iterate over " + W)
        result = ""
        for s in W:
            result += s
        return result

    # Iterates N times
    def IterateN(self, W, N):
        curr = W
        for i in range(N):
            curr = self.Iterate(curr)
            self.strings.append(curr)

    def AddSymbol(self,S):
        self.alphabet.append(S)
        self.rules.append([])

    def AddRule(self,S, R):
        print()

    # initialize an L-system with an axiom (W) and N strings
    def Initialize(self, W, A, Name="Unnamed"):
        self.name = Name
        self.axiom = W
        self.alphabet = A
        self.strings.append(W)
        for s in self.alphabet:
            self.rules.append([])

l = LSystem()
l.Initialize("ABC", ["A","B","C"])
l.Display()
l.IterateN(l.axiom, 3)
