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

        # this the master copy of the L-system to be analyzed
        self.lSystem_master = LSystem()
        self.lSystem_master.name = self.lSystem_original.name

        # create the AI
        #aiClass = getattr(importlib.import_module("AI." + aiType + "." + aiType), aiType)
        #self.ai = aiClass()
        self.lSystem_original.Display()

    # Inputs:
    # - A sequence of words

    def Execute(self):
        # Step 1 - Pre-Analyze L-system
        # In this step, an initial pass is done to establish the most basic of facts about the successors

        error = float("inf")
        tabooSolutions = list()

        while error > 0:
            # Step 2 - Project the L-system onto a copy excluding all identity symbols

            # Step 3 - Analyze the projected L-system

            # Step 4 - Search for a solution

            # Step 5 - If no solution found, add the solution to the taboo list

            # Step 6 - Backtrack


            error = 0
            pass



        if error > 0:
            print("No matching L-system was found. Displaying best candidates.")
        else:
            print("One or more L-systems found. Displaying all suitable L-systems found.")

        # Step N - Compare original and found if in experimental mode
        if self.mode == "Experimental":
            print("Comparing found L-systems with original L-system")

        return ""

