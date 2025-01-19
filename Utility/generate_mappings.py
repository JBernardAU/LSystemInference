def generate_mappings(strings, F_has_identity=False):
    """
    Generate a mapping dictionary for unique symbols in strings and identify turtle graphics symbols.

    Args:
        strings (list of str): A list of strings to process.
        F_has_identity (bool): Whether to treat 'F' as a turtle graphics symbol.

    Returns:
        tuple: A tuple containing:
            - mapping (dict): A dictionary mapping unique symbols to unique integers.
            - identity (set): A set of turtle graphics symbols.
    """
    # Define the default turtle graphics symbols
    turtle_symbols = {"+", "-", "[", "]"}

    if F_has_identity:
        turtle_symbols.add("F")

    unique_symbols = set()
    identity = set()

    # Iterate through each string to process symbols
    for s in strings:
        for char in s:
            if char in turtle_symbols:
                identity.add(char)
            else:
                unique_symbols.add(char)

    # Create a mapping dictionary for unique symbols
    mapping = {symbol: idx for idx, symbol in enumerate(sorted(unique_symbols))}

    return mapping, identity

if __name__ == "__main__":
    strings = ["ABA", "ABABCBABA"]
    mapping, identity = generate_mappings(strings)
    print("Mapping:", mapping)
    print("Identity:", identity)

    # Example with turtle graphics
    strings_with_turtle = ["A+[FB]-C"]
    mapping, identity = generate_mappings(strings_with_turtle, F_has_identity=True)
    print("Mapping:", mapping)
    print("Identity:", identity)
