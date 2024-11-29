from GlobalSettings import *
from Processor import Processor

def ExtractSetting(Line):
    return line.split(":")[1].strip()

settings = list()
with open("settings.txt", "r") as file:
    iLine = 0
    for line in file:
        if iLine == iSetting_LSystemName:
            settings.append(ExtractSetting(line))
        elif iLine == iSetting_AIType:
            settings.append(ExtractSetting(line))
        elif iLine == iSetting_AssumeContextKnown:
            settings.append(ExtractSetting(line))
        iLine += 1

p = Processor(settings)