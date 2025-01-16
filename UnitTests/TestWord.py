import unittest
from WordsAndSymbols.Word import Word
from WordsAndSymbols.SaC import SaC


class TestWord(unittest.TestCase):
    def setUp(self):
        self.SaC = SaC
        self.mapping = {'A': 1, 'B': 2, 'C': 3, 'CC': 4}
        self.reverse_mapping = {1: 'A', 2: 'B', 3: 'C', 4: 'CC'}

    def test_word_initialization(self):
        sac1 = self.SaC([1], 2, [3])
        sac2 = self.SaC([2], 3, [1])
        word = Word([sac1, sac2])

        self.assertEqual(len(word), 2)
        self.assertEqual(word.sac_counts, {2: 1, 3: 1})

    def test_to_string(self):
        sac1 = self.SaC([1], 2, [3])
        sac2 = self.SaC([2], 3, [1])
        sac3 = self.SaC([2], 4, [1])
        word = Word([sac1, sac2, sac3])

        result = word.to_string(self.reverse_mapping)
        self.assertEqual(result, "BC_CC_")

    def test_from_string(self):
        word_string = "ABCB_CC_A"
        word = Word.from_string(word_string, self.mapping)

        self.assertEqual(len(word), 6)
        self.assertEqual(word.sac_counts, {1: 2, 2: 2, 3: 1, 4: 1})
        self.assertEqual(word.sac_list[0].symbol, 1)
        self.assertEqual(word.sac_list[1].symbol, 2)

    def test_append_word(self):
        sac1 = self.SaC([1], 2, [3])
        sac2 = self.SaC([2], 3, [1])
        word1 = Word([sac1])
        word2 = Word([sac2])

        word1.append_word(word2)

        self.assertEqual(len(word1), 2)
        self.assertEqual(word1.sac_counts, {2: 1, 3: 1})

    def test_add_sac(self):
        sac1 = self.SaC([1], 2, [3])
        sac2 = self.SaC([2], 3, [1])
        word = Word([sac1])
        word.add_sac(sac2)

        self.assertEqual(len(word), 2)
        self.assertEqual(word.sac_counts, {2: 1, 3: 1})

if __name__ == "__main__":
    unittest.main()
