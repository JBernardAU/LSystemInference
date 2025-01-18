from typing import List, Tuple

from Utility.generate_mappings import generate_mappings
from LSystems.LSystem import LSystem
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.Word import Word

class Evidence:
    def __init__(self, strings: List[str], alphabet: Alphabet, F_has_identity: bool = False, known_context: bool = False, i: int = 0, j: int = 0):
        """
        Initialize the Evidence object.

        :param strings: A sequence of strings representing the evidence.
        :param alphabet: The Alphabet object for symbol management.
        :param F_has_identity: Whether to include 'F' in context calculations.
        :param known_context: Mode for context creation: "Known" or "Unknown".
        :param i: Left context depth (if mode is "Known").
        :param j: Right context depth (if mode is "Known").
        """
        self.strings = strings
        self.alphabet = alphabet
        self.include_f = F_has_identity
        self.known_context = known_context
        self.i = i
        self.j = j

        if self.known_context == True:
            self.words = [Word.from_string(s, alphabet.mappings, self.i, self.j) for s in strings]
        elif self.known_context == False:
            self.i, self.j = self._determine_context_depth()
            self.words = [Word.from_string(s, alphabet.mappings, self.i, self.j) for s in strings]
        else:
            raise ValueError("Mode must be either 'Known' or 'Unknown'.")

    def _determine_context_depth(self) -> Tuple[int, int]:
        """
        Determine the longest possible left and right context depths.

        :return: A tuple of (max_i, max_j).
        """
        max_i, max_j = 0, 0

        for s in self.strings:
            for idx, char in enumerate(s):
                if char in "+-[]" or (char == "F" and not self.include_f):
                    continue  # Turtle graphics and optionally 'F' do not contribute to context

                left_depth = self._calculate_context(s, idx, "left")
                right_depth = self._calculate_context(s, idx, "right")

                max_i = max(max_i, left_depth)
                max_j = max(max_j, right_depth)

        return max_i, max_j

    def _calculate_context(self, string: str, index: int, direction: str) -> int:
        """
        Calculate the context depth for a symbol at a given index in a given direction.

        :param string: The string to analyze.
        :param index: The position of the symbol in the string.
        :param direction: "left" or "right".
        :return: The context depth.
        """
        step = -1 if direction == "left" else 1
        depth = 0
        cursor = index + step

        while 0 <= cursor < len(string):
            char = string[cursor]
            if char in "+-[]" or (char == "F" and not self.include_f):
                break  # Stop at turtle graphics or excluded 'F'
            depth += 1
            cursor += step

        return depth

    def to_lsystem(self, name: str = "Unknown") -> 'LSystem':
        """
        Convert the evidence into an LSystem object (without rules).

        :return: An LSystem object.
        """
        lsystem = LSystem(
            name=name,
            axiom=self.strings[0],
            alphabet=self.alphabet,
            i=self.i,
            j=self.j
        )
        lsystem.words = self.words
        return lsystem

if __name__ == "__main__":
    raw_strings = ["ABABBBABA","ABABBBABABBBBBBBBBABABBBABA"]
    mappings, identities = generate_mappings(raw_strings, F_has_identity=False)
    a = Alphabet(mappings, identities)
    e = Evidence(strings=raw_strings, alphabet=a, known_context=False)
    ls = e.to_lsystem(name="Test A")
    ls.display()