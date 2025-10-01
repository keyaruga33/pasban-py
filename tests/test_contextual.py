import pytest

from pasban.normalizer import ContextualCleaner


@pytest.fixture
def cleaner():
    return ContextualCleaner()


@pytest.mark.parametrize(
    "text,expected",
    [
            ("حافظ شیرازی", "شیرازی"),  # (حافظ) شیرازی → شیرازی
            ("آرامگاه حافظ", "آرامگاه"),  # آرامگاه (حافظ) → آرامگاه
            ("اشعار حافظ زیباست", "اشعار زیباست"),  # اشعار (حافظ) → اشعار
            ("فال حافظ خوب است", "فال خوب است"),  # فال (حافظ) → فال
            ("کشور کره جنوبی", "کشور جنوبی"),  # کشور (کره) جنوبی → کشور جنوبی
            ("قیصر امین پور", "قیصر پور"),  # قیصر (امین) پور → قیصر پور
            ("می شوم و می روم", "می و می روم"),  # می (شوم) → می
            ("بابا طاهر شاعر است", "بابا شاعر است"),  # بابا (طاهر) → بابا
            ("آقای مدیری آمد", "آقای آمد"),  # آقای (مدیری) → آقای
            ("مهران مدیری خوب است", "مهران خوب است")  # مهران (مدیری) → مهران
    ]
)
def test_clean_text_contextual_patterns(cleaner, text, expected):
    """
    Test that ContextualCleaner removes only the parts inside parentheses
    according to contextual_patterns while keeping the rest of the text intact.
    """
    result = cleaner.clean_text(text)
    assert result == expected


def test_clean_text_multiple_patterns(cleaner):
    """
    Test text with multiple contextual patterns simultaneously.
    """
    text = "آرامگاه حافظ و قیصر امین پور زیباست"
    expected = "آرامگاه و قیصر پور زیباست"
    assert cleaner.clean_text(text) == expected


def test_clean_text_no_patterns(cleaner):
    """
    Text without any patterns should remain unchanged.
    """
    text = "این یک متن ساده بدون پترن است"
    assert cleaner.clean_text(text) == text


def test_replacement_dict_not_empty(cleaner):
    """
    Ensure replacement_dict is not empty after initialization.
    """
    assert len(cleaner.replacement_dict) > 0
