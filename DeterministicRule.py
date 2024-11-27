from GlobalSettings import *
UnitTest_DeterministicRule = False


# Two properties
# Predecessor is a tuple consisting of symbol (S), left context (L) and right context (R)
# Successor is the replacement string
class DeterministicRule:
    def __init__(self, Pred, Succ):
        self.predecessor = Pred
        self.successor = Succ
        maxL = 0
        maxR = 0
        for pred in self.predecessor:
            if pred[iLeft] != anySymbol and len(pred[iLeft]) > maxL:
                maxL = int(len(pred[iLeft]))
            if pred[iRight] != anySymbol and len(pred[iRight]) > maxR:
                maxR = int(len(pred[iRight]))
        self.contextSize = (maxL,maxR)

    def Display(self):
        for iSucc, succ in enumerate(self.successor):
            print(self.predecessor[iSucc][iLeft] + " < " + self.predecessor[iSucc][iSymbol] + " > " + self.predecessor[iSucc][iRight] + " -> " + succ)

    def GetLeftContextSize(self):
        return self.contextSize[0]

    def GetRightContextSize(self):
        return self.contextSize[1]

    def Add(self,Pred,Succ):
        self.predecessor.append(Pred)
        self.successor.append(Succ)

    def Replace(self, S, L, R):
        result = ""
        if identityOnNoMatch:
            result = S
        #conditions
        # symbols must match
        iSucc = 0
        isMatch = False
        isExactMatch = False
        while (iSucc < len(self.successor)) and not isExactMatch:
            symbolMatch = (S == self.predecessor[iSucc][iSymbol])

            #check left symbols to left context
            leftMatch = (self.predecessor[iSucc][iLeft] == anySymbol) # if the predecessor left context is any symbol, then it automatically matches
            if not leftMatch:
                iPos1 = len(L)-1 # start from the right side of the context and move left
                iPos2 = len(self.predecessor[iSucc][iLeft]) - 1
                leftMatch = True # initialize to true
                while iPos1 >= 0 and iPos2 >= 0 and leftMatch:
                    leftMatch = leftMatch and (self.predecessor[iSucc][iLeft][iPos2] == L[iPos1])
                    iPos1 -= 1
                    iPos2 -= 1

            #check right symbols to right context
            rightMatch = (self.predecessor[iSucc][iRight] == anySymbol) # if the predecessor left context is any symbol, then it automatically matches
            if not rightMatch:
                iPos1 = 0 # start from the left side of the context and move right
                iPos2 = 0 # start from the left side of the context and move right
                rightMatch = True # initialize to true
                while iPos1 < len(R) and iPos2 < len(self.predecessor[iSucc][iRight]) and rightMatch:
                    rightMatch = rightMatch and (self.predecessor[iSucc][iRight][iPos2] == R[iPos1])
                    iPos1 += 1
                    iPos2 += 1

            isMatch = symbolMatch and leftMatch and rightMatch
            bool1 = self.predecessor[iSucc][iLeft] == anySymbol
            bool2 = self.predecessor[iSucc][iRight] == anySymbol
            bool3 = len(self.predecessor[iSucc][iLeft]) == len(L)
            bool4 = len(self.predecessor[iSucc][iRight]) == len(R)
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
                result = self.successor[iSucc]

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



