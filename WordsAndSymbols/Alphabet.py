from WordsAndSymbols.SaC import EMPTY_SYMBOL, EMPTY_SYMBOL_ID, ANY_SYMBOL, ANY_SYMBOL_ID


class Alphabet:
    def __init__(self, mappings=None, identity_symbols=None):
        """
        Initialize the Alphabet class with mappings and identity symbols.

        :param mappings: A dictionary mapping symbols to IDs.
        :param identity_symbols: A set of symbols that have identity production rules.
        """
        self.mappings = mappings or {}
        self.reverse_mappings = {v: k for k, v in self.mappings.items()}
        self.identity_symbols = identity_symbols or set()
        self.homomorphisms = {}

        # Add AnySymbol and EmptySymbol to the mappings
        self.mappings.update({EMPTY_SYMBOL: EMPTY_SYMBOL_ID, ANY_SYMBOL: ANY_SYMBOL_ID})  # λ for EmptySymbol, * for AnySymbol
        self.reverse_mappings.update({EMPTY_SYMBOL_ID: EMPTY_SYMBOL, ANY_SYMBOL_ID: ANY_SYMBOL})

    def add_symbol(self, symbol, id_):
        """
        Add a new symbol to the alphabet with its corresponding ID.

        :param symbol: The symbol to add.
        :param id_: The ID to assign to the symbol.
        """
        self.mappings[symbol] = id_
        self.reverse_mappings[id_] = symbol

    def get_id(self, symbol):
        """
        Retrieve the ID for a given symbol.

        :param symbol: The symbol to look up.
        :return: The ID of the symbol.
        """
        return self.mappings.get(symbol, None)

    def get_symbol(self, id_):
        """
        Retrieve the symbol for a given ID.

        :param id_: The ID to look up.
        :return: The symbol corresponding to the ID.
        """
        return self.reverse_mappings.get(id_, None)

    def get_context(self, string, index, direction, max_depth, contextual_F):
        """
        Get the context for a symbol at a given index.

        :param string: The full string.
        :param index: Current index in the string.
        :param direction: "left" or "right".
        :param max_depth: Maximum number of symbols to include in the context.
        :param contextual_F: Whether to include 'F' in the context.
        :return: List of IDs representing the context. If no context exists, AnySymbol is returned.
        """
        char = string[index]
        if char in "+-[]" or (char == "F" and not contextual_F):
            # Turtle symbols and excluded 'F' return AnySymbol context
            return [ANY_SYMBOL_ID]

        step = -1 if direction == "left" else 1
        context = []
        depth = 0
        i = index + step

        while 0 <= i < len(string) and depth < max_depth:
            next_char = string[i]
            if next_char in "[]":  # Stop at brackets
                break
            if next_char not in "+-[]" and (contextual_F or next_char != "F"):
                context.append(self.get_id(next_char))
                depth += 1
            i += step

        if direction == "left":
            context.reverse()  # Ensure left context is in correct order

        # Return AnySymbol if the context is empty
        return context if context else [ANY_SYMBOL_ID]

    def set_homomorphism(self, source_symbol, target_symbol):
        """
        Define a homomorphism mapping from one symbol to another.

        :param source_symbol: The source symbol.
        :param target_symbol: The target symbol.
        """
        source_id = self.get_id(source_symbol)
        target_id = self.get_id(target_symbol)
        if source_id is not None and target_id is not None:
            self.homomorphisms[source_id] = target_id

    def apply_homomorphism(self, id_):
        """
        Apply the homomorphism mapping to an ID.

        :param id_: The ID to transform.
        :return: The transformed ID or the original ID if no mapping exists.
        """
        if self.is_any_symbol(id_) or self.is_empty_symbol(id_):
            return id_  # Do not apply homomorphism to special symbols
        return self.homomorphisms.get(id_, id_)

    def is_any_symbol(self, symbol_id):
        """
        Check if a symbol ID corresponds to AnySymbol (*).

        :param symbol_id: The symbol ID to check.
        :return: True if it is AnySymbol, False otherwise.
        """
        return symbol_id == self.mappings.get("*", None)

    def is_empty_symbol(self, symbol_id):
        """
        Check if a symbol ID corresponds to EmptySymbol (λ).

        :param symbol_id: The symbol ID to check.
        :return: True if it is EmptySymbol, False otherwise.
        """
        return symbol_id == self.mappings.get("λ", None)

    def is_identity(self, symbol):
        """
        Check if a symbol has an identity production rule.

        :param symbol: The symbol to check.
        :return: True if the symbol is an identity, False otherwise.
        """
        return symbol in self.identity_symbols

    def __repr__(self):
        """
        Provide a string representation of the Alphabet for debugging.
        """
        return (
            f"Alphabet(mappings={self.mappings}, "
            f"identity_symbols={self.identity_symbols}, "
            f"homomorphisms={self.homomorphisms})"
        )
