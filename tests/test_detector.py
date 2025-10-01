from pasban.core.data_types import DetectData
from pasban.detector import WordDetector
from tests.word_list import WORDS_DICT


class BaseWordDetectorTest:
    """
    Base test class for WordDetector.

    This class sets up a shared instance of `WordDetector`
    that loads the dictionary only once per test class.
    This improves performance by avoiding repeated automaton builds.
    """

    @classmethod
    def setup_class(cls):
        """
        Runs once per test class.

        Initializes the WordDetector, loads the dictionary,
        and builds the Aho-Corasick automaton for word detection.
        """
        cls.detector = WordDetector()
        cls.detector._words = WORDS_DICT
        cls.detector._load()  # Build automaton once

    def detect(self, text: str) -> DetectData:
        """
        Helper method: Detect foreign words in a text
        and return a DetectData object.

        Args:
            text (str): Input text to analyze.

        Returns:
            DetectData: Object containing detected words and statistics.
        """
        return self.detector.detect(text, normalize=False, contextual=False)

    def find(self, text: str):
        """
        Helper method: Find foreign words in a text.

        Args:
            text (str): Input text to analyze.

        Returns:
            List[str]: List of matched foreign words found in the text.
        """
        return self.detector.find_words_in_text(text)


class TestWordDetector(BaseWordDetectorTest):
    """
    Test suite for WordDetector.
    Inherits from BaseWordDetectorTest to reuse the shared detector instance.
    """

    def test_find_single_word(self):
        """Ensure the detector can find a single foreign word in text."""
        text = "او از کاندوم استفاده کرد."
        matches = self.find(text)
        assert "کاندوم" in matches

    def test_find_multiple_words(self):
        """Ensure the detector can find multiple words in one text."""
        text = "او با کامپیوتر و موبایل دابل کلیک کرد."
        # Update dictionary dynamically for this test
        self.detector._words.update({"کامپیوتر": "رایانه", "موبایل": "همراهک"})
        self.detector._load()
        matches = self.find(text)
        assert "کامپیوتر" in matches
        assert "موبایل" in matches
        assert "دابل کلیک" in matches

    def test_detect_words_returns_mapping(self):
        """Ensure detect_words() returns the correct mapping of word → replacement."""
        text = "گاردن زیبا بود اما مضر هم بود."
        detected = self.detector.detect_words(text, normalize=False, contextual=False)
        assert detected.get("گاردن") == "باغ"
        assert "مضر" in detected

    def test_detect_returns_detectdata(self):
        """Ensure detect() returns a DetectData object with correct properties."""
        text = "او در تفریح و تزکیه‌ی نفس کوشید."
        result = self.detect(text)

        assert isinstance(result, DetectData)
        assert "تفریح" in result.words
        assert "تزکیه‌ی نفس" in result.words
        assert result.text == text
        assert result.count >= 2
        assert result.unique_count >= 2

    def test_zwnj_boundary(self):
        """Ensure words with ZWNJ (‌) are detected correctly."""
        text = "تزکیه‌ی نفس راه رستگاری است."
        matches = self.find(text)
        assert "تزکیه‌ی نفس" in matches

    def test_repr_contains_word_count(self):
        """Ensure __repr__ contains useful debug information about WordDetector."""
        repr_str = repr(self.detector)
        assert "WordDetector" in repr_str
        assert "words=" in repr_str
