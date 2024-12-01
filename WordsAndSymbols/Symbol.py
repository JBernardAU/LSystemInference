from GlobalSettings import multicharacterIndicator

UnitTest_Symbol = False

class Symbol:
    def __init__(self, S, Id, IsIdentity=False, IsForbidden=False, Multicharacter=False):
        """
        :type S: string
        :type Id: int
        :type IsIdentity: Boolean         :type Multicharacter: Boolean
        """
        self._character = S
        self._id = Id  # assigned by the alphabet
        self._isIdentity = IsIdentity
        self._multicharacter = Multicharacter
        self._isForbidden = IsForbidden
        if len(self._character) > 1:
            self._multicharacter = True

    def GetCharacter(self):
        return self._character

    def GetID(self):
        return self._id

    def GetIsIdentity(self):
        return self._isIdentity

    def GetIsForbidden(self):
        return self._isForbidden

    def __eq__(self, other):
        if type(other) == str:
            return self._character == other
        else:
            return self._id == other.GetID()

    def __len__(self):
        if not self._multicharacter:
            return len(self._character)
        else:
            return len(self._character + multicharacterIndicator)

    def __str__(self):
        if not self._multicharacter:
            return self._character
        else:
            return self._character + multicharacterIndicator

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

if UnitTest_Symbol:
    print("Test 1 - Single character, print without newlines")
    a = Symbol("A",0)
    print(a, end="")

    print("\nTest 2 - Single character, print with newline")
    b = Symbol("B",1)
    print(b)

    print("\nTest 3 - Multiple character, print without newline")
    cc = Symbol("CC",2)
    print(cc, end="")

    print("\nTest 4 - Single character, print with newline")
    dd = Symbol("DD",3)
    print(dd)

    print("Test 5 - Single character as multicharacter, print without newlines")
    a = Symbol("A",0, False, True)
    print(a, end="")

    print("\nTest 6 -Single character as multicharacter, print with newline")
    b = Symbol("B",1, False, True)
    print(b,)

    print("\nTest 7 - Two Single character are equal")
    a1 = Symbol("A", 0)
    a2 = Symbol("A", 0)
    print(a1 == a2)

    print("\nTest 8 - Two Multi character are equal")
    a1 = Symbol("BB", 1)
    a2 = Symbol("BB", 1)
    print(a1 == a2)

    print("\nTest 8 - Two Multi character are equal? No")
    a1 = Symbol("BB", 1)
    a2 = Symbol("CC", 2)
    print(a1 == a2)
