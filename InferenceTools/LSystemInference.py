import importlib
import math

from InferenceTools.Evidence import Evidence
from LSystems.LSystemsSettings import LSystemSettings
from Utility.analysis_utils import calculate_weighted_mean, calculate_modified_weighted_mean
from Utility.context_utils import histogram_context
from Utility.generate_mappings import generate_mappings
from Utility.parikh_analysis import analyze_words_growth, analyze_words_length
from WordsAndSymbols.Alphabet import Alphabet


class LSystemInference:
    def __init__(self, settings_file: str):
        """
        Initialize the LSystemInference system by loading settings and L-system class.

        :param settings_file: Path to the JSON settings file.
        """
        # Load settings
        self.settings = LSystemSettings.from_json(settings_file)
        self.evidence = None

        if self.settings.mode == "Experiment":
            # Dynamically load the corresponding L-system class based on the name in settings
            try:
                lsystem_module = f"LSystems.{self.settings.name}.{self.settings.name}"
                lsystem_class = getattr(importlib.import_module(lsystem_module), self.settings.name)
                self.lsystem = lsystem_class()

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

    def infer_context_size(self, alphabet):
        histo_left, histo_right = histogram_context(strings=self.problem.strings, alphabet=alphabet,
                                                    F_has_identity=self.settings.f_has_identity)
        i = 0
        j = 0
        for symbol in histo_left:
            hl = dict(sorted(histo_left[symbol].items(), key=lambda item: item[1], reverse=True))
            lengths = list(hl.keys())
            frequencies = list(hl.values())
            # i.append(calculate_weighted_mean(lengths, frequencies))
            i = math.ceil(max(i, calculate_modified_weighted_mean(lengths, frequencies)))

            hr = dict(sorted(histo_right[symbol].items(), key=lambda item: item[1], reverse=True))
            lengths = list(hr.keys())
            frequencies = list(hr.values())
            # j.append(calculate_weighted_mean(lengths, frequencies))
            j = math.ceil(max(j, calculate_modified_weighted_mean(lengths, frequencies)))

        print(f"i = {i} | j = {j}")
        return i, j

    def run(self):
        """
        Placeholder method for running inference or execution tasks.
        """
        self.display_settings()
        if self.settings.mode == "Experiment":
            print("L-SYSTEM TO FIND")
            self.lsystem.display()

            print("\nSTART INFERENCE")

            # 1. infer the alphabet
            print("Infer Alphabet")
            mappings, identities = generate_mappings(self.problem.strings, F_has_identity=self.settings.f_has_identity)
            a = Alphabet(mappings, identities)
            print(f"   {a}")

            # 2. Infer the context size - if needed
            k = -1
            l = -1
            if not self.settings.known_context:
                print("\nInfer Context Size")
                k, l = self.infer_context_size(a)

            k = 0
            l = 0

            # 3. Create the evidence object
            self.evidence = Evidence(strings=self.problem.strings, alphabet=a, k=k, l=l, F_has_identity=self.settings.f_has_identity)

            print(f"\nWords")
            for i, w in enumerate(self.evidence.words):
               print(f"{i} | {w.sacs_to_string(self.evidence.alphabet.reverse_mappings)}")

            # 4 Pre-analysis
            print(f"\PRE-ANALYSIS")
            for w in self.evidence.words:
                sacs_in_word = list(set(w))
                self.evidence.alphabet.sacs = list(set(self.evidence.alphabet.sacs + sacs_in_word))

            # A. Parikh Analysis
            growth_matrix = analyze_words_growth(self.evidence)
            length_matrix = analyze_words_length(self.evidence)

        elif self.settings.mode == "Inference":
            pass
        else:
            raise ValueError(f"Unknown inference mode '{self.settings.mode}'")



