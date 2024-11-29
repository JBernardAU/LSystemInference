from LSystem import LSystem
from ProductionRules.DeterministicRule import DeterministicRule
from ProductionRules.UnknownRule import UnknownRule
from Utility import *
from GlobalSettings import *
UnitTest_LSystemExtended = False

class LSystemExtended(LSystem):
    def __init__(self):
        super().__init__()

    # Inputs:
    # - None
    # Outputs
    # - None
    # Function:
    # Adds the functionality that allows an L-system to be analyzed
    def ExtendLSystem(self):
        pass

    def InitalizeFromSelf(self, Name="Unnamed"):
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
        self.Display()
        pass


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