"""
Benchmark script for ContextualCleaner class.

This script measures performance of ContextualCleaner initialization and
the `clean_text` method across sample texts of different sizes. For each
benchmark, it reports average, minimum, maximum, median, and standard
deviation times.

Additionally:
- Text length (in characters) is displayed.
- Cleaned result length (in characters) is displayed.

Usage:
    Run this file directly to execute benchmarks on the sample texts.
"""

import statistics
import timeit

from pasban.normalizer import ContextualCleaner

# Sample texts to simulate real-world use cases
SAMPLE_TEXTS = {
        "BigText": """امروز به حافظ شیرازی و کره شمالی اشاره شد. 
    همچنین درباره سعدی شیرازی و چین کمونیست صحبت کردند. 
    این متن طولانی‌تر است تا فشار بیشتری به ContextualCleaner وارد شود.""",
        "SmallText": """حافظ شیرازی شاعر بزرگی بود.""",
        "PurePersian": """کوه بلند است و رود روان. این متن ساده و بدون الگو است.""",
}


def benchmark_cleaner(cls, text: str, repeat_init=50, repeat_clean=100):
    """
    Benchmark initialization and cleaning performance for ContextualCleaner.

    Args:
        cls (Type): The cleaner class to benchmark.
        text (str): Input text to run cleaning on.
        repeat_init (int): Number of times to repeat initialization.
        repeat_clean (int): Number of times to repeat clean_text.

    Returns:
        dict: Benchmark results containing stats and result length.
    """

    # Measure initialization times
    init_times = timeit.repeat(lambda: cls(), repeat=repeat_init, number=1)

    # Instance for detection test
    instance = cls()

    def clean_test():
        instance.clean_text(text)

    # Measure cleaning times
    clean_times = timeit.repeat(clean_test, repeat=repeat_clean, number=1)

    # Run once to get actual cleaned text length
    cleaned = instance.clean_text(text)
    result_len = len(cleaned)

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
            "class": cls.__name__,
            "init": stats(init_times),
            "clean": stats(clean_times),
            "result_len": result_len,
    }


if __name__ == "__main__":
    for text_name, text_value in SAMPLE_TEXTS.items():
        print(f"\n=== Benchmark on {text_name} ===")
        print(f"Text length: {len(text_value)} characters")
        r = benchmark_cleaner(ContextualCleaner, text_value)
        print(f"Class: {r['class']} (Cleaned length: {r['result_len']})")
        print(
            f"  Init   -> Avg: {r['init']['avg']:.6f}s | "
            f"Min: {r['init']['min']:.6f}s | Max: {r['init']['max']:.6f}s | "
            f"Median: {r['init']['median']:.6f}s | StdDev: {r['init']['std']:.6f}s"
        )
        print(
            f"  Clean  -> Avg: {r['clean']['avg']:.6f}s | "
            f"Min: {r['clean']['min']:.6f}s | Max: {r['clean']['max']:.6f}s | "
            f"Median: {r['clean']['median']:.6f}s | StdDev: {r['clean']['std']:.6f}s\n"
        )
