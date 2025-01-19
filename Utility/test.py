def determine_context(word, idx, k=-1, l=-1, ignore_list=None):
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
    symbol = word[idx]
    left_context, right_context = [], []

    # Determine left context
    for i in range(idx - 1, -1, -1):  # Scan backward
        char = word[i]
        if char == "]":
            branch_stack.append("]")
        elif char == "[":
            if branch_stack:
                branch_stack.pop()
            else:
                break  # Stop when exiting a branch
        elif not branch_stack and char not in ignore_list:
            left_context.append(char)
            if k != -1 and len(left_context) >= k:
                break

    # Determine right context
    branch_stack = []  # Reset branch stack
    for i in range(idx + 1, len(word)):  # Scan forward
        char = word[i]
        if char == "[":
            branch_stack.append("[")
        elif char == "]":
            if branch_stack:
                branch_stack.pop()
            else:
                break  # Stop when exiting a branch
        elif not branch_stack and char not in ignore_list:
            right_context.append(char)
            if l != -1 and len(right_context) >= l:
                break

    # Reverse left context since it was collected in reverse order
    left_context.reverse()

    # Return results
    return left_context, symbol, right_context


# Example Usage
word = "ABC[+FG]DBA"
idx = 6  # Index of 'G'
ignore_list = ["+", "-"]

# Find context with k=-1 and l=-1
context = determine_context(word, idx, k=-1, l=-1, ignore_list=ignore_list)
print("Left Context:", context[0])
print("Symbol:", context[1])
print("Right Context:", context[2])

idx = 8

# Find context with k=-1 and l=-1
context = determine_context(word, idx, k=-1, l=-1, ignore_list=ignore_list)
print("Left Context:", context[0])
print("Symbol:", context[1])
print("Right Context:", context[2])

# Find context with k=-1 and l=-1
context = determine_context(word, idx, k=3, l=1, ignore_list=ignore_list)
print("Left Context:", context[0])
print("Symbol:", context[1])
print("Right Context:", context[2])
