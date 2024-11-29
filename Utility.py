from GlobalSettings import *
import numpy as np

def GetSAC(W,P,J,K,F=None):
    s = W[P]
    lc = GetLeftContext(W,P,J,F)
    rc = GetRightContext(W,P,K,F)
    if lc == "":
        lc = anySymbol
    if rc == "":
        rc = anySymbol
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

def CreateMatrix(W,H,V=0):
    return [[V for x in range(W)] for y in range(H)]

def DisplayMatrix(M):
    print(np.matrix(M))

def CountSACs(W, SACs,F=None):
    result = [0] * len(SACs)
    lcs = 0
    rcs = 0
    for iSac, sac in enumerate(SACs):
        if sac[1] != anySymbol:
            lcs = len(sac[1])
        if sac[2] != anySymbol:
            rcs = len(sac[2])
        for i, w in enumerate(W):
            xSac = GetSAC(W,i,lcs,rcs,F)
            if xSac == sac:
                result[iSac] += 1

    return result

def PerformOperation(a, n):
    i = 0
    j = 0
    k = 0
    c = 0
    flag = 0
    m = 0
    pro = 0

    # Performing elementary operations
    for i in range(n):
        if (a[i][i] == 0):

            c = 1
            while ((i + c) < n and a[i + c][i] == 0):
                c += 1
            if ((i + c) == n):

                flag = 1
                break

            j = i
            for k in range(1 + n):

                temp = a[j][k]
                a[j][k] = a[j+c][k]
                a[j+c][k] = temp

        for j in range(n):

            # Excluding all i == j
            if (i != j):
                # Converting Matrix to reduced row
                # echelon form(diagonal matrix)
                p = a[j][i] / a[i][i]

                k = 0
                for k in range(n + 1):
                    a[j][k] = a[j][k] - (a[i][k]) * p

    return flag
