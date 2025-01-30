import importlib
from InferenceTools.MasterAnalysisObject import MasterAnalysisObject
from LSystems.LSystemsSettings import LSystemSettings
from Utility.parikh_analysis import analyze_words_growth, analyze_words_length


class LSystemInference:
    def __init__(self, settings_file: str):
        """
        Initialize the LSystemInference system by loading settings and L-system class.

        :param settings_file: Path to the JSON settings file.
        """
        # Load settings
        self.settings = LSystemSettings.from_json(settings_file)
        self.evidence = None
        self.MAO = None

        if self.settings.mode == "Experiment":
            # Dynamically load the corresponding L-system class based on the name in settings
            try:
                print("L-SYSTEM TO FIND")
                lsystem_module = f"LSystems.{self.settings.name}.{self.settings.name}"
                lsystem_class = getattr(importlib.import_module(lsystem_module), self.settings.name)
                self.lsystem = lsystem_class()
                self.lsystem.display()

                print("\nESTABLISHING PROBLEM")
                problem_module = f"LSystems.{self.settings.name}.{self.settings.name}Problem"
                problem_class = getattr(importlib.import_module(problem_module), f"{self.settings.name}Problem")
                self.problem = problem_class()
            except (ModuleNotFoundError, AttributeError) as e:
                raise ImportError(f"Error loading L-system class '{self.settings.name}': {e}")
        else:
            self.lsystem = None

    def display_settings(self):
        """
        Display the loaded settings for debugging or information purposes.
        """
        print("Loaded Settings:", self.settings)

    def run(self):
        """
        Placeholder method for running inference or execution tasks.
        """
        self.display_settings()
        print("\nSTART INFERENCE")
        print(f" PRE-ANALYSIS - CREATING MAO")
        # Create the MAO and conduct the naive analysis
        self.MAO = MasterAnalysisObject(problem=self.problem)

        print(f"\n Check for Ambiguity")
        self.MAO.compute_length_absolute_min_max()

        while self.MAO.flag:
            print(f"\n RESET MAO FLAG")
            self.MAO.flag = False

            print(f"\n STEP 1 - COMPUTE LENGTH | Total Length Production")

            print(f"\n STEP 1 - REFINE WORD METRICS")
            # Refine unaccounted for growth & length
            self.MAO.compute_unaccounted_growth_matrix()
            self.MAO.compute_unaccounted_length_matrix()

            print(f"\n STEP 3 - PARIKH ANALYSIS")
            # A. Parikh Analysis
            print(f"   Solve Parikh Growth Matrix")
            growth_matrix = analyze_words_growth(self.problem)
            print(f"   Solve Parikh Length Matrix")
            length_matrix = analyze_words_length(self.problem)

            print(f"\n STEP 4 - Computing Length from Total Symbol Production")
            self.MAO.compute_length_total_symbol_production()

            print(f"\n STEP 5 - Computing Total Length from Total Symbol Production")
            #print(f"\n          Without Identities")
            self.MAO.compute_total_length_total_symbol_production(include_identities=False)
            # TODO: Check this later with other L-systems there is potential information here, maybe. It is odd.
            #print(f"\n          With Identities")
            #self.MAO.compute_total_length_total_symbol_production(include_identities=True)

            print(f"\n STEP 5 - Computing Length from Total Length")
            #print(f"\n          Without Identities")
            self.MAO.compute_length_total_length()

            print(f"\n STEP X - Computing Fragment from Markers")
            print(f"\n STEP X - Computing Fragment from Overlapping")
            print(f"\n STEP X - Computing Fragment from Partial Solution")
            print(f"\n STEP X - Localization")

            print(f"\n Compute Minimum Variables")
            selected_sacs = self.MAO.find_minimum_sacs_set()
            print(selected_sacs)
            print(f"\n Compute Minimum P-Space")
            selected_sacs, pspace_size = self.MAO.find_smallest_pspace()
            print(f"{selected_sacs}\n{pspace_size}")
            pass







