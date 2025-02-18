from ProductionRules.ProductionRule import ProductionRule
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import SaC, ANY_SYMBOL_ID, EMPTY_SYMBOL_ID
from WordsAndSymbols.Word import Word

class LSystem:
    def __init__(self, name: str, axiom: str, alphabet: Alphabet, k: int=0, l: int=0):
        """
        Initialize the L-system with an axiom, alphabet, and context depth.

        :param axiom: The initial string of the L-system.
        :param alphabet: The Alphabet object for symbol management.
        :param k: Maximum left context depth.
        :param l: Maximum right context depth.
        """
        self.name = name
        self.axiom = axiom
        self.alphabet = alphabet
        self.k = k
        self.l = l
        self.words = [Word.from_string(axiom, alphabet, k, l)]  # Store all words
        self.rules = []

#        for w in self.words:
#            sacs_in_word = list(set(w.sac_list))
#            self.alphabet.sacs = list(set(self.alphabet.sacs + sacs_in_word))

    def add_rule(self, sac: SaC, rule: ProductionRule):
        """
        Add a production rule to the L-system.

        :param sac: The left-hand side of the rule (SaC object).
        :param rule: The production rule object.
        """
        self.rules.append((sac, rule))

    def apply_rule(self, sac: SaC) -> Word:
        """
        Apply the first matching rule to a given SaC.

        :param sac: The SaC to which the rule should be applied.
        :return: The resulting Word if a rule matches, or the original SaC as a Word.
        """
        for rule_sac, rule in self.rules:
            if rule_sac == sac:
                return rule.apply(sac)
        return Word([sac])  # No matching rule, return the original SaC as a Word.

    def iterate(self, n: int):
        """
        Perform n iterations of the L-system.

        :param n: Number of iterations to perform.
        """
        for _ in range(n):
            new_sac_list = []
            for sac in self.words[-1].sacs:  # Use the last word in the list
                new_word = self.apply_rule(sac)
                new_sac_list.extend(new_word.sacs)
            self.words.append(Word(new_sac_list))  # Append the new word to the list

    def display(self):
        """
        Display the L-system details: alphabet, rules, and all words.

        The alphabet is displayed as SaCs (e.g., * < A > *).
        """
        print("\nAlphabet:")
        print(f"  {self.alphabet.symbols}")

        print("\nRules:")
        for sac, rule in self.rules:
            left_context = ",".join(self.alphabet.reverse_mappings.get(id_, "?") for id_ in sac.left_context) or "*"
            symbol = self.alphabet.reverse_mappings.get(sac.symbol, "?")
            right_context = ",".join(self.alphabet.reverse_mappings.get(id_, "?") for id_ in sac.right_context) or "*"
            print(
                f"  {left_context} < {symbol} > {right_context} -> {rule.word.sacs_to_string(self.alphabet.reverse_mappings)}")

        print("\nWords:")
        for i, word in enumerate(self.words):
            print(f"  Word {i}: {word.sacs_to_string(self.alphabet.reverse_mappings)}")

    def to_string(self) -> str:
        """
        Convert the current state of the L-system to a string representation.

        :return: String representation of the current word.
        """
        return self.words[-1].sacs_to_string(self.alphabet.reverse_mappings)
