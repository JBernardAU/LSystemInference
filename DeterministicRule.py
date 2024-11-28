from GlobalSettings import *
from ProductionRule import ProductionRule

UnitTest_DeterministicRule = False


# Two properties
# Predecessor is a tuple consisting of symbol (S), left context (L) and right context (R)
# Successor is the replacement string
class DeterministicRule(ProductionRule):
    def __init__(self, Pred, Succ):
        super().__init__(Pred,Succ)

    def Replace(self, S, L, R):
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
            """
            if UnitTest:
                print("self.predecessor[iSucc][iLeft] == anySymbol => " + str(bool1))
                print("self.predecessor[iSucc][iRight] == anySymbol => " + str(bool2))
                print("len(self.predecessor[iSucc][iLeft]) == len(L) => " + str(bool3))
                print("len(self.predecessor[iSucc][iLeft]) == len(L) => " + str(bool4))
                print(bool5)
            """

            isExactMatch = isMatch and ((bool1 or bool3) and (bool2 or bool4))

            if isExactMatch or isMatch:
                result = self.successors[iSucc]

            iSucc += 1

        return result

if UnitTest_DeterministicRule:
    predecessors = [("A","BB","*"),("A","*","B"),("A","*","*")]
    successors = ["AAA","ABBA","ABA"]
    r = DeterministicRule(predecessors,successors)

    word = "ABABBBABA"
    iPos = 0
    leftContextSize = r.contextSize[0]
    rightContextSize = r.contextSize[1]
    result = ""
    while iPos < len(word):
        S = word[iPos]
        L = word[max(iPos-leftContextSize,0):iPos]
        R = word[iPos+1:iPos+1+rightContextSize]
        L = L.rjust(leftContextSize, emptySymbol)
        R = R.ljust(rightContextSize, emptySymbol)

        print(L + " < " + S + " > " + R)
        result += r.Replace(S,L,R) + "|"
        iPos += 1

    print(result)



