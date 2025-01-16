from typing import List, Dict

from WordsAndSymbols.SaC import SaC


class Word:
    def __init__(self, sac_list: List[SaC]):
        """
        Initialize a Word object as a collection of SaC objects.

        :param sac_list: List of SaC objects representing the word.
        """
        self.sac_list = sac_list
        self.parameters = [{} for _ in sac_list]  # Dictionary of parameters for each position
        self.sac_counts = self._count_sacs()

    def __len__(self) -> int:
        """Return the number of symbols (SaCs) in the word."""
        return len(self.sac_list)

    def __getitem__(self, index: int) -> SaC:
        """Get the SaC object at the specified index."""
        return self.sac_list[index]

    def __repr__(self) -> str:
        """Provide a string representation of the Word for debugging."""
        return f"Word({self.sac_list})"

    def to_string(self, reverse_mapping: Dict[int, str]) -> str:
        """
        Convert the Word object to a string representation.

        :param reverse_mapping: Dictionary mapping IDs back to characters.
        :return: A string representation of the entire word.
        """
        parts = []
        for sac in self.sac_list:
            symbol_str = reverse_mapping[sac.symbol]
            if len(symbol_str) > 1:
                parts.append(f"_{symbol_str}_")
            else:
                parts.append(symbol_str)
        return ''.join(parts)

    @staticmethod
    def from_string(string: str, mapping: Dict[str, int]) -> 'Word':
        """
        Create a Word object from a string and a character-to-ID mapping.

        :param string: A string representation of the word, where individual
                       SaC objects are either concatenated or separated by underscores.
        :param mapping: Dictionary mapping characters to IDs.
        :return: A Word object.
        """
        sac_list = []
        i = 0
        while i < len(string):
            if string[i] == '_':
                # Multi-character symbol
                end = string.find('_', i + 1)
                if end == -1:
                    raise ValueError("Malformed string with unmatched underscores.")
                multi_char_symbol = string[i + 1:end]
                if multi_char_symbol not in mapping:
                    raise ValueError(f"Unknown symbol: {multi_char_symbol}")
                sac_list.append(SaC([], mapping[multi_char_symbol], []))  # Contexts will need to be added separately
                i = end + 1
            else:
                single_char_symbol = string[i]
                if single_char_symbol not in mapping:
                    raise ValueError(f"Unknown symbol: {single_char_symbol}")
                sac_list.append(SaC([], mapping[single_char_symbol], []))
                i += 1
        return Word(sac_list)

    def add_sac(self, sac: SaC):
        """Add a SaC object to the word."""
        self.sac_list.append(sac)
        self.parameters.append({})  # Add a new dictionary for the new position
        self.sac_counts = self._count_sacs()

    def find_by_symbol(self, symbol_id: int) -> List[int]:
        """
        Find all indices where the given symbol ID appears in the word.

        :param symbol_id: The symbol ID to search for.
        :return: A list of indices where the symbol appears.
        """
        return [i for i, sac in enumerate(self.sac_list) if sac.symbol == symbol_id]

    def get_contexts(self, index: int) -> SaC:
        """
        Retrieve the SaC object at the given index.

        :param index: Index of the desired SaC.
        :return: The SaC object at the specified index.
        """
        if 0 <= index < len(self.sac_list):
            return self.sac_list[index]
        raise IndexError("Index out of bounds for Word.")

    def append_word(self, other: 'Word'):
        """
        Append another Word object to this Word.

        :param other: Another Word object.
        """
        self.sac_list.extend(other.sac_list)
        self.parameters.extend(other.parameters)
        self.sac_counts = self._count_sacs()

    def _count_sacs(self) -> Dict[int, int]:
        """
        Count the occurrences of each symbol in the word.

        :return: A dictionary where keys are symbol IDs and values are their counts.
        """
        counts = {}
        for sac in self.sac_list:
            counts[sac.symbol] = counts.get(sac.symbol, 0) + 1
        return counts
