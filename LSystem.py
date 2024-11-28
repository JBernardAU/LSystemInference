from DeterministicRule import DeterministicRule
from IdentityRule import IdentityRule
from Utility import *
from GlobalSettings import *
UnitTest_LSystem = True

class LSystem:
    def __init__(self):
        self.name = ""
        self.axiom = ""
        self.alphabet = []
        self.rules = []
        self.words = []

    # make a clone of the L-system with an altered alphabet
    def Clone(self, A):
        # first make a copy
        result = LSystem()
        result.name = self.name
        result.axiom = self.axiom
        result.alphabet = A
        result.rules = self.rules
        result.words = self.words

        # Printing the result
        toRemove = list(set(self.alphabet) - set(result.alphabet))

        # determine what symbols are to be removed

        # remove the symbols
        # 1. filter axiom
        result.axiom = Filter(result.axiom, toRemove)

        # 2. filter strings
        for (iWord, word) in enumerate(result.words):
            result.words[iWord] = Filter(result.axiom, toRemove)

        # 3. filter rules
        # If the rule's symbol is not in toRemove, then ignore it (in essence remove the rule compeltely)
        # Otherwise call Filter
        rules = []
        for (iRule, rule) in enumerate(result.rules):
            if rule.predecessors[0][iSymbol] not in toRemove:
                rule.Filter(toRemove)
                rules.append(rule)

        result.rules = rules

        return result


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
        for st in self.words:
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
            self.words.append(curr)

    def AddSymbol(self,S):
        self.alphabet.append(S)
        self.rules.append([])

    def AddRules(self, R):
        self.rules.append(R)

    def AddIdentity(self, S):
        self.alphabet.append(S)
        predecessors = [(S, "*", "*")]
        successors = [S]
        self.AddRules(IdentityRule(predecessors, successors))

    # initialize an L-system with an axiom (W) and N strings
    def Initialize(self, W, A, Name="Unnamed"):
        self.name = Name
        self.axiom = W
        self.alphabet = A
        self.words.append(W)

    def GetSymbolID(self, S):
        return self.alphabet.index(S)

    def GetSymbol(self, I):
        return self.alphabet[I]

if UnitTest_LSystem:
    l = LSystem()
    l.Initialize("A+B-A", ["A","B"])

    # add rules
    # For symbol A
    predecessors = [("A","*","*")]
    successors = ["A+B-A"]
    l.AddRules(DeterministicRule(predecessors,successors))

    # For symbol B
    predecessors = [("B","*","*")]
    successors = ["[B-B+B]"]
    l.AddRules(DeterministicRule(predecessors, successors))

    # For identities
    l.AddIdentity("+")
    l.AddIdentity("-")
    l.AddIdentity("[")
    l.AddIdentity("]")

    l.IterateN(l.axiom, 3)
    l.Display()

    a2 = ["A","B","+"]
    l2 = l.Clone(a2)
    l2.Display()
