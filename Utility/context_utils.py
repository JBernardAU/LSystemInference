from typing import Tuple

from Utility.string_utils import substrings_from_left, substrings_from_right
from WordsAndSymbols.Alphabet import Alphabet
from WordsAndSymbols.SaC import ANY_SYMBOL, ANY_SYMBOL_ID, EMPTY_SYMBOL

def get_context(string, idx, alphabet, k=-1, l=-1, ignore_list=None):
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
    if ignore_list is None:
        ignore_list = []

    # Helper function to skip ignored symbols
    def skip_ignored(seq):
        return [s for s in seq if s not in ignore_list]

    # Stack to manage branch scoping
    branch_stack = []

    # Target symbol
    symbol = string[idx]
    left_context, right_context = [], []

    # Determine left context
    for i in range(idx - 1, -1, -1):  # Scan backward
        if k != -1 and len(left_context) < k:
            char = string[i]
            if char == "]":
                branch_stack.append("]")
            elif char == "[":
                if branch_stack:
                    branch_stack.pop()
                else:
                    break  # Stop when exiting a branch
            elif not branch_stack and char not in ignore_list:
                left_context.append(alphabet.mappings[char])
        else:
            break


    # Determine right context
    branch_stack = []  # Reset branch stack
    for i in range(idx + 1, len(string)):  # Scan forward
        if l != -1 and len(right_context) < l:
            char = string[i]
            if char == "[":
                branch_stack.append("[")
            elif char == "]":
                if branch_stack:
                    branch_stack.pop()
                else:
                    break  # Stop when exiting a branch
            elif not branch_stack and char not in ignore_list:
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
            if char in alphabet.identity_symbols:
                continue  # Turtle graphics and optionally 'F' do not have context
            lc, s, rc = get_context(string=s, idx=idx, k=-1, l=-1, alphabet=alphabet, ignore_list=alphabet.ignore_list)

            max_i = max(max_i, len(lc)) if lc != [ANY_SYMBOL_ID] else max_i
            max_j = max(max_j, len(rc)) if rc != [ANY_SYMBOL_ID] else max_j

    return max_i, max_j

def histogram_context(strings, alphabet: Alphabet, F_has_identity=True):
    """
    Produce a histogram of every context for each symbol in the alphabet (defined by `mappings`).

    :param strings: List of strings to analyze.
    :param alphabet: Dictionary mapping characters to IDs.
    :param f_has_identity: Whether 'F' is included in the context.
    :return: Dictionary where keys are symbols and values are dictionaries with 'left' and 'right' histograms.
    """
    exclude_symbols = {EMPTY_SYMBOL, ANY_SYMBOL}
    histo_left = {symbol: {} for symbol in alphabet.mappings.keys()
                  if symbol not in alphabet.identity_symbols and symbol not in exclude_symbols}
    histo_right = {symbol: {} for symbol in alphabet.mappings.keys()
                  if symbol not in alphabet.identity_symbols and symbol not in exclude_symbols}

    for s in strings:
        for idx, symbol in enumerate(s):
            if symbol in histo_left:
                # Process left context
                lc = get_context(string=s, index=idx, direction="left", max_depth=-1,
                                 mapping=alphabet.mappings, F_has_identity=F_has_identity)
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

                rc = get_context(string=s, index=idx, direction="right", max_depth=-1,
                                 mapping=alphabet.mappings, F_has_identity=F_has_identity)
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
