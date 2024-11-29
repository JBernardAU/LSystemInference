from Utility import GetLeftContext, GetRightContext, DisplaySAC


class Analyzer:
    # Inputs:
    # - none
    def __init__(self):
        pass

    # Inputs:
    # - A sequence of words (W)
    # - A left and right context size (CS). Duple (left, right)
    # - An identity alphabet
    # Outputs:
    # - An alphabet
    # - All possible predecessors
    def LSystemFromWords(self, L):
        alphabet = list()
        predecessors = list()

        # for each word

        L.alphabet = alphabet