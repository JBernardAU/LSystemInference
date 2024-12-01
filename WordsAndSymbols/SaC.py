import math

import GlobalSettings
from WordsAndSymbols.SpecialSymbols.AnyWord import AnyWord
from WordsAndSymbols.SpecialSymbols.EmptyWord import EmptyWord
from WordsAndSymbols.Symbol import Symbol
from WordsAndSymbols.Word import Word

UnitTest_SAC = False

"""
This class represents a symbol and context or a SAC.
"""
class SaC:
    """
    Input:
    - A symbol object (S)
    - A word object for the left context (LC)
    - A word object for the left context (RC)
    """
    def __init__(self, S, LC, RC):
        if not issubclass(type(S),Symbol):
            raise Exception("SaC(): Type Error - SAC argument is not a subclass of Symbol")
        if not issubclass(type(LC),Word):
            raise Exception("SaC(): Type Error - LC argument is not a subclass of Word")
        if not issubclass(type(LC),Word):
            raise Exception("SaC(): Type Error - RC argument is not a subclass of Word")
        self.__symbol = S
        self.__left = LC
        self.__right = RC
        if not issubclass(type(self.__left),AnyWord):
            self.__k = len(LC)
        else:
            self.__k = 0
        if not issubclass(type(self.__right),AnyWord):
            self.__l = len(RC)
        else:
            self.__l = 0

    def PartialMatch(self,other):
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

    a = SaC(s1, lc, rc)
    print(a + " " + str(len(lc)) + " " + str(len(rc)))


