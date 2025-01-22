def find_minimum_sacs(word_sacs):
    """
    Find the minimum set of sacs needed to solve all equations.

    Args:
        word_sacs (dict): A dictionary where keys are words (equations),
                          and values are sets of sacs (variables) involved in the word.

    Returns:
        set: The minimum set of sacs needed to solve all words.
    """
    uncovered_words = set(word_sacs.keys())
    selected_sacs = set()

    # Loop until all words are covered
    while uncovered_words:
        # Count how many uncovered words each sac can solve
        sac_coverage = {}
        for word in uncovered_words:
            for sac in word_sacs[word]:
                sac_coverage[sac] = sac_coverage.get(sac, 0) + 1

        # Select the sac that solves the most uncovered words
        best_sac = max(sac_coverage, key=sac_coverage.get)
        selected_sacs.add(best_sac)

        # Remove all words covered by this sac
        uncovered_words = {
            word for word in uncovered_words if best_sac not in word_sacs[word]
        }

    return selected_sacs

def find_smallest_pspace(word_sacs, min_length, max_length):
    """
    Find the smallest p-space of sacs to solve all equations.

    Args:
        word_sacs (dict): A dictionary where keys are words (equations),
                          and values are sets of sacs (variables) involved in the word.
        min_length (dict): A dictionary mapping each sac to its minimum length.
        max_length (dict): A dictionary mapping each sac to its maximum length.

    Returns:
        set: The set of sacs that minimizes the p-space.
    """
    uncovered_words = set(word_sacs.keys())
    selected_sacs = set()
    total_product = 1

    # Loop until all words are covered
    while uncovered_words:
        # Evaluate the impact of adding each sac to the solution
        best_sac = None
        best_increase = float('inf')

        for sac in min_length.keys():
            if sac in selected_sacs:
                continue  # Already selected

            # Compute range product increase
            range_size = max_length[sac] - min_length[sac] + 1
            new_product = total_product * range_size

            # Count how many uncovered words this sac can solve
            covers = sum(1 for word in uncovered_words if sac in word_sacs[word])

            # Heuristic: prioritize sacs that solve more words with minimal range impact
            if covers > 0 and new_product < best_increase:
                best_sac = sac
                best_increase = new_product

        # Add the best sac to the solution
        selected_sacs.add(best_sac)
        total_product = best_increase

        # Remove all words covered by this sac
        uncovered_words = {
            word for word in uncovered_words if best_sac not in word_sacs[word]
        }

    return selected_sacs, total_product

# Example data
word_sacs = {
    "word1": {"A", "B"},
    "word2": {"A", "B", "C"},
    "word3": {"C", "D"}
}

min_length = {"A": 2, "B": 1, "C": 3, "D": 5}
max_length = {"A": 5, "B": 7, "C": 6, "D": 8}

# Find minimum sacs
min_sacs = find_minimum_sacs(word_sacs)
print("Minimum set of sacs:", min_sacs)

# Find smallest p-space
smallest_pspace, pspace_product = find_smallest_pspace(word_sacs, min_length, max_length)
print("Smallest p-space set of sacs:", smallest_pspace)
print("P-space product:", pspace_product)
