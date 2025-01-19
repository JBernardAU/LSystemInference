import unittest
from ProductionRules.ProductionRule import DeterministicProductionRule
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC, ANY_SYMBOL, ANY_SYMBOL_ID, EMPTY_SYMBOL
from WordsAndSymbols.Word import Word


class TestProductionRule(unittest.TestCase):
    def setUp(self):
        # Create the alphabet
        self.alphabet = Alphabet(
            mappings={"A": 1, "B": 2, "C": 3, "F": 4, "+": 5, "-": 6, "[": 7, "]": 8},
            identity_symbols={"F", "+", "-", "[", "]"}
        )

        self.i = 0
        self.j = 0
        # Define the initial string and convert it to a Word
        self.initial_string = "A+[FB]-C"
        self.word = Word.from_string(self.initial_string, self.alphabet.mappings, self.i, self.j)
        self.first_word = Word.from_string("F+[A]+[FFB]-AC", self.alphabet.mappings, self.i, self.j)
        self.second_word = Word.from_string("F+[F+[A]]+[FFFB]-F+[A]AC", self.alphabet.mappings, self.i, self.j)

        # Define production rules
        self.rules = [
            DeterministicProductionRule(
                SaC([ANY_SYMBOL_ID], self.alphabet.get_id("A"), [ANY_SYMBOL_ID]),  # A -> F+[A]
                Word.from_string("F+[A]", self.alphabet.mappings, self.i, self.j)
            ),
            DeterministicProductionRule(
                SaC([ANY_SYMBOL_ID], self.alphabet.get_id("B"), [ANY_SYMBOL_ID]),  # B -> F
                Word.from_string("FB", self.alphabet.mappings, self.i, self.j)
            ),
            DeterministicProductionRule(
                SaC([ANY_SYMBOL_ID], self.alphabet.get_id("C"), [ANY_SYMBOL_ID]),  # C -> C
                Word.from_string(EMPTY_SYMBOL, self.alphabet.mappings, self.i, self.j)
            )
        ]

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
        current_word.display(self.alphabet.reverse_mappings,mode="sacs")

        # Apply rules to produce the first new word
        current_word = self._apply_rules(current_word)
        first_string = current_word.sacs_to_string(self.alphabet.reverse_mappings)
        print("First Produced String:", first_string)
        current_word.display(self.alphabet.reverse_mappings,mode="sacs")

        # Apply rules again to produce the second new word
        current_word = self._apply_rules(current_word)
        second_string = current_word.sacs_to_string(self.alphabet.reverse_mappings)
        print("Second Produced String:", second_string)
        current_word.display(self.alphabet.reverse_mappings,mode="sacs")

        # Add assertions to verify correctness
        # A -> F+[A]
        # B -> FB
        # C -> AC
        # A+[FB]-C
        # F+[A]+[FFB]-AC
        # F+[F+[A]]+[FFFB]-F+[A]AC
        self.assertEqual("F+[A]+[FFB]-λ", first_string)  # Example output
        self.assertEqual("F+[F+[A]]+[FFFB]-F+[A]", second_string)

if __name__ == "__main__":
    unittest.main()
