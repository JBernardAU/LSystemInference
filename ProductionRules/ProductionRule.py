from typing import List, Dict, Union
import random

from WordsAndSymbols.SaC import SaC
from WordsAndSymbols.Word import Word


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
        if self.sac == sac:
            return self.word
        return None

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
        if self.sac.symbol == sac.symbol and self.sac.left_context == sac.left_context and self.sac.right_context == sac.right_context:
            return self.parametric_function(sac)
        return None
