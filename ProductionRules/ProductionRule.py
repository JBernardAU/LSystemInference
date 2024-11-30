from GlobalSettings import *

class ProductionRule():
    def __init__(self, Succ):
        self.successors = Succ
        """
        DEPRECATED
        maxL = 0
        maxR = 0
        for pred in self.predecessors:
            if pred[iLeft] != anySymbol and len(pred[iLeft]) > maxL:
                maxL = int(len(pred[iLeft]))
            if pred[iRight] != anySymbol and len(pred[iRight]) > maxR:
                maxR = int(len(pred[iRight]))
        self.contextSize = (maxL,maxR)
        """

    def Display(self, SAC):
        for succ in self.successors:
            if succ is not None:
                print(SAC[iSACLeft] + " < " + SAC[iSACSymbol] + " > " + SAC[iSACRight] + " -> " + succ)
            else:
                print(SAC[iSACLeft] + " < " + SAC[iSACSymbol] + " > " + SAC[iSACRight] + " -> ???")


    """
    DEPRECATED
    def GetLeftContextSize(self):
        return self.contextSize[0]
    """

    """
    DEPRECATED
    def GetRightContextSize(self):
        return self.contextSize[1]
    """

    """
    Input: An alphabet (A)
    Output: None
    This function projects a rule onto a new alphabet 
    """
    def Project(self, A):
        for iSucc, succ in enumerate(self.successors):
            self.successors[iSucc] = Filter(succ, A)

    def Replace(self):
        print("ProductionRule.Replace() must be overridden in a subclass")