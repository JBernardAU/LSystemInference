import importlib
import json
from LSystems.LSystemsSettings import LSystemSettings

class LSystemInference:
    def __init__(self, settings_file: str):
        """
        Initialize the LSystemInference system by loading settings and L-system class.

        :param settings_file: Path to the JSON settings file.
        """
        # Load settings
        self.settings = LSystemSettings.from_json(settings_file)

        # Dynamically load the corresponding L-system class based on the name in settings
        try:
            lsystem_module = f"LSystems.{self.settings.name}"
            lsystem_class = getattr(importlib.import_module(lsystem_module), self.settings.name)
            self.lsystem = lsystem_class()
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"Error loading L-system class '{self.settings.name}': {e}")

    def display_settings(self):
        """
        Display the loaded settings for debugging or information purposes.
        """
        print("Loaded Settings:", self.settings)

    def run(self):
        """
        Placeholder method for running inference or execution tasks.
        """
        self.lsystem.display()
        print(f"Running L-system inference for: {self.settings.name}")
