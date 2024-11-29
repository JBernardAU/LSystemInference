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
    def InferAlphabetAndPredecessors(self, W, CS, Identity):
        alphabet = list()
        predecessors = list()

        # for each word
        for w in W:
            # for each symbol in the word
            for s in w:
                # If it is not a known identity and the alphabet doesn't already contain the symbol (s)
                if s not in Identity and s not in alphabet:
                    alphabet.append(s)

        # add the identity symbols to the end
        alphabet += Identity
        print(alphabet)

        return alphabet, predecessors


