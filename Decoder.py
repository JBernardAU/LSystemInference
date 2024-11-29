#This class is a super class that decodes a solution into an L-system
#It requires:
# 1. A list Rules formatted as duples. The duple is a predecessor (tuple) and a successor (string)
# 2.
class Decoder:
    def __init__(self, Rules, Words):
        self.rules = Rules
        self.words = Words

    # This resets the successors in the rules to prepare for decoding a new solution
    def Reset(self):
        for rule in self.rules:
            rule.successor = ""

    # Inputs:
    # - a set of lengths (L)
    # Outputs:
    # - a tuple of successors, number of correct lines, and errors on the incorrect line
    def ScanByLength(L):
        print("Decoder Scan() function must be overridden in a subclass.")




