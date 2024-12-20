from ProductionRules.IdentityRule import IdentityRule
from ProductionRules.ProductionRule import ProductionRule
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC
from WordsAndSymbols.SaCLibrary import SaCLibrary
from WordsAndSymbols.Word import Word
from GlobalSettings import *

UnitTest_LSystem = False

class LSystem:
    _name: str
    _axiom: str
    _alphabet: Alphabet
    _sacLibrary: SaCLibrary
    _rules: list[ProductionRule]
    _words: list[Word]
    _contextSize: tuple[int, int]

    def __init__(self):
        self._name = ""
        self._axiom = ""
        self._alphabet = None
        self._sacLibrary = None
        #self.__identities = list()
        #self.__forbidden = list()
        self._rules = list()
        self._words = list()
        self._contextSize = None

    # PROPERTY GETTERS

    def GetName(self):
        return self._name
    
    def GetAxiom(self):
        return self._axiom

    def GetAlphabet(self):
        return self._alphabet

    def GetSACLibrary(self):
        return self._sacLibrary

    def GetContextSize(self):
        return self._contextSize

    def GetWords(self):
        return self._words

    # METHODS

    def GetSymbol(self,I):
        return self._alphabet.GetSymbol(I)

    def GetSymbolID(self,I):
        return self._alphabet.GetID(I)

    def GetSAC(self,I):
        return self.__sacs.GetSAC(I)

    def GetSACID(self,I):
        return self.__sacs.GetSACID(I)

    def GetRule(self, SAC):
        return self._sacLibrary.GetRule(SAC)

    def GetWord(self, I):
        return self._words[I]

    # METHODS

    # make a clone of the L-system with an altered alphabet
    def Project(self, A):
        # first make a copy
        result = LSystem()
        result._name = self._name
        result.axiom = self._axiom
        result.alphabet = A
        result.rules = self._rules
        result.words = self._words

        """
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
            if rule.predecessors[0][iSACSymbol] not in toRemove:
                rule.Filter(toRemove)
                rules.append(rule)

        result.rules = rules
        """
        return result

    def Display(self, WithSACS=True, WithRules=True):
        print("L-system: " + self._name)
        print("Alphabet: ", end="")
        sep = ""
        for s in self._alphabet:
            print(sep + s, end="")
            sep = ", "
        print()
        print("Axiom: " + str(self._axiom))

        if WithSACS:
            print("SAC Library: ")
            self._sacLibrary.Display()

        """
        DEPRECATED - Rules are in the SAC Library
        if WithRules:
            print("Rules: ")
            for sac in self.__sacLibrary:
                rules = self.GetRules(sac)
                for r in rules:
                    r.Display(sac)
        """

        print("Words: ")
        for w in self._words:
            print(w)

    """
    Inputs:
    - An axiom
    - An alphabet including identities. This can be a list of strings or an Alphabet object
    - (optional) A list of symbols with known identity production rules
    - (optional) A list of forbidden symbols. Context may not pass a forbidden symbol
    - (optional) A name     
    Outputs:
    - none
    Function:
    This initializes a simple L-system using known values. This is mainly used for when no analysis is required and
    a known L-system is to be used for simulation purposes.
    """
    def Initialize(self, W, A, k=0, l=0, Identities=None, Forbidden=None, Name="Unnamed"):
        if Identities is None:
            Identities = list()

        if Forbidden is None:
            Forbidden = list()

        self._name = Name

        # setup the alphabet
        if type(Alphabet) is Alphabet:
            self._alphabet = A
        else:
            self._alphabet = Alphabet(A, Identities, Forbidden)

        self._sacLibrary = SaCLibrary(self._alphabet)
        self._axiom = Word(self._alphabet.ConvertString2List(W))
        self._words.append(self._axiom)
        self._contextSize = (k, l)

    """
    Input: 
    - A symbol and context (SAC). This can be a SAC object or a tuple[str, str, str]
    - A rule associated with the SAC
    """
    def AddSAC(self, SAC, R):
        if self._sacLibrary is None:
            raise Exception("LSystem.AddSAC(): SACLibrary property is None.")
        sac = SAC
        if type(SAC) is not SAC:
            # convert the tuple to a SAC
            s = self._alphabet.FindSymbol(sac[iSACSymbol])
            #TODO: Possibly extend the contexts
            lc = self._alphabet.ConvertString2List(sac[iSACLeft])
            rc = self._alphabet.ConvertString2List(sac[iSACRight])
            if len(lc) > 0 and lc[0] == self._alphabet.anySymbol:
                lc = self._alphabet.anyWord
            else:
                lc = Word(lc)
            if len(rc) > 0 and rc[0] == self._alphabet.anySymbol:
                rc = self._alphabet.anyWord
            else:
                rc = Word(rc)
            sac = SaC(s,lc,rc)

        self._sacLibrary.Add(sac, R)

    """
    Inputs: None
    Outputs: None
    Creates a SAC library from the words of L-system
    """
    def InferSACLibrary(self):
        pass

    # This iterates a generation from a word
    def Iterate(self, W):
        if self._sacLibrary is None:
            raise Exception("LSystem.Iterate(): SAC Library is not initialized")
        if not W.IsExtended():
            W.Extend()
            self._sacLibrary.ExtendWord(W,self._contextSize[iContextLeft],self._contextSize[iContextRight])
        result = Word([])
        for (iPos, s) in enumerate(W):
            sac = W.GetSAC(iPos)
            rule = self.GetRule(sac)
            result.Append(rule.Replace())
        return result

    # Iterates N times
    def IterateN(self, W, N):
        if self._sacLibrary is None:
            raise Exception("SAC Library is not initialized")
        else:
            curr = W
            for i in range(N):
                curr = self.Iterate(curr)
                self._words.append(curr)

    """
    Inputs: A symbol (S)
    Outputs: None
    Purpose: This adds a symbol to the alphabet. This should not be necessary that often since the L-system should
    be initialized but could be useful if trying to build an L-system analytically.
    """
    def AddSymbol(self,S):
        self.alphabet.append(S)

    """
    Inputs: A rule (SAC)
    Outputs: None
    Purpose: This adds a rule to the L-system. Note, the position in the list must exactly match the SAC list as this
    is how rules are found.
    """
    def AddRules(self, R):
        self.rules.append(R)

    def AddIdentityRules(self):
        for i, s in enumerate(self._alphabet):
            if s.GetIsIdentity():
                self._sacLibrary.Add(SaC(s, self._alphabet.anyWord, self._alphabet.anyWord),IdentityRule([Word([s],[self._alphabet.GetID(i)])]))

    def GetSymbolID(self, S):
        return self.alphabet.index(S)

    def GetSymbol(self, I):
        return self.alphabet[I]

    def GetSACID(self, SAC):
        return self.sacs.index(SAC)

    def GetSAC(self, I):
        return self.sacs[I]

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

"""
DEPRECATED - Need a new test case
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
"""
