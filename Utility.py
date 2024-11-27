from GlobalSettings import emptySymbol


# Given a string (S), a position in that string (P), and a left context size (N), return the left context
def GetLeftContext(S,P,N):
    result = S[max(P - N, 0):P].rjust(N, emptySymbol)
    return result

# Given a string (S), a position in that string (P), and a left context size (N), return the right context
def GetRightContext(S,P,N):
    result = S[P+1:P+1+N].ljust(N, emptySymbol)
    return result
