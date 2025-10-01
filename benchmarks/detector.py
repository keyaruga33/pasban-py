"""
Benchmark script for comparing performance of word detection classes.

This script measures initialization time and detection time of different
word detector implementations (`WordDetector`, `WordDetectorRegex`) across
sample texts of different sizes. For each benchmark, it reports average,
minimum, maximum, median, and standard deviation times. Additionally:
- Text length (in characters) is displayed.
- Detection result length (number of detected words) is displayed.

Usage:
    Run this file directly to execute benchmarks on the sample texts.
"""

import statistics
import timeit
from typing import List, Type

from pasban import WordDetectorRegex, WordDetector

# List of detector classes to benchmark
CHILD_CLASSES: List[Type] = [
        WordDetector,
        WordDetectorRegex,
]

# Sample texts to simulate real-world use cases
SAMPLE_TEXTS = {
        "BigText":
            """ امروز در مسیر زندگی، با چالش‌های فراوانی روبرو شدیم. برخی افراد می‌خواستند که کارها سریع‌تر و بی‌وقفه انجام شوند، اما گروهی دیگر ناآشنا با روش‌های نوین، مقاومت نشان می‌دادند. بی‌اعتمادی‌ها و سوءتفاهم‌ها گاه کار را پیچیده‌تر می‌کرد، و تلاش‌های پی‌درپی امیدواری را افزایش داد. در میان کوچه‌ها و بازارها، صداهای متفاوت شنیده می‌شد؛ کودکان می‌دویدند، نوجوانان بازی می‌کردند و بزرگ‌ترها مشغول گفتگو بودند. تجربه‌ها نشان داده که برنامه‌ریزی دقیق و رعایت نظم، تاثیر بسزایی در موفقیت دارد. این متن شامل واژگان کمتر رایج و بیگانه‌گونه فارسی است: هژمونی، دیالکتیک، تراجنسی، آنتروپی، پدیدارشناسی، اپیستمولوژی، فرمالیزم، متافیزیک، ژانر شناسی، استراتژیست، سوژه‌گرایی، کانتکست وار، کازموپولیتن، متیس‌گرایی، نئومدرنیسم، هگلی، اگزیستانسیالیسم، پساساختارگرایی. همچنین ترکیب‌هایی با پیشوند و پسوند: می‌پویید، ناپیوسته، بی‌تفاهم، آموزنده‌تر، قابل‌اعتماد، خوش‌فکر، بی‌نظیر، خوشایند، نامانوس، و اصطلاحات روزمره: سرعت پردازش، واژگان دشوار، تست عملکرد، تحلیل دقیق، اطلاعات جامع. هدف این متن این است که بار واقعی روی WordDetector شبیه‌سازی شود و تمام حالات واژگانی فارسی بیگانه‌گونه، با پیشوند و پسوند، بررسی گردد تا زمان init و detect_words به شکل دقیق پروفایل شود. این متن طولانی و کبیر است و حاوی واژگان بیگانه است 
                    """,
        "SmallText": """امروز بحث درباره هژمونی و اپیستمولوژی بود.
دوست من از استراتژیست‌ها و متافیزیک هم گفت.""",
        "PurePersian": """خورشید بر کوهسار تابید. 
پرندگان در دشت‌ها آواز می‌خواندند.
مردمان به کار و زندگی درگیر بودند.""",
}


def benchmark_detector(cls, text: str, repeat_init=50, repeat_detect=50):
    """
    Benchmark initialization and detection performance for a detector class.

    Args:
        cls (Type): The detector class to benchmark.
        text (str): Input text to run detection on.
        repeat_init (int): Number of times to repeat class initialization.
        repeat_detect (int): Number of times to repeat detection calls.

    Returns:
        dict: Benchmark results containing class name, init stats, detect stats, and result length.
    """
    # Measure initialization times
    init_times = timeit.repeat(lambda: cls(), repeat=repeat_init, number=1)

    # Instance for detection test
    instance = cls()

    def detect_test():
        instance.detect_words(text, normalize=False, contextual=False)

    # Measure detection times
    detect_times = timeit.repeat(detect_test, repeat=repeat_detect, number=1)

    # Run once to get actual detection result length
    detection_result = instance.detect_words(text, normalize=False, contextual=False)
    result_len = len(detection_result) if detection_result is not None else 0

    def stats(times):
        """Compute descriptive statistics for a list of times."""
        return {
                "avg": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "median": statistics.median(times),
                "std": statistics.pstdev(times),
        }

    return {
            "class": cls.__name__,
            "init": stats(init_times),
            "detect": stats(detect_times),
            "result_len": result_len,
    }


if __name__ == "__main__":
    for text_name, text_value in SAMPLE_TEXTS.items():
        print(f"\n=== Benchmark on {text_name} ===")
        print(f"Text length: {len(text_value)} characters")  # ✅ show text length
        for cls in CHILD_CLASSES:
            r = benchmark_detector(cls, text_value)
            print(f"Class: {r['class']} (Detected words: {r['result_len']})")  # ✅ show len(result)
            print(
                f"  Init   -> Avg: {r['init']['avg']:.6f}s | "
                f"Min: {r['init']['min']:.6f}s | Max: {r['init']['max']:.6f}s | "
                f"Median: {r['init']['median']:.6f}s | StdDev: {r['init']['std']:.6f}s"
            )
            print(
                f"  Detect -> Avg: {r['detect']['avg']:.6f}s | "
                f"Min: {r['detect']['min']:.6f}s | Max: {r['detect']['max']:.6f}s | "
                f"Median: {r['detect']['median']:.6f}s | StdDev: {r['detect']['std']:.6f}s\n"
            )
