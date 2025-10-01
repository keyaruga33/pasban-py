from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from pasban.utility.word_claclator import words_calculator


class AhoCorasickNode:
    """
    Node in the Aho-Corasick trie.

    Attributes:
        children (Dict[str, AhoCorasickNode]): Mapping from character to child node.
        failure (Optional[AhoCorasickNode]): Failure link used during matching.
        output (List[str]): List of words that end at this node.
    """

    def __init__(self):
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.failure: Optional['AhoCorasickNode'] = None
        self.output: List[str] = []


class AhoCorasickAutomaton:
    """
    Aho-Corasick automaton for multi-pattern string matching.

    Attributes:
        root (AhoCorasickNode): Root node of the trie.
    """

    def __init__(self):
        """
        Initializes the automaton with an empty root node.

        Time Complexity: O(1)
        """
        self.root = AhoCorasickNode()

    def add_word(self, word: str):
        """
        Adds a word to the trie.

        Args:
            word (str): Word to be added.

        Time Complexity: O(m)
            - m: length of the word
        """
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        node.output.append(word)

    def build_failure_links(self):
        """
        Builds failure links for the Aho-Corasick automaton using BFS.

        The failure link points to the longest proper suffix of the current
        node's string that exists in the trie.

        Time Complexity: O(n * sigma)
            - n: total number of nodes in the trie
            - sigma: size of the alphabet
        """
        queue = deque()

        # Level 1 nodes fail to root
        for child in self.root.children.values():
            child.failure = self.root
            queue.append(child)

        # BFS traversal to set failure links for deeper nodes
        while queue:
            current_node = queue.popleft()

            for char, child_node in current_node.children.items():
                queue.append(child_node)

                # Find failure node
                failure_node = current_node.failure
                while failure_node is not None and char not in failure_node.children:
                    failure_node = failure_node.failure

                # Set failure link
                if failure_node is not None:
                    child_node.failure = failure_node.children[char]
                else:
                    child_node.failure = self.root

                # Merge outputs from failure link
                if child_node.failure:
                    child_node.output.extend(child_node.failure.output)

    def search(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Searches for all added words in the given text.

        Args:
            text (str): Text to search in.

        Returns:
            List[Tuple[str, int, int]]: List of tuples containing:
                - matched word
                - start position (inclusive)
                - end position (exclusive)

        Time Complexity: O(L + z)
            - L: length of the text
            - z: total number of matches found
        """
        results = []
        node = self.root

        for i, char in enumerate(text.lower()):
            # Follow failure links until a valid transition is found
            while node is not None and node != self.root and char not in node.children:
                node = node.failure

            # Move to next state if possible
            if char in node.children:
                node = node.children[char]
            elif node == self.root:
                pass  # stay at root
            else:
                node = self.root
                continue

            # Record all matches ending at this character
            for word in node.output:
                start_pos = i - len(word) + 1
                end_pos = i + 1
                results.append((word, start_pos, end_pos))

        return results


@dataclass
class DetectData:
    """
    Container for results of detecting foreign words in text.

    Provides:
    - Raw detected words and their translations.
    - Lazy statistical calculations (word counts, percentages, summaries).
    - Persian textual report.

    Attributes:
        foreign_words (List[str]): List of detected foreign words (may contain duplicates).
        words (Dict[str, str]): Mapping of unique foreign words to Persian equivalents.
        text (str): Original or processed input text.
    """

    foreign_words: List[str]
    words: Dict[str, str]
    text: str

    # Lazy evaluation cache (not part of init/repr/eq)
    _total_words: Optional[int] = field(default=None, init=False, repr=False, compare=False)
    _foreign_unique_count: Optional[int] = field(default=None, init=False, repr=False, compare=False)
    _summary: Optional[Tuple[int, int]] = field(default=None, init=False, repr=False, compare=False)

    # -----------------------------
    # Basic stats
    # -----------------------------
    @property
    def count(self) -> int:
        """Total number of detected foreign word occurrences (with duplicates)."""
        return len(self.foreign_words)

    @property
    def unique_count(self) -> int:
        """Number of unique detected foreign words."""
        if self._foreign_unique_count is None:
            self._foreign_unique_count = len(self.words)
        return self._foreign_unique_count

    # -----------------------------
    # Lazy word calculations
    # -----------------------------
    @property
    def total_words(self) -> int:
        """Total number of words in the text."""
        if self._total_words is None:
            self._total_words = words_calculator.get_word_count(self.text)
        return self._total_words

    @property
    def summary(self) -> Tuple[int, int]:
        """Summary of total and foreign word counts."""
        if self._summary is None:
            self._summary = (self.total_words, self.count)
        return self._summary

    @property
    def foreign_percentage(self) -> float:
        """Percentage of foreign words relative to total words."""
        total, foreign = self.summary
        return words_calculator.percentage_calculation(total, foreign)

    # -----------------------------
    # Persian textual report
    # -----------------------------
    @property
    def to_text(self) -> str:
        """Generate a formatted Persian text report of detected foreign words."""
        if not self.words:
            return "هیچ واژه‌ی بیگانه‌ای یافت نشد."

        body = "\n".join(f"● {w} 👈 {p}" for w, p in self.words.items())
        return f"{body}\n\n#پارسی_را_پاس_داریم"

    @property
    def to_summary_text(self):
        total, foreign = self.summary
        percentage = self.foreign_percentage
        return (
                f"📊 شمار همه واژه‌ها: {total}\n"
                f"🌍 شمار واژه‌های بیگانه: {foreign} (یکتا: {self.unique_count})\n"
                f"📈 درسد واژه‌های بیگانه: {percentage:.2f}%\n"
        )
        # -----------------------------

    # Debug representation
    # -----------------------------
    def __repr__(self) -> str:
        """Compact string representation for debugging."""
        total, foreign = self.summary
        return f"DetectData(foreign={foreign}, unique={self.unique_count}, total={total})"
