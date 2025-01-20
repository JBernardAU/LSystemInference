import numpy as np

from LSystems.InferenceProblem import InferenceProblem


def analyze_words_growth(problem: InferenceProblem):
    num_sacs = len(problem.evidence.sacs_to_solve)
    num_words = len(problem.evidence.words)
    num_symbols = len(problem.evidence.alphabet.variables) + len(problem.evidence.alphabet.identities)

    # P: Matrix representing the predecessor words
    # S: Matrix representing the successor words
    # G: The growth matrix
    P = np.zeros((num_words-1, num_sacs), dtype=int)
    S = np.zeros((num_words-1, num_symbols), dtype=int)

    # set up the P matrix
    # Only include SaCs that need to be solved
    for row, w in enumerate(problem.evidence.words[:-1]):
        for col, sac in enumerate(problem.evidence.sacs_to_solve):
            if sac in w.sac_counts:
                P[row, col] += w.sac_counts[sac]

    # set up the S matrix
    # Since identity symbols are not in the P matrix (as their rules are known)
    # The S matrix must only include unaccounted for growth
    for iWord, w in enumerate(problem.evidence.words[1:]):
        for symbol in problem.evidence.alphabet.symbols:
            S[iWord,problem.evidence.alphabet.get_id(symbol)] = problem.MAO.word_unaccounted_growth[iWord][problem.evidence.alphabet.get_id(symbol)]

    G = solve_matrix_equation(P,S)

    return G

def analyze_words_length(problem: InferenceProblem):
    num_sacs = len(problem.evidence.sacs_to_solve)
    num_words = len(problem.evidence.words)

    # P: Matrix representing the predecessor words
    # S: Matrix representing the successor words
    # L: The length matrix
    P = np.zeros((num_words-1, num_sacs), dtype=int)
    S = np.zeros((num_words-1, 1), dtype=int)

    # set up the P matrix
    # Only include SaCs that need to be solved
    for row, w in enumerate(problem.evidence.words[:-1]):
        for col, sac in enumerate(problem.evidence.sacs_to_solve):
            if sac in w.sac_counts:
                P[row, col] += w.sac_counts[sac]

    for row, w in enumerate(problem.evidence.words[1:]):
        S[row, 0] += problem.MAO.word_unaccounted_length[row]

    N = solve_matrix_equation(P,S)

    return N

def solve_matrix_equation(P, S):
    """
    Solves the matrix equation P x N = S for N.

    Parameters:
        P (numpy.ndarray): The predecessor matrix
        S (numpy.ndarray): The successor matrix

    Returns:
        N (numpy.ndarray): The solution matrix (n x p).
    """
    try:
        # Check if M is square
        if P.shape[0] == P.shape[1]:  # Square matrix
            # Check if M is invertible
            if np.linalg.det(P) != 0:
                # Solve using the inverse
                N = np.floor(np.round(np.linalg.inv(P) @ S, decimals=6)).astype(int)
                return N
            else:
                print("      Matrix P is singular and cannot be inverted.")
    except np.linalg.LinAlgError as e:
        print(f"Linear algebra error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def solve_matrix_equation2(M, A, N):
    """
    Solves the matrix equation M x N = A for N, taking into account that -1 in N means unknown,
    but any other value (0 or greater) means known.

    Parameters:
        M (numpy.ndarray): The known matrix (m x n).
        A (numpy.ndarray): The resulting matrix (m x p).
        N (numpy.ndarray): The solution matrix (n x p), where -1 indicates unknown values.

    Returns:
        N (numpy.ndarray): The updated solution matrix (n x p) with solved values for unknowns.
    """
    try:
        # Identify known and unknown values in N
        mask_known = (N >= 0)  # True for known values, False for unknowns

        # Initialize the solution matrix
        N_solution = N.copy()

        # Subtract the contribution of known values from A
        if np.any(mask_known):
            A_adjusted = A - M @ (N_solution * mask_known)
        else:
            A_adjusted = A

        # Solve for the unknown values using pseudo-inverse
        mask_unknown = ~mask_known
        M_reduced = M[:, mask_unknown.any(axis=0)]  # Extract columns corresponding to unknowns

        # Solve only for unknowns
        N_unknown = np.linalg.pinv(M_reduced) @ A_adjusted

        # Update the solution matrix
        N_solution[mask_unknown] = N_unknown

        # Ensure all values are non-negative integers
        N_solution = np.maximum(0, np.floor(N_solution).astype(int))

        return N_solution

    except np.linalg.LinAlgError as e:
        print(f"Linear algebra error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    # Replace these with your code to fill in M and A
    M = np.array([[1, 2], [3, 4]])  # Example M (2x2)
    A = np.array([[5, 6], [7, 8]])  # Example A (2x2)

    # Solve for N
    N = solve_matrix_equation(M, A)
    print("Solution Matrix N:")
    print(N)