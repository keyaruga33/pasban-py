import re
from typing import Dict, List

from pasban.core.data_types import DetectData
from pasban.core.vars import suffix_pattern
from pasban.normalizer import contextual_cleaner, WordNormalizer
from ._base import BaseDetector


class WordDetectorRegex(BaseDetector):
    """
    Regex-based detector for predefined words in a text.

    This detector finds words using a compiled regular expression pattern,
    with optional normalization and contextual cleaning.

    Attributes:
        pattern (re.Pattern | None): Compiled regex pattern for detecting words.
    """

    def __init__(self) -> None:
        """
        Initialize the WordDetectorRegex.

        Compiles the regex pattern from the internal word list.

        Time Complexity: O(n log n + m)
            - n: number of words (sorting)
            - m: total length of all words (regex escaping & joining)
        """
        super().__init__()
        self.pattern: re.Pattern | None = None
        self._load()

    def _load(self) -> None:
        """
        Build and compile the regex pattern for word detection.

        Time Complexity: O(n log n + m)
        """
        self.pattern = self._load_words_pattern()

    def reload(self) -> None:
        """
        Reload the word list and recompile the regex pattern.

        Time Complexity: O(n log n + m)
        """
        super().reload()
        self._load()

    def _load_words_pattern(self) -> re.Pattern:
        """
        Prepare and compile the regex pattern for all known words.

        Steps:
            1. Sort words by length (longest first) to avoid partial matches.
            2. Escape regex-special characters in words.
            3. Join words with the '|' operator.
            4. Wrap pattern with boundaries and suffix support.

        Returns:
            re.Pattern: Compiled regex pattern.

        Time Complexity: O(n log n + m)
            - n: number of words
            - m: total characters in all words
        """
        words_sorted = sorted(self._words.keys(), key=len, reverse=True)
        escaped_words = [re.escape(str(word)) for word in words_sorted]
        joined_words = '|'.join(escaped_words)
        pattern_str = (
                rf'(?<![\w\u0600-\u06FF‌‍])('
                + joined_words
                + rf')(?={suffix_pattern}(?![\w\u0600-\u06FF‌‍])|\b)'
        )
        return re.compile(pattern_str, re.IGNORECASE)

    def find_words_in_text(self, text: str) -> List[str]:
        """
        Find all words in the text using the compiled regex pattern.

        Args:
            text (str): Input text to search.

        Returns:
            List[str]: List of matched words.

        Time Complexity: O(L * k)
            - L: length of text
            - k: number of words in regex
        """
        if not self.pattern:
            return []
        return self.pattern.findall(text)

    def detect_words(self, text: str, normalize: bool = True, contextual: bool = True) -> Dict[str, str]:
        """
        Detect words and return a dictionary mapping each word to its value.

        Args:
            text (str): Input text.
            normalize (bool): Apply normalization if True.
            contextual (bool): Apply contextual cleaning if True.

        Returns:
            Dict[str, str]: Mapping of detected words to their stored values.

        Time Complexity: O(L * k + m)
            - L: length of text
            - k: number of words in regex
            - m: number of matches
        """
        if normalize:
            text = WordNormalizer.normalize_text(text)
        if contextual:
            text = contextual_cleaner.clean_text(text)
        matches = self.find_words_in_text(text)
        return {word: self._words[word] for word in matches}

    def detect(self, text: str, normalize: bool = True, contextual: bool = True) -> DetectData:
        """
        Detect words and return a DetectData object.

        Args:
            text (str): Input text.
            normalize (bool): Apply normalization if True.
            contextual (bool): Apply contextual cleaning if True.

        Returns:
            DetectData: Object containing detected words, word values, and processed text.

        Time Complexity: O(L * k + m)
        """
        if normalize:
            text = WordNormalizer.normalize_text(text)
        if contextual:
            text = contextual_cleaner.clean_text(text)
        matches = self.find_words_in_text(text)
        return DetectData(
            foreign_words=matches,
            words={word: self._words[word] for word in matches},
            text=text
        )

    def __repr__(self) -> str:
        """
        Return a string representation with word count.

        Returns:
            str: Example: "WordDetectorRegex(words=123)"

        Time Complexity: O(1)
        """
        return f"WordDetectorRegex(words={self.get_words_count()})"
