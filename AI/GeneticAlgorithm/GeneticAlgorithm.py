from AI import AI
from GeneticAlgorithmConfiguration import *

UnitTest_GeneticAlgorithm = True

class GeneticAlgorithm(AI):
    # Create a genetic algorithm
    # Initialization is done using Configuration() which takes a configuration
    # This is done as the configuration may not be known at the time of creation
    def __init__(self):
        super().__init__()
        self.type = "Optimizer"
        self.population = list()
        self.crossover = None
        self.selector = None
        self.mutator = None

    # Input:
    # - A genetic algorithm configuration
    # Outputs:
    # - None
    def Configure(self, GAC):
        for iPop in range(GAC.initialPopulationSize):
            print(iPop)
