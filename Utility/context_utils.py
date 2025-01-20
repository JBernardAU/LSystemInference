import math
from typing import Tuple

from Utility.analysis_utils import calculate_modified_weighted_mean
from Utility.string_utils import substrings_from_left, substrings_from_right
#from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import ANY_SYMBOL, ANY_SYMBOL_ID, EMPTY_SYMBOL

def get_context(string, index, alphabet, k=-1, l=-1):
    """
    Determine the context of a symbol in an L-system string.

    Parameters:
    - word (str): The L-system string.
    - idx (int): The index of the target symbol in the string.
    - k (int): The maximum length of the left context (-1 for longest possible).
    - l (int): The maximum length of the right context (-1 for longest possible).
    - ignore_list (list): A list of symbols to ignore when determining context.

    Returns:
    - tuple: (left_context, symbol, right_context) where:
      - left_context (list): The left context symbols.
      - symbol (str): The target symbol.
      - right_context (list): The right context symbols.
    """
    # Helper function to skip ignored symbols
    def skip_ignored(seq):
        return [s for s in seq if s not in alphabet.ignore_list]

    # Stack to manage branch scoping
    branch_stack = []

    # Target symbol
    symbol = string[index]
    left_context, right_context = [], []

    # Determine left context
    for i in range(index - 1, -1, -1):  # Scan backward
        if k == -1 or len(left_context) < k:
            char = string[i]
            if char == "]":
                branch_stack.append("]")
            elif char == "[":
                if branch_stack:
                    branch_stack.pop()
                else:
                    break  # Stop when exiting a branch
            elif not branch_stack and char not in alphabet.ignore_list:
                left_context.append(alphabet.mappings[char])
        else:
            break


    # Determine right context
    branch_stack = []  # Reset branch stack
    for i in range(index + 1, len(string)):  # Scan forward
        if l == -1 or len(right_context) < l:
            char = string[i]
            if char == "[":
                branch_stack.append("[")
            elif char == "]":
                if branch_stack:
                    branch_stack.pop()
                else:
                    break  # Stop when exiting a branch
            elif not branch_stack and char not in alphabet.ignore_list:
                right_context.append(alphabet.mappings[char])
        else:
            break


    # Reverse left context since it was collected in reverse order
    left_context.reverse()

    if not left_context : left_context = [ANY_SYMBOL_ID]
    if not right_context : right_context = [ANY_SYMBOL_ID]

    # Return results
    return left_context, symbol, right_context

def determine_context_depth(strings, alphabet) -> Tuple[int, int]:
    """
    Determine the longest possible left and right context depths.

    :return: A tuple of (max_i, max_j).
    """
    max_i, max_j = 0, 0

    for s in strings:
        for idx, char in enumerate(s):
            if char in alphabet.identities:
                continue  # Turtle graphics and optionally 'F' do not have context
            lc, s, rc = get_context(string=s, index=idx, k=-1, l=-1, alphabet=alphabet)

            max_i = max(max_i, len(lc)) if lc != [ANY_SYMBOL_ID] else max_i
            max_j = max(max_j, len(rc)) if rc != [ANY_SYMBOL_ID] else max_j

    return max_i, max_j

def histogram_context(strings, alphabet):
    """
    Produce a histogram of every context for each symbol in the alphabet (defined by `mappings`).

    :param strings: List of strings to analyze.
    :param alphabet: Dictionary mapping characters to IDs.
    :return: Dictionary where keys are symbols and values are dictionaries with 'left' and 'right' histograms.
    """
    histo_left = {symbol: {} for symbol in alphabet.mappings.keys()
                  if symbol not in alphabet.ignore_list}
    histo_right = {symbol: {} for symbol in alphabet.mappings.keys()
                  if symbol not in alphabet.ignore_list}

    for s in strings:
        for idx, symbol in enumerate(s):
            if symbol in histo_left:
                # Process left context
                lc, _, _= get_context(string=s, index=idx, alphabet=alphabet, k=-1, l=-1)
                if lc != [ANY_SYMBOL_ID] and lc != [ANY_SYMBOL]:
                    subs = substrings_from_right(alphabet.ids_to_string(lc, True, True))
                    #for ss in subs:
                    #    if ss in histo_left[symbol]:
                    #        histo_left[symbol][ss] += 1
                    #    else:
                    #        histo_left[symbol][ss] = 1

                    for ss in subs:
                        if len(ss) in histo_left[symbol]:
                            histo_left[symbol][len(ss)] += 1
                        else:
                            histo_left[symbol][len(ss)] = 1

                _, _ , rc = get_context(string=s, index=idx, alphabet=alphabet, k=-1, l=-1)
                if rc != [ANY_SYMBOL_ID] and rc != [ANY_SYMBOL]:
                    subs = substrings_from_left(alphabet.ids_to_string(rc, True, True))
                    #for ss in subs:
                    #    if ss in histo_right[symbol]:
                    #        histo_right[symbol][ss] += 1
                    #    else:
                    #        histo_right[symbol][ss] = 1
                    for ss in subs:
                        if len(ss) in histo_right[symbol]:
                            histo_right[symbol][len(ss)] += 1
                        else:
                            histo_right[symbol][len(ss)] = 1


    return histo_left, histo_right

def infer_context_size(strings, alphabet):
    histo_left, histo_right = histogram_context(strings=strings, alphabet=alphabet)
    i = 0
    j = 0
    for symbol in histo_left:
        hl = dict(sorted(histo_left[symbol].items(), key=lambda item: item[1], reverse=True))
        lengths = list(hl.keys())
        frequencies = list(hl.values())
        # i.append(calculate_weighted_mean(lengths, frequencies))
        i = math.ceil(max(i, calculate_modified_weighted_mean(lengths, frequencies)))

        hr = dict(sorted(histo_right[symbol].items(), key=lambda item: item[1], reverse=True))
        lengths = list(hr.keys())
        frequencies = list(hr.values())
        # j.append(calculate_weighted_mean(lengths, frequencies))
        j = math.ceil(max(j, calculate_modified_weighted_mean(lengths, frequencies)))

    print(f"i = {i} | j = {j}")
    return i, j
