import unittest

from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC
from WordsAndSymbols.Word import Word


class TestAlphabetAndWord(unittest.TestCase):
    def setUp(self):
        # Create the alphabet
        self.alphabet = Alphabet(
            mappings={"A": 1, "B": 2, "C": 3, "F": 4, "+": 5, "-": 6, "[": 7, "]": 8},
            identity_symbols={"F", "+", "-", "[", "]"}
        )

        # Set homomorphisms: A and B map to X (ID = 9)
        self.alphabet.add_symbol("X", 9)
        self.alphabet.set_homomorphism("A", "X")
        self.alphabet.set_homomorphism("B", "X")

        # Define the sequence of strings
        self.strings = [
            "A[+FB]-C",
            "B[-F+A]C[+F-A]",
            "C[F+A-B]"
        ]

        # Create words from strings with i=3, j=3 context sensitivity
        self.words = []
        for string in self.strings:
            sac_list = []
            for i, char in enumerate(string):
                left_context = self.alphabet.get_context(string, i, direction="left", max_depth=3, include_f=False)
                right_context = self.alphabet.get_context(string, i, direction="right", max_depth=3, include_f=False)
                sac = SaC(left_context, self.alphabet.get_id(char), right_context)
                sac_list.append(sac)
            self.words.append(Word(sac_list))

    def test_display_true_and_homomorphized_words(self):
        print("\nTrue Words:")
        for word in self.words:
            print(word.to_string(self.alphabet.reverse_mappings))

        print("\nHomomorphized Words:")
        for word in self.words:
            homomorphized = [
                SaC(
                    [self.alphabet.apply_homomorphism(id_) for id_ in sac.left_context],
                    self.alphabet.apply_homomorphism(sac.symbol),
                    [self.alphabet.apply_homomorphism(id_) for id_ in sac.right_context]
                )
                for sac in word.sac_list
            ]
            homomorphized_word = Word(homomorphized)
            print(homomorphized_word.to_string(self.alphabet.reverse_mappings))

    def test_display_sac_counts(self):
        print("\nSaC Counts:")
        for i, word in enumerate(self.words):
            print(f"Word {i + 1} counts:")
            sac_counts = {}
            for sac in word.sac_list:
                # Convert SaC to a symbol-based tuple for human-readable counting
                left_context = tuple(self.alphabet.get_symbol(id_) for id_ in sac.left_context)
                symbol = self.alphabet.get_symbol(sac.symbol)
                right_context = tuple(self.alphabet.get_symbol(id_) for id_ in sac.right_context)
                sac_key = (left_context, symbol, right_context)
                sac_counts[sac_key] = sac_counts.get(sac_key, 0) + 1

            for sac, count in sac_counts.items():
                left_context, symbol, right_context = sac
                print(f"  Left: {left_context}, Symbol: {symbol}, Right: {right_context}, Count: {count}")

    def test_display_unique_sacs(self):
        unique_sacs = set()
        for word in self.words:
            unique_sacs.update(word.sac_list)

        print("\nUnique SaCs:")
        for sac in unique_sacs:
            left_context = [self.alphabet.get_symbol(id_) for id_ in sac.left_context]
            symbol = self.alphabet.get_symbol(sac.symbol)
            right_context = [self.alphabet.get_symbol(id_) for id_ in sac.right_context]
            print(f"Left: {left_context}, Symbol: {symbol}, Right: {right_context}")


if __name__ == "__main__":
    unittest.main()
