from typing import List
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.Word import Word

class Evidence:
    def __init__(self, strings: List[str], alphabet: Alphabet, k: int, l: int):
        """
        Initialize the Evidence object.

        :type problem: The parameters of the problem to be solved, raw strings, k, l, etc.
        :param alphabet: The Alphabet object for symbol management.
        """
        self.alphabet = alphabet
        self.k = k
        self.l = l
        self.words = [Word.from_string(string=s, alphabet=self.alphabet, k=self.k, l=self.l) for s in strings]
        self.sacs = list()
        self.sacs_to_solve = list()

        for i, w in enumerate(self.words):
            w.original_string = strings[i]

        for w in self.words[:-1]:
            sacs_in_word = set(w)
            for sac in sacs_in_word:
                if self.alphabet.get_symbol(sac.symbol) in self.alphabet.variables and sac not in self.sacs_to_solve:
                    self.sacs_to_solve.append(sac)
                if sac not in self.sacs:
                    self.sacs.append(sac)