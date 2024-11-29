from GlobalSettings import *
import importlib

class Processor:
    def __init__(self, Settings):
        self.LSystemFileName = Settings[iSetting_LSystemName]
        self.aiType = Settings[iSetting_AIType]

        lSystemClass = getattr(importlib.import_module("LSystems.CantorDust"), "CantorDust")
        l = lSystemClass(3)
        l.Display()

    def Execute(self):
        return ""

