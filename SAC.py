import math

from Symbol import Symbol
from Word import Word

UnitTest_SAC = False

"""
This class represents a symbol and context or a SAC.
"""
class SAC:
    """
    Input:
    - A symbol object (S)
    - A word object for the left context (LC)
    - A word object for the left context (RC)
    """
    def __init__(self, S, LC, RC):
        if type(S) is not Symbol:
            raise Exception("Type Error. SAC requires S to be a Symbol")
        if type(LC) is not Word:
            raise Exception("Type Error. SAC requires LC to be a Word")
        if type(RC) is not Word:
            raise Exception("Type Error. SAC requires RC to be a Word")
        self.__symbol = S
        self.__left = LC
        self.__right = RC
        self.__k = len(LC)
        self.__l = len(RC)

    def Match(self,other):
        error = 0
        if self.__symbol != other.symbol:
            error = math.inf
        else:
            error += self.__left.Match(other.self.left)
            error += self.__right.Match(other.self.right)

        return error

    def GetSymbol(self):
        return self.__symbol

    def GetLeftContext(self):
        return self.__left

    def GetRightContext(self):
        return self.__right

    def __eq__(self, other):
        return self.__symbol == other.GetSymbol() and self.__left == other.GetLeftContext() and self.__right == other.GetRightContext()

    def __str__(self):
        return self.__left + " < " + self.__symbol + " > " + self.__right

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

if UnitTest_SAC:
    print("Test 1 - Initialize and print a SAC, single character symbol and contexts")
    s1 = Symbol("A",0)
    s2 = Symbol("B",1)
    s3 = Symbol("C",2)

    lc = Word([s2,s1])
    rc = Word([s1,s3])

    a = SAC(s1, lc, rc)
    print(a + " " + str(len(lc)) + " " + str(len(rc)))


