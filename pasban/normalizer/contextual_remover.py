import re

from pasban.core.vars import contextual_patterns


class ContextualCleaner:
    """
    Clean text based on predefined contextual patterns.

    Responsibilities:
    - Replace or remove specific phrases efficiently.
    - Preprocess patterns into a dictionary for fast replacement.
    - Avoid repeated regex matching at runtime.

    Attributes:
        patterns (list[str]): List of patterns like ["(حافظ) شیرازی", "(کره) شمالی"].
        replacement_dict (dict[str, str]): Dictionary mapping full patterns to their replacements.
    """

    def __init__(self):
        """
        Initialize the cleaner with a list of contextual patterns.

        Big-O: O(p), p = number of patterns
        """
        self.patterns = contextual_patterns
        self.replacement_dict = self._create_replacement_dict()

    def _create_replacement_dict(self) -> dict[str, str]:
        """
        Build a dictionary for fast pattern replacement.

        Each key is the full pattern (with parentheses replaced by inner text),
        and the value is the simplified text after removing the inner part.

        Returns:
            dict[str, str]: Mapping from full pattern to replacement.

        Big-O: O(p), p = number of patterns
        """
        replacement_dict = {}
        for pattern in self.patterns:
            match = re.search(r'\((.*?)\)', pattern)
            if match:
                inner_text = match.group(1)
                full_pattern = pattern.replace(f"({inner_text})", inner_text)
                # Store the replacement string (remove inner_text from full pattern)
                replacement_dict[full_pattern] = full_pattern.replace(inner_text, '')
        return replacement_dict

    def clean_text(self, text: str) -> str:
        """
        Clean the input text by replacing all patterns found in replacement_dict.

        Args:
            text (str): Input string to be cleaned.

        Returns:
            str: Cleaned text with contextual patterns removed.

        Big-O: O(p * n), p = number of patterns, n = length of text
        """
        result = text
        for pattern, replacement in self.replacement_dict.items():
            result = result.replace(pattern, replacement)
        result = re.sub(r'\s+', ' ', result)
        return result.strip()


# Singleton instance
contextual_cleaner = ContextualCleaner()
