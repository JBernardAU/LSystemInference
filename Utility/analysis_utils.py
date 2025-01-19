# Weighted Mean
def calculate_weighted_mean(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = sum(y)
    return numerator / denominator

# Modified Weighted Mean with Length Penalty
def calculate_modified_weighted_mean(x, y):
    numerator = sum((b / a) * a for a, b in zip(x, y))
    denominator = sum(b / a for a, b in zip(x, y))
    return numerator / denominator
