class Fragment:
    def __init__(self, frag, is_true=False):
        """
        Initialize a Fragment with optional string and truth value.
        """
        self.fragment = frag
        self.is_true = is_true


class FragmentSigned(Fragment):
    def __init__(self, frag, is_true=False, left_signature="", right_signature=""):
        """
        Initialize a FragmentSigned, inheriting from Fragment.
        """
        super().__init__(frag, is_true)
        self.left_signature = left_signature
        self.right_signature = right_signature
        self.uncertain = []  # List of associated FragmentSigned objects
        self.sac_count = 0

    def compute_sac_count(self, s):
        """
        Count occurrences of a symbol 's' in the left and right signatures.
        """
        self.sac_count = self.left_signature.count(s) + self.right_signature.count(s)

    def update(self, frag):
        """
        Update the fragment with a new string.
        """
        self.fragment = frag


# Example usage
fragment = Fragment("example", True)
fragment_signed = FragmentSigned(fragment.fragment, fragment.is_true, "abcSabc", "defS")
fragment_signed.compute_sac_count("S")
print(f"SAC Count: {fragment_signed.sac_count}")
fragment_signed.update("updated_example")
print(f"Updated Fragment: {fragment_signed.fragment}")
