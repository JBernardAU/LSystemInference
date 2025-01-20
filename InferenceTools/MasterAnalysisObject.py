import copy


class MasterAnalysisObject:
    def __init__(self, problem):
        """
        Initialize the MasterAnalysisObject.

        Parameters:
        - evidence: An object containing a list of words.
        - problem: An object containing sacs_to_solve (list of sacs) and alphabet (with mappings dictionary).
        """
        self.problem = problem
        self.flag = True

        self.min_growth = []
        self.max_growth = []
        self.min_lengths = []
        self.max_lengths = []
        self.fragments = []  # List of Fragment objects

        # These numbers get calculated a LOT so store them makes life easier
        self.num_symbols = len(self.problem.evidence.alphabet.symbols)
        self.num_sacs = len(self.problem.evidence.sacs)
        self.num_words = len(self.problem.evidence.words)

        # Initialize N x M' matrices with zeros
        self.min_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_sacs)]
        self.max_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_sacs)]

        self.min_length = [0 for _ in range(self.num_sacs)]
        self.max_length = [0 for _ in range(self.num_sacs)]

        self.word_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_words-1)]
        self.word_unaccounted_growth = [[0 for _ in range(self.num_symbols)] for _ in range(self.num_words-1)]
        self.word_unaccounted_length = [0 for _ in range(self.num_words-1)]

        # Conduct Naive/Initial analysis
        self.naive_min_max()
        self.compute_word_growth()

        # Initialize Unaccounted Growth & Length
        self.compute_unaccounted_growth()
        self.compute_unaccounted_length()
        self.problem.MAO = self

    def set_min_growth(self, sac, symbol, value):
        pass

    def set_max_growth(self, sac, symbol, value):
        pass

    def set_min_length(self, sac, symbol, value):
        pass

    def set_max_length(self, sac, symbol, value):
        pass

    def compute_word_growth(self):
        """
        Compute the growth of words by analyzing the frequency of symbols
        in subsequent words within the evidence data.

        This function iterates through each word in the `problem.evidence.words` list (excluding the last word).
        For each symbol in the alphabet, it counts the occurrences of the symbol in the next word's
        `original_string`. The count is then stored in the `word_growth` attribute, indexed by the
        current word's index and the symbol's unique ID in the alphabet.
        """
        for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            for symbol in self.problem.evidence.alphabet.symbols:
                count = self.problem.evidence.words[iWord+1].original_string.count(symbol)
                self.word_growth[iWord][self.problem.evidence.alphabet.get_id(symbol)] = count

    def compute_unaccounted_growth(self):
        """
        Compute the unaccounted growth of symbols for each word in the evidence data.

        This function calculates the difference between the total growth of a symbol in a word
        and the growth of the symbol that can be attributed to specific structures (SACs).

        For each symbol in the alphabet and each word (excluding the last word):
            - Calculate the accounted growth of the symbol in the word based on SAC counts.
            - Subtract the accounted growth from the total growth to determine the unaccounted growth.
        """
        for symbol in self.problem.evidence.alphabet.symbols:
            for iWord, w in enumerate(self.problem.evidence.words[:-1]):
                accounted_growth_of_symbol_in_word = 0
                for iSaC, sac in enumerate(self.problem.evidence.sacs):
                    if sac in w.sac_counts:
                        min_growth_of_symbol_by_sac = self.min_growth[iSaC][
                            self.problem.evidence.alphabet.get_id(symbol)]
                        sac_count = w.sac_counts[sac]
                        accounted_growth_of_symbol_in_word += min_growth_of_symbol_by_sac * sac_count
                self.word_unaccounted_growth[iWord][self.problem.evidence.alphabet.get_id(symbol)] = (self.word_growth[iWord][self.problem.evidence.alphabet.get_id(symbol)] - accounted_growth_of_symbol_in_word)

    def compute_unaccounted_length(self):
        """
        Compute the unaccounted length for each word in the evidence data.

        This function calculates the difference between the total length of the next word
        and the length that can be attributed to specific structures (SACs).

        For each word (excluding the last word):
            - Calculate the accounted length based on SAC counts and their minimum lengths.
            - Subtract the accounted length from the total length of the next word to determine
              the unaccounted length.
        """
        for iWord, w in enumerate(self.problem.evidence.words[:-1]):
            accounted_length_in_word = 0
            for iSaC, sac in enumerate(self.problem.evidence.sacs):
                if sac in w.sac_counts:
                    min_length_by_sac = self.min_length[iSaC]
                    sac_count = w.sac_counts[sac]
                    accounted_length_in_word += min_length_by_sac * sac_count
            self.word_unaccounted_length[iWord] = len(self.problem.evidence.words[iWord+1]) - accounted_length_in_word

    def naive_min_max(self):
        """
        This function processes the evidence from the `problem` object, updating matrices that track the
        minimum and maximum growth and length associated with each `sac` (Symbolic Alphabet Component). The
        computation depends on whether each `sac` belongs to the set of `identities` or not.

        Key steps include:
        - Setting `min_growth` and `max_growth` for each `sac` based on its presence in `identities`.
        - Determining `min_length` and `max_length` based on the shortest word length following the appearance
          of a `sac` in the provided list of evidence words.
        """
        sacs = self.problem.evidence.sacs
        identities = self.problem.evidence.alphabet.identities_ids
        naive_min = self.problem.absolute_min_length

        # Compute min and max growth
        for iSac, sac in enumerate(sacs):
            if sac.symbol in identities:
                self.min_growth[iSac][sac.symbol] = 1
                self.max_growth[iSac][sac.symbol] = 1
            else:
                self.min_growth[iSac][sac.symbol] = 0
                self.max_growth[iSac][sac.symbol] = 0

        shortest_word_length = max(len(word) for word in self.problem.evidence.words[1:])

        for iSac, sac in enumerate(sacs):
            if sac.symbol in identities:
                self.min_length[iSac] = 1
                self.max_length[iSac] = 1
            else:
                # find the shortest word after the sac appears
                for iWord, w in enumerate(self.problem.evidence.words[:-1]):
                    if sac in w.sac_list:
                        shortest_word_length = len(self.problem.evidence.words[iWord+1])
                self.min_length[iSac] = naive_min
                self.max_length[iSac] = shortest_word_length