def substrings_from_left(s):
    """Generate substrings starting from the left."""
    return [s[:i] for i in range(1, len(s) + 1)]

def substrings_from_right(s):
    """Generate substrings starting from the right."""
    return [s[-i:] for i in range(1, len(s) + 1)][::-1]