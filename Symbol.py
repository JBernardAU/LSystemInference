from GlobalSettings import multicharacterIndicator

UnitTest_Symbol = False

class Symbol:
    def __init__(self, S, Id, IsIdentity=False, IsForbidden=False, Multicharacter=False):
        """
        :type S: string
        :type Id: int
        :type IsIdentity: Boolean         :type Multicharacter: Boolean
        """
        self.__character = S
        self.__id = Id  # assigned by the alphabet
        self.__isIdentity = IsIdentity
        self.__multicharacter = Multicharacter
        self.__isForbidden = IsForbidden
        if len(self.__character) > 1:
            self.__multicharacter = True

    def GetCharacter(self):
        return self.__character

    def GetID(self):
        return self.__id

    def GetIsIdentity(self):
        return self.__isIdentity

    def GetIsForbidden(self):
        return self.__isForbidden

    def __eq__(self, other):
        if type(other) == str:
            return self.__character == other
        else:
            return self.__id == other.GetID()

    def __len__(self):
        if not self.__multicharacter:
            return len(self.__character)
        else:
            return len(self.__character + multicharacterIndicator)

    def __str__(self):
        if not self.__multicharacter:
            return self.__character
        else:
            return self.__character + multicharacterIndicator

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
