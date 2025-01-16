import unittest
from ProductionRules.ProductionRule import DeterministicProductionRule
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC
from WordsAndSymbols.Word import Word


class TestProductionRule(unittest.TestCase):
    def setUp(self):
        # Create the alphabet
        self.alphabet = Alphabet(
            mappings={"A": 1, "B": 2, "C": 3, "F": 4, "+": 5, "-": 6, "[": 7, "]": 8},
            identity_symbols={"F", "+", "-", "[", "]"}
        )

        # Define the initial string and convert it to a Word
        self.initial_string = "A+[FB]-C"
        self.word = self._string_to_word(self.initial_string)

        self.first_word = self._string_to_word("F+[A]+[FFB]-AC")
        self.second_word = self._string_to_word("F+[F+[A]]+[FFFB]-F+[A]AC")

        # Define production rules
        self.rules = [
            DeterministicProductionRule(
                SaC([], self.alphabet.get_id("A"), []),  # A -> F+[A]
                self._string_to_word("F+[A]")
            ),
            DeterministicProductionRule(
                SaC([], self.alphabet.get_id("B"), []),  # B -> F
                self._string_to_word("FB")
            ),
            DeterministicProductionRule(
                SaC([], self.alphabet.get_id("C"), []),  # C -> C
                self._string_to_word("AC")
            )
        ]

    def _string_to_word(self, string: str) -> Word:
        """
        Helper to convert a string to a Word object.
        """
        sac_list = []
        for i, char in enumerate(string):
            left_context = self._get_context(string, i, direction="left", max_depth=1)
            right_context = self._get_context(string, i, direction="right", max_depth=1)
            sac = SaC(left_context, self.alphabet.get_id(char), right_context)
            sac_list.append(sac)
        return Word(sac_list)

    def _get_context(self, string, index, direction, max_depth):
        """
        Get the context for a symbol at a given index.
        """
        step = -1 if direction == "left" else 1
        context = []
        depth = 0
        i = index + step

        while 0 <= i < len(string) and depth < max_depth:
            char = string[i]
            if char in "[]":  # Stop at brackets
                break
            if char not in "+-[]":
                context.append(self.alphabet.get_id(char))
                depth += 1
            i += step

        if direction == "left":
            context.reverse()
        return context

    def _apply_rules(self, word: Word) -> Word:
        """
        Apply production rules to a word.
        """
        new_sac_list = []
        for sac in word.sac_list:
            for rule in self.rules:
                result = rule.apply(sac)
                if result:
                    new_sac_list.extend(result.sac_list)
                    break
            else:
                new_sac_list.append(sac)  # If no rule matches, retain the original SaC
        return Word(new_sac_list)

    def test_production_rules(self):
        print("Initial String:", self.initial_string)
        current_word = self.word

        # Apply rules to produce the first new word
        current_word = self._apply_rules(current_word)
        first_string = current_word.to_string(self.alphabet.reverse_mappings)
        print("First Produced String:", first_string)

        # Apply rules again to produce the second new word
        current_word = self._apply_rules(current_word)
        second_string = current_word.to_string(self.alphabet.reverse_mappings)
        print("Second Produced String:", second_string)

        # Add assertions to verify correctness
        # A -> F+[A]
        # B -> FB
        # C -> AC
        # A+[FB]-C
        # F+[A]+[FFB]-AC
        # F+[F+[A]]+[FFFB]-F+[A]AC
        self.assertEqual(first_string, "F+[A]+[FFB]-AC")  # Example output
        self.assertEqual(second_string, "F+[F+[A]]+[FFFB]-F+[A]AC")

if __name__ == "__main__":
    unittest.main()
