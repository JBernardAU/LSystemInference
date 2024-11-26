from GlobalSettings import *
UnitTest = False


# Two properties
# Predecessor is a tuple consisting of symbol (S), left context (L) and right context (R)
# Successor is the replacement string
class DeterministicRule:
    def __init__(self, Pred, Succ):
        self.predecessor = [Pred]
        self.successor = [Succ]

    def Display(self):
        for iSucc, succ in enumerate(self.successor):
            print(self.predecessor[iSucc][iLeft] + " < " + self.predecessor[iSucc][iSymbol] + " > " + + self.predecessor[iSucc][iRight] + " -> " + succ)

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
        while (iSucc < len(self.successor)) and not isMatch:
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
            #check left symbols to left context
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
            if isMatch:
                result = self.successor[iSucc]
            else:
                iSucc += 1

        return result

if UnitTest:
    r = DeterministicRule(("A","BB","*"),"AAA")
    r.Add(("A","*","B"),"ABBA")
    r.Add(("A","*","*"),"ABA")

    word = "ABABBBABA"
    iPos = 0
    leftContextSize = 2
    rightContextSize = 2
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



