from typing import List, Tuple
from Utility.context_utils import determine_context_depth
from Utility.generate_mappings import generate_mappings
from LSystems.LSystem import LSystem
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.Word import Word

class Evidence:
    def __init__(self, strings: List[str], alphabet: Alphabet, k: int = -1, l: int = -1, F_has_identity: bool = False):
        """
        Initialize the Evidence object.

        :param strings: A sequence of strings representing the evidence.
        :param alphabet: The Alphabet object for symbol management.
        :param F_has_identity: Whether to include 'F' in context calculations.
        :param known_context: Mode for context creation: "Known" or "Unknown".
        :param k: Left context depth (if mode is "Known").
        :param l: Right context depth (if mode is "Known").
        """
        self.strings = strings
        self.alphabet = alphabet
        self.include_f = F_has_identity
        self.k = k
        self.l = l
        self.words = [Word.from_string(s, alphabet.mappings, self.k, self.l) for s in strings]

    def to_lsystem(self, name: str = "Unknown") -> 'LSystem':
        """
        Convert the evidence into an LSystem object (without rules).

        :return: An LSystem object.
        """
        lsystem = LSystem(
            name=name,
            axiom=self.strings[0],
            alphabet=self.alphabet,
            k=self.k,
            l=self.l
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