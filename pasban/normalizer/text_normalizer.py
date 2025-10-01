import re
import unicodedata

from pasban.core.vars import TRANSLATE_TABLE

# Precompiled regex pattern to match all characters that are NOT:
# - Standard Persian letters (including پ، چ، ژ، گ)
# - Zero-Width Non-Joiner (ZWNJ, \u200C)
# - Space
# Everything else (punctuation, digits, foreign letters, tashkeel, etc.) will be removed/replaced
_PERSIAN_ONLY_PATTERN = re.compile(
    r'[^\u0621-\u063A\u0641-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u200C ]+'
)


class WordNormalizer:
    """
    High-performance Persian text normalizer.

    This class provides a fast and reliable method to normalize Persian text
    for NLP, search, or text preprocessing tasks. The normalization process
    preserves spaces and the Zero-Width Non-Joiner (ZWNJ) while removing
    all other non-standard characters such as punctuation, numbers,
    foreign letters, tashkeel, and typographical marks.

    Steps performed by `normalize_text`:
        1. Unicode Normalization (NFKC) to standardize characters.
        2. Character translation using `TRANSLATE_TABLE` to convert
           non-standard Persian letters to their standard form
           (e.g., ك -> ک, ي -> ی, ة -> ه).
        3. Removal of all characters not matching standard Persian letters,
           space, or ZWNJ.
        4. Collapse multiple spaces into a single space and trim leading/trailing spaces.

    Example:
        ```python
        normalizer = WordNormalizer()
        text = "این متن شامل ك، ي و ة است!"
        normalized = normalizer.normalize_text(text)
        print(normalized)
        # Output: "این متن شامل ک ی ه است"
        ```
    """

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize Persian text.

        Args:
            text (str): The input Persian text to normalize.

        Returns:
            str: The normalized Persian text with only standard letters,
                 ZWNJ, and spaces. Extra spaces are collapsed.

        Notes:
            - This method is highly optimized for speed on long texts.
            - Zero-Width Non-Joiner characters are preserved.
            - All non-Persian characters, punctuation, numbers, and
              tashkeel are removed.
            - The method relies on `TRANSLATE_TABLE` for correcting
              non-standard letters.

        Big-O Complexity:
            O(n), where n is the length of the input text.
        """
        # Step 1: Unicode normalization
        text = unicodedata.normalize('NFKC', text)
        # Step 2: Translate non-standard Persian letters
        text = text.translate(TRANSLATE_TABLE)
        # Step 3: Remove all non-Persian characters except space and ZWNJ
        text = _PERSIAN_ONLY_PATTERN.sub('', text)
        # Step 4: Collapse multiple spaces into one and strip edges

        text = ' '.join(text.split())
        return text
