from LSystems.LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule
from ProductionRules.UnknownRule import UnknownRule
from Scanner import Scanner
from Utility import *
from GlobalSettings import *

UnitTest_LSystemExtended = False

class LSystemExtended(LSystem):
    def __init__(self):
        super().__init__()
        self.localizationMaps = list()
        self.parikhLY = None
        self.parikhLZ = None
        self.parikhGY = None
        self.parikhGZ = None
        self.lengths = None
        self.growths = None
        self.prefixFragment = ""
        self.suffixFragment = ""
        self.otherFragments = list()
        self.solved = False

    """
    Inputs: None
    Outputs: None
    This determines is an L-system has been solved. An L-system is solved when the min and max lengths for all SACs are equal.
    """
    def CheckIfSolved(self):
        iLength = 0
        self.solved = True
        while iLength < self.lengths and self.solved:
            self.solved = self.lengths[iLength][iMin] == self.lengths[iLength][iMax]
        if self.solved:
            scanner = Scanner()

    def SetMaxGrowth(self, iSAC, iSymbol, V):
        flag = False
        if V <= self.growths[iSAC][iSymbol][iMax]:
            self.growths[iSAC][iSymbol][iMax] = V
            flag = True
        return flag

    def SetMinGrowth(self, iSAC, iSymbol, V):
        flag = False
        if V >= self.growths[iSAC][iSymbol][iMin]:
            self.growths[iSAC][iSymbol][iMin] = V
            flag = True
        return flag

    def SetMaxLength(self, iSAC, V):
        flag = False
        if V <= self.lengths[iSAC][iMax]:
            self.lengths[iSAC][iMax] = V
            flag = True
        return flag

    def SetMinLength(self, iSAC, V):
        flag = False
        if V >= self.lengths[iSAC][iMin]:
            self.lengths[iSAC][iMin] = V
            flag = True
        return flag

    """
    Inputs: None
    Outputs: None
    This does a pre-analysis of the L-system to establish the most basic facts before starting the analysis.
    It also creates and initializes any necessary structures.
    """
    """
    TODO: BROKEN
    def PreAnalysis(self):
        print("Starting Pre-analysis")
        defaultMin = 0
        defaultMax = math.inf
        solutionFound = False
        solution = list()

        # create length and growth structures
        self.lengths = list()
        for iSac, sac in enumerate(self._sacs):
            self.lengths.append([defaultMin, defaultMax])

        self.growths = list()
        for sac in self._sacLibrary:
            growth = list()
            for s in self._alphabet:
                growth.append([defaultMin, defaultMax])
            self.growths.append(growth)

        # Create the Parikh vectors
        numSACs = len(self.sacs)
        numWords = len(self.words)
        numSymbols = len(self.alphabet)
        print("PARIKH MATRICES - GROWTH INITIALIZED")
        self.parikhGY = CreateMatrix(numSACs, numWords - 1)
        self.parikhGZ = CreateMatrix(numSymbols, numWords - 1)
        countsY = list()
        for iWord in range(1, len(self.words)):
            if iWord == 1:
                countsY = CountSACs(self.words[iWord - 1], self.sacs, self.forbidden)
            countsZ = CountSACs(self.words[iWord], self.sacs, self.forbidden)

            self.parikhGY[iWord - 1] = countsY
            self.parikhGZ[iWord - 1] = countsZ
            countsY = countsZ

        print("PARIKH MATRICES - LENGTH INITIALIZED")
        self.parikhLY = CreateMatrix(numSACs, numWords - 1)
        self.parikhLZ = CreateMatrix(1, numWords - 1)
        for iWord in range(1, len(self.words)):
            countsY = CountSACs(self.words[iWord - 1], self.sacs, self.forbidden)
            countsZ = [len(self.words[iWord])]

            self.parikhLY[iWord - 1] = countsY
            self.parikhLZ[iWord - 1] = countsZ

        print("CHECKING FOR A SOLUTION FROM PARIKH MATRICES") \
            #TODO: Filter out identities
        numEquations = len(self.sacs)
        if len(self.parikhLY[0]) >= numEquations:
            mY = CreateMatrix(numSACs, numEquations)
            mZ = CreateMatrix(1, numEquations)
            for iRow in range(numEquations):
                mZ[iRow][0] = self.parikhLZ[iRow][0]
                for iSac in range(numSACs):
                    mY[iRow][iSac] = self.parikhLY[iRow][iSac]
            aY = np.array(mY)
            aZ = np.array(mZ)
            parikhFlag = True
            try:
                aML = np.linalg.solve(aY, aZ)
                for iSac, sac in enumerate(self.sacs):
                    if math.fmod(aML[iSac][0], 1) == 0.0:
                        value = int(aML[iSac][0])
                        self.SetMinLength(iSac, value)
                        self.SetMaxLength(iSac, value)
                    else:
                        parikhFlag = False
            except:
                print("Matrix is not invertible.")
                parikhFlag = False

            if parikhFlag:
                solutionFound = True
        else:
            print("INSUFFICIENT ROWS - NO SOLUTION POSSIBLE")

        if solutionFound:
            print("*** SOLUTION FOUND ***")
            print(self.lengths)
        else:
            print("LOCALIZATION - INITIALIZATION")
            for iWord in range(1, len(self.words)):
                map = CreateMatrix(len(self.words[iWord]), len(self.words[iWord - 1]))
                self.localizationMaps.append(map)
                #DisplayMatrix(map)

            print("GROWTH PRE-ANALYSIS")
            # create length and growth initial structures

            # compute initial growths
            for iWord in range(1, len(self.words)):
                countsSACS = CountSACs(self.words[iWord - 1], self.sacs, self.forbidden)
                countsSymbols = [[x, self.words[iWord].count(x)] for x in set(self.words[iWord])]

                for iSac in range(len(self.growths)):
                    if not IsSACIdentity(self.sacs[iSac], self.identities):
                        sacCount = countsSACS[iSac]
                        for iSymbol, s in enumerate(self.alphabet):
                            for iCount in range(len(countsSymbols)):
                                if countsSymbols[iCount][0] == s:
                                    if (sacCount > 0):
                                        growthSbySAC = math.floor(countsSymbols[iCount][1] / sacCount)
                                        self.SetMaxGrowth(iSac, iSymbol, growthSbySAC)
                    else:
                        for iSymbol, s in enumerate(self.alphabet):
                            if s == self.sacs[iSac][iSACSymbol]:
                                self.SetMinGrowth(iSac, iSymbol, 1)
                                self.SetMaxGrowth(iSac, iSymbol, 1)
                            else:
                                self.SetMinGrowth(iSac, iSymbol, 0)
                                self.SetMaxGrowth(iSac, iSymbol, 0)

            # compute initial lengths
            for iSac, sac in enumerate(self.sacs):
                if not IsSACIdentity(sac, self.identities):
                    growths = self.growths[iSac]
                    minLength = 0
                    maxLength = 0
                    for iSymbol, s in enumerate(self.alphabet):
                        minLength += growths[iSymbol][iMin]
                        maxLength += growths[iSymbol][iMax]
                    self.SetMinLength(iSac, minLength)
                    self.SetMaxLength(iSac, maxLength)
                else:
                    self.SetMinLength(iSac, 1)
                    self.SetMaxLength(iSac, 1)

    def InitalizeFromLsystem(self, L, Name="Unnamed"):
        self._axiom = L.GetAxiom()
        self._alphabet = L.GetAlphabet()
        self._words = L.GetWords()
        self._sacLibrary = L.GetSACLibrary()
        #TODO: make this an option
        self._contextSize = L._contextSize
        self.InitializeFromSelf()
    """

    """
    TODO: BROKEN
    def InitializeFromSelf(self, Name="Unnamed"):
        #self.InitializeFromWords(self._words, self._identities, self._forbidden, Name)
    """

    """
    Inputs:
    Outputs:
    This initialization method should be called to initialize an L-system from a sequence of words (W)
    Typically, InitializeFromSelf() should be called to use the words stored in the L-system itself
    """
    """
    TODO: BROKEN
    def InitializeFromWords(self, W, Identities=None, Forbidden=None, Name="Unnamed"):
        # if not already named, then use the incoming name
        # also, if the incoming name is not the default value, then assume the intent is to rename the L-system
        if self._name == "" or Name != "Unnamed":
            self.name = Name

        # Step 2.
        # Identify the alphabet
        # Identify all SACs
        # Add a rule with no successor for every SAC
        for w in W:
            # for each symbol in the word
            for p, s in enumerate(w):
                # If it is not a known identity and the alphabet doesn't already contain the symbol (s)
                if s not in Identities and s not in self.alphabet:
                    self.alphabet.append(s)

                # get the symbol in context
                lc = GetLeftContext(w, p, self.contextSize[0], Forbidden)
                rc = GetRightContext(w, p, self.contextSize[1], Forbidden)

                if lc == "":
                    lc = anySymbol

                if rc == "":
                    rc = anySymbol

                sac = (s, lc, rc)
                if sac not in self.sacs:
                    self.sacs.append(sac)
                    self.rules.append(UnknownRule())

        # add the identity symbols to the end if not already there
        for s in self.identities:
            if s not in self.alphabet:
                self.AddIdentity(s)
    """
