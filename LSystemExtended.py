from LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule
from ProductionRules.UnknownRule import UnknownRule
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
        self.lengths = list()
        self.growths = list()
        self.prefixFragment = ""
        self.suffixFragment = ""
        self.otherFragments = list()

    """
    Inputs: None
    Outputs: None
    This does a pre-analysis of the L-system to establish the most basic facts before starting the analysis.
    It also creates and initializes any necessary structures.
    """
    def PreAnalysis(self):
        print("Starting Pre-analysis")

        # Step 1. create localization maps
        for iWord in range(1,len(self.words)):
            print("LOCALIZATION MAP INITIALIZED")
            map = CreateMatrix(len(self.words[iWord]), len(self.words[iWord-1]))
            self.localizationMaps.append(map)
            #DisplayMatrix(map)

        # Create the Parikh vectors
        numSACs = len(self.sacs)
        numWords = len(self.words)
        numSymbols = len(self.alphabet)
        print("PARIKH MATRICES - GROWTH INITIALIZED")
        self.parikhGY = CreateMatrix(numSACs,numWords-1)
        self.parikhGZ = CreateMatrix(numSymbols,numWords-1)
        countsY = list()
        for iWord in range(1,len(self.words)):
            if iWord == 1:
                countsY = CountSACs(self.words[iWord-1], self.sacs, self.forbidden)
            countsZ = CountSACs(self.words[iWord], self.sacs, self.forbidden)

            self.parikhGY[iWord-1] = countsY
            self.parikhGZ[iWord-1] = countsZ
            countsY = countsZ

        print("PARIKH MATRICES - LENGTH INITIALIZED")
        self.parikhLY = CreateMatrix(numSACs,numWords-1)
        self.parikhLZ = CreateMatrix(1,numWords-1)
        for iWord in range(1,len(self.words)):
            countsY = CountSACs(self.words[iWord-1], self.sacs, self.forbidden)
            countsZ = [len(self.words[iWord])]

            self.parikhLY[iWord-1] = countsY
            self.parikhLZ[iWord-1] = countsZ

        DisplayMatrix(self.parikhLY)
        DisplayMatrix(self.parikhLZ)

        """
        import numpy as np
        a = np.array([[2, 1], [8, 19]])
        b = np.array([9, 81])
        x = np.linalg.solve(a, b)
        print(x)
        """
        print("GROWTH PRE-ANALYSIS")
        counts1 = list()
        for iWord in range(1,len(self.words)):
            countsSACS = CountSACs(self.words[iWord - 1], self.sacs, self.forbidden)
            countsSymbols = [[x, self.words[iWord].count(x)] for x in set(self.words[iWord])]

            for sac in self.sacs:


            print(counts1)
            print(counts2)
            counts1 = counts2

        pass




    def InitalizeFromLsystem(self, L, Name="Unnamed"):
        self.axiom = L.axiom
        self.alphabet = L.alphabet
        self.identities = L.identities
        self.forbidden = L.forbidden
        self.words = L.words
        #TODO: make this an option
        self.contextSize = L.contextSize
        self.InitializeFromSelf()

    def InitializeFromSelf(self, Name="Unnamed"):
        self.InitializeFromWords(self.words, self.identities, self.forbidden, Name)

    # This initialization method should be called to initialize an L-system from a sequence of words (W)
    # Typically, InitializeFromSelf() should be called to use the words stored in the L-system itself
    def InitializeFromWords(self, W, Identities=None, Forbidden=None, Name="Unnamed"):
        # if not already named, then use the incoming name
        # also, if the incoming name is not the default value, then assume the intent is to rename the L-system
        if self.name == "" or Name != "Unnamed":
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
                lc = GetLeftContext(w,p,self.contextSize[0],Forbidden)
                rc = GetRightContext(w,p,self.contextSize[1],Forbidden)

                if lc == "":
                    lc = anySymbol

                if rc == "":
                    rc = anySymbol

                sac = (s, lc , rc)
                if sac not in self.sacs:
                    self.sacs.append(sac)
                    self.rules.append(UnknownRule())

        # add the identity symbols to the end
        self.alphabet += self.identities

if UnitTest_LSystemExtended:
    l = LSystemExtended()
    l.Initialize("A+B-A", ["A","B"])

    # add rules
    # For symbol A
    predecessors = [("A","*","*")]
    successors = ["A+B-A"]
    l.AddRules(DeterministicRule(predecessors,successors))

    # For symbol B
    predecessors = [("B","*","*")]
    successors = ["[B-B+B]"]
    l.AddRules(DeterministicRule(predecessors, successors))

    # For identities
    l.AddIdentity("+")
    l.AddIdentity("-")
    l.AddIdentity("[")
    l.AddIdentity("]")

    l.IterateN(l.axiom, 3)
    l.Display()

    a2 = ["A","B","+"]
    l2 = l.Project(a2)
    l2.Display()