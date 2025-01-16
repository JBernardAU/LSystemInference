from typing import Dict, Set

class Alphabet:
    def __init__(self, mappings: Dict[str, int], identity_symbols: Set[str] = None):
        """
        Initialize an Alphabet object.

        :param mappings: Dictionary mapping symbols (characters) to unique IDs.
        :param identity_symbols: Set of symbols considered identity by default (e.g., 'F', '+', '-', '[', ']').
        """
        self.mappings = mappings
        self.reverse_mappings = {v: k for k, v in mappings.items()}
        self.identity_symbols = identity_symbols or {"F", "+", "-", "[", "]"}
        self.homomorphisms = {id_: id_ for id_ in mappings.values()}  # By default, each symbol maps to itself

    def add_symbol(self, symbol: str, id_: int):
        """Add a new symbol and its ID to the alphabet."""
        if symbol in self.mappings or id_ in self.reverse_mappings:
            raise ValueError("Symbol or ID already exists in the alphabet.")
        self.mappings[symbol] = id_
        self.reverse_mappings[id_] = symbol
        self.homomorphisms[id_] = id_

    def set_homomorphism(self, from_symbol: str, to_symbol: str):
        """
        Define a homomorphism between two symbols.

        :param from_symbol: The symbol to be mapped.
        :param to_symbol: The symbol it maps to.
        """
        if from_symbol not in self.mappings or to_symbol not in self.mappings:
            raise ValueError("Both symbols must exist in the alphabet.")
        from_id = self.mappings[from_symbol]
        to_id = self.mappings[to_symbol]
        self.homomorphisms[from_id] = to_id

    def get_id(self, symbol: str) -> int:
        """Get the ID of a symbol."""
        return self.mappings.get(symbol)

    def get_symbol(self, id_: int) -> str:
        """Get the symbol corresponding to an ID."""
        return self.reverse_mappings.get(id_)

    def get_context(self, string, index, direction, max_depth, include_f):
        """
        Get the context for a symbol at a given index.

        :param string: The full string.
        :param index: Current index in the string.
        :param direction: "left" or "right".
        :param max_depth: Maximum number of symbols to include in the context.
        :param include_f: Whether to include 'F' in the context.
        :return: List of IDs representing the context.
        """
        char = string[index]
        if char in "+-[]" or (char == "F" and not include_f):
            # Turtle symbols and excluded 'F' always have empty context
            return []

        step = -1 if direction == "left" else 1
        context = []
        depth = 0
        i = index + step

        while 0 <= i < len(string) and depth < max_depth:
            next_char = string[i]
            if next_char in "[]":  # Stop at brackets
                break
            if next_char not in "+-[]" and (include_f or next_char != "F"):
                context.append(self.get_id(next_char))
                depth += 1
            i += step

        if direction == "left":
            context.reverse()
        return context

    def is_identity(self, symbol_or_id: str or int) -> bool:
        """Check if a symbol or ID is an identity symbol."""
        if isinstance(symbol_or_id, str):
            symbol_or_id = self.mappings.get(symbol_or_id)
        return symbol_or_id is not None and self.reverse_mappings[symbol_or_id] in self.identity_symbols

    def apply_homomorphism(self, id_: int) -> int:
        """Apply the homomorphism mapping to an ID."""
        return self.homomorphisms.get(id_, id_)

    def view_with_homomorphism(self) -> Dict[int, int]:
        """View the homomorphism mappings."""
        return self.homomorphisms

    def __repr__(self):
        """Provide a string representation of the Alphabet object."""
        return (
            f"Alphabet(mappings={self.mappings}, identity_symbols={self.identity_symbols}, "
            f"homomorphisms={self.homomorphisms})"
        )
