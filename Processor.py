from GlobalSettings import *
import importlib
from LSystems.LSystemExtended import LSystemExtended


class Processor:
    def __init__(self, Settings):
        self.mode = Settings[iSetting_Mode]
        LSystemFileName = Settings[iSetting_LSystemName]
        aiType = Settings[iSetting_AIType]
        self.contextMode = Settings[iSetting_ContextMode]

        if self.mode == "Experimental":
            # load the original L-system
            lSystemClass = getattr(importlib.import_module("LSystems." + LSystemFileName), LSystemFileName)
            self.lSystem_original = lSystemClass()
            print("Experimental mode activated. This is the original L-system.")
            self.lSystem_original.Display()
            self.lSystem_master = LSystemExtended()
            self.lSystem_master.InitalizeFromLsystem(self.lSystem_original, "Unknown L-system")
            print("*****************************************")

        # this the master copy of the L-system to be analyzed
        # a master copy is needed as this will undergo projections and backtracking
        # so it is necessary to be able to return to the original
        if self.mode == "Inference":
            # load the unknown L-system
            lSystemClass = getattr(importlib.import_module("LSystems." + LSystemFileName), LSystemFileName)
            self.lSystem_master = lSystemClass()
            print("Inference mode activated. ", end="")

        print("Attempting to find the following L-system.")
        self.lSystem_master.Display()

    # Inputs:
    # - A sequence of words

    def Execute(self):
        # Step 1 - Pre-Analyze L-system
        # In this step, an initial pass is done to establish the most basic of facts about the successors
        # And create the necessary structures to do the analysis
        self.lSystem_master.PreAnalysis()
        self.lSystem_master.CheckIfSolved()

        error = float("inf")
        tabooSolutions = list()
        if self.lSystem_master == True:
            error = 0

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

