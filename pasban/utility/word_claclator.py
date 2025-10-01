from typing import Tuple


class WordsCalculations:
    """
    Perform calculations on normalized text.

    Responsibilities:
    - Count words
    - Compute percentages of foreign words
    - Return summary tuple of total and foreign words

    Methods are static for lightweight usage and efficiency.
    """

    @staticmethod
    def get_word_count(text: str) -> int:
        """
        Count words in a string.

        Args:
            text (str): Input text.

        Returns:
            int: Number of words.

        Big-O: O(n), n = length of text
        """
        if not text or text.isspace():
            return 0
        return len(text.split())

    @staticmethod
    def percentage_calculation(total_words: int, foreign_words: int) -> float:
        """
        Compute the percentage of foreign words.

        Args:
            total_words (int): Total word count.
            foreign_words (int): Number of foreign words.

        Returns:
            float: Percentage of foreign words. Returns 0 if total_words is 0.

        Big-O: O(1)
        """
        if total_words == 0:
            return 0.0
        return (foreign_words / total_words) * 100

    @staticmethod
    def words_summary(text: str, foreign: int) -> Tuple[int, int]:
        """
        Return total words and foreign words as a tuple.

        Args:
            text (str): Input text.
            foreign (int): Number of foreign words.

        Returns:
            Tuple[int, int]: (total_words, foreign_words)

        Big-O: O(n), n = length of text
        """
        total = WordsCalculations.get_word_count(text)
        return total, foreign


# Singleton instances
words_calculator = WordsCalculations()
