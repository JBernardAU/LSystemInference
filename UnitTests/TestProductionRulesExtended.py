import unittest
from WordsAndSymbols.Word import Word
from WordsAndSymbols.SaC import SaC
from WordsAndSymbols.Alphabet import Alphabet
from ProductionRules.ProductionRule import StochasticProductionRule, ParametricProductionRule, DeterministicProductionRule
import random

import random

class TestProductionRuleExtended(unittest.TestCase):
    def setUp(self):
        # Seed the random number generator for reproducibility
        random.seed(42)

        # Initialize the alphabet
        self.alphabet = Alphabet(
            mappings={"A": 1, "B": 2, "C": 3, "F": 4, "+": 5, "-": 6, "[": 7, "]": 8},
            identity_symbols={"F", "+", "-", "[", "]"}
        )

        # Define helper method to create Words
        self._string_to_word = lambda s: Word([
            SaC([], self.alphabet.get_id(c), []) for c in s
        ])

    def test_stochastic_production_rule(self):
        # Define the stochastic rule: A -> {F with 70%, B with 30%}
        rule = StochasticProductionRule(
            sac=SaC([], self.alphabet.get_id("A"), []),
            word_options={
                self._string_to_word("F"): 0.7,
                self._string_to_word("B"): 0.3
            }
        )

        # Apply the rule multiple times and count occurrences
        results = {"F": 0, "B": 0}
        for _ in range(1000):
            produced_word = rule.apply(SaC([], self.alphabet.get_id("A"), []))
            if produced_word:
                symbol = self.alphabet.get_symbol(produced_word.sac_list[0].symbol)
                results[symbol] += 1

        print("Stochastic Rule Results:", results)
        # Assert the results are roughly proportional to probabilities
        self.assertTrue(650 <= results["F"] <= 750)
        self.assertTrue(250 <= results["B"] <= 350)

    def test_parametric_production_rule(self):
        # Define the parametric rule: A -> F, with external parameters
        def parametric_function(sac):
            # Use the parameters directly without embedding in the string
            param = sac.parameters.get("n", 1)  # Default parameter value is 1
            # Symbol remains "F"; parameters are stored externally
            return self._string_to_word("F")

        rule = ParametricProductionRule(
            sac=SaC([], self.alphabet.get_id("A"), []),
            parametric_function=parametric_function
        )

        # Define test parameters
        parameters_list = [
            {"n": 1},
            {"n": 5}
        ]

        # Apply the rule with different parameters
        sac_with_param_1 = SaC([], self.alphabet.get_id("A"), [])
        sac_with_param_1.parameters = parameters_list[0]
        sac_with_param_5 = SaC([], self.alphabet.get_id("A"), [])
        sac_with_param_5.parameters = parameters_list[1]

        word_1 = rule.apply(sac_with_param_1)
        word_5 = rule.apply(sac_with_param_5)

        print("Parametric Rule Results:")
        print("n=1:", word_1.to_string(self.alphabet.reverse_mappings), parameters_list[0])
        print("n=5:", word_5.to_string(self.alphabet.reverse_mappings), parameters_list[1])

        # Assert correct outputs
        self.assertEqual(word_1.to_string(self.alphabet.reverse_mappings), "F")
        self.assertEqual(word_5.to_string(self.alphabet.reverse_mappings), "F")

    def test_rule_applies_to_word(self):
        # Define deterministic rule: A -> F
        det_rule = DeterministicProductionRule(
            sac=SaC([], self.alphabet.get_id("A"), []),
            word=self._string_to_word("F")
        )

        # Define input word and expected output
        input_word = self._string_to_word("AAB")
        expected_word = self._string_to_word("FFB")

        # Apply rule to the input word
        output_sac_list = []
        for sac in input_word.sac_list:
            result = det_rule.apply(sac)
            if result:
                output_sac_list.extend(result.sac_list)
            else:
                output_sac_list.append(sac)

        output_word = Word(output_sac_list)
        print("Deterministic Rule Application Results:")
        print("Input Word:", input_word.to_string(self.alphabet.reverse_mappings))
        print("Output Word:", output_word.to_string(self.alphabet.reverse_mappings))

        # Assert correctness
        self.assertEqual(output_word.to_string(self.alphabet.reverse_mappings), expected_word.to_string(self.alphabet.reverse_mappings))

    def test_stochastic_rule_applies_to_word(self):
        # Define stochastic rule: A -> {F with 6%, B with 94%}
        stochastic_rule = StochasticProductionRule(
            sac=SaC([], self.alphabet.get_id("A"), []),
            word_options={
                self._string_to_word("F"): 0.50,
                self._string_to_word("B"): 0.50
            }
        )

        # Define input word
        input_word = self._string_to_word("AAB")

        # Apply rule to the input word 1000 times and track results of first and second A
        first_a_results = {"F": 0, "B": 0}
        second_a_results = {"F": 0, "B": 0}

        for _ in range(1000):
            output_sac_list = []
            for sac in input_word.sac_list:
                result = stochastic_rule.apply(sac)
                if result:
                    output_sac_list.extend(result.sac_list)
                else:
                    output_sac_list.append(sac)

            output_word = Word(output_sac_list)
            first_symbol = self.alphabet.get_symbol(output_word.sac_list[0].symbol)
            second_symbol = self.alphabet.get_symbol(output_word.sac_list[1].symbol)

            first_a_results[first_symbol] += 1
            second_a_results[second_symbol] += 1

        print("Stochastic Rule Applied to Word:")
        print("First A Results:", first_a_results)
        print("Second A Results:", second_a_results)

if __name__ == "__main__":
    unittest.main()
