from lib2to3.fixes.fix_next import is_subtree

from GlobalSettings import *

class DeterministicRule:
    def __init__(self, S, L, R, Succ):
        self.symbol = S
        self.left = []
        self.right = []
        self.successor = []
        self.Add(L,R,Succ)

    def Display(self):
        for iSucc in enumerate(self.successor):
            print(self.left[iSucc] + " < " + self.symbol + " > " + self.right[iSucc] + " -> " + self.successor[iSucc])

    def Add(self,L,R,Succ):
        self.left.append(L)
        self.right.append(R)
        self.successor.append(Succ)

    def Replace(self, S, L, R):
        result = ""
        if identityOnNoMatch:
            result = S
        #conditions
        # symbols must match
        iSucc = 0
        isMatch = False
        while (iSucc < len(self.successor)) and not isMatch:
            symbolMatch = (S == self.symbol)
            leftMatch = (L == self.left) or (L == emptyString)
            rightMatch = (R == self.right) or (R == emptyString)
            isMatch = symbolMatch and leftMatch and rightMatch
            iSucc += 1

        return result