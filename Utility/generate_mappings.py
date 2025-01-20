from LSystems import InferenceProblem


def generate_mappings(problem: InferenceProblem):
    """
    Generate a mapping dictionary for unique symbols in strings and identify turtle graphics symbols.

    Args:
        problem: The source from which to determine the mappings. It provides the identities, ignore list and the
        raw strings.

    Returns:
        tuple: A tuple containing:
            - mapping (dict): A dictionary mapping unique symbols to unique integers.
    """
    # Define the default turtle graphics symbols
    # Iterate through each string to process symbols
    unique_symbols = set()

    for s in problem.strings:
        for char in s:
            if char not in problem.identities and char not in problem.ignore_list and char not in unique_symbols:
                unique_symbols.add(char)

    # Create a mapping dictionary for unique symbols
    mapping = {symbol: idx for idx, symbol in enumerate(sorted(unique_symbols))}

    return mapping

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
