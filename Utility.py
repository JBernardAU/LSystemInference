from GlobalSettings import *


def GetSAC(W,P,J,K,F=None):
    s = W[P]
    lc = GetLeftContext(W,P,J,F)
    rc = GetRightContext(W,P,J,F)
    return s,lc,rc

# Given a word (W), a position in that string (P), and a left context size (J), return the left context
# Optionally takes a list of forbidden symbols (F). Context may not pass any forbidden symbol.
def GetLeftContext(W, P, J, F=None):
    result = W[max(P - J, 0):P]

    # check to see if the context passes any forbidden symbol, and trim as needed
    if F is not None:
        # TODO: convert this to be a formula using p and length of result
        enumResult = tuple(enumerate(result))
        for p, s in reversed(enumResult):
            if s in F:
                # forbidden symbol found, trim the context
                result = result[p+1:]
                pass

    return result.rjust(J, emptySymbol)

# Given a word (W), a position in that string (P), and a right context size (K), return the right context
# Optionally takes a list of forbidden symbols (F). Context may not pass any forbidden symbol.
def GetRightContext(W, P, K, F=None):
    result = W[P+1:P + 1 + K]

    # check to see if the context passes any forbidden symbol, and trim as needed
    if F is not None:
        for p, s in enumerate(result):
            if s in F:
                # forbidden symbol found, trim the context
                result = result[0:p]

    return result.ljust(K, emptySymbol)

# Filters a word (W) based on alphabet (A)
def Filter(W, A):
    return W.translate({ord(s): '' for s in A})

# Since it is done so often, this display a symbol with the left and right context
def DisplaySAC(SIC, NewLine=True):
    if NewLine:
        print(SIC[1] + " < " + SIC[0] + " > " + SIC[2])
    else:
        print(SIC[1] + " < " + SIC[0] + " > " + SIC[2], end="")

def PredecessorFromSAC(SAC):
    # use the SAC symbols, unless the left/right context is empty, in which case use "*" (or whatever any symbol is set to)
    predecessor = (SAC[iSymbol],SAC[iLeft].rjust(1,anySymbol),SAC[iRight].ljust(1,anySymbol))
    return predecessor