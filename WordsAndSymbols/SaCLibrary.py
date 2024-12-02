import math

from ProductionRules.ProductionRule import ProductionRule
from WordsAndSymbols.SaC import SaC
from WordsAndSymbols.Word import Word


class SaCLibrary:
    __sacs: list[SaC]
    __ids: list[int]
    __rules: list[ProductionRule]

    def __init__(self, Alphabet):
        self.__sacs = list()
        self.__ids = list()
        self.__rules = list()
        self.__alphabet = Alphabet

    def __len__(self):
        return len(self.__sacs)

    def Display(self):
        for i, s in enumerate(self.__sacs):
            print(s)
            print(self.__rules[i])

    def __iter__(self):
        return iter(self.__sacs)

    def GetSAC(self, I):
        return self.__sacs[I]

    def GetID(self, I):
        return self.__ids[I]

    def GetRuleBySAC(self, SAC):
        bestIdx = -1
        bestErr = math.inf
        for i, sac in enumerate(self.__sacs):
            if sac == SAC:
                return self.GetRuleByIndex(i)
            else:
                #is this a partial match?
                error = SAC.PartialMatch(sac)
                if error < bestErr:
                    bestIdx = i
                    bestErr = error

        if bestIdx > -1:
            return self.GetRuleByIndex(bestIdx)
        else:
            raise Exception("No matching rule for " + SAC)

    def GetRuleByIndex(self, I):
        return self.__rules[I]

    def GetSaCID(self, SAC):
        for i, sac in self.__sacs:
            if sac == SAC:
                return self.__ids[i]

    def Add(self, SAC, R):
        if not issubclass(type(SAC),SaC):
            raise Exception("SACLibrary.Add(): Type Error - SAC argument is not a subclass of SaC object.")
        if not issubclass(type(R),ProductionRule):
            raise Exception("SACLibrary.Add(): Type Error - R argument is not a subclass of ProductionRule object.")
        id = len(self.__sacs)
        self.__sacs.append(SAC)
        self.__rules.append(R)
        self.__ids.append(id)

    """
    Inputs:
    - A word (W)
    - A context size, k,l
    Outputs:
    - None. Modifies W.
    This function extends a word by calculating the SACs in the word, the counts, and other metrics.
    This should be used when the only available information are the words themselves.
    TODO: This could be made more efficient using the window trick
    """
    def ExtendWord(self, W, k, l):
        # set SACs for W
        for i, s in enumerate(W):
            # find the SAC at position I
            lc = list()
            rc = list()
            lPos = i-1
            rPos = i+1

            # scan left
            curr = None
            flag = True
            count = 0
            while lPos >= 0 and count < k and flag:
                curr = W.GetSymbol(lPos)
                if not curr.IsForbidden():
                    lc.append(curr)
                    lPos -= 1
                else:
                    flag = False

            # scan right
            curr = None
            flag = True
            count = 0
            while rPos < len(W) and count < l and flag:
                curr = W.GetSymbol(lPos)
                if not curr.IsForbidden():
                    lc.append(curr)
                    count += 1
                    rPos += 1
                else:
                    flag = False

            if len(lc) == 0:
                lc = self.__alphabet.anyWord
            else:
                lc = Word(lc)
            if len(rc) == 0:
                rc = self.__alphabet.anyWord
            else:
                rc = Word(rc)

            sac = SaC(s,lc,rc)
            W.AddSAC(sac)

    """
    Input: A symbol and context (SAC)
    Output: A list of rules that match the SAC
    Purpose: This returns a list of rules that could potentially match a provided symbol and context. If there is an 
    exact rule match, then only that rule will be returned; otherwise; all possible partial matches are returned
    including the degree of mismatch. Typically done before calling the rule's Replace() function.
    """
    def GetRule(self, SAC):
        flag = False
        for i, sac in enumerate(self.__sacs):
            if sac == SAC:
                flag = True
                return self.__rules[i]

        if not flag:
            raise Exception("SaCLibrary.GetRule: No matching rule found for SaC " + SAC)
