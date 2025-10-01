from pasban.core.data_types import DetectData
from pasban.detector._base import BaseDetector


# --- Mock subclass for testing BaseDetector ---
class MockDetector(BaseDetector):
    """
    A mock subclass of BaseDetector to allow testing
    the abstract base class functionality.
    """

    def reload(self) -> None:
        """
        Reload words from the database.
        """
        super().reload()

    def detect_words(self, text: str) -> dict:
        """
        Simple detection implementation for testing:
        returns words present in the input text.
        """
        return {w: v for w, v in self._words.items() if w in text}

    def detect(self, text: str) -> DetectData:
        """
        Returns a DetectData object for words found in text.
        """
        matches = self.detect_words(text)
        return DetectData(
            foreign_words=list(matches.keys()),
            words=matches,
            text=text
        )

    def __repr__(self):
        """
        Returns string representation including word count.
        """
        return f"<MockDetector words={len(self._words)}>"


# --- Unit test for BaseDetector using MockDetector ---
def test_base_detector_methods(monkeypatch):
    """
    Test BaseDetector methods using MockDetector and
    mocked WordRepo to avoid database dependency.
    """

    # Mock WordRepo.get_all_words to return fixed dictionary
    monkeypatch.setattr(
        "pasban.db.WordRepo.get_all_words",
        lambda reload=False: {"apple": "fruit", "car": "vehicle"}
    )

    detector = MockDetector()

    # Test get_words_count and len()
    assert detector.get_words_count() == 2
    assert len(detector) == 2

    # Test get_words_dict
    words_dict = detector.get_words_dict()
    assert words_dict == {"apple": "fruit", "car": "vehicle"}

    # Test get_word_list
    word_list = detector.get_word_list()
    assert ("apple", "fruit") in word_list
    assert ("car", "vehicle") in word_list
    assert len(word_list) == 2

    # Test detect_words
    detected = detector.detect_words("I like apple and car")
    assert detected == {"apple": "fruit", "car": "vehicle"}

    # Test detect returning DetectData
    detect_data = detector.detect("apple")
    assert isinstance(detect_data, DetectData)
    assert detect_data.foreign_words == ["apple"]
    assert detect_data.words == {"apple": "fruit"}
    assert detect_data.text == "apple"

    # Test __repr__
    repr_str = repr(detector)
    assert "<MockDetector words=2>" in repr_str
