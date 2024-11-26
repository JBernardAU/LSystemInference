a = "ABA"
b = "ABABBBABA"

iPos = 0
leftContextSize = 2
rightContextSize = 2

while iPos < len(b):
    print(b[max(iPos-leftContextSize,0):iPos] + " < " + b[iPos] + " > " + b[iPos+1:iPos+1+rightContextSize])
    iPos += 1

