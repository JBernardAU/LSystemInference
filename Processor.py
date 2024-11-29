from Analyzer import Analyzer
from GlobalSettings import *
import importlib

from LSystem import LSystem


class Processor:
    def __init__(self, Settings):
        self.mode = Settings[iSetting_Mode]
        LSystemFileName = Settings[iSetting_LSystemName]
        aiType = Settings[iSetting_AIType]
        self.contextMode = Settings[iSetting_ContextMode]

        # create the target L-system
        lSystemClass = getattr(importlib.import_module("LSystems." + LSystemFileName), LSystemFileName)
        self.lSystem_original = lSystemClass()
        self.lSystem_found = LSystem()
        self.lSystem_found.name = self.lSystem_original.name

        # create the AI
        #aiClass = getattr(importlib.import_module("AI." + aiType + "." + aiType), aiType)
        #self.ai = aiClass()
        self.lSystem_original.Display()

    # Inputs:
    # - A sequence of words

    def Execute(self):
        # Step 1 - Deduce an initial L-system from a sequence of words
        analyzer = Analyzer()
        words = self.lSystem_original.words
        if self.mode == "Inference":
            alphabet, predecessors = analyzer.InferAlphabetAndPredecessors(words, (0,0),list())
            self.lSystem_found.alphabet = alphabet
            self.lSystem_found.Display(True)

        elif self.mode == "Experimental":
            pass

        # Step 2 - Analyze L-system

        #


        return ""

