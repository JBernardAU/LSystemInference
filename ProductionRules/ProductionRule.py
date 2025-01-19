from typing import Union, Dict
from WordsAndSymbols.Word import Word
from WordsAndSymbols.SaC import SaC
import random

class ProductionRule:
    def __init__(self, sac: SaC, word: Word):
        """
        Base class for a production rule: SaC -> Word.

        :param sac: The left-hand side of the rule (a Symbol and Context).
        :param word: The right-hand side of the rule (a Word object).
        """
        self.sac = sac
        self.word = word

    def apply(self, sac: SaC) -> Union[Word, None]:
        """
        Apply the rule to a matching SaC.

        :param sac: The SaC to which the rule should be applied.
        :return: The resulting Word if the rule matches, otherwise None.
        """
        if self.sac == sac:  # Handles AnySymbol and EmptySymbol via SaC equality logic
            return self.word
        return None

    def __repr__(self):
        """
        Display the production rule in human-readable format.
        Format: left_context < symbol > right_context -> replacement string
        """
        left_context = "".join(str(x) for x in self.sac.left_context) if self.sac.left_context else "*"
        symbol = self.sac.symbol
        right_context = "".join(str(x) for x in self.sac.right_context) if self.sac.right_context else "*"
        replacement = self.word.sacs_to_string(reverse_mapping={}) if self.word else ""
        return f"{left_context} < {symbol} > {right_context} -> {replacement}"

class DeterministicProductionRule(ProductionRule):
    def __init__(self, sac: SaC, word: Word):
        super().__init__(sac, word)

class StochasticProductionRule(ProductionRule):
    def __init__(self, sac: SaC, word_options: Dict[Word, float]):
        """
        Stochastic production rule: SaC -> Word with probabilities.

        :param sac: The left-hand side of the rule.
        :param word_options: A dictionary mapping possible Words to their probabilities.
        """
        super().__init__(sac, None)  # word is not fixed in stochastic rules
        self.word_options = word_options

    def apply(self, sac: SaC) -> Union[Word, None]:
        """
        Apply the stochastic rule to a matching SaC.

        :param sac: The SaC to which the rule should be applied.
        :return: A randomly selected Word if the rule matches, otherwise None.
        """
        if self.sac == sac:
            choices, probabilities = zip(*self.word_options.items())
            return random.choices(choices, weights=probabilities, k=1)[0]
        return None

class ParametricProductionRule(ProductionRule):
    def __init__(self, sac: SaC, parametric_function):
        """
        Parametric production rule: SaC with parameters -> Word.

        :param sac: The left-hand side of the rule.
        :param parametric_function: A callable that takes SaC parameters and produces a Word.
        """
        super().__init__(sac, None)  # word is generated dynamically
        self.parametric_function = parametric_function

    def apply(self, sac: SaC) -> Union[Word, None]:
        """
        Apply the parametric rule to a matching SaC.

        :param sac: The SaC to which the rule should be applied.
        :return: The resulting Word if the rule matches, otherwise None.
        """
        if (
            self.sac._match_symbol(self.sac.symbol, sac.symbol) and
            self.sac._match_context(self.sac.left_context, sac.left_context) and
            self.sac._match_context(self.sac.right_context, sac.right_context)
        ):
            return self.parametric_function(sac)
        return None