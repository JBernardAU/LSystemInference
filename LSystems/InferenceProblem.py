import json
import os

from InferenceTools.Evidence import Evidence
from InferenceTools.MasterAnalysisObject import MasterAnalysisObject
from Utility.context_utils import infer_context_size
from Utility.generate_mappings import generate_mappings
from WordsAndSymbols.Alphabet import Alphabet


class InferenceProblem:
    def __init__(self, settings_file=None, name="Unknown"):
        self.name = name
        self.identities = []  # known identity symbols
        self.ignore_list = [] # known symbols to ignore
        self.strings = [] # the observed raw strings
        self.MAO = None

        k = -1
        l = -1

        # Load settings from the JSON file if provided
        # Strings are loaded either from a provided Lsystem (below)
        # or must be in the subclass
        if settings_file:
            path = os.path.dirname(__file__)
            # Ensure settings_file is relative by stripping leading slashes
            settings_file = settings_file.lstrip("\\/")
            settings_path = os.path.join(path, settings_file)
            try:
                with open(settings_path, 'r') as file:
                    settings = json.load(file)
                    self.name = settings.get("name", "Unknown")
                    k = settings.get("k", -1)
                    l = settings.get("l", -1)
                    self.identities = set(settings.get("identities", []))
                    self.ignore = set(settings.get("ignore", []))
                    self.absolute_min_length = settings.get("Absolute Min Length")
            except FileNotFoundError:
                print(f"Settings file '{settings_file}' not found.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from settings file '{settings_file}'.")

        # Load the strings taken by observation
        self._load_strings()
        if not self.strings:
            raise ValueError("Strings are required to solve an L-system inference problem.")

        # Establish the alphabet and the k,l values to initialize the evidence
        # 1. infer the alphabet
        print("Infer Alphabet")
        mappings = generate_mappings(self)
        a = Alphabet(mappings, self.identities)
        print(f"   {a}")

        # 2. Infer the context size - if needed
        if k == -1 and l == -1:
            print("\nInfer Context Size")
            k, l = infer_context_size(strings=self.strings, alphabet=a)

        # The evidence discovered about the problem
        self.evidence = Evidence(strings=self.strings, alphabet=a, k=k, l=l)

        print(f"\nWords (original vs computed)")
        for i, w in enumerate(self.evidence.words):
            print(f"{i} | {w.original_string} vs. {w.sacs_to_string(self.evidence.alphabet.reverse_mappings)}")


    def _load_strings(self):
        pass