import importlib
import json

from InferenceTools.Evidence import Evidence
from LSystems.LSystemsSettings import LSystemSettings
from WordsAndSymbols.Word import Word


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
                lsystem_module = f"LSystems.{self.settings.name}"
                lsystem_class = getattr(importlib.import_module(lsystem_module), self.settings.name)
                self.lsystem = lsystem_class()
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
        if self.settings.mode == "Experiment":
            self.lsystem.display()

            raw_strings = []
            for w in self.lsystem.words:
                raw_strings.append(Word.to_string(w, self.lsystem.alphabet.reverse_mappings))
                self.evidence = Evidence(strings=raw_strings, alphabet=self.lsystem.alphabet, F_has_identity=self.settings.f_has_identity, known_context=self.settings.known_context)
        elif self.settings.mode == "Inference":
            pass
        else:
            raise ValueError(f"Unknown inference mode '{self.settings.mode}'")



