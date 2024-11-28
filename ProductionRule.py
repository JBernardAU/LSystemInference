from GlobalSettings import *
from Utility import Filter

class ProductionRule():
    def __init__(self, Pred, Succ):
        self.predecessors = Pred
        self.successors = Succ
        maxL = 0
        maxR = 0
        for pred in self.predecessors:
            if pred[iLeft] != anySymbol and len(pred[iLeft]) > maxL:
                maxL = int(len(pred[iLeft]))
            if pred[iRight] != anySymbol and len(pred[iRight]) > maxR:
                maxR = int(len(pred[iRight]))
        self.contextSize = (maxL,maxR)

    def Display(self):
        for iSucc, succ in enumerate(self.successors):
            print(self.predecessors[iSucc][iLeft] + " < " + self.predecessors[iSucc][iSymbol] + " > " +
                  self.predecessors[iSucc][iRight] + " -> " + succ)

    def GetLeftContextSize(self):
        return self.contextSize[0]

    def GetRightContextSize(self):
        return self.contextSize[1]

    def Filter(self, A):
        for iSucc, succ in enumerate(self.successors):
            self.successors[iSucc] = Filter(succ, A)
            symbol = self.predecessors[iSucc][iSymbol]
            left = Filter(self.predecessors[iSucc][iLeft],A)
            right = Filter(self.predecessors[iSucc][iRight],A)
            self.predecessors[iSucc] = (symbol, left, right)

    def Replace(self, S, L, R):
        print("ProductionRule.Replace() must be overridden in a subclass")
