from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from pasban.core.data_types import DetectData
from pasban.db import WordRepo


class BaseDetector(ABC):
    """
    Abstract base class for word detectors.

    Provides basic methods to access words and defines abstract methods
    that subclasses must implement for detection logic.

    Attributes:
        _words (Dict[str, str]): Dictionary of known words mapped to their
                                 associated values loaded from WordRepo.
    """

    def __init__(self):
        """
        Initializes the BaseDetector by loading all known words
        from the database (WordRepo).

        Time Complexity: O(n)
            - n: number of words returned by WordRepo
        """
        self._words: Dict[str, str] = WordRepo.get_all_words()

    def get_words_count(self) -> int:
        """
        Returns the number of known words.

        Returns:
            int: Number of words in the detector.

        Time Complexity: O(1)
        """
        return len(self._words)

    # Allow len(detector) to return the number of words
    __len__ = get_words_count

    def get_words_dict(self) -> Dict[str, str]:
        """
        Returns the internal dictionary of words.

        Returns:
            Dict[str, str]: Mapping of words to their associated values.

        Time Complexity: O(1)
        """
        return self._words

    # Allow dict(detector) to return the word dictionary
    __dict__ = get_words_dict

    def get_word_list(self) -> List[Tuple[str, str]]:
        """
        Returns the words as a list of tuples (word, value).

        Returns:
            List[Tuple[str, str]]: List of all word-value pairs.

        Time Complexity: O(n)
            - n: number of words
        """
        return [(w, p) for w, p in self._words.items()]

    @abstractmethod
    def reload(self) -> None:
        """
        Reloads the words from the database.

        Subclasses should implement any additional steps needed for
        reloading or refreshing internal state.

        Time Complexity: O(n)
            - n: number of words reloaded from WordRepo
        """
        self._words: Dict[str, str] = WordRepo.get_all_words(reload=True)

    @abstractmethod
    def detect_words(self, text: str) -> Dict[str, str]:
        """
        Abstract method to detect words in the given text and return
        a dictionary of matches.

        Args:
            text (str): Text to search for known words.

        Returns:
            Dict[str, str]: Found words and their associated values.

        Time Complexity: Depends on subclass implementation.
        """
        pass

    @abstractmethod
    def detect(self, text: str) -> DetectData:
        """
        Abstract method to detect words and return a DetectData object
        containing matched words, their values, and the original text.

        Args:
            text (str): Text to analyze.

        Returns:
            DetectData: Detection result object.

        Time Complexity: Depends on subclass implementation.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        Abstract method to return a string representation of the detector.

        Returns:
            str: String representation of the object.

        Time Complexity: O(1)
        """
        pass
