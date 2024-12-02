from WordsAndSymbols.Symbol import Symbol
UnitTest_Word = False

class Word:
    """
    Properties:
    - A list of Symbol objects
    """
    _symbols: list[Symbol]

    def __init__(self, Symbols, Ids=None, SACs=None, SACIDs=None):
        """
        :type Symbols: list[Symbol]
        """
        self._symbols = Symbols
        self._ids = Ids
        self._parameters = None
        self._sacs = SACs
        self._sacIds = SACIDs
        self._sacCounts = None

    def __len__(self):
        return len(self._symbols)

    def __eq__(self, other):
        iW = 0
        flag = True
        if self is other:
            return True
        elif len(self) == len(other):
            while iW < len(self._symbols) and flag:
                flag = self._symbols[iW] == other.GetSymbol(iW)
                iW += 1
        return flag

    def __add__(self, other):
        for i, s in enumerate(other):
            self._symbols.append(s)

    def __str__(self):
        result = ""
        for s in self._symbols:
            result += str(s)
        return result

    def __iter__(self):
        return iter(self._symbols)

    """
    Inputs: A word (W)
    Outputs: None. Modifies self.
    This appends one word to another. Equivalent to += for strings. Note, this destroys the extensions for self.
    Parameters in particular should be saved before calling Append().
    """
    def Append(self, W):
        if issubclass(type(W),Word) and len(W) > 0:
            self.Deextend()
        for i, s in enumerate(W):
            self._symbols.append(s)


    def GetSymbol(self, I):
        return self._symbols[I]

    def GetSymbolID(self, I):
        return self._ids[I]

    def GetSAC(self, I):
        return self._sacs[I]

    def GetSACID(self, I):
        return self._sacIds[I]

    def AddSymbol(self, S):
        self._symbols.append(S)

    def AddSAC(self, SAC):
        self._sacs.append(SAC)

    def Parametrize(self):
        self._parameters = list()

    def AddParameters(self, P):
        self.Parametrize()
        pass

    def Extend(self):
        self._sacs = list()
        self._sacCounts = list()

    def Deextend(self):
        self._sacs = None
        self._sacIds = None
        self._sacCounts = None
        self._parameters = None

    def IsExtended(self):
        if self._sacs is None:
            return False
        else:
            return True

if UnitTest_Word:
    from Symbol import Symbol

    print("Test 1 - Initialize and display a word")
    a = Symbol("A",0,True)
    b = Symbol("B",1, True)
    cc = Symbol("CC", 2)
    dd = Symbol("DD",3)
    l = [a,b,cc,dd]
    w = Word(l)
    print(w)

    print("\nTest 2 - Are two words equal? Yes")
    a2 = Symbol("A",0,True)
    b2 = Symbol("B",1, True)
    cc2 = Symbol("CC", 2)
    dd2 = Symbol("DD",3)
    l2 = [a2,b2,cc2,dd2]
    w2 = Word(l2)
    print(w + " == " + w2 + "? " +  str(w == w2))

    print("\nTest 3 - Are two words equal? No")
    a3 = Symbol("A",0,True)
    b3 = Symbol("B",1, True)
    cc3 = Symbol("CC", 2)
    dd3 = Symbol("DD",3)
    l3 = [b2,a3,cc2,dd2]
    w3 = Word(l3)
    print(w + " == " + w3 + "? " + str(w == w3))

