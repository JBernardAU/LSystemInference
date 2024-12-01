from Symbol import Symbol

UnitTest_Alphabet = False

class Alphabet:
    """
    Inputs:
    - Symbols - an optional list of strings.
    - Identities - an optional list of strings that have an identity production
    - Forbidden - an optional list of strings that have that block context
    """
    def __init__(self, Symbols=None, Identities=None, Forbidden=None):
        self.__symbols = list()
        self.__ids = list()
        if Symbols is not None:
            for s in Symbols:
                self.Add(s)
            for s in Identities:
                isForbidden = s in Forbidden
                self.Add(s,IsIdentity=True,IsForbidden=isForbidden)

    def __len__(self):
        return len(self.__symbols)

    def __str__(self):
        sep = ""
        for i, s in enumerate(self.__symbols):
            print(sep + s + "[" + str(self.__ids[i]) + "]", end="" )
            sep = ", "
        print()

    def __iter__(self):
        return iter(self.__symbols)

    """
    Input: - a symbol (S) as a string
    Output - the corresponding symbol from the alphabet
    """
    def FindSymbol(self, S):
        for i, s in enumerate(self.__symbols):
            if s == S:
                return s

    def FindSymbolID(self, S):
        for i, s in enumerate(self.__symbols):
            if s == S:
                return self.__ids[i]

    def GetSymbol(self, I):
        return self.__symbols[I]


    def GetID(self, I):
        return self.__ids[I]

    def Add(self, S, IsIdentity=False, IsForbidden=False):
        id = len(self.__symbols)
        self.__symbols.append(Symbol(S, id, IsIdentity, IsForbidden))
        self.__ids.append(id)



    """
    Input: a string
    Output: a list of Symbols
    """
    def ConvertString2List(self, S) -> list[Symbol]:
        """
        :rtype: list(Symbol)
        """
        x = list()
        for s in S:
            x.append(self.FindSymbol(s))
        return x

    """
    Input: a string
    Output: a list of Symbol IDs
    """
    def ConvertString2SymbolIDs(self, S) -> list[int]:
        """
        :rtype: list(int)
        """
        x = list()
        for s in S:
            x.append(self.FindSymbolID(s))
        return x

if UnitTest_Alphabet:
    import Symbol

    a = Alphabet()
    a.Add("X")
    a.Add("Y")
    a.Add("F", IsIdentity=True, IsForbidden=True)
    a.Add("+", IsIdentity=True, IsForbidden=True)
    a.Add("-", IsIdentity=True, IsForbidden=True)