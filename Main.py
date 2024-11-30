from GlobalSettings import *
from Processor import Processor

def ExtractSetting(Line):
    return line.split(":")[1].strip()

settings = list()
with open("settings_experimental.txt", "r") as file:
    iLine = 0
    for line in file:
        if  iLine == iSetting_Mode:
            settings.append(ExtractSetting(line))
        elif iLine == iSetting_LSystemName:
            settings.append(ExtractSetting(line))
        elif iLine == iSetting_AIType:
            settings.append(ExtractSetting(line))
        elif iLine == iSetting_ContextMode:
            settings.append(ExtractSetting(line))
        iLine += 1

p = Processor(settings)
p.Execute()
