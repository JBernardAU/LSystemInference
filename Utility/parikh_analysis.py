import numpy as np

def analyze_words_growth(evidence):
    sacs = []
    for row, w in enumerate(evidence.words[:-1]):
        sacs_in_word = list(set(w))
        sacs = list(set(sacs + sacs_in_word))

    num_sacs = len(sacs)
    num_words = len(evidence.words)
    num_symbols = len(evidence.alphabet.symbols)

    M = np.zeros((num_words-1, num_sacs), dtype=int)
    A = np.zeros((num_words-1, num_symbols), dtype=int)

    for row, w in enumerate(evidence.words[:-1]):
        sacs_in_word = list(set(w))
        for sac in sacs_in_word:
        #for col, sac in enumerate(evidence.alphabet.sacs):
            if sac in w.sac_counts:
                col = sacs.index(sac)
                M[row, col] = w.sac_counts[sac]

    for row, w in enumerate(evidence.words[1:]):
        for sac in evidence.alphabet.sacs:
            if sac in w.sac_counts:
                col = sac.symbol
                A[row, col] += w.sac_counts[sac]

    N = solve_matrix_equation(M,A)

    return N

def analyze_words_length(evidence):
    sacs = []
    for row, w in enumerate(evidence.words[:-1]):
        sacs_in_word = list(set(w))
        sacs = list(set(sacs + sacs_in_word))

    num_sacs = len(sacs)
    num_words = len(evidence.words)
    num_symbols = len(evidence.alphabet.symbols)

    M = np.zeros((num_words-1, num_sacs), dtype=int)
    A = np.zeros((num_words-1, 1), dtype=int)

    for row, w in enumerate(evidence.words[:-1]):
        sacs_in_word = list(set(w))
        for sac in sacs_in_word:
        #for col, sac in enumerate(evidence.alphabet.sacs):
            if sac in w.sac_counts:
                col = sacs.index(sac)
                M[row, col] = w.sac_counts[sac]

    for row, w in enumerate(evidence.words[1:]):
        A[row, 0] += len(w)

    N = solve_matrix_equation(M,A)

    return N

def solve_matrix_equation(M, A):
    """
    Solves the matrix equation M x N = A for N.

    Parameters:
        M (numpy.ndarray): The known matrix (m x n).
        A (numpy.ndarray): The resulting matrix (m x p).

    Returns:
        N (numpy.ndarray): The solution matrix (n x p).
    """
    try:
        # Check if M is square
        if M.shape[0] == M.shape[1]:  # Square matrix
            # Check if M is invertible
            if np.linalg.det(M) != 0:
                # Solve using the inverse
                N = np.floor(np.round(np.linalg.inv(M) @ A, decimals=6)).astype(int)
            else:
                print("Matrix M is singular and cannot be inverted.")
        else:
            # Use the pseudo-inverse for non-square matrices or singular square matrices
            #N = np.linalg.pinv(M) @ A
            N = np.floor(np.round(np.linalg.pinv(M) @ A, decimals=6)).astype(int)
        N = np.maximum(0,np.floor(N).astype(int))
        return N

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