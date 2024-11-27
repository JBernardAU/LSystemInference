from DeterministicRule import DeterministicRule
from Utility import *
UnitTest_LSystem = True

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
                r.Display()

        print("Strings: ")
        for st in self.strings:
            print(st)

    # This iterates a generation from a word
    def Iterate(self, W):
        #print("Iterate over " + W)
        result = ""
        for (iPos, s) in enumerate(W):
            symbolID = self.GetSymbolID(s)
            rule = self.rules[symbolID]
            L = GetLeftContext(W,iPos,rule.GetLeftContextSize())
            R = GetRightContext(W,iPos,rule.GetRightContextSize())
            result += rule.Replace(s,L,R)
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

    def AddRules(self,S, R):
        symbolID = self.GetSymbolID(S)
        self.rules[symbolID] = R

    # initialize an L-system with an axiom (W) and N strings
    def Initialize(self, W, A, Name="Unnamed"):
        self.name = Name
        self.axiom = W
        self.alphabet = A
        self.strings.append(W)
        for s in self.alphabet:
            self.rules.append([])

    def GetSymbolID(self, S):
        return self.alphabet.index(S)

    def GetSymbol(self, I):
        return self.alphabet[I]

if UnitTest_LSystem:
    l = LSystem()
    l.Initialize("ABA", ["A","B"])

    # add rules
    # For symbol A
    predecessors = [("A","*","*")]
    successors = ["ABA"]
    l.AddRules("A", DeterministicRule(predecessors,successors))

    # For symbol B
    predecessors = [("B","*","*")]
    successors = ["BBB"]
    l.AddRules("B", DeterministicRule(predecessors, successors))

    l.IterateN(l.axiom, 3)
    l.Display()
