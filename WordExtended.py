from GlobalSettings import anySymbol
from Word import Word

UnitTest_WordExtended = False

"""
This class extends Word by adding additional properties to support the analytical processes, while
the base class is intended for visualization purposes only. This class requires additional memory.
"""
class WordExtended(Word):
    def __init__(self, S):
        super().__init__(S)

        for iPos in enumerate(self.__symbols):
            self.SetSACatPos(iPos, K, L, Identities, Forbidden)

    def GetSAC(self,P):
        return self.__sacs[P]

    def Extend(self):
        pass

    """
    Inputs:
    - A position in the word (P)
    - A left context size (K)
    - A right context size (L)
    - A list of identity SACs (I)
    - A list of forbidden SACs (F). Context may not pass through a forbidden SAC.
    """
    def SetSACatPos(self, P, K, L, I, F):
        s = self.__symbols[P]

        # scan left

        lc = GetLeftContext(W, P, J, F)
        rc = GetRightContext(W, P, K, F)
        if lc == "":
            lc = anySymbol
        if rc == "":
            rc = anySymbol
        return s, lc, rc


if UnitTest_WordExtended:
    from Symbol import Symbol
    from SAC import SAC

    a = Symbol("A",0,Multicharacter=True)
    b = Symbol("B",1, Multicharacter=True)
    cc = Symbol("CC", 2)
    dd = Symbol("DD",3)
    any = Symbol(anySymbol,4)
    wAny = Word(any)
    wA = Word(a)

    aSac = SAC(a,wAny, wAny)
    b1Sac = SAC(b,wAny, wAny)
    b2Sac = SAC(b,wA, wA)
    ccSac = SAC(cc,wAny, wAny)
    ddSac = SAC(dd,wAny, wAny)
    sacs = [aSac, b1Sac, b2Sac, ccSac, ddSac]

    print("Test 1 - Initialize and display an extended word")
    l = [a,b,a,cc,a,dd,b,a,b,a]
    w = WordExtended(l, sacs)
    print(w)

