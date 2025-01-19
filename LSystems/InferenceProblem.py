from typing import List
from WordsAndSymbols.Word import Word

class InferenceProblem():
    def __init__(self, lsystem=None):
        self.strings = []
        self.i = -1
        self.j = -1

        if lsystem is not None:
            self.i = lsystem.k
            self.j = lsystem.l

            for w in lsystem.words:
                self.strings.append(Word.sacs_to_string(w, lsystem.alphabet.reverse_mappings))