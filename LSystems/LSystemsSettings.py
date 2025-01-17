import json

class LSystemSettings:
    def __init__(self, name: str, mode: str = "Inference", ai_type: str = "GeneticAlgorithm", i: int = -1, j: int = -1):
        """
        Initialize settings for an L-system.

        :param name: The name of the L-system.
        :param mode: Execution mode (e.g., "Inference").
        :param ai_type: AI type used (e.g., "GeneticAlgorithm").
        :param i: Left context depth (-1 indicates unknown depth).
        :param j: Right context depth (-1 indicates unknown depth).
        """
        self.name = name
        self.mode = mode
        self.ai_type = ai_type
        self.i = i
        self.j = j

    @classmethod
    def from_json(cls, filepath: str) -> 'LSystemSettings':
        """
        Load LSystemSettings from a JSON file.

        :param filepath: Path to the JSON file.
        :return: An instance of LSystemSettings.
        """
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
            return cls(
                name=data.get("name", "Unnamed LSystem"),
                mode=data.get("mode", "Inference"),
                ai_type=data.get("ai_type", "GeneticAlgorithm"),
                i=data.get("i", -1),
                j=data.get("j", -1)
            )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading settings from {filepath}: {e}")

    def is_context_known(self) -> bool:
        """
        Check if the context depths are known.

        :return: True if both i and j are not -1, False otherwise.
        """
        return self.i != -1 and self.j != -1

    def __repr__(self):
        """
        Provide a string representation of the settings for debugging and display.
        """
        return (f"LSystemSettings("
                f"name={self.name}, mode={self.mode}, ai_type={self.ai_type}, "
                f"i={self.i}, j={self.j})")
