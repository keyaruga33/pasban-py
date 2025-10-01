import pytest

from pasban.core.data_types import DetectData
from pasban.db import WordRepo
from pasban.detector import WordDetectorRegex
# Assumption: WORDS_DICT is imported from a data file
from tests.word_list import WORDS_DICT  # hypothetical path, adjust to the real path


class TestWordDetectorRegex:
    """
    Professional tests for WordDetectorRegex using real WORDS_DICT.
    Tests include:
    - basic detection
    - suffix handling
    - DetectData output
    - reload and representation
    """

    @pytest.fixture(autouse=True)
    def setup_detector(self, monkeypatch):
        # Mock WordRepo to use the real WORDS_DICT
        monkeypatch.setattr(
            WordRepo,
            "get_all_words",
            lambda reload=False: WORDS_DICT
        )
        self.detector = WordDetectorRegex()

    def test_basic_detection(self):
        # Test a few sample words from WORDS_DICT
        sample_text = "سلاحهای تزکیه‌ی نفس و کاندوم"
        detected = self.detector.detect_words(sample_text, normalize=False, contextual=False)
        assert "سلاحهای" in detected
        assert "تزکیه\u200cی نفس" in detected
        assert "کاندوم" in detected
        # Ensure the values are correct
        assert detected["سلاحهای"] == "جنگ افزارهای"
        assert detected["تزکیه\u200cی نفس"] == "جان\u200cپالایی، پالایش جان"
        assert detected["کاندوم"] == "کامپوش"

    def test_detectdata_object(self):
        sample_text = "مشغول شدن و معافیت"
        result: DetectData = self.detector.detect(sample_text, normalize=False, contextual=False)
        assert isinstance(result, DetectData)
        # Words should be detected
        assert "مشغول شدن" in result.foreign_words
        assert "معافیت" in result.foreign_words
        # Values should be correct
        assert result.words["مشغول شدن"] == "سرگرم شدن، درکارشدن، به کار پرداختن"
        assert result.words["معافیت"] == "رهایی، برکناری، بخشودگی"
        # Original text should match
        assert result.text == sample_text

    def test_suffix_handling(self):
        # Test words with Persian suffixes
        sample_text = "سلاحهایی تزکیه‌ی نفس‌ها و کاندوم‌ها"
        detected = self.detector.detect_words(sample_text, normalize=False, contextual=False)
        # Base words should be detected
        assert "سلاحهای" in detected
        assert "تزکیه\u200cی نفس" in detected
        assert "کاندوم" in detected

    def test_reload_and_repr(self):
        old_repr = repr(self.detector)
        assert "words=" in old_repr

        # Reload should recompile the pattern
        self.detector.reload()
        new_repr = repr(self.detector)
        assert old_repr == new_repr  # Word count should remain the same
