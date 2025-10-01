"""
Benchmark script for WordNormalizer class.

This script measures performance of the `normalize_text` method in
`WordNormalizer` across sample texts of different sizes. For each benchmark,
it reports average, minimum, maximum, median, and standard deviation times.
Additionally:
- Text length (in characters) is displayed.
- Normalized result length (number of characters) is displayed.

Usage:
    Run this file directly to execute benchmarks on the sample texts.
"""

import statistics
import timeit

from pasban.normalizer import WordNormalizer

# Sample texts to simulate real-world use cases
SAMPLE_TEXTS = {
        "BigText": """
#ٱین یک متن تستی‌ست کـه در آن از حروف غیـر پارسی مانند ك، ي، ة و کشیدگی‌هـای ـــ استفاده شده‌است!
#همچنین، اعداد ۱۲۳۴۵۶۷۸۹۰ و نشانه‌هایی مانند ؛ : ؟ ، و ... وجود دارد.  
#این متن بـرای تست سرعت و کاراییِ نـرم‌افزار نرمالایزر است. مرڪز فناوری ڪانال عـﺎلی ٳستفاده از داده‌ها.
""",
        "SmallText": """سلام! این متن كوتاه شامل ك، ي و ة است!""",
        "PurePersian": """خورشید بر کوهسار تابید.
پرندگان در دشت‌ها آواز می‌خواندند.
مردمان به کار و زندگی درگیر بودند.""",
}


def benchmark_normalizer(text: str, repeat=100):
    """
    Benchmark performance of WordNormalizer.normalize_text on a given text.

    Args:
        text (str): Input text to normalize.
        repeat (int): Number of times to repeat normalization.

    Returns:
        dict: Benchmark results containing stats and result length.
    """

    def normalize_test():
        WordNormalizer.normalize_text(text)

    # Measure detection times
    times = timeit.repeat(normalize_test, repeat=repeat, number=1)

    # Run once to get actual normalized text length
    normalized = WordNormalizer.normalize_text(text)
    result_len = len(normalized)

    def stats(values):
        """Compute descriptive statistics for a list of times."""
        return {
                "avg": statistics.mean(values),
                "min": min(values),
                "max": max(values),
                "median": statistics.median(values),
                "std": statistics.pstdev(values),
        }

    return {
            "detect": stats(times),
            "result_len": result_len,
    }


if __name__ == "__main__":
    for text_name, text_value in SAMPLE_TEXTS.items():
        print(f"\n=== Benchmark on {text_name} ===")
        print(f"Text length: {len(text_value)} characters")
        r = benchmark_normalizer(text_value)
        print(f"Normalized length: {r['result_len']} characters")
        print(
            f"  Normalize -> Avg: {r['detect']['avg']:.6f}s | "
            f"Min: {r['detect']['min']:.6f}s | Max: {r['detect']['max']:.6f}s | "
            f"Median: {r['detect']['median']:.6f}s | StdDev: {r['detect']['std']:.6f}s\n"
        )
