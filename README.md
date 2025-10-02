# 🛡️ Pasban | پاسبان

<div align="center">

**Pure Persian Text Processing Library | کتابخانهٔ پردازش متن پارسی سره**

[![PyPI version](https://badge.fury.io/py/pasban.svg)](https://badge.fury.io/py/pasban)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

🌐 [تارنما](https://pasbans.ir) • 📚 [راهنما](https://pasban-py.readthedocs.io) •
📦 [PyPI](https://pypi.org/project/pasban/) • 💬 [تلگرام](https://t.me/pasbanparsi) •
🐙 [GitHub](https://github.com/keyaruga33/pasban-py)

#### این پروژه بخشی از پروژهٔ بزرگ پاسبان پارسی است. برای آشنایی و بهره‌گیری از پاسبان می‌توانید به [تارنما](https://pasbans.ir) و [کانال تلگرام پاسبان](https://t.me/pasbanparsi) سر بزنید.

[English](#english) | [پارسی](#persian)

</div>

---

## <a name="english"></a>🇬🇧 English

### What is Pasban?

Pasban is a high-performance Python library for detecting and replacing foreign (non-Persian) words in Persian text.
Built with speed and accuracy in mind, it offers:

- ⚡ **Lightning Fast**: Aho-Corasick algorithm for multi-pattern matching (17-30× faster)
- 🎯 **Highly Accurate**: Regex-based engine available for maximum precision
- 🧹 **Smart Processing**: Advanced normalization and contextual cleaning
- 📊 **Comprehensive Reports**: Detailed statistics and Persian-language summaries
- 🔌 **Fully Offline**: Works offline after initial database download
- 🔧 **Extensible**: Easy-to-manage word database

> **⚠️ Internet Required**: First-time database download and updates require an internet connection. If you're in a
> restricted region, you may need a VPN for initial setup.

### Database Source

Pasban automatically downloads its word database from the [
`keyaruga33/pasban_db`](https://github.com/keyaruga33/pasban_db) repository on first run. The database contains
thousands of foreign words and their Persian equivalents, maintained and updated regularly.

### Quick Start

```bash
pip install pasban
```

```python
from pasban.detector import WordDetector

# Initialize detector (downloads database on first run)
detector = WordDetector()

# Detect foreign words
text = "من با کامپیوتر کار می‌کنم و از اینترنت استفاده می‌کنم."
result = detector.detect(text)

# View results
print(f"Foreign words found: {result.foreign_words}")
# Output: ['کامپیوتر', 'اینترنت']

print(f"Persian equivalents: {result.words}")
# Output: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

print(f"Foreign word percentage: {result.foreign_percentage:.1f}%")
# Output: 28.6%

# Get full Persian report
print(result.to_summary_text)
```

### Which Detector Should I Use?

| Engine                | Speed         | Accuracy | Best For                           |
|-----------------------|---------------|----------|------------------------------------|
| **WordDetector** ✅    | 17-30× faster | ~98%     | Production, large texts, real-time |
| **WordDetectorRegex** | Slower        | ~99%+    | Small texts, maximum precision     |

```python
from pasban.detector import WordDetector, WordDetectorRegex

# For most use cases (recommended)
detector = WordDetector()

# For maximum accuracy
detector_regex = WordDetectorRegex()
```

### Performance Benchmark

Tested on Intel Core i7-8650U (100 iterations):

| Text Size               | WordDetector | WordDetectorRegex | Speed Gain |
|-------------------------|--------------|-------------------|------------|
| Large (1216 chars)      | 0.65 ms      | 12.09 ms          | **18.6×**  |
| Small (86 chars)        | 0.05 ms      | 0.92 ms           | **17×**    |
| Pure Persian (94 chars) | 0.04 ms      | 1.15 ms           | **30×**    |

### Advanced Usage

```python
# Disable normalization for raw text
result = detector.detect(text, normalize=False)

# Disable contextual cleaning for faster processing
result = detector.detect(text, contextual=False)

# Get only the word mappings
words = detector.detect_words(text)
# Output: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

# Reload database after updates
detector.reload()
```

### Documentation

📚 **Full documentation**: [Read the Docs](https://pasban-py.readthedocs.io)

### Requirements

- Python 3.9+
- requests
- Internet connection (only for initial database download)

---

## <a name="persian"></a>🇮🇷 پارسی

<div dir="rtl">

### پاسبان چیست؟

پاسبان کتابخانه‌ای برای پردازش متن پارسی سره است که شناسایی و جایگزینی واژگان بیگانه را با دقت و سرعت بالا انجام می‌دهد.
این کتابخانه دارای ویژگی‌های زیر است:

- ⚡ **سرعت بسیار بالا**: الگوریتم آهو-کُراسیک برای جستجوی چندالگویی (۱۷-۳۰ برابر سریع‌تر)
- 🎯 **دقت بالا**: موتور برپایهٔ عبارت منظم برای دقت بیشینه
- 🧹 **پردازش هوشمند**: نرمال‌سازی پیشرفته و پالایش زمینه‌ای
- 📊 **گزارش‌های جامع**: آمار دقیق و خلاصه‌های پارسی
- 🔌 **کاملاً آفلاین**: پس از بارگیری نخستین، نیازی به اینترنت ندارد
- 🔧 **قابل گسترش**: پایگاه واژگان قابل مدیریت

> **⚠️ نیازمند اینترنت**: برای بارگیری نخستین پایگاه‌داده و به‌روزرسانی‌ها به پیوند اینترنت نیاز دارید. اگر در ناحیهٔ
> محدود شده هستید، ممکن است برای راه‌اندازی نخستین به VPN نیاز داشته باشید.

### منبع پایگاه‌داده

پاسبان به‌صورت خودکار پایگاه واژگان خود را از ریپازیتوری [
`keyaruga33/pasban_db`](https://github.com/keyaruga33/pasban_db) در اجرای نخست بارگیری می‌کند. این پایگاه‌داده شامل
هزاران واژهٔ بیگانه و برابرهای پارسی آن‌هاست که به‌صورت منظم نگهداری و به‌روزرسانی می‌شود.

### آغاز پرشتاب

```bash
pip install pasban
```

```python
from pasban.detector import WordDetector

# راه‌اندازی شناساگر (بارگیری پایگاه‌داده در نخست)
detector = WordDetector()

# شناسایی واژگان بیگانه
text = "من با کامپیوتر کار می‌کنم و از اینترنت استفاده می‌کنم."
result = detector.detect(text)

# نمایش براورد ها
print(f"واژگان بیگانه یافته‌شده: {result.foreign_words}")
# دستاورد ها: ['کامپیوتر', 'اینترنت']

print(f"برابرهای پارسی: {result.words}")
# دستاورد ها: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

print(f"درصد واژگان بیگانه: {result.foreign_percentage:.1f}%")
# دستاورد: 28.6%

# دریافت گزارش واژگام به پارسی
print(result.to_summary_text)
```

### کدام موتور را برگزینم؟

| موتور                 | شتاب                  | دقت   | بهترین برای                  |
|-----------------------|-----------------------|-------|------------------------------|
| **WordDetector** ✅    | ۱۷-۳۰ برابر پرشتاب‌تر | ~۹۸٪  | تولید، متن‌های بزرگ، بلادرنگ |
| **WordDetectorRegex** | کندتر                 | ~۹۹٪+ | متن‌های کوچک، دقت بیشینه     |

```python
from pasban.detector import WordDetector, WordDetectorRegex

# برای بیشتر کاربردها (پیشنهاد می‌شود)
detector = WordDetector()

# برای هوشمنداری بیشینه
detector_regex = WordDetectorRegex()
```

### سنجش کارایی

آزمایش شده بر روی Intel Core i7-8565U (۱۰۰ بار):

| اندازهٔ متن          | WordDetector    | WordDetectorRegex | برتری سرعت     |
|----------------------|-----------------|-------------------|----------------|
| بزرگ (۱۲۱۶ نویسه)    | ۰.۶۵ میلی‌ثانیه | ۱۲.۰۹ میلی‌ثانیه  | **۱۸.۶ برابر** |
| کوچک (۸۶ نویسه)      | ۰.۰۵ میلی‌ثانیه | ۰.۹۲ میلی‌ثانیه   | **۱۷ برابر**   |
| پارسی سره (۹۴ نویسه) | ۰.۰۴ میلی‌ثانیه | ۱.۱۵ میلی‌ثانیه   | **۳۰ برابر**   |

### کاربرد پیشرفته

```python
# بی کنش کردن نرمال‌سازی برای نوشتار خام
result = detector.detect(text, normalize=False)

# بی کنس کردن پالایش زمینه‌ای برای پردازش پرشتاب‌تر
result = detector.detect(text, contextual=False)

# دریافت فقط دیکشنری واژگان
words = detector.detect_words(text)
# دستاورد: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

# بارگذاری دوبارهٔ پایگاه‌داده پس از به‌روزرسانی
detector.reload()
```

### داکیومنت

📚 **راهنمای بکارگیری**: [Read the Docs](https://pasban-py.readthedocs.io)

### پیش‌نیازها

- پایتون 3.9 یا بالاتر
- requests
- پیوند اینترنت (تنها برای بارگیری نخستین پایگاه‌داده)

</div>

---

<div align="center">

**Made with ❤️ for Persian Language | با ❤️ برای زبان پارسی**

[Documentation](https://pasban-py.readthedocs.io) • [PyPI](https://pypi.org/project/pasban/) • [Issues](https://github.com/keyaruga33/pasban-py/issues)

</div>
