from typing import List, Union

ANY_SYMBOL = "*"
EMPTY_SYMBOL = "λ"
MULTICHAR_SYMBOL = "_"
ANY_SYMBOL_ID = -1  # Special ID for AnySymbol
EMPTY_SYMBOL_ID = -2  # Special ID for EmptySymbol
MULTICHAR_SYMBOL_ID = -3  # Special ID for Multchar_Symbol

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

        def match_context(ctx1, ctx2):
            # Empty list matches AnySymbol or EmptySymbol
            if not ctx1 or ctx1 == [ANY_SYMBOL_ID] or ctx1 == [EMPTY_SYMBOL_ID]:
                return not ctx2 or ctx2 == [ANY_SYMBOL_ID] or ctx2 == [EMPTY_SYMBOL_ID]
            return ctx1 == ctx2

        def match_symbol(sym1, sym2):
            # AnySymbol matches any symbol
            return sym1 == sym2 or sym1 == ANY_SYMBOL_ID or sym2 == EMPTY_SYMBOL_ID

        return (
                match_context(self.left_context, other.left_context) and
                match_symbol(self.symbol, other.symbol) and
                match_context(self.right_context, other.right_context)
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

    def _match_symbol(self, sym1: int, sym2: int) -> bool:
        """
        Check if two symbols match, considering AnySymbol and EmptySymbol.

        :param sym1: The first symbol ID.
        :param sym2: The second symbol ID.
        :return: True if the symbols match, False otherwise.
        """
        return sym1 == sym2 or sym1 == ANY_SYMBOL_ID or sym2 == ANY_SYMBOL_ID

    def _match_context(self, ctx1: List[int], ctx2: List[int]) -> bool:
        """
        Check if two contexts match, considering AnySymbol and EmptySymbol.

        :param ctx1: The first context (list of IDs).
        :param ctx2: The second context (list of IDs).
        :return: True if the contexts match, False otherwise.
        """
        if not ctx1 and not ctx2:
            return True
        if not ctx1 or not ctx2:
            return False
        if ctx1 == [EMPTY_SYMBOL] or ctx2 == [EMPTY_SYMBOL]:
            return True
        return ctx1 == ctx2

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
        left_context = [mapping[char] for char in parts[0] if char in mapping]
        symbol = mapping[parts[1]]
        right_context = [mapping[char] for char in parts[2] if char in mapping]
        return SaC(left_context, symbol, right_context)

    def to_string(self, reverse_mapping: dict) -> str:
        """
        Convert a SymbolAndContext object to a string representation.

        :param reverse_mapping: Dictionary mapping IDs back to characters.
        :return: String representation in the format 'L_S_R'.
        """
        left_str = ''.join(reverse_mapping[id_] for id_ in self.left_context if id_ != self.EMPTY_SYMBOL)
        symbol_str = reverse_mapping[self.symbol]
        right_str = ''.join(reverse_mapping[id_] for id_ in self.right_context if id_ != self.EMPTY_SYMBOL)
        return f"{left_str}_{symbol_str}_{right_str}"
