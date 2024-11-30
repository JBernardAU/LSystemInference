from SAC import SAC

class SACAlphabet:
    __sacs: list[SAC]
    __ids: list[int]

    def __init__(self):
        self.__sacs = list()
        self.__ids = list()

    def __len__(self):
        return len(self.__sacs)

    def __str__(self):
        for s in self.__sacs:
            print(s)

    def __iter__(self):
        return iter(self.__sacs)

    def GetSAC(self, I):
        return self.__sacs[I]

    def GetID(self, I):
        return self.__ids[I]

    def GetSACID(self, SAC):
        for i, sac in self.__sacs:
            if sac == SAC:
                return self.__ids[i]

    def Add(self, S, LC, RC):
        id = len(self.__sacs)
        self.__sacs.append(SAC(S, LC, RC))
        self.__ids.append(id)
