import math

# Special symbols
anySymbol = "*"
anySymbolID = math.inf-1
emptySymbol = "~"
emptySymbolID = math.inf-2

# Turtle graphics
moveForward = "F"
turnLeft = "+"
turnRight = "-"
turn180 = "|"
startBranch = "["
endBranch = "]"
identityAlphabet2D = [moveForward, turnLeft, turnRight, turn180, startBranch, endBranch]
#identityAlphabet3D = [moveForward, turnLeft, turnRight, turn180, startBranch, endBranch]
contextForbidden = [turnLeft, turnRight, turn180, startBranch, endBranch] # these symbols may not appear in a context

# SAC Positions
iSACSymbol = 0
iSACLeft = 1
iSACRight = 2

# J,K Positions
iContextLeft = 0
iContextRight = 0

# Settings indices
iSetting_Mode = 0 # Possible modes: Experimental and Inference
iSetting_LSystemName = 1
iSetting_AIType = 2
iSetting_ContextMode = 3

# Bounds indices
iMin = 0
iMax = 1

# default actions
identityOnNoMatch = True

multicharacterIndicator = "."



