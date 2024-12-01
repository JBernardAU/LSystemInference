from typing import List, Any

from ProductionRules.DeterministicRule import DeterministicRule
from ProductionRules.IdentityRule import IdentityRule
from ProductionRules.ProductionRule import ProductionRule
from Alphabet import Alphabet
from SaCLibrary import SaCLibrary
from Symbol import Symbol
from Word import Word
from GlobalSettings import *

UnitTest_LSystem = False

class LSystem:
    __name: str
    __axiom: str
    __alphabet: Alphabet
    __sacLibrary: SaCLibrary
    __rules: list[ProductionRule]
    __words: list[Word]
    __contextSize: tuple[int, int]

    def __init__(self):
        self.__name = ""
        self.__axiom = ""
        self.__alphabet = None
        self.__sacLibrary = None
        #self.__identities = list()
        #self.__forbidden = list()
        self.__rules = list()
        self.__words = list()
        self.__contextSize = None

    def GetName(self):
        return self.__name
    
    def GetAxiom(self):
        return self.__axiom

    def GetSymbol(self,I):
        return self.__alphabet.GetSymbol(I)

    def GetSymbolID(self,I):
        return self.__alphabet.GetID(I)

    def GetSAC(self,I):
        return self.__sacs.GetSAC(I)

    def GetSACID(self,I):
        return self.__sacs.GetSACID(I)

    def GetRule(self, SAC):
        pass

    def GetWord(self, I):
        return self.__words[I]

    # make a clone of the L-system with an altered alphabet
    def Project(self, A):
        # first make a copy
        result = LSystem()
        result.__name = self.__name
        result.axiom = self.__axiom
        result.alphabet = A
        result.rules = self.__rules
        result.words = self.__words

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
        print("L-system: " + self.__name)
        print("Alphabet: ", end="")
        sep = ""
        for s in self.__alphabet:
            print(sep + s, end="")
            sep = ", "
        print("Axiom: " + self.__axiom)

        if WithSACS:
            print("SAC Library: ")
            print(self.__sacLibrary)

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
        for w in self.__words:
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

    # noinspection PyTypeChecker
    def Initialize(self, W, A, k=0, l=0, Identities=None, Forbidden=None, Name="Unnamed"):
        if Identities is None:
            Identities = list()

        if Forbidden is None:
            Forbidden = list()

        self.__name = Name

        # setup the alphabet
        if type(Alphabet) is Alphabet:
            self.__alphabet = A
        else:
            self.__alphabet = Alphabet(A,Identities,Forbidden)

        self.__axiom = Word(self.__alphabet.ConvertString2List(W))
        self.__words.append(self.__axiom)
        self.__contextSize = (k,l)

    """
    Input: 
    - A symbol and context (SAC). This can be a SAC object or a tuple[str, str, str]
    - A rule associated with the SAC
    """
    def AddSAC(self, SAC, R):
        sac = SAC
        if type(SAC) is not SAC:
            # convert the tuple to a SAC
            s = self.__alphabet.FindSymbol(sac[iSACSymbol])
            lc = Word(self.__alphabet.ConvertString2List(sac[iSACLeft]))
            rc = Word(self.__alphabet.ConvertString2List(sac[iSACRight]))
            sac = SAC(s,lc,rc)

        self.__sacLibrary.Add(sac,R)



        pass

    """
    Inputs: None
    Outputs: None
    Creates a SAC library from the words of L-system
    """
    def InferSACLibrary(self):
        pass

    # This iterates a generation from a word
    def Iterate(self, W):
        if self.__sacLibrary is None:
            raise Exception("SAC Library is not initialized")
        else:
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
        if self.__sacLibrary is None:
            raise Exception("SAC Library is not initialized")
        else:
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

    def AddIdentityRules(self):
        for s in self.identities:
            self.AddIdentity(s)

    def AddIdentity(self, S):
        self.alphabet.append(S)
        self.sacs.append((S, "*", "*"))
        self.AddRules(IdentityRule([S]))

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
