from WordsAndSymbols.SaC import ANY_SYMBOL


def get_context(string, index, direction, max_depth, mapping, include_f=True):
    """
    Extract context around a character at a given index.

    :param string: The input string.
    :param index: Index of the central character.
    :param direction: "left" or "right" for context direction.
    :param max_depth: Maximum depth for context extraction.
    :param mapping: Dictionary mapping characters to IDs.
    :param include_f: Whether to include 'F' in the context.
    :return: List of IDs representing the context. Returns [AnySymbol] if no valid context.
    """
    step = -1 if direction == "left" else 1
    context = []
    depth = 0
    cursor = index + step

    while 0 <= cursor < len(string) and depth < max_depth:
        char = string[cursor]
        if char in "[]":  # Stop at brackets
            break
        if char not in "+-[]" and (include_f or char != "F"):
            context.append(mapping[char])
            depth += 1
        cursor += step

    if direction == "left":
        context.reverse()  # Ensure left context is in the correct order

    # Return AnySymbol if the context is empty
    return context if context else [mapping[ANY_SYMBOL]]
