from AI.PopulationMember import PopulationMember
from GlobalSettings import *

class Genome(PopulationMember):

    # Inputs:
    # - Number of values (N)
    # - Bounds for each value (B). Each bound is duple (min,max)
    def __init__(self, N, B):
        super().__init__(N)
        self.bounds = B

        for iValue in range(N):
            self.values[iValue] = self.bounds[iValue][iMin]



