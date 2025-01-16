from typing import List, Union

class SaC:
    def __init__(self, left_context: List[int], symbol: int, right_context: List[int]):
        """
        Initialize a SymbolAndContext (SaC) object.

        :param left_context: List of IDs representing the left context.
        :param symbol: The central symbol as an ID.
        :param right_context: List of IDs representing the right context.
        """
        self.left_context = left_context
        self.symbol = symbol
        self.right_context = right_context

    def __eq__(self, other):
        if not isinstance(other, SaC):
            return False
        return (
                self.left_context == other.left_context and
                self.symbol == other.symbol and
                self.right_context == other.right_context
        )

    def __hash__(self):
        return hash((tuple(self.left_context), self.symbol, tuple(self.right_context)))

    def __repr__(self) -> str:
        """Provide a string representation for debugging and visualization."""
        return (
            f"SymbolAndContext("
            f"left_context={self.left_context}, "
            f"symbol={self.symbol}, "
            f"right_context={self.right_context})"
        )

    @staticmethod
    def from_string(string: str, mapping: dict) -> 'SaC':
        """
        Create a SymbolAndContext object from a string and a mapping of characters to IDs.

        :param string: A string in the format 'L_S_R' where:
                       L = left context as a sequence of characters (no spaces).
                       S = single central character (the symbol).
                       R = right context as a sequence of characters (no spaces).
        :param mapping: Dictionary mapping characters to IDs.
        :return: A SymbolAndContext object.
        """
        parts = string.split('_')
        if len(parts) != 3:
            raise ValueError("String format must be 'L_S_R'")
        left_context = [mapping[char] for char in parts[0]]
        symbol = mapping[parts[1]]
        right_context = [mapping[char] for char in parts[2]]
        return SaC(left_context, symbol, right_context)

    def to_string(self, reverse_mapping: dict) -> str:
        """
        Convert a SymbolAndContext object to a string representation.

        :param reverse_mapping: Dictionary mapping IDs back to characters.
        :return: String representation in the format 'L_S_R'.
        """
        left_str = ''.join(reverse_mapping[id_] for id_ in self.left_context)
        symbol_str = reverse_mapping[self.symbol]
        right_str = ''.join(reverse_mapping[id_] for id_ in self.right_context)
        return f"{left_str}_{symbol_str}_{right_str}"
