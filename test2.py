class Word:
    def __init__(self, name, sac_counts):
        """
        Represents a word (or equation) and its associated sacs.

        Args:
            name (str): The name of the word.
            sac_counts (dict): A dictionary where keys are sacs and values are counts or relevance.
        """
        self.name = name
        self.sac_counts = sac_counts


class Problem:
    def __init__(self, words, is_sac_identity):
        """
        Represents the overall problem with a collection of words.

        Args:
            words (list): A list of Word objects.
            is_sac_identity (function): A function to determine if a sac is an identity sac.
        """
        self.evidence = Evidence(words)
        self.is_sac_identity = is_sac_identity


class Evidence:
    def __init__(self, words):
        """
        Holds the list of Word objects.

        Args:
            words (list): A list of Word objects.
        """
        self.words = words


# Core function to find the minimum set of sacs to solve all words
def find_minimum_sacs(problem):
    """
    Finds the minimum set of sacs required to solve all equations.

    Args:
        problem (Problem): The problem containing words and sacs.

    Returns:
        set: The minimum set of sacs needed to solve all words.
    """
    uncovered_words = set(word.name for word in problem.evidence.words)
    selected_sacs = set()
    found_sacs = set()

    # Add all identity sacs to selected_sacs
    for word in problem.evidence.words:
        for sac in word.sac_counts.keys():
            if problem.is_sac_identity(sac):
                selected_sacs.add(sac)

    # Loop until all words are covered
    while uncovered_words:
        # Count how many uncovered words each sac can solve
        sac_coverage = {}
        for word in uncovered_words:
            word_obj = next((w for w in problem.evidence.words if w.name == word), None)
            if word_obj:
                for sac in word_obj.sac_counts.keys():
                    # Only consider sacs that have not already been selected
                    if sac not in selected_sacs and sac not in found_sacs:
                        sac_coverage[sac] = sac_coverage.get(sac, 0) + 1

        # Select the sac that solves the most uncovered words
        if not sac_coverage:
            raise RuntimeError("No valid sac can cover remaining words.")

        best_sac = max(sac_coverage, key=sac_coverage.get)
        selected_sacs.add(best_sac)

        # Remove all words that are now fully covered (explicitly or implicitly)
        while True:
            new_found_sacs = set()
            uncovered_words = {
                word for word in uncovered_words
                if not all(
                    sac in selected_sacs or sac in found_sacs or
                    all(
                        other_sac in selected_sacs or other_sac in found_sacs
                        for other_sac in next(
                            (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
                        )
                        if other_sac != sac
                    )
                    for sac in next(
                        (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
                    )
                ) or new_found_sacs.update(
                    sac for sac in next(
                        (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
                    ) if sac not in selected_sacs and sac not in found_sacs
                )
            }
            if new_found_sacs:
                found_sacs.update(new_found_sacs)
            else:
                break

    return selected_sacs


# Core function to find the smallest p-space of sacs
def find_smallest_pspace(problem, min_length, max_length):
    """
    Finds the smallest p-space of sacs to solve all equations.

    Args:
        problem (Problem): The problem containing words and sacs.
        min_length (dict): A dictionary mapping each sac to its minimum length.
        max_length (dict): A dictionary mapping each sac to its maximum length.

    Returns:
        tuple: A set of sacs that minimizes the p-space and the p-space product.
    """
    uncovered_words = set(word.name for word in problem.evidence.words)
    selected_sacs = set()
    found_sacs = set()

    # Add all identity sacs to selected_sacs
    for word in problem.evidence.words:
        for sac in word.sac_counts.keys():
            if problem.is_sac_identity(sac):
                selected_sacs.add(sac)

    total_product = 1

    # Loop until all words are covered
    while uncovered_words:
        # Evaluate the impact of adding each sac to the solution
        best_sac = None
        best_increase = float('inf')

        for sac in min_length.keys():
            if sac in selected_sacs or sac in found_sacs:
                continue  # Already selected or found

            # Compute range product increase
            range_size = max_length[sac] - min_length[sac] + 1
            new_product = total_product * range_size

            # Count how many uncovered words this sac can solve
            covers = sum(1 for word in uncovered_words if sac in next(
                (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
            ))

            # Heuristic: prioritize sacs that solve more words with minimal range impact
            if covers > 0 and new_product < best_increase:
                best_sac = sac
                best_increase = new_product

        # Add the best sac to the solution
        selected_sacs.add(best_sac)
        total_product = best_increase

        # Remove all words that are now fully covered (explicitly or implicitly)
        while True:
            new_found_sacs = set()
            uncovered_words = {
                word for word in uncovered_words
                if not all(
                    sac in selected_sacs or sac in found_sacs or
                    all(
                        other_sac in selected_sacs or other_sac in found_sacs
                        for other_sac in next(
                            (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
                        )
                        if other_sac != sac
                    )
                    for sac in next(
                        (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
                    )
                ) or new_found_sacs.update(
                    sac for sac in next(
                        (w.sac_counts.keys() for w in problem.evidence.words if w.name == word), []
                    ) if sac not in selected_sacs and sac not in found_sacs
                )
            }
            if new_found_sacs:
                found_sacs.update(new_found_sacs)
            else:
                break

    return selected_sacs, total_product


# Example Usage
if __name__ == "__main__":
    # Example data
    words = [
        Word("word1", {"A": 1, "B": 2, "C": 3}),
        Word("word2", {"A": 1, "B": 4, "D": 4}),
        Word("word3", {"C": 2, "B": 3, "D": 4}),
    ]


    def is_sac_identity(sac):
        return sac == "B"


    problem = Problem(words, is_sac_identity)
    min_length = {"A": 2, "B": 1, "C": 3, "D": 5}
    max_length = {"A": 5, "B": 7, "C": 6, "D": 8}

    # Find minimum sacs
    min_sacs = find_minimum_sacs(problem)
    print("Minimum set of sacs:", min_sacs)

    # Find smallest p-space
    smallest_pspace, pspace_product = find_smallest_pspace(problem, min_length, max_length)
    print("Smallest p-space set of sacs:", smallest_pspace)
    print("P-space product:", pspace_product)
