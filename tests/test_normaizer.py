import pytest

from pasban.normalizer import WordNormalizer

normalizer = WordNormalizer()


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
            # Basic Persian letters
            ("سلام دنیا", "سلام دنیا"),
            # Non-standard letters mapped via TRANSLATE_TABLE
            ("ك ي ة", "ک ی ه"),
            # Extra punctuation and digits removed
            ("این! متن؟ شامل، 123 و $%^&* است.", "این متن شامل و است"),
            # ZWNJ converted to normal space
            ("می\u200Cروم", "می روم"),
            # Multiple spaces collapsed
            ("این    متن  با  فاصله   زیاد", "این متن با فاصله زیاد"),
            # Mixed foreign characters removed, keep Persian words
            ("Text انگلیسی و عربی عربى", "انگلیسی و عربی عربی"),
            # Combining everything
            ("ك، ي! 123 می\u200Cروم ـــ", "ک ی می روم"),
    ]
)
def test_normalize_text(input_text, expected_output):
    result = normalizer.normalize_text(input_text)
    assert result == expected_output
