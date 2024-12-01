import math

from ProductionRules.ProductionRule import ProductionRule
from WordsAndSymbols.SaC import SaC

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

    def __str__(self):
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
    """
    def ExtendWord(self, W, k, l):
        for i, s in enumerate(W):
            lc = list()
            rc = list()
            # scan left

            # scan right

            pass

        pass
