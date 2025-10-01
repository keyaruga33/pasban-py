import re
from typing import Dict, List, Optional

from pasban.core.data_types import AhoCorasickAutomaton, DetectData
from pasban.core.vars import suffix_pattern
from pasban.detector._base import BaseDetector
from pasban.normalizer import WordNormalizer, contextual_cleaner


class WordDetector(BaseDetector):
    """
    Word detection engine using the Aho-Corasick automaton with boundary-aware matching.

    This detector searches for words from a predefined dictionary inside the input text.
    It provides advanced handling of:
        - Text normalization
        - Contextual cleaning
        - Boundary validation (both left and right, including suffix handling)
        - Overlap resolution (prioritizing longer matches)

    Attributes:
        automaton (Optional[AhoCorasickAutomaton]): Automaton for fast multi-pattern searching.
        word_char_regex (re.Pattern): Regex to classify valid word characters (supports Persian/Arabic ranges).
        suffix_regex (re.Pattern): Regex to detect valid suffixes in words.
    """

    def __init__(self) -> None:
        """
        Initialize the WordDetector.

        Compiles regex patterns for word and suffix detection, initializes the
        automaton, and loads the predefined dictionary of words.

        Time Complexity:
            O(n * m)
            - n: number of words
            - m: average word length
        """
        super().__init__()
        self.automaton: Optional[AhoCorasickAutomaton] = None
        # Word character regex: excludes punctuation, supports Persian/Arabic letters, diacritics, and ZWNJ/ZWJ.
        self.word_char_regex = re.compile(
            r'[\w\u0621-\u063A\u0640-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u200c\u200d]'
        )
        self.suffix_regex: re.Pattern = re.compile(suffix_pattern, re.IGNORECASE)
        self._load()

    def _load(self) -> None:
        """Build the Aho-Corasick automaton from the internal word list."""
        self.automaton = self._build_automaton()

    def reload(self) -> None:
        """
        Reload the word list and rebuild the automaton.

        Time Complexity:
            O(n * m)
        """
        super().reload()
        self._load()

    def _build_automaton(self) -> AhoCorasickAutomaton:
        """
        Construct and return a fully built Aho-Corasick automaton with failure links.

        Returns:
            AhoCorasickAutomaton: Ready-to-use automaton for fast string matching.

        Time Complexity:
            O(n * m)
        """
        automaton = AhoCorasickAutomaton()
        for word in self._words.keys():
            automaton.add_word(word)
        automaton.build_failure_links()
        return automaton

    def _is_word_char(self, char: str) -> bool:
        """
        Check if a character is considered a valid word character.

        Args:
            char (str): Single character to evaluate.

        Returns:
            bool: True if the character is a valid word character, False otherwise.
        """
        return bool(self.word_char_regex.match(char))

    def _check_left_boundary(self, text: str, pos: int) -> bool:
        """
        Validate the left boundary of a candidate match.

        Args:
            text (str): The text being analyzed.
            pos (int): Start index of the candidate match.

        Returns:
            bool: True if the left boundary is valid.

        Time Complexity:
            O(1)
        """
        if pos <= 0:
            return True
        return not self._is_word_char(text[pos - 1])

    def _check_right_boundary(self, text: str, pos: int) -> bool:
        """
        Validate the right boundary of a candidate match, with suffix support.

        Equivalent logic to regex:
            (?={suffix_pattern}(?![\w\u0600-\u06FF‌‍])|\b)

        Args:
            text (str): The text being analyzed.
            pos (int): End index of the candidate match.

        Returns:
            bool: True if the right boundary is valid.

        Time Complexity:
            O(s)
            - s: maximum suffix length
        """
        if pos >= len(text):
            return True

        next_char = text[pos]

        # Treat ZWNJ/ZWJ as valid word boundaries
        if next_char in ('\u200c', '\u200d'):
            return True

        remaining = text[pos:]

        # Suffix check (e.g., "ها", "ی", etc.)
        suffix_match = self.suffix_regex.match(remaining)
        if suffix_match:
            after_suffix_pos = pos + len(suffix_match.group(0))
            if after_suffix_pos >= len(text):
                return True
            after_suffix_char = text[after_suffix_pos]
            if after_suffix_char in ('\u200c', '\u200d'):
                return True
            return not self._is_word_char(after_suffix_char)

        # If no suffix, enforce strict boundary
        return not self._is_word_char(next_char)

    def _is_valid_match(self, text: str, word: str, start: int, end: int) -> bool:
        """
        Validate a match by checking both left and right boundaries.

        Args:
            text (str): Input text.
            word (str): Candidate match word.
            start (int): Start index of the match.
            end (int): End index of the match.

        Returns:
            bool: True if both boundaries are valid.

        Time Complexity:
            O(s)
        """
        return self._check_left_boundary(text, start) and self._check_right_boundary(text, end)

    def find_words_in_text(self, text: str) -> List[str]:
        """
        Find all valid words in the given text.

        Workflow:
            1. Use the automaton to find candidate matches.
            2. Validate each match with boundary rules.
            3. Deduplicate matches.
            4. Sort matches (longer words first, then left-to-right order).
            5. Resolve overlaps by prioritizing longer matches.

        Args:
            text (str): Input text.

        Returns:
            List[str]: List of detected valid words.

        Time Complexity:
            O(L + z + k log k)
            - L: length of input text
            - z: number of automaton matches
            - k: number of valid matches
        """
        if not text or not self.automaton:
            return []

        all_matches = self.automaton.search(text)
        valid_matches = [(w, s, e) for w, s, e in all_matches if self._is_valid_match(text, w, s, e)]

        # Deduplicate matches
        seen = set()
        unique_matches = []
        for word, start, end in valid_matches:
            key = (word.lower(), start, end)
            if key not in seen:
                seen.add(key)
                unique_matches.append((word, start, end))

        # Sort: longer first, then earlier positions
        unique_matches.sort(key=lambda x: (-len(x[0]), x[1]))

        # Overlap resolution
        selected_words = []
        used_positions = set()
        for word, start, end in unique_matches:
            if not any(pos in used_positions for pos in range(start, end)):
                selected_words.append(word)
                used_positions.update(range(start, end))

        return selected_words

    def detect_words(self, text: str, normalize: bool = True, contextual: bool = True) -> Dict[str, str]:
        """
        Detect words in text and return a mapping of word → meaning.

        Args:
            text (str): Input text.
            normalize (bool): If True, apply text normalization.
            contextual (bool): If True, apply contextual cleaning.

        Returns:
            Dict[str, str]: Dictionary mapping detected words to their stored meanings.

        Time Complexity:
            O(L + z + k log k)
        """
        if normalize:
            text = WordNormalizer.normalize_text(text)
        if contextual:
            text = contextual_cleaner.clean_text(text)

        matches = self.find_words_in_text(text)
        return {word: self._words[word] for word in matches if word in self._words}

    def detect(self, text: str, normalize: bool = True, contextual: bool = True) -> DetectData:
        """
        Detect words and return a DetectData object containing results.

        Args:
            text (str): Input text.
            normalize (bool): If True, apply text normalization.
            contextual (bool): If True, apply contextual cleaning.

        Returns:
            DetectData: Structured object containing:
                - foreign_words: list of detected words
                - words: dictionary of word → meaning
                - text: processed text

        Time Complexity:
            O(L + z + k log k)
        """
        if normalize:
            text = WordNormalizer.normalize_text(text)
        if contextual:
            text = contextual_cleaner.clean_text(text)

        matches = self.find_words_in_text(text)

        return DetectData(
            foreign_words=matches,
            words={w: self._words[w] for w in matches},
            text=text
        )

    def __repr__(self) -> str:
        """
        Return a string representation with word count.

        Returns:
            str: Representation in the format:
                 "WordDetector(words=<count>)"

        Time Complexity:
            O(1)
        """
        return f"WordDetector(words={self.get_words_count()})"
