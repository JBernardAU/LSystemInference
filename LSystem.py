from ProductionRules.DeterministicRule import DeterministicRule
from IdentityRule import IdentityRule
from Utility import *
from GlobalSettings import *
UnitTest_LSystem = False

class LSystem:
    def __init__(self):
        self.name = ""
        self.axiom = ""
        self.alphabet = list()
        self.sacs = list()
        self.identities = list()
        self.forbidden = None
        self.rules = list()
        self.words = list()
        self.contextSize = (0,0)

    # make a clone of the L-system with an altered alphabet
    def Project(self, A):
        # first make a copy
        result = LSystem()
        result.name = self.name
        result.axiom = self.axiom
        result.alphabet = A
        result.identities = self.identities
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

    def Display(self, WithSACS=True, WithRules=True):
        print("L-system: " + self.name)
        print("Alphabet: ", end="")
        sep = ""
        for s in self.alphabet:
            if s in self.identities:
                mark = "*"
            else:
                mark = ""
            print(sep + s + mark, end="")
            sep = ","
        print()
        print("Axiom: " + self.axiom)

        if WithSACS and not WithRules:
            print("SACS: ")
            for sac in self.sacs:
                DisplaySAC(sac)

        if WithRules:
            print("Rules: ")
            for sac in self.sacs:
                rules = self.GetRules(sac)
                for r in rules:
                    r.Display(sac)

        print("Strings: ")
        for st in self.words:
            print(st)

    """
    Inputs:
    - An axiom
    - An alphabet including identities
    - (optional) A list of symbols with known identity production rules
    - (optional) A list of forbidden symbols. Context may not pass a forbidden symbol
    - (optional) A name     
    Outputs:
    - none
    Function:
    This initializes a simple L-system using known values. This is mainly used for when no analysis is required and
    a known L-system is to be used for simulation purposes.
    """
    def Initialize(self, Axiom, Alphabet, Identities=None, Forbidden=None, Name="Unnamed"):
        if Identities is None:
            Identities = list()
        self.name = Name
        self.axiom = Axiom
        self.alphabet = Alphabet
        self.identities = Identities
        self.forbidden = Forbidden
        self.words.append(Axiom)

    # This iterates a generation from a word
    def Iterate(self, W):
        #print("Iterate over " + W)
        result = ""
        for (iPos, s) in enumerate(W):
            sac = GetSAC(W,iPos,self.contextSize[iContextLeft],self.contextSize[iContextRight],self.forbidden)
            rules = self.GetRules(sac)
            # by default, use rule zero
            rule = rules[0]
            result += rule.Replace()
        return result

    # Iterates N times
    def IterateN(self, W, N):
        curr = W
        for i in range(N):
            curr = self.Iterate(curr)
            self.words.append(curr)

    """
    Inputs: A symbol (S)
    Outputs: None
    Purpose: This adds a symbol to the alphabet. This should not be necessary that often since the L-system should
    be initialized but could be useful if trying to build an L-system analytically.
    """
    def AddSymbol(self,S):
        self.alphabet.append(S)

    """
    Inputs: A symbol and context (SAC)
    Outputs: None
    Purpose: This adds a SAC to the symbol and context list. This should not be necessary that often since the L-system 
    should be initialized but could be useful if trying to build an L-system analytically. Note, the SAC must align with
    the rules so AddRule should be called immediately afterward.
    """
    def AddSAC(self,SAC):
        self.alphabet.append(SAC)
        self.rules.append([])

    """
    Inputs: A rule (SAC)
    Outputs: None
    Purpose: This adds a rule to the L-system. Note, the position in the list must exactly match the SAC list as this
    is how rules are found.
    """
    def AddRules(self, R):
        self.rules.append(R)

    def AddIdentity(self, S):
        self.alphabet.append(S)
        predecessors = [(S, "*", "*")]
        successors = [S]
        self.AddRules(IdentityRule(predecessors, successors))

    def GetSymbolID(self, S):
        return self.alphabet.index(S)

    def GetSymbol(self, I):
        return self.alphabet[I]

    def GetSACID(self, SAC):
        return self.sacs.index(SAC)

    def GetSAC(self, I):
        return self.sacs[I]

    """
    Input: A symbol and context (SAC)
    Output: A list of rules that match the SAC
    Purpose: This returns a list of rules that could potentially match a provided symbol and context. If there is an 
    exact rule match, then only that rule will be returned; otherwise; all possible partial matches are returned
    including the degree of mismatch. Typically done before calling the rule's Replace() function.
    """
    def GetRules(self, SAC):
        result = list()
        pred = PredecessorFromSAC(SAC)
        try:
            ruleID = self.sacs.index(pred)
        except:
            ruleID = None

        if ruleID is not None:
            result.append(self.rules[ruleID])
        else:
            for r in self.rules:
                pass

        return result

"""
        result = ""
        if identityOnNoMatch:
            result = S
        #conditions
        # symbols must match
        iSucc = 0
        isMatch = False
        isExactMatch = False
        while (iSucc < len(self.successors)) and not isExactMatch:
            symbolMatch = (S == self.predecessors[iSucc][iSymbol])

            #check left symbols to left context
            leftMatch = (self.predecessors[iSucc][iLeft] == anySymbol) # if the predecessor left context is any symbol, then it automatically matches
            if not leftMatch:
                iPos1 = len(L)-1 # start from the right side of the context and move left
                iPos2 = len(self.predecessors[iSucc][iLeft]) - 1
                leftMatch = True # initialize to true
                while iPos1 >= 0 and iPos2 >= 0 and leftMatch:
                    leftMatch = leftMatch and (self.predecessors[iSucc][iLeft][iPos2] == L[iPos1])
                    iPos1 -= 1
                    iPos2 -= 1

            #check right symbols to right context
            rightMatch = (self.predecessors[iSucc][iRight] == anySymbol) # if the predecessor left context is any symbol, then it automatically matches
            if not rightMatch:
                iPos1 = 0 # start from the left side of the context and move right
                iPos2 = 0 # start from the left side of the context and move right
                rightMatch = True # initialize to true
                while iPos1 < len(R) and iPos2 < len(self.predecessors[iSucc][iRight]) and rightMatch:
                    rightMatch = rightMatch and (self.predecessors[iSucc][iRight][iPos2] == R[iPos1])
                    iPos1 += 1
                    iPos2 += 1

            isMatch = symbolMatch and leftMatch and rightMatch
            bool1 = self.predecessors[iSucc][iLeft] == anySymbol
            bool2 = self.predecessors[iSucc][iRight] == anySymbol
            bool3 = len(self.predecessors[iSucc][iLeft]) == len(L)
            bool4 = len(self.predecessors[iSucc][iRight]) == len(R)
            bool5 = isMatch and ((bool1 or bool3) and (bool2 or bool4))

            isExactMatch = isMatch and ((bool1 or bool3) and (bool2 or bool4))

            if isExactMatch or isMatch:
                result = self.successors[iSucc]

            iSucc += 1
"""

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
    l2 = l.Project(a2)
    l2.Display()
