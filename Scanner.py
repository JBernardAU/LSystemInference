class Scanner:
    def __init__(self):
        pass

    """
    Input: 
    - A sequences of words (Words)
    - A sequence of symbols and context (SACs)
    - A sequence of lengths (Solution). Must be in the same order as the SACs list
    Output:
    - A list of successors in SAC order
    - An error value
    """
    def DecodeLengths(self, Words, SACs, Lengths):
        for iWord, w in enumerate(Words):
            for iPos, s in enumerate(w):
                pass
