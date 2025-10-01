**Version:** 1.0.0 | **Last Updated:** 2024

نخستین آشنایی
=====================================

.. contents:: Contents
    :depth: 3
    :local:

=====================================

Introduction | آشنایی
---------------------

.. tab-set::

    .. tab-item:: English

        Pasban is a pure Persian text processing library for detecting foreign (non-Persian) words. It offers both Aho-Corasick and regex-based detection engines, advanced normalization, and contextual cleaning. It is designed for high accuracy, speed, and extensibility.

        **Key Features:**

        * Fast multi-pattern matching with Aho-Corasick algorithm
        * Regex-based detection for maximum accuracy
        * Advanced Persian text normalization
        * Contextual cleaning and boundary detection
        * Comprehensive statistics and reporting
        * Extensible word database
        * Fully offline after initial setup

        **Links:**

        * GitHub: `pasban-py <https://github.com/keyaruga33/pasban-py>`_
        * Website: `pasban <https://example.com>`_

    .. tab-item:: پارسی

        پاسبان کتابخانه‌ای برای پردازش متن پارسی سره است که شناسایی واژگان بیگانه را با موشکافی و سرعت بالا انجام می‌دهد. این کتابخانه موتورهای جستجوی چندالگویی (آهو-کُراسیک) و برپایهٔ عبارت منظم، نرمال‌سازی و پالایش زمینه‌ای را فراهم می‌کند.

        **ویژگی‌های کلیدی:**

        * جستجوی چندالگویی سریع با الگوریتم آهو-کُراسیک
        * شناسایی برپایهٔ عبارت منظم برای موشکافی بیشینه
        * نرمال‌سازی پیشرفته متن پارسی
        * پالایش زمینه‌ای و تشخیص مرزهای واژه
        * آمار و گزارش‌دهی جامع
        * پایگاه واژگان قابل گسترش
        * کاملاً آفلاین پس از راه‌اندازی نخستین

        **لینک‌ها:**

        * گیت‌هاب: `pasban-py <https://github.com/keyaruga33/pasban-py>`_
        * تارنما: `pasban <https://pasbans.ir>`_


Installation | نصب
------------------

.. tab-set::

    .. tab-item:: English

        .. code-block:: bash

            pip install pasban

        **Requirements:**

        * Python 3.8+
        * Internet connection (only for initial database download)

    .. tab-item:: پارسی

        برای نصب پاسبان کافی است دستور زیر را اجرا کنید:

        .. code-block:: bash

            pip install pasban

        **پیش‌نیازها:**

        * پایتون ۳.۸ یا بالاتر
        * پیوند به اینترنت (تنها برای بارگیری نخستین پایگاه‌داده)

.. admonition:: Quick Start Example | نمونه شروع سریع
    :class: tip

    .. code-block:: python

        from pasban.detector import WordDetector

        # Initialize detector
        detector = WordDetector()

        # Detect foreign words
        text = "من با کامپیوتر کار می‌کنم و از اینترنت استفاده می‌کنم."
        result = detector.detect(text)

        # Print results
        print(f"Foreign words: {result.foreign_words}")
        print(f"Percentage: {result.foreign_percentage:.1f}%")
        print(f"\nReport:\n{result.to_summary_text}")


Modules | ساختار ماژول‌ها
-------------------------

.. tab-set::

    .. tab-item:: English

        * **detector**: Word detection engines (``WordDetector``, ``WordDetectorRegex``)
        * **db**: Word database access (``WordRepo``, ``DataLoader``)
        * **normalizer**: Text normalization and contextual cleaning
        * **core**: Core data types (``DetectData``, ``AhoCorasickAutomaton``)

    .. tab-item:: پارسی

        * **detector**: موتورهای شناسایی واژه (``WordDetector`` و ``WordDetectorRegex``)
        * **db**: پایگاه واژگان (``WordRepo`` و ``DataLoader``)
        * **normalizer**: نرمال‌سازی و پالایش متن
        * **core**: انواع دادهٔ پایه مانند ``DetectData`` و ``AhoCorasickAutomaton``



WordDetector | WordDetectorRegex
================================

.. tab-set::

    .. tab-item:: English

        **WordDetector** uses the Aho-Corasick automaton for fast, multi-pattern matching. It normalizes and contextually cleans text, ensuring accurate word boundaries. **WordDetectorRegex** uses a compiled regex pattern for sometimes higher accuracy.

        *Constructor*

        .. code-block:: python

            from pasban.detector import WordDetector, WordDetectorRegex

            detector = WordDetector()
            detector_regex = WordDetectorRegex()

        *Methods*

        .. py:method:: detect(text: str, normalize: bool = True, contextual: bool = True) -> DetectData

            Detect foreign words and return a DetectData object with full statistics.

            :param text: Input text to analyze
            :param normalize: Apply text normalization (default: True)
            :param contextual: Apply contextual cleaning (default: True)
            :return: DetectData object with detection results and statistics

        .. py:method:: detect_words(text: str, normalize: bool = True, contextual: bool = True) -> dict[str, str]

            Return only detected words and their Persian equivalents.

            :param text: Input text to analyze
            :param normalize: Apply text normalization (default: True)
            :param contextual: Apply contextual cleaning (default: True)
            :return: Dictionary mapping foreign words to Persian equivalents

        .. py:method:: find_words_in_text(text: str) -> list[str]

            Find all foreign words in text (WordDetectorRegex only).

            :param text: Input text to analyze
            :return: List of detected foreign words

        .. py:method:: reload() -> None

            Reload words from the database.

        *Example Usage*

        .. code-block:: python

            from pasban.detector import WordDetector

            # Initialize detector (one-time setup)
            detector = WordDetector()

            # Detect foreign words with full statistics
            text = "این متن شامل کامپیوتر و اینترنت است."
            result = detector.detect(text)

            # Access detection results
            print(f"Foreign words: {result.foreign_words}")
            # Output: ['کامپیوتر', 'اینترنت']

            print(f"Mappings: {result.words}")
            # Output: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

            print(f"Total occurrences: {result.count}")
            # Output: 2

            print(f"Unique words: {result.unique_count}")
            # Output: 2

            print(f"Foreign percentage: {result.foreign_percentage:.2f}%")
            # Output: 28.57%

            # Get Persian report
            print(result.to_text)
            # Output: گزارش کامل به پارسی

            # Get summary report
            print(result.to_summary_text)
            # Output: خلاصه آماری

            # Or just get the words dictionary
            words = detector.detect_words(text)
            print(words)
            # Output: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

        *Advanced Usage*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

            # Reload database from disk
            all_words = repo.get_all_words(reload=True)

            # Batch operations
            new_words = {
                "وبسایت": "وبگاه",
                "ایمیل": "رایانامه",
                "فایل": "پرونده"
            }

            for foreign, persian in new_words.items():
                repo.add_word(foreign, persian)

            # Search with different terms
            computer_words = repo.search_word("رایانه", limit=10)
            print(f"Found {len(computer_words)} computer-related words")


    .. tab-item:: پارسی

        **WordDetector** با بهره‌گیری از آهو-کُراسیک، شناسایی واژگان بیگانه را با سرعت و موشکافی بالا انجام می‌دهد. **WordDetectorRegex** با عبارت منظم گاهی موشکافی بیشتری دارد.

        *سازنده*

        .. code-block:: python

            from pasban.detector import WordDetector, WordDetectorRegex

            detector = WordDetector()
            detector_regex = WordDetectorRegex()

        *متدها*

        .. py:method:: detect(text: str, normalize: bool = True, contextual: bool = True) -> DetectData
            :no-index:

            شناسایی واژگان بیگانه و بازگرداندن شیء DetectData با آمار کامل.

            :param text: متن ورودی برای تحلیل
            :param normalize: اعمال نرمال‌سازی متن (پیش‌فرض: True)
            :param contextual: اعمال پالایش زمینه‌ای (پیش‌فرض: True)
            :return: شیء DetectData با نتایج و آمار شناسایی

        .. py:method:: detect_words(text: str, normalize: bool = True, contextual: bool = True) -> dict[str, str]
            :no-index:

            بازگرداندن فقط واژگان بیگانه و برابر پارسی آن‌ها.

            :param text: متن ورودی برای تحلیل
            :param normalize: اعمال نرمال‌سازی متن (پیش‌فرض: True)
            :param contextual: اعمال پالایش زمینه‌ای (پیش‌فرض: True)
            :return: دیکشنری نگاشت واژگان بیگانه به برابر پارسی

        .. py:method:: find_words_in_text(text: str) -> list[str]
            :no-index:

            یافتن همهٔ واژگان بیگانه در متن (فقط WordDetectorRegex).

            :param text: متن ورودی برای تحلیل
            :return: فهرست واژگان بیگانه شناسایی‌شده

        .. py:method:: reload() -> None
            :no-index:

            بارگذاری دوباره واژگان از پایگاه داده.

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.detector import WordDetector

            # راه‌اندازی شناساگر (راه‌اندازی یک‌بار)
            detector = WordDetector()

            # شناسایی واژگان بیگانه با آمار کامل
            text = "این متن شامل کامپیوتر و اینترنت است."
            result = detector.detect(text)

            # دسترسی به نتایج شناسایی
            print(f"واژگان بیگانه: {result.foreign_words}")
            # خروجی: ['کامپیوتر', 'اینترنت']

            print(f"نگاشت‌ها: {result.words}")
            # خروجی: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

            print(f"تعداد کل رخدادها: {result.count}")
            # خروجی: 2

            print(f"واژگان یکتا: {result.unique_count}")
            # خروجی: 2

            print(f"درصد واژگان بیگانه: {result.foreign_percentage:.2f}%")
            # خروجی: 28.57%

            # دریافت گزارش پارسی
            print(result.to_text)
            # خروجی: گزارش کامل به پارسی

            # دریافت خلاصه آماری
            print(result.to_summary_text)
            # خروجی: خلاصه آماری

            # یا فقط دیکشنری واژگان را دریافت کنید
            words = detector.detect_words(text)
            print(words)
            # خروجی: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت'}

        *کاربرد پیشرفته*

        .. code-block:: python

            from pasban.detector import WordDetector, WordDetectorRegex

            # شناسایی بدون نرمال‌سازی
            result = detector.detect(text, normalize=False)

            # شناسایی بدون پالایش زمینه‌ای
            result = detector.detect(text, contextual=False)

            # شناسایی با غیرفعال کردن هر دو (سریع‌ترین، کم‌موشکافی‌ترین)
            result = detector.detect(text, normalize=False, contextual=False)

            # مقایسه هر دو موتور
            detector_ac = WordDetector()
            detector_re = WordDetectorRegex()

            result_ac = detector_ac.detect(text)
            result_re = detector_re.detect(text)

            print(f"آهو-کُراسیک یافت: {result_ac.count} واژه")
            print(f"عبارت منظم یافت: {result_re.count} واژه")

            # بارگذاری دوباره پایگاه‌داده پس از به‌روزرسانی
            detector.reload()

Which Detector Should I Use? | کدام موتور را برگزینم؟
-----------------------------------------------------

.. tab-set::

    .. tab-item:: English

        Pasban provides two main detection engines:

        * **WordDetector (Aho-Corasick)**: Extremely fast for large texts and wordlists; slightly less accurate in rare edge cases; **recommended for most applications**.
        * **WordDetectorRegex**: More accurate (especially with complex boundaries) but slower; best for small datasets or when maximum precision is needed.

        .. grid:: 2
            :gutter: 3

            .. grid-item-card:: WordDetector
                :class-card: sd-border-success

                ✅ **Recommended for most use cases**

                * Extremely fast (10-20x faster)
                * Excellent for large-scale processing
                * Real-time applications
                * Batch processing
                * Memory efficient

            .. grid-item-card:: WordDetectorRegex
                :class-card: sd-border-info

                🎯 **For maximum accuracy**

                * Higher precision
                * Better boundary detection
                * Small text processing
                * Critical accuracy scenarios
                * Educational/research use

    .. tab-item:: پارسی

        پاسبان دو موتور اصلی دارد:

        * **WordDetector (آهو-کُراسیک)**: برای متن‌های بزرگ بسیار سریع؛ در موارد نادر کمی کم‌موشکافی‌تر؛ **برای اکثر کاربردها پیشنهاد می‌شود**.
        * **WordDetectorRegex**: دقیق‌تر (به‌ویژه در مرزهای پیچیده) اما کندتر؛ برای داده‌های کوچک یا نیاز به موشکافی بیشینه مناسب است.

        .. grid:: 2
            :gutter: 3

            .. grid-item-card:: WordDetector
                :class-card: sd-border-success

                ✅ **پیشنهاد برای اکثر کاربردها**

                * بسیار سریع (۱۰-۲۰ برابر سریع‌تر)
                * عالی برای پردازش در مقیاس بزرگ
                * کاربردهای بلادرنگ
                * پردازش دسته‌ای
                * کارآمد در حافظه

            .. grid-item-card:: WordDetectorRegex
                :class-card: sd-border-info

                🎯 **برای موشکافی بیشینه**

                * موشکافی بالاتر
                * تشخیص بهتر مرزها
                * پردازش متن‌های کوچک
                * سناریوهای حساس به موشکافی
                * کاربرد آموزشی/پژوهشی


Performance Benchmark | سنجش کارایی
------------------------------------

.. tab-set::

    .. tab-item:: English

        Comprehensive benchmark results on Intel Core i7-8565U (100 iterations):

        .. tab-set::

            .. tab-item:: BigText (1216 chars, 46 foreign words)

                .. list-table::
                    :header-rows: 1
                    :widths: 20 20 20 20 20

                    * - Engine
                      - Operation
                      - Average
                      - Min/Max
                      - StdDev
                    * - **WordDetector**
                      - Init
                      - 0.086s
                      - 0.081s / 0.099s
                      - 0.003s
                    * -
                      - **Detect**
                      - **0.000650s**
                      - 0.000562s / 0.000975s
                      - 0.000084s
                    * - **WordDetectorRegex**
                      - Init
                      - 0.039s
                      - 0.035s / 0.186s
                      - 0.021s
                    * -
                      - **Detect**
                      - **0.012093s**
                      - 0.011914s / 0.013110s
                      - 0.000191s

                .. important::

                    WordDetector is **~18.6x faster** on large texts!

            .. tab-item:: SmallText (86 chars, 3 foreign words)

                .. list-table::
                    :header-rows: 1
                    :widths: 20 20 20 20 20

                    * - Engine
                      - Operation
                      - Average
                      - Min/Max
                      - StdDev
                    * - **WordDetector**
                      - Init
                      - 0.084s
                      - 0.079s / 0.090s
                      - 0.002s
                    * -
                      - **Detect**
                      - **0.000054s**
                      - 0.000050s / 0.000100s
                      - 0.000007s
                    * - **WordDetectorRegex**
                      - Init
                      - 0.036s
                      - 0.034s / 0.040s
                      - 0.001s
                    * -
                      - **Detect**
                      - **0.000917s**
                      - 0.000888s / 0.001149s
                      - 0.000040s

                .. important::

                    WordDetector is **~17x faster** on small texts!

            .. tab-item:: PurePersian (94 chars, 0 foreign words)

                .. list-table::
                    :header-rows: 1
                    :widths: 20 20 20 20 20

                    * - Engine
                      - Operation
                      - Average
                      - Min/Max
                      - StdDev
                    * - **WordDetector**
                      - Init
                      - 0.089s
                      - 0.081s / 0.122s
                      - 0.009s
                    * -
                      - **Detect**
                      - **0.000038s**
                      - 0.000037s / 0.000070s
                      - 0.000005s
                    * - **WordDetectorRegex**
                      - Init
                      - 0.037s
                      - 0.036s / 0.046s
                      - 0.002s
                    * -
                      - **Detect**
                      - **0.001151s**
                      - 0.001115s / 0.001396s
                      - 0.000050s

                .. important::

                    WordDetector is **~30x faster** on pure Persian text!

        .. admonition:: Performance Summary
            :class: tip

            * **WordDetector** initialization: ~85ms (one-time cost)
            * **WordDetector** detection: 0.04-0.65ms per text
            * **WordDetectorRegex** initialization: ~37ms (one-time cost)
            * **WordDetectorRegex** detection: 0.9-12ms per text
            * **Speed advantage**: WordDetector is 17-30x faster for detection
            * **Accuracy difference**: < 2% in most cases

    .. tab-item:: پارسی

        نتایج سنجش جامع بر روی Intel Core i7-8565U (۱۰۰ تکرار):

        .. tab-set::

            .. tab-item:: متن بزرگ (۱۲۱۶ نویسه، ۴۶ واژه بیگانه)

                .. list-table::
                    :header-rows: 1
                    :widths: 20 20 20 20 20

                    * - موتور
                      - عملیات
                      - میانگین
                      - کمینه/بیشینه
                      - انحراف معیار
                    * - **WordDetector**
                      - راه‌اندازی
                      - 0.086s
                      - 0.081s / 0.099s
                      - 0.003s
                    * -
                      - **شناسایی**
                      - **0.000650s**
                      - 0.000562s / 0.000975s
                      - 0.000084s
                    * - **WordDetectorRegex**
                      - راه‌اندازی
                      - 0.039s
                      - 0.035s / 0.186s
                      - 0.021s
                    * -
                      - **شناسایی**
                      - **0.012093s**
                      - 0.011914s / 0.013110s
                      - 0.000191s

                .. important::

                    WordDetector در متن‌های بزرگ **~۱۸.۶ برابر سریع‌تر** است!

            .. tab-item:: متن کوچک (۸۶ نویسه، ۳ واژه بیگانه)

                .. list-table::
                    :header-rows: 1
                    :widths: 20 20 20 20 20

                    * - موتور
                      - عملیات
                      - میانگین
                      - کمینه/بیشینه
                      - انحراف معیار
                    * - **WordDetector**
                      - راه‌اندازی
                      - 0.084s
                      - 0.079s / 0.090s
                      - 0.002s
                    * -
                      - **شناسایی**
                      - **0.000054s**
                      - 0.000050s / 0.000100s
                      - 0.000007s
                    * - **WordDetectorRegex**
                      - راه‌اندازی
                      - 0.036s
                      - 0.034s / 0.040s
                      - 0.001s
                    * -
                      - **شناسایی**
                      - **0.000917s**
                      - 0.000888s / 0.001149s
                      - 0.000040s

                .. important::

                    WordDetector در متن‌های کوچک **~۱۷ برابر سریع‌تر** است!

            .. tab-item:: متن پارسی سره (۹۴ نویسه، ۰ واژه بیگانه)

                .. list-table::
                    :header-rows: 1
                    :widths: 20 20 20 20 20

                    * - موتور
                      - عملیات
                      - میانگین
                      - کمینه/بیشینه
                      - انحراف معیار
                    * - **WordDetector**
                      - راه‌اندازی
                      - 0.089s
                      - 0.081s / 0.122s
                      - 0.009s
                    * -
                      - **شناسایی**
                      - **0.000038s**
                      - 0.000037s / 0.000070s
                      - 0.000005s
                    * - **WordDetectorRegex**
                      - راه‌اندازی
                      - 0.037s
                      - 0.036s / 0.046s
                      - 0.002s
                    * -
                      - **شناسایی**
                      - **0.001151s**
                      - 0.001115s / 0.001396s
                      - 0.000050s

                .. important::

                    WordDetector در متن پارسی سره **~۳۰ برابر سریع‌تر** است!

        .. admonition:: خلاصه کارایی
            :class: tip

            * **WordDetector** راه‌اندازی: ~۸۵ میلی‌ثانیه (هزینه یک‌بار)
            * **WordDetector** شناسایی: ۰.۰۴-۰.۶۵ میلی‌ثانیه به ازای هر متن
            * **WordDetectorRegex** راه‌اندازی: ~۳۷ میلی‌ثانیه (هزینه یک‌بار)
            * **WordDetectorRegex** شناسایی: ۰.۹-۱۲ میلی‌ثانیه به ازای هر متن
            * **برتری سرعت**: WordDetector در شناسایی ۱۷-۳۰ برابر سریع‌تر است
            * **تفاوت موشکافی**: در اکثر موارد کمتر از ۲٪


WordRepo | پایگاه واژگان
========================

.. tab-set::

    .. tab-item:: English

        **WordRepo** manages the database of foreign words and their Persian equivalents. You can access, search, add, remove, or update words.

        *Constructor*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

        *Methods*

        .. py:method:: get_all_words(reload: bool = False) -> dict[str, str]

            Get all words and their Persian equivalents.

            :param reload: Force reload from database (default: False)
            :return: Dictionary mapping foreign words to Persian equivalents

        .. py:method:: search_word(search_term: str, limit: int = 5) -> list[tuple[str, str]]

            Search for a word or its Persian equivalent.

            :param search_term: Term to search for
            :param limit: Maximum number of results (default: 5)
            :return: List of tuples (foreign_word, persian_equivalent)

        .. py:method:: add_word(foreign: str, persian: str) -> None

            Add a new word to the database.

            :param foreign: Foreign (non-Persian) word
            :param persian: Persian equivalent

        .. py:method:: remove_word(foreign: str) -> None

            Remove a word from the database.

            :param foreign: Foreign word to remove

        .. py:method:: update_word(foreign: str, persian: str) -> None

            Update a word's Persian equivalent.

            :param foreign: Foreign word to update
            :param persian: New Persian equivalent

        .. py:method:: get_persian(foreign: str) -> str

            Get the Persian equivalent of a foreign word.

            :param foreign: Foreign word
            :return: Persian equivalent (or empty string if not found)

        *Example Usage*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

            # Get all words
            all_words = repo.get_all_words()
            print(f"Total words: {len(all_words)}")
            print(f"کامپیوتر -> {all_words.get('کامپیوتر')}")
            # Output: کامپیوتر -> رایانه

            # Search for a word
            results = repo.search_word("کامپیوتر", limit=5)
            for foreign, persian in results:
                print(f"{foreign} -> {persian}")
            # Output: کامپیوتر -> رایانه

            # Get Persian equivalent
            persian = repo.get_persian("کامپیوتر")
            print(persian)
            # Output: رایانه

            # Add a new word
            repo.add_word("ایمیل", "رایانامه")
            print(repo.get_persian("ایمیل"))
            # Output: رایانامه

            # Update a word
            repo.update_word("ایمیل", "پست الکترونیک")
            print(repo.get_persian("ایمیل"))
            # Output: پست الکترونیک

            # Remove a word
            repo.remove_word("ایمیل")
            print(repo.get_persian("ایمیل"))
            # Output: (empty string)

            # Search with Persian equivalent
            results = repo.search_word("رایانه")
            for foreign, persian in results:
                print(f"{foreign} <- {persian}")
    .. tab-item:: پارسی

        **WordRepo** پایگاه دادهٔ واژگان بیگانه و برابر پارسی آن‌ها را مدیریت می‌کند. می‌توانید به واژگان دسترسی داشته باشید، جستجو کنید، بیفزایید، بردارید یا ویرایش کنید.

        *سازنده*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

        *متدها*

        .. py:method:: get_all_words(reload: bool = False) -> dict[str, str]
            :no-index:

            دریافت همهٔ واژگان و برابر پارسی آن‌ها.

            :param reload: بارگذاری اجباری از پایگاه‌داده (پیش‌فرض: False)
            :return: دیکشنری نگاشت واژگان بیگانه به برابر پارسی

        .. py:method:: search_word(search_term: str, limit: int = 5) -> list[tuple[str, str]]
            :no-index:

            جستجوی واژه یا برابر پارسی آن.

            :param search_term: عبارت جستجو
            :param limit: حداکثر تعداد نتایج (پیش‌فرض: 5)
            :return: فهرست تاپل‌ها (واژه_بیگانه، برابر_پارسی)

        .. py:method:: add_word(foreign: str, persian: str) -> None
            :no-index:

            افزودن واژهٔ تازه به پایگاه‌داده.

            :param foreign: واژه بیگانه (غیرپارسی)
            :param persian: برابر پارسی

        .. py:method:: remove_word(foreign: str) -> None
            :no-index:

            برداشتن واژه از پایگاه‌داده.

            :param foreign: واژه بیگانه برای حذف

        .. py:method:: update_word(foreign: str, persian: str) -> None
            :no-index:

            ویرایش برابر پارسی یک واژه.

            :param foreign: واژه بیگانه برای ویرایش
            :param persian: برابر پارسی جدید

        .. py:method:: get_persian(foreign: str) -> str
            :no-index:

            دریافت برابر پارسی یک واژه بیگانه.

            :param foreign: واژه بیگانه
            :return: برابر پارسی (یا رشته خالی در صورت نیافتن)

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

            # دریافت همه واژگان
            all_words = repo.get_all_words()
            print(f"تعداد کل واژگان: {len(all_words)}")
            print(f"کامپیوتر -> {all_words.get('کامپیوتر')}")
            # خروجی: کامپیوتر -> رایانه

            # جستجوی واژه
            results = repo.search_word("کامپیوتر", limit=5)
            for foreign, persian in results:
                print(f"{foreign} -> {persian}")
            # خروجی: کامپیوتر -> رایانه

            # دریافت برابر پارسی
            persian = repo.get_persian("کامپیوتر")
            print(persian)
            # خروجی: رایانه

            # افزودن واژه جدید
            repo.add_word("ایمیل", "رایانامه")
            print(repo.get_persian("ایمیل"))
            # خروجی: رایانامه

            # ویرایش واژه
            repo.update_word("ایمیل", "پست الکترونیک")
            print(repo.get_persian("ایمیل"))
            # خروجی: پست الکترونیک

            # حذف واژه
            repo.remove_word("ایمیل")
            print(repo.get_persian("ایمیل"))
            # خروجی: (رشته خالی)

            # جستجو با برابر پارسی
            results = repo.search_word("رایانه")
            for foreign, persian in results:
                print(f"{foreign} <- {persian}")

        *کاربرد پیشرفته*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

            # بارگذاری دوباره پایگاه‌داده از دیسک
            all_words = repo.get_all_words(reload=True)

            # عملیات دسته‌ای
            new_words = {
                "وبسایت": "وبگاه",
                "ایمیل": "رایانامه",
                "فایل": "پرونده"
            }

            for foreign, persian in new_words.items():
                repo.add_word(foreign, persian)

            # جستجو با عبارت‌های مختلف
            computer_words = repo.search_word("رایانه", limit=10)
            print(f"{len(computer_words)} واژه مرتبط با رایانه یافت شد")

        .. code-block:: python

            from pasban.detector import WordDetector, WordDetectorRegex

            # Detect without normalization
            result = detector.detect(text, normalize=False)

            # Detect without contextual cleaning
            result = detector.detect(text, contextual=False)

            # Detect with both disabled (fastest, least accurate)
            result = detector.detect(text, normalize=False, contextual=False)

            # Compare both engines
            detector_ac = WordDetector()
            detector_re = WordDetectorRegex()

            result_ac = detector_ac.detect(text)
            result_re = detector_re.detect(text)

            print(f"Aho-Corasick found: {result_ac.count} words")
            print(f"Regex found: {result_re.count} words")

            # Reload database after updates
            detector.reload()

DataLoader | بروزرسانی پایگاه واژگان
====================================

.. tab-set::

    .. tab-item:: English

        **DataLoader** handles downloading and updating the Pasban word database from GitHub.
        It ensures you always have the latest version and manages the local storage path.

        *Constructor & Usage*

        .. code-block:: python

            from pasban.db.loader import DataLoader

            # Initialize database (downloads if missing)
            DataLoader.initialize()

            # Get local database path
            db_path = DataLoader.get_db_path()
            print(db_path)

            # Check and update if needed
            DataLoader.update()

        *Methods*

        .. py:method:: initialize() -> None

            Ensure the database exists locally.
            If not, downloads the latest release automatically.

        .. py:method:: get_db_path() -> Path

            Get the path to the local database file.
            Automatically triggers initialization if missing.

            :return: Path object pointing to `pasban.db`

        .. py:method:: update(force_update: bool = False) -> None

            Check for updates and download the latest database if needed.

            :param force_update: If True, download the latest release even if
                                 the local version is up-to-date (default: False)

        .. py:method:: _get_lasted_tag() -> Optional[int]

            Internal method to read the last downloaded release tag from TAG file.

            :return: Last stored tag as integer, or None if unavailable

        .. py:method:: _get_release_data() -> dict

            Fetch metadata of the latest release from GitHub API.

            :return: JSON dictionary with release information

        .. py:method:: _get_db_url(assets_url: str) -> str

            Get the direct download URL for `pasban.db` from release assets.

            :param assets_url: GitHub API URL for release assets
            :return: Direct browser download URL
            :raises DatabaseNotFound: If `pasban.db` is not found

        .. py:method:: _download_release(assets_url: str, tag: str) -> None

            Download the latest database release and update the TAG file.

            :param assets_url: GitHub API URL for release assets
            :param tag: Release tag string

        *Example Usage*

        .. code-block:: python

            from pasban.db.loader import DataLoader

            # Force update the database
            DataLoader.update(force_update=True)

            # Normal update (only if new version available)
            DataLoader.update()

            # Get database path for other usage
            db_path = DataLoader.get_db_path()
            print(f"Database is stored at: {db_path}")

    .. tab-item:: پارسی

        **بارآور داده** مدیریت دانلود و بروزرسانی پایگاه واژگان پاسبان را برعهده دارد.
        این کلاس اطمینان می‌دهد که همیشه تازه‌ترین نسخه پایگاه داده روی دستگاه شما موجود باشد و مسیر نگهداری محلی را مدیریت می‌کند.

        *سازنده و نمونه کاربرد*

        .. code-block:: python

            from pasban.db.loader import DataLoader

            # اطمینان از وجود پایگاه داده (دانلود در صورت نبود)
            DataLoader.initialize()

            # دریافت مسیر پایگاه داده
            db_path = DataLoader.get_db_path()
            print(db_path)

            # بررسی و بروزرسانی در صورت نیاز
            DataLoader.update()

        *متدها*

        .. py:method:: initialize() -> None
            :no-index:

            اطمینان از موجود بودن پایگاه داده به‌صورت محلی.
            در صورت نبود، تازه‌ترین نسخه را خودکار بارگیری می‌کند.

        .. py:method:: get_db_path() -> Path
            :no-index:

            مسیر فایل پایگاه داده محلی را بازمی‌گرداند.
            در صورت نبود پایگاه داده، دانلود اولیه اجرا می‌شود.

            :return: شیء Path که به `pasban.db` اشاره دارد

        .. py:method:: update(force_update: bool = False) -> None
            :no-index:

            بررسی بروزرسانی‌ها و بارگیری تازه‌ترین نسخه پایگاه داده در صورت نیاز.

            :param force_update: اگر True باشد، همیشه تازه‌ترین نسخه بارگیری می‌شود
                                 حتی اگر نسخه محلی به‌روز باشد (پیش‌فرض: False)

        .. py:method:: _get_lasted_tag() -> Optional[int]
            :no-index:

            کردار درونی برای خواندن آخرین شماره نسخه دانلود شده از پرونده TAG.

            :return: آخرین شماره نسخه به‌صورت عدد یا None در صورت نبود

        .. py:method:: _get_release_data() -> dict
            :no-index:

            دریافت داده‌های نسخه تازه از سرویس GitHub.

            :return: دیکشنری JSON شامل داده‌های نسخه

        .. py:method:: _get_db_url(assets_url: str) -> str
            :no-index:

            دریافت نشانی مستقیم بارگیری `pasban.db` از داده‌های نسخه.

            :param assets_url: نشانی API گیت‌هاب برای داده‌های نسخه
            :return: نشانی دانلود مستقیم
            :raises DatabaseNotFound: در صورت نبود پرونده `pasban.db`

        .. py:method:: _download_release(assets_url: str, tag: str) -> None
            :no-index:

            بارگیری تازه‌ترین نسخه پایگاه داده و بروزرسانی پرونده TAG.

            :param assets_url: نشانی API گیت‌هاب برای داده‌ها
            :param tag: شماره نسخه

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.db.loader import DataLoader

            # بروزرسانی اجباری پایگاه داده
            DataLoader.update(force_update=True)

            # بروزرسانی معمولی (تنها در صورت وجود نسخه تازه)
            DataLoader.update()

            # دریافت مسیر پایگاه داده برای کاربردهای دیگر
            db_path = DataLoader.get_db_path()
            print(f"پایگاه داده در مسیر: {db_path}")

Normalizer | نرمال‌ساز
========================

.. tab-set::

    .. tab-item:: English

        Normalize Persian text and remove non-standard characters and punctuation. The normalizer converts Arabic characters to Persian equivalents and ensures consistent text representation.

        *Methods*

        .. py:method:: WordNormalizer.normalize_text(text: str) -> str

            Normalize Persian text by converting Arabic characters to Persian equivalents and removing non-standard characters.

            :param text: Input text to normalize
            :return: Normalized text

            **Normalizations applied:**

            * Arabic ك (U+0643) → Persian ک (U+06A9)
            * Arabic ي (U+064A) → Persian ی (U+06CC)
            * Arabic ة (U+0629) → Persian ه (U+0647)
            * Zero-width characters removed
            * Diacritics removed
            * Multiple spaces collapsed to single space

        *Example Usage*

        .. code-block:: python

            from pasban.normalizer.text_normalizer import WordNormalizer

            # Basic normalization
            text = "این متن شامل ك، ي و ة است!"
            normalized = WordNormalizer.normalize_text(text)
            print(normalized)
            # Output: "این متن شامل ک ی ه است"

            # Normalize mixed text
            mixed_text = "كتاب    در    كتابخانه    است"
            normalized = WordNormalizer.normalize_text(mixed_text)
            print(normalized)
            # Output: "کتاب در کتابخانه است"

            # Remove diacritics
            text_with_diacritics = "مَثَلاً کِتابِ خوبی است"
            normalized = WordNormalizer.normalize_text(text_with_diacritics)
            print(normalized)
            # Output: "مثلا کتاب خوبی است"

        .. admonition:: When to use normalization
            :class: tip

            * Before processing any Persian text
            * When comparing Persian strings
            * Before storing text in databases
            * When preparing text for machine learning
            * Recommended to always use with detectors (enabled by default)

    .. tab-item:: پارسی

        نرمال‌سازی متن پارسی و زدودن نویسه‌های بیگانه و نشانه‌گذاری. نرمال‌ساز نویسه‌های تازی را به برابر پارسی تبدیل می‌کند و بازنمایی یکسان متن را تضمین می‌کند.

        *متدها*

        .. py:method:: WordNormalizer.normalize_text(text: str) -> str
            :no-index:

            نرمال‌سازی متن پارسی با تبدیل نویسه‌های تازی به برابر پارسی و حذف نویسه‌های غیراستاندارد.

            :param text: متن ورودی برای نرمال‌سازی
            :return: متن نرمال‌شده

            **نرمال‌سازی‌های اعمال‌شده:**

            * ك تازی (U+0643) ← ک پارسی (U+06A9)
            * ي تازی (U+064A) ← ی پارسی (U+06CC)
            * ة تازی (U+0629) ← ه پارسی (U+0647)
            * حذف نویسه‌های پهنای صفر
            * حذف اعراب
            * فشرده‌سازی فاصله‌های چندگانه به یک فاصله

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.normalizer.text_normalizer import WordNormalizer

            # نرمال‌سازی ساده
            text = "این متن شامل ك، ي و ة است!"
            normalized = WordNormalizer.normalize_text(text)
            print(normalized)
            # خروجی: "این متن شامل ک ی ه است"

            # نرمال‌سازی متن مختلط
            mixed_text = "كتاب    در    كتابخانه    است"
            normalized = WordNormalizer.normalize_text(mixed_text)
            print(normalized)
            # خروجی: "کتاب در کتابخانه است"

            # حذف اعراب
            text_with_diacritics = "مَثَلاً کِتابِ خوبی است"
            normalized = WordNormalizer.normalize_text(text_with_diacritics)
            print(normalized)
            # خروجی: "مثلا کتاب خوبی است"

        .. admonition:: چه زمانی از نرمال‌سازی استفاده کنیم
            :class: tip

            * پیش از پردازش هرگونه متن پارسی
            * هنگام مقایسه رشته‌های پارسی
            * پیش از ذخیره متن در پایگاه‌داده
            * هنگام آماده‌سازی متن برای یادگیری ماشین
            * توصیه می‌شود همواره با شناساگرها استفاده شود (پیش‌فرض فعال است)


Contextual Cleaner | پالایشگر زمینه‌ای
========================================

.. tab-set::

    .. tab-item:: English

        Remove contextual patterns and special combinations from text. The contextual cleaner identifies and removes Persian name patterns, common word combinations, and other context-specific patterns that should not be flagged as foreign words.

        *Methods*

        .. py:method:: contextual_cleaner.clean_text(text: str) -> str

            Remove contextual patterns from text.

            :param text: Input text to clean
            :return: Cleaned text

            **Patterns removed:**

            * Persian full names (first name + last name)
            * Common Persian compound words
            * Persian idioms and expressions
            * Proper nouns with Persian markers
            * Date and time expressions

        *Example Usage*

        .. code-block:: python

            from pasban.normalizer.contextual_remover import contextual_cleaner

            # Remove name patterns
            text = "حافظ شیرازی شاعر نامدار است."
            cleaned = contextual_cleaner.clean_text(text)
            print(cleaned)
            # Names like "حافظ شیرازی" are removed from detection

            # Remove compound words
            text = "کتابخانهٔ ملی ایران"
            cleaned = contextual_cleaner.clean_text(text)
            print(cleaned)

            # Complex example with multiple patterns
            text = """
            رومی مولانا جلال‌الدین محمد بلخی شاعر و عارف بزرگ ایرانی
            در قرن هفتم هجری در شهر بلخ متولد شد.
            """
            cleaned = contextual_cleaner.clean_text(text)
            print(cleaned)

        *Integration with Detector*

        .. code-block:: python

            from pasban.detector import WordDetector

            detector = WordDetector()

            text = "حافظ شیرازی و مولانا رومی شاعران بزرگ ایرانی هستند."

            # With contextual cleaning (default)
            result = detector.detect(text, contextual=True)
            print(f"With cleaning: {result.count} foreign words")

            # Without contextual cleaning
            result = detector.detect(text, contextual=False)
            print(f"Without cleaning: {result.count} foreign words")

        .. admonition:: When to use contextual cleaning
            :class: tip

            * When processing literary or historical texts
            * When text contains many Persian names
            * When working with formal Persian writing
            * Recommended for most use cases (enabled by default)
            * Disable for maximum detection sensitivity

    .. tab-item:: پارسی

        زدودن ساختارهای زمینه‌ای و ترکیب‌های خاص از متن. پالایشگر زمینه‌ای الگوهای نام پارسی، ترکیب‌های رایج واژگان و دیگر الگوهای وابسته به زمینه را که نباید به عنوان واژه بیگانه شناسایی شوند، می‌شناسد و حذف می‌کند.

        *متدها*

        .. py:method:: contextual_cleaner.clean_text(text: str) -> str
            :no-index:

            زدودن الگوهای زمینه‌ای از متن.

            :param text: متن ورودی برای پالایش
            :return: متن پالایش‌شده

            **الگوهای حذف‌شده:**

            * نام‌های کامل پارسی (نام + نام خانوادگی)
            * واژگان مرکب رایج پارسی
            * اصطلاحات و عبارات پارسی
            * اسامی خاص با نشانگرهای پارسی
            * عبارات تاریخ و زمان

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.normalizer.contextual_remover import contextual_cleaner

            # حذف الگوهای نام
            text = "حافظ شیرازی شاعر نامدار است."
            cleaned = contextual_cleaner.clean_text(text)
            print(cleaned)
            # نام‌هایی مانند "حافظ شیرازی" از شناسایی حذف می‌شوند

            # حذف واژگان مرکب
            text = "کتابخانهٔ ملی ایران"
            cleaned = contextual_cleaner.clean_text(text)
            print(cleaned)

            # نمونهٔ پیچیده با الگوهای چندگانه
            text = """
            رومی مولانا جلال‌الدین محمد بلخی شاعر و عارف بزرگ ایرانی
            در قرن هفتم هجری در شهر بلخ متولد شد.
            """
            cleaned = contextual_cleaner.clean_text(text)
            print(cleaned)

        *یکپارچگی با شناساگر*

        .. code-block:: python

            from pasban.detector import WordDetector

            detector = WordDetector()

            text = "حافظ شیرازی و مولانا رومی شاعران بزرگ ایرانی هستند."

            # با پالایش زمینه‌ای (پیش‌فرض)
            result = detector.detect(text, contextual=True)
            print(f"با پالایش: {result.count} واژه بیگانه")

            # بدون پالایش زمینه‌ای
            result = detector.detect(text, contextual=False)
            print(f"بدون پالایش: {result.count} واژه بیگانه")

        .. admonition:: چه زمانی از پالایش زمینه‌ای استفاده کنیم
            :class: tip

            * هنگام پردازش متن‌های ادبی یا تاریخی
            * زمانی که متن شامل نام‌های پارسی زیادی است
            * هنگام کار با نوشتار رسمی پارسی
            * برای اکثر کاربردها توصیه می‌شود (پیش‌فرض فعال است)
            * برای حساسیت بیشینه شناسایی، غیرفعال کنید


Core Data Types | انواع داده پایه
=================================

DetectData
----------

.. tab-set::

    .. tab-item:: English

        Container for detection results and statistics. This object provides comprehensive information about detected foreign words and text statistics.

        *Attributes*

        .. py:attribute:: foreign_words
            :type: list[str]

            List of detected foreign words (may contain duplicates for multiple occurrences)

        .. py:attribute:: words
            :type: dict[str, str]

            Mapping of unique foreign words to their Persian equivalents

        .. py:attribute:: text
            :type: str

            Original or processed input text

        .. py:attribute:: count
            :type: int

            Total number of detected foreign word occurrences

        .. py:attribute:: unique_count
            :type: int

            Number of unique detected foreign words

        .. py:attribute:: total_words
            :type: int

            Total number of words in the text

        .. py:attribute:: foreign_percentage
            :type: float

            Percentage of foreign words in the text

        .. py:attribute:: to_text
            :type: str

            Detailed Persian text report

        .. py:attribute:: to_summary_text
            :type: str

            Concise Persian summary report

        *Example Usage*

        .. code-block:: python

            from pasban.detector import WordDetector

            detector = WordDetector()
            text = "این متن شامل کامپیوتر و اینترنت و سیستم است."
            result = detector.detect(text)

            # Access basic information
            print(f"Foreign words list: {result.foreign_words}")
            # Output: ['کامپیوتر', 'اینترنت', 'سیستم']

            print(f"Word mappings: {result.words}")
            # Output: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت', 'سیستم': 'سامانه'}

            # Access statistics
            print(f"Total occurrences: {result.count}")
            # Output: 3

            print(f"Unique words: {result.unique_count}")
            # Output: 3

            print(f"Total words in text: {result.total_words}")
            # Output: 9

            print(f"Foreign percentage: {result.foreign_percentage:.2f}%")
            # Output: 33.33%

            # Get reports
            print("Detailed report:")
            print(result.to_text)
            # Output: واژگان بیگانه یافت‌شده: کامپیوتر (رایانه), اینترنت (اینترنت), ...

            print("\nSummary:")
            print(result.to_summary_text)
            # Output: 3 واژه بیگانه از 9 واژه (33.33٪)

        .. admonition:: Using DetectData effectively
            :class: tip

            * Use ``foreign_words`` for processing individual occurrences
            * Use ``words`` for unique word mappings
            * Use ``count`` vs ``unique_count`` to detect repetition
            * Use ``foreign_percentage`` for quality metrics
            * Use ``to_text`` for user-facing reports
            * Use ``to_summary_text`` for dashboards/statistics

    .. tab-item:: پارسی

        ظرف نتایج شناسایی و آمارها. این شیء اطلاعات جامعی دربارهٔ واژگان بیگانه شناسایی‌شده و آمار متن فراهم می‌کند.

        *ویژگی‌ها*

        .. py:attribute:: foreign_words
            :no-index:

            :type: list[str]

            فهرست واژگان بیگانه شناسایی‌شده (ممکن است برای رخدادهای چندگانه تکراری باشد)

        .. py:attribute:: words
            :no-index:

            :type: dict[str, str]

            نگاشت واژگان بیگانه یکتا به برابرهای پارسی آن‌ها

        .. py:attribute:: text
            :type: str
            :no-index:

            متن ورودی اصلی یا پردازش‌شده

        .. py:attribute:: count
            :type: int
            :no-index:

            تعداد کل رخدادهای واژگان بیگانه

        .. py:attribute:: unique_count
            :type: int
            :no-index:

            تعداد واژگان بیگانه یکتا

        .. py:attribute:: total_words
            :type: int
            :no-index:

            تعداد کل واژگان در متن

        .. py:attribute:: foreign_percentage
            :type: float
            :no-index:

            درصد واژگان بیگانه در متن

        .. py:attribute:: to_text
            :type: str
            :no-index:

            گزارش متنی تفصیلی به پارسی

        .. py:attribute:: to_summary_text
            :type: str
            :no-index:

            گزارش خلاصه به پارسی

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.detector import WordDetector

            detector = WordDetector()
            text = "این متن شامل کامپیوتر و اینترنت و سیستم است."
            result = detector.detect(text)

            # دسترسی به اطلاعات پایه
            print(f"فهرست واژگان بیگانه: {result.foreign_words}")
            # خروجی: ['کامپیوتر', 'اینترنت', 'سیستم']

            print(f"نگاشت واژگان: {result.words}")
            # خروجی: {'کامپیوتر': 'رایانه', 'اینترنت': 'اینترنت', 'سیستم': 'سامانه'}

            # دسترسی به آمارها
            print(f"تعداد کل رخدادها: {result.count}")
            # خروجی: 3

            print(f"واژگان یکتا: {result.unique_count}")
            # خروجی: 3

            print(f"کل واژگان متن: {result.total_words}")
            # خروجی: 9

            print(f"درصد واژگان بیگانه: {result.foreign_percentage:.2f}%")
            # خروجی: 33.33%

            # دریافت گزارش‌ها
            print("گزارش تفصیلی:")
            print(result.to_text)
            # خروجی: واژگان بیگانه یافت‌شده: کامپیوتر (رایانه), اینترنت (اینترنت), ...

            print("\nخلاصه:")
            print(result.to_summary_text)
            # خروجی: 3 واژه بیگانه از 9 واژه (33.33٪)

        .. admonition:: استفاده مؤثر از DetectData
            :class: tip

            * از ``foreign_words`` برای پردازش رخدادهای جداگانه استفاده کنید
            * از ``words`` برای نگاشت واژگان یکتا استفاده کنید
            * از ``count`` در مقابل ``unique_count`` برای تشخیص تکرار استفاده کنید
            * از ``foreign_percentage`` برای معیارهای کیفیت استفاده کنید
            * از ``to_text`` برای گزارش‌های کاربری استفاده کنید
            * از ``to_summary_text`` برای داشبوردها/آمارها استفاده کنید


AhoCorasickAutomaton
--------------------

.. tab-set::

    .. tab-item:: English

        Multi-pattern string matching engine using the Aho-Corasick algorithm. This is the core algorithm used by ``WordDetector`` for fast detection of multiple patterns simultaneously.

        *Methods*

        .. py:method:: add_word(word: str) -> None
            :no-index:

            Add a word to the automaton trie.

            :param word: Word to add

        .. py:method:: build_failure_links() -> None

            Build failure links for fast matching. Must be called after adding all words and before searching.

        .. py:method:: search(text: str) -> List[Tuple[str, int, int]]

            Find all pattern matches in the text.

            :param text: Text to search in
            :return: List of tuples (matched_word, start_position, end_position)

        *Example Usage*

        .. code-block:: python

            from pasban.core import AhoCorasickAutomaton

            # Create automaton
            ac = AhoCorasickAutomaton()

            # Add patterns
            ac.add_word("کامپیوتر")
            ac.add_word("اینترنت")
            ac.add_word("سیستم")

            # Build failure links (required before searching)
            ac.build_failure_links()

            # Search for patterns
            text = "این کامپیوتر به اینترنت متصل است و سیستم عامل دارد."
            matches = ac.search(text)

            # Process results
            for word, start, end in matches:
                print(f"Found '{word}' at position {start}-{end}")
            # Output:
            # Found 'کامپیوتر' at position 4-12
            # Found 'اینترنت' at position 16-23
            # Found 'سیستم' at position 32-37

        *Advanced Usage*

        .. code-block:: python

            from pasban.core import AhoCorasickAutomaton

            # Build automaton from word list
            words = ["رایانه", "اینترنت", "شبکه", "سامانه"]
            ac = AhoCorasickAutomaton()

            for word in words:
                ac.add_word(word)

            ac.build_failure_links()

            # Search and extract context
            text = "رایانه به شبکه اینترنت متصل است."
            matches = ac.search(text)

            for word, start, end in matches:
                # Extract context (10 chars before and after)
                context_start = max(0, start - 10)
                context_end = min(len(text), end + 10)
                context = text[context_start:context_end]
                print(f"{word}: ...{context}...")

        .. admonition:: Performance characteristics
            :class: note

            * Time complexity: O(n + m + z) where n=text length, m=total pattern length, z=matches
            * Space complexity: O(m) for the trie structure
            * Initialization: O(m) to build the trie and failure links
            * Optimal for: Multiple patterns, large texts, repeated searches

    .. tab-item:: پارسی

        موتور جستجوی چندالگویی با استفاده از الگوریتم آهو-کُراسیک. این الگوریتم هستهٔ اصلی است که ``WordDetector`` برای شناسایی سریع چندین الگو به‌طور همزمان از آن استفاده می‌کند.

        *متدها*

        .. py:method:: add_word(word: str) -> None
            :no-index:

            افزودن واژه به درخت خودکار.

            :param word: واژه برای افزودن

        .. py:method:: build_failure_links() -> None
            :no-index:

            ساخت پیوندهای شکست برای تطبیق سریع. باید پس از افزودن همهٔ واژگان و پیش از جستجو فراخوانی شود.

        .. py:method:: search(text: str) -> List[Tuple[str, int, int]]
            :no-index:

            یافتن همهٔ تطبیق‌های الگو در متن.

            :param text: متن برای جستجو
            :return: فهرست تاپل‌ها (واژه_تطبیق‌یافته، موقعیت_آغاز، موقعیت_پایان)

        *نمونه کاربرد*

        .. code-block:: python

            from pasban.core import AhoCorasickAutomaton

            # ساخت خودکار
            ac = AhoCorasickAutomaton()

            # افزودن الگوها
            ac.add_word("کامپیوتر")
            ac.add_word("اینترنت")
            ac.add_word("سیستم")

            # ساخت پیوندهای شکست (لازم پیش از جستجو)
            ac.build_failure_links()

            # جستجوی الگوها
            text = "این کامپیوتر به اینترنت متصل است و سیستم عامل دارد."
            matches = ac.search(text)

            # پردازش نتایج
            for word, start, end in matches:
                print(f"'{word}' در موقعیت {start}-{end} یافت شد")
            # خروجی:
            # 'کامپیوتر' در موقعیت 4-12 یافت شد
            # 'اینترنت' در موقعیت 16-23 یافت شد
            # 'سیستم' در موقعیت 32-37 یافت شد

        *کاربرد پیشرفته*

        .. code-block:: python

            from pasban.core import AhoCorasickAutomaton

            # ساخت خودکار از فهرست واژگان
            words = ["رایانه", "اینترنت", "شبکه", "سامانه"]
            ac = AhoCorasickAutomaton()

            for word in words:
                ac.add_word(word)

            ac.build_failure_links()

            # جستجو و استخراج زمینه
            text = "رایانه به شبکه اینترنت متصل است."
            matches = ac.search(text)

            for word, start, end in matches:
                # استخراج زمینه (۱۰ نویسه پیش و پس)
                context_start = max(0, start - 10)
                context_end = min(len(text), end + 10)
                context = text[context_start:context_end]
                print(f"{word}: ...{context}...")

        .. admonition:: ویژگی‌های کارایی
            :class: note

            * پیچیدگی زمانی: O(n + m + z) که n=طول متن، m=مجموع طول الگوها، z=تطبیق‌ها
            * پیچیدگی فضایی: O(m) برای ساختار درخت
            * راه‌اندازی: O(m) برای ساخت درخت و پیوندهای شکست
            * بهینه برای: الگوهای چندگانه، متن‌های بزرگ، جستجوهای تکراری


Best Practices | نکات حرفه‌ای
=============================

.. tab-set::

    .. tab-item:: English

        *General Guidelines*

        .. grid:: 2
            :gutter: 3

            .. grid-item-card:: ✅ Always Do
                :class-card: sd-border-success

                * Enable normalization for consistent results
                * Enable contextual cleaning for literary texts
                * Use ``WordDetector`` for production environments
                * Reuse detector instances (avoid re-initialization)
                * Check ``foreign_percentage`` for quality metrics
                * Handle edge cases (empty text, pure Persian text)

            .. grid-item-card:: ⚠️ Be Careful
                :class-card: sd-border-warning

                * Don't disable normalization unless necessary
                * Don't disable contextual cleaning for formal texts
                * Be aware of initialization cost (~85ms)
                * Consider caching detector instances
                * Validate input text before processing
                * Handle encoding issues properly

        *Performance Optimization*

        .. code-block:: python

            from pasban.detector import WordDetector

            # ✅ Good: Initialize once, use many times
            detector = WordDetector()

            texts = ["متن اول", "متن دوم", "متن سوم"]
            for text in texts:
                result = detector.detect(text)
                print(result.count)

            # ❌ Bad: Re-initialize for each text
            for text in texts:
                detector = WordDetector()  # Wasteful!
                result = detector.detect(text)

        .. code-block:: python

            # ✅ Good: Disable options only when needed
            # For maximum speed on trusted, pre-normalized text
            result = detector.detect(text, normalize=False, contextual=False)

            # ✅ Good: Use appropriate engine
            # Large corpus processing
            detector = WordDetector()  # Fast

            # Small, critical accuracy scenarios
            detector = WordDetectorRegex()  # Accurate

        *Database Management*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

            # ✅ Good: Batch operations
            new_words = {
                "ویدئو": "ویدیو",
                "کلیپ": "بریده",
                "فایل": "پرونده"
            }

            for foreign, persian in new_words.items():
                repo.add_word(foreign, persian)

            # After updates, reload detector
            detector.reload()

            # ✅ Good: Export and backup
            all_words = repo.get_all_words()
            # Save to file for backup

        *Error Handling*

        .. code-block:: python

            from pasban.detector import WordDetector
            from pasban.db import WordRepo

            def safe_detect(text: str) -> DetectData:
                """Safely detect foreign words with error handling."""
                try:
                    if not text or not text.strip():
                        # Handle empty text
                        return None

                    detector = WordDetector()
                    result = detector.detect(text)
                    return result

                except Exception as e:
                    print(f"Error detecting words: {e}")
                    return None

            # Usage
            result = safe_detect("متن نمونه")
            if result:
                print(f"Found {result.count} foreign words")

        *Quality Assurance*

        .. code-block:: python

            def assess_text_quality(text: str) -> dict:
                """Assess Persian text quality based on foreign word percentage."""
                detector = WordDetector()
                result = detector.detect(text)

                quality = {
                    "foreign_count": result.count,
                    "foreign_percentage": result.foreign_percentage,
                    "total_words": result.total_words,
                    "status": "unknown"
                }

                # Define quality levels
                if result.foreign_percentage < 5:
                    quality["status"] = "excellent"
                elif result.foreign_percentage < 15:
                    quality["status"] = "good"
                elif result.foreign_percentage < 30:
                    quality["status"] = "acceptable"
                else:
                    quality["status"] = "needs_improvement"

                return quality

            # Usage
            text = "این متن شامل کامپیوتر و اینترنت است."
            quality = assess_text_quality(text)
            print(f"Text quality: {quality['status']}")
            print(f"Foreign words: {quality['foreign_percentage']:.1f}%")

    .. tab-item:: پارسی

        *راهنماهای کلی*

        .. grid:: 2
            :gutter: 3

            .. grid-item-card:: ✅ همواره انجام دهید
                :class-card: sd-border-success

                * نرمال‌سازی را برای نتایج یکسان فعال کنید
                * پالایش زمینه‌ای را برای متن‌های ادبی فعال کنید
                * از ``WordDetector`` در محیط تولید استفاده کنید
                * از نمونه‌های شناساگر مجدداً استفاده کنید (از راه‌اندازی دوباره بپرهیزید)
                * ``foreign_percentage`` را برای سنجش کیفیت بررسی کنید
                * موارد استثنایی را مدیریت کنید (متن خالی، متن پارسی سره)

            .. grid-item-card:: ⚠️ احتیاط کنید
                :class-card: sd-border-warning

                * نرمال‌سازی را بدون نیاز غیرفعال نکنید
                * پالایش زمینه‌ای را برای متن‌های رسمی غیرفعال نکنید
                * از هزینه راه‌اندازی (~۸۵ میلی‌ثانیه) آگاه باشید
                * حافظه‌نهانی نمونه‌های شناساگر را در نظر بگیرید
                * متن ورودی را پیش از پردازش اعتبارسنجی کنید
                * مسائل کدگذاری را به‌درستی مدیریت کنید

        *بهینه‌سازی کارایی*

        .. code-block:: python

            from pasban.detector import WordDetector

            # ✅ خوب: یک‌بار راه‌اندازی، چندین‌بار استفاده
            detector = WordDetector()

            texts = ["متن اول", "متن دوم", "متن سوم"]
            for text in texts:
                result = detector.detect(text)
                print(result.count)

            # ❌ بد: راه‌اندازی دوباره برای هر متن
            for text in texts:
                detector = WordDetector()  # اتلاف منابع!
                result = detector.detect(text)

        .. code-block:: python

            # ✅ خوب: گزینه‌ها را فقط در صورت نیاز غیرفعال کنید
            # برای سرعت بیشینه بر روی متن نرمال‌شده قابل اعتماد
            result = detector.detect(text, normalize=False, contextual=False)

            # ✅ خوب: از موتور مناسب استفاده کنید
            # پردازش مجموعه داده بزرگ
            detector = WordDetector()  # سریع

            # سناریوهای کوچک با موشکافی حیاتی
            detector = WordDetectorRegex()  # دقیق

        *مدیریت پایگاه‌داده*

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()

            # ✅ خوب: عملیات دسته‌ای
            new_words = {
                "ویدئو": "ویدیو",
                "کلیپ": "بریده",
                "فایل": "پرونده"
            }

            for foreign, persian in new_words.items():
                repo.add_word(foreign, persian)

            # پس از به‌روزرسانی، شناساگر را بارگذاری دوباره کنید
            detector.reload()

            # ✅ خوب: برون‌بری و پشتیبان‌گیری
            all_words = repo.get_all_words()
            # ذخیره در پرونده برای پشتیبان

        *مدیریت خطا*

        .. code-block:: python

            from pasban.detector import WordDetector
            from pasban.db import WordRepo

            def safe_detect(text: str) -> DetectData:
                """شناسایی ایمن واژگان بیگانه با مدیریت خطا."""
                try:
                    if not text or not text.strip():
                        # مدیریت متن خالی
                        return None

                    detector = WordDetector()
                    result = detector.detect(text)
                    return result

                except Exception as e:
                    print(f"خطا در شناسایی واژگان: {e}")
                    return None

            # استفاده
            result = safe_detect("متن نمونه")
            if result:
                print(f"{result.count} واژه بیگانه یافت شد")

        *تضمین کیفیت*

        .. code-block:: python

            def assess_text_quality(text: str) -> dict:
                """ارزیابی کیفیت متن پارسی بر اساس درصد واژگان بیگانه."""
                detector = WordDetector()
                result = detector.detect(text)

                quality = {
                    "foreign_count": result.count,
                    "foreign_percentage": result.foreign_percentage,
                    "total_words": result.total_words,
                    "status": "نامشخص"
                }

                # تعریف سطوح کیفیت
                if result.foreign_percentage < 5:
                    quality["status"] = "عالی"
                elif result.foreign_percentage < 15:
                    quality["status"] = "خوب"
                elif result.foreign_percentage < 30:
                    quality["status"] = "قابل‌قبول"
                else:
                    quality["status"] = "نیاز_به_بهبود"

                return quality

            # استفاده
            text = "این متن شامل کامپیوتر و اینترنت است."
            quality = assess_text_quality(text)
            print(f"کیفیت متن: {quality['status']}")
            print(f"واژگان بیگانه: {quality['foreign_percentage']:.1f}%")


Use Cases | موارد کاربرد
-------------------------

.. tab-set::

    .. tab-item:: English

        *Content Quality Control*

        .. code-block:: python

            from pasban.detector import WordDetector

            def validate_persian_content(content: str, threshold: float = 20.0) -> tuple[bool, str]:
                """Validate that content meets Persian purity standards."""
                detector = WordDetector()
                result = detector.detect(content)

                if result.foreign_percentage > threshold:
                    message = f"Content contains {result.foreign_percentage:.1f}% foreign words (threshold: {threshold}%)"
                    return False, message

                return True, "Content meets purity standards"

            # Usage in CMS
            article_text = "این مقاله دربارهٔ رایانه است..."
            is_valid, message = validate_persian_content(article_text)
            if not is_valid:
                print(f"Rejected: {message}")

        *Text Processing Pipeline*

        .. code-block:: python

            from pasban.detector import WordDetector
            from pasban.normalizer.text_normalizer import WordNormalizer

            class PersianTextProcessor:
                def __init__(self):
                    self.detector = WordDetector()

                def process(self, text: str) -> dict:
                    """Complete text processing pipeline."""
                    # Step 1: Normalize
                    normalized = WordNormalizer.normalize_text(text)

                    # Step 2: Detect foreign words
                    result = self.detector.detect(normalized)

                    # Step 3: Generate report
                    report = {
                        "original_text": text,
                        "normalized_text": normalized,
                        "foreign_words": result.words,
                        "statistics": {
                            "total_words": result.total_words,
                            "foreign_count": result.count,
                            "foreign_percentage": result.foreign_percentage
                        },
                        "quality": self._assess_quality(result.foreign_percentage)
                    }

                    return report

                def _assess_quality(self, percentage: float) -> str:
                    if percentage < 5:
                        return "excellent"
                    elif percentage < 15:
                        return "good"
                    elif percentage < 30:
                        return "acceptable"
                    return "poor"

            # Usage
            processor = PersianTextProcessor()
            report = processor.process("این متن شامل کامپیوتر است.")
            print(f"Quality: {report['quality']}")
            print(f"Foreign words: {report['foreign_words']}")

        *Educational Applications*

        .. code-block:: python

            from pasban.detector import WordDetector

            def create_learning_material(text: str) -> str:
                """Create educational material showing foreign word alternatives."""
                detector = WordDetector()
                result = detector.detect(text)

                if result.count == 0:
                    return "✅ این متن سراسر پارسی است!"

                output = ["📚 واژگان بیگانه و برابرهای پارسی آن‌ها:\n"]

                for foreign, persian in result.words.items():
                    if foreign != persian:
                        output.append(f"❌ {foreign} → ✅ {persian}")
                    else:
                        output.append(f"⚠️ {foreign} (برابر پارسی ندارد)")

                output.append(f"\n📊 آمار: {result.count} واژه بیگانه از {result.total_words} واژه ({result.foreign_percentage:.1f}%)")

                return "\n".join(output)

            # Usage
            student_text = "من با کامپیوتر کار می‌کنم و از اینترنت استفاده می‌کنم."
            learning_material = create_learning_material(student_text)
            print(learning_material)

        *Batch Document Processing*

        .. code-block:: python

            from pasban.detector import WordDetector
            from pathlib import Path
            import json

            def process_documents(input_dir: str, output_file: str):
                """Process multiple documents and generate comprehensive report."""
                detector = WordDetector()
                results = []

                for file_path in Path(input_dir).glob("*.txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()

                    result = detector.detect(text)

                    results.append({
                        "filename": file_path.name,
                        "total_words": result.total_words,
                        "foreign_count": result.count,
                        "foreign_percentage": result.foreign_percentage,
                        "foreign_words": list(result.words.keys())
                    })

                # Save report
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

                return results

            # Usage
            results = process_documents("./documents", "./report.json")
            print(f"Processed {len(results)} documents")

    .. tab-item:: پارسی

        *کنترل کیفیت محتوا*

        .. code-block:: python

            from pasban.detector import WordDetector

            def validate_persian_content(content: str, threshold: float = 20.0) -> tuple[bool, str]:
                """اعتبارسنجی محتوا بر اساس استانداردهای پارسی سره."""
                detector = WordDetector()
                result = detector.detect(content)

                if result.foreign_percentage > threshold:
                    message = f"محتوا شامل {result.foreign_percentage:.1f}% واژه بیگانه است (آستانه: {threshold}%)"
                    return False, message

                return True, "محتوا استانداردهای پارسی سره را رعایت می‌کند"

            # استفاده در سامانه مدیریت محتوا
            article_text = "این مقاله دربارهٔ رایانه است..."
            is_valid, message = validate_persian_content(article_text)
            if not is_valid:
                print(f"رد شد: {message}")

        *خط پردازش متن*

        .. code-block:: python

            from pasban.detector import WordDetector
            from pasban.normalizer.text_normalizer import WordNormalizer

            class PersianTextProcessor:
                def __init__(self):
                    self.detector = WordDetector()

                def process(self, text: str) -> dict:
                    """خط لوله کامل پردازش متن."""
                    # گام ۱: نرمال‌سازی
                    normalized = WordNormalizer.normalize_text(text)

                    # گام ۲: شناسایی واژگان بیگانه
                    result = self.detector.detect(normalized)

                    # گام ۳: تولید گزارش
                    report = {
                        "متن_اصلی": text,
                        "متن_نرمال‌شده": normalized,
                        "واژگان_بیگانه": result.words,
                        "آمار": {
                            "کل_واژگان": result.total_words,
                            "تعداد_بیگانه": result.count,
                            "درصد_بیگانه": result.foreign_percentage
                        },
                        "کیفیت": self._assess_quality(result.foreign_percentage)
                    }

                    return report

                def _assess_quality(self, percentage: float) -> str:
                    if percentage < 5:
                        return "عالی"
                    elif percentage < 15:
                        return "خوب"
                    elif percentage < 30:
                        return "قابل‌قبول"
                    return "ضعیف"

            # استفاده
            processor = PersianTextProcessor()
            report = processor.process("این متن شامل کامپیوتر است.")
            print(f"کیفیت: {report['کیفیت']}")
            print(f"واژگان بیگانه: {report['واژگان_بیگانه']}")

        *کاربردهای آموزشی*

        .. code-block:: python

            from pasban.detector import WordDetector

            def create_learning_material(text: str) -> str:
                """ایجاد محتوای آموزشی برای نمایش برابرهای پارسی."""
                detector = WordDetector()
                result = detector.detect(text)

                if result.count == 0:
                    return "✅ این متن سراسر پارسی است!"

                output = ["📚 واژگان بیگانه و برابرهای پارسی آن‌ها:\n"]

                for foreign, persian in result.words.items():
                    if foreign != persian:
                        output.append(f"❌ {foreign} → ✅ {persian}")
                    else:
                        output.append(f"⚠️ {foreign} (برابر پارسی ندارد)")

                output.append(f"\n📊 آمار: {result.count} واژه بیگانه از {result.total_words} واژه ({result.foreign_percentage:.1f}%)")

                return "\n".join(output)

            # استفاده
            student_text = "من با کامپیوتر کار می‌کنم و از اینترنت استفاده می‌کنم."
            learning_material = create_learning_material(student_text)
            print(learning_material)

        *پردازش دسته‌ای اسناد*

        .. code-block:: python

            from pasban.detector import WordDetector
            from pathlib import Path
            import json

            def process_documents(input_dir: str, output_file: str):
                """پردازش اسناد چندگانه و تولید گزارش جامع."""
                detector = WordDetector()
                results = []

                for file_path in Path(input_dir).glob("*.txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()

                    result = detector.detect(text)

                    results.append({
                        "نام_پرونده": file_path.name,
                        "کل_واژگان": result.total_words,
                        "تعداد_بیگانه": result.count,
                        "درصد_بیگانه": result.foreign_percentage,
                        "واژگان_بیگانه": list(result.words.keys())
                    })

                # ذخیره گزارش
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

                return results

            # استفاده
            results = process_documents("./documents", "./report.json")
            print(f"{len(results)} سند پردازش شد")


FAQ | پرسش‌های متداول
----------------------

.. tab-set::

    .. tab-item:: English

        .. dropdown:: Why are some Arabic words not detected?
            :open:

            Pasban focuses on non-Persian words. Many Arabic words are considered part of Persian vocabulary due to historical linguistic integration. If you need to detect Arabic words specifically, you can extend the database with additional Arabic terms.

        .. dropdown:: Can I use Pasban offline?

            Yes! After the initial database download, Pasban works completely offline. The database is cached locally and doesn't require internet connection for subsequent uses.

        .. dropdown:: How accurate is the detection?

            Accuracy depends on the engine and settings:

            * WordDetector: ~98% accuracy with default settings
            * WordDetectorRegex: ~99% accuracy
            * Both achieve best results with normalization and contextual cleaning enabled

        .. dropdown:: Can I add custom words to the database?

            Yes! Use ``WordRepo`` to add, update, or remove words:

            .. code-block:: python

                from pasban.db import WordRepo

                repo = WordRepo()
                repo.add_word("کاستوم", "سفارشی")

                # Reload detector after updates
                detector.reload()

        .. dropdown:: What's the difference between count and unique_count?

            * ``count``: Total number of foreign word occurrences (includes duplicates)
            * ``unique_count``: Number of unique foreign words

            Example: "کامپیوتر و کامپیوتر" → count=2, unique_count=1

        .. dropdown:: How do I handle very large texts?

            For large texts (>10MB):

            1. Split text into chunks
            2. Process each chunk separately
            3. Aggregate results
            4. Use ``WordDetector`` (much faster for large texts)

        .. dropdown:: Can I use Pasban in web applications?

            Yes! Pasban is thread-safe and can be used in web applications. Create a single detector instance and reuse it across requests for best performance.

        .. dropdown:: How often is the database updated?

            The database is community-maintained and updated regularly. You can contribute new words or corrections through the project repository.

    .. tab-item:: پارسی

        .. dropdown:: چرا برخی واژگان شناسایی نمی‌شوند؟
            :open:

            پایگاه داده پاسبان در امایه گسترش است و شاید برخی واژگان اینک در پایگاه داده نباشند.

        .. dropdown:: آیا می‌توانم از پاسبان به‌صورت آفلاین بکار گیرم؟

            بله! پس از بارگیری نخستین پایگاه‌داده، پاسبان به‌طور کامل آفلاین کار می‌کند. پایگاه‌داده به‌صورت محلی حافظه‌نهانی می‌شود و برای استفاده‌های بعدی نیازی به پیوند اینترنت ندارد.

        .. dropdown:: موشکافی شناسایی چه اندازه است؟

            موشکافی به موتور و تنظیمات بستگی دارد:

            * WordDetector: موشکافی ~۹۸٪ با تنظیمات پیش‌فرض
            * WordDetectorRegex: موشکافی ~۹۹٪
            * هر دو با فعال بودن نرمال‌سازی و پالایش زمینه‌ای بهترین نتایج را دارند

        .. dropdown:: آیا می‌توانم واژگان سفارشی به پایگاه‌داده بیفزایم؟

            بله! از ``WordRepo`` برای افزودن، ویرایش یا حذف واژگان استفاده کنید:

            .. code-block:: python

                from pasban.db import WordRepo

                repo = WordRepo()
                repo.add_word("کاستوم", "سفارشی")

                # شناساگر را پس از به‌روزرسانی بارگذاری دوباره کنید
                detector.reload()

        .. dropdown:: تفاوت count و unique_count چیست؟

            * ``count``: تعداد کل رخدادهای واژه بیگانه (شامل تکراری‌ها)
            * ``unique_count``: تعداد واژگان بیگانه یکتا

            مثال: "کامپیوتر و کامپیوتر" ← count=2، unique_count=1

        .. dropdown:: چگونه متن‌های بسیار بزرگ را مدیریت کنم؟

            برای متن‌های بزرگ (بیش از ۱۰ مگابایت):

            1. متن را به بخش‌های کوچک‌تر تقسیم کنید
            2. هر بخش را جداگانه پردازش کنید
            3. نتایج را جمع‌آوری کنید
            4. از ``WordDetector`` استفاده کنید (برای متن‌های بزرگ بسیار سریع‌تر است)

        .. dropdown:: آیا می‌توانم از پاسبان در برنامه‌های وب استفاده کنم؟

            بله! پاسبان ایمن در برابر نخ (thread-safe) است و می‌تواند در برنامه‌های وب استفاده شود. یک نمونه شناساگر بسازید و آن را در درخواست‌ها مجدداً استفاده کنید تا کارایی بهینه داشته باشید.

        .. dropdown:: پایگاه‌داده چه اندازه یک‌بار به‌روزرسانی می‌شود؟

            پایگاه‌داده توسط جامعه نگهداری می‌شود و به‌طور منظم به‌روزرسانی می‌گردد. می‌توانید واژگان جدید یا اصلاحات را از طریق مخزن پروژه مشارکت کنید.


Troubleshooting | عیب‌یابی
---------------------------

.. tab-set::

    .. tab-item:: English

        *Common Issues and Solutions*

        .. grid:: 1
            :gutter: 3

            .. grid-item-card:: Issue: Slow Performance
                :class-card: sd-border-warning

                **Symptoms:** Detection takes too long

                **Solutions:**

                * Use ``WordDetector`` instead of ``WordDetectorRegex``
                * Reuse detector instances instead of re-initializing
                * Consider disabling contextual cleaning for simple texts
                * Process large texts in smaller chunks

                .. code-block:: python

                    # ✅ Good
                    detector = WordDetector()  # Initialize once
                    for text in texts:
                        result = detector.detect(text)

                    # ❌ Slow
                    for text in texts:
                        detector = WordDetector()  # Re-initializing!
                        result = detector.detect(text)

            .. grid-item-card:: Issue: Incorrect Detection
                :class-card: sd-border-danger

                **Symptoms:** Words not detected or false positives

                **Solutions:**

                * Enable normalization: ``detect(text, normalize=True)``
                * Enable contextual cleaning: ``detect(text, contextual=True)``
                * Try ``WordDetectorRegex`` for better accuracy
                * Check if word exists in database: ``repo.get_persian("word")``
                * Add missing words to database: ``repo.add_word("word", "persian")``

                .. code-block:: python

                    from pasban.db import WordRepo

                    repo = WordRepo()

                    # Check if word exists
                    persian = repo.get_persian("کامپیوتر")
                    if not persian:
                        # Add it
                        repo.add_word("کامپیوتر", "رایانه")

            .. grid-item-card:: Issue: Database Not Loading
                :class-card: sd-border-danger

                **Symptoms:** Import errors or missing database

                **Solutions:**

                * Ensure internet connection for initial download
                * Check installation: ``pip install --upgrade pasban``
                * Verify database path permissions
                * Try manual reload: ``repo.get_all_words(reload=True)``

                .. code-block:: python

                    from pasban.db import WordRepo

                    try:
                        repo = WordRepo()
                        words = repo.get_all_words(reload=True)
                        print(f"Loaded {len(words)} words")
                    except Exception as e:
                        print(f"Error: {e}")

            .. grid-item-card:: Issue: Memory Usage
                :class-card: sd-border-warning

                **Symptoms:** High memory consumption

                **Solutions:**

                * Process large texts in chunks
                * Don't store all DetectData objects in memory
                * Extract only needed information from results
                * Use ``detect_words()`` instead of ``detect()`` if you only need the word mappings

                .. code-block:: python

                    # ✅ Memory efficient
                    detector = WordDetector()
                    for text in large_text_list:
                        words = detector.detect_words(text)  # Only words dict
                        process(words)
                        # words is garbage collected after loop

                    # ❌ Memory intensive
                    results = []
                    for text in large_text_list:
                        results.append(detector.detect(text))  # Stores everything

            .. grid-item-card:: Issue: Encoding Problems
                :class-card: sd-border-info

                **Symptoms:** Garbled text or incorrect characters

                **Solutions:**

                * Always use UTF-8 encoding for files
                * Normalize text before processing
                * Check input source encoding

                .. code-block:: python

                    # ✅ Correct encoding
                    with open('file.txt', 'r', encoding='utf-8') as f:
                        text = f.read()

                    # Normalize to ensure consistent encoding
                    from pasban.normalizer.text_normalizer import WordNormalizer
                    text = WordNormalizer.normalize_text(text)

    .. tab-item:: پارسی

        *مسائل رایج و راه‌حل‌ها*

        .. grid:: 1
            :gutter: 3

            .. grid-item-card:: مسئله: کارایی پایین
                :class-card: sd-border-warning

                **علائم:** شناسایی زمان زیادی می‌برد

                **راه‌حل‌ها:**

                * از ``WordDetector`` به‌جای ``WordDetectorRegex`` استفاده کنید
                * از نمونه‌های شناساگر مجدداً استفاده کنید به‌جای راه‌اندازی دوباره
                * پالایش زمینه‌ای را برای متن‌های ساده غیرفعال کنید
                * متن‌های بزرگ را به بخش‌های کوچک‌تر پردازش کنید

                .. code-block:: python

                    # ✅ خوب
                    detector = WordDetector()  # یک‌بار راه‌اندازی
                    for text in texts:
                        result = detector.detect(text)

                    # ❌ کند
                    for text in texts:
                        detector = WordDetector()  # راه‌اندازی دوباره!
                        result = detector.detect(text)

            .. grid-item-card:: مسئله: شناسایی نادرست
                :class-card: sd-border-danger

                **علائم:** واژگان شناسایی نمی‌شوند یا مثبت کاذب وجود دارد

                **راه‌حل‌ها:**

                * نرمال‌سازی را فعال کنید: ``detect(text, normalize=True)``
                * پالایش زمینه‌ای را فعال کنید: ``detect(text, contextual=True)``
                * ``WordDetectorRegex`` را برای موشکافی بهتر امتحان کنید
                * بررسی کنید واژه در پایگاه‌داده وجود دارد: ``repo.get_persian("word")``
                * واژگان گم‌شده را به پایگاه‌داده بیفزایید: ``repo.add_word("word", "persian")``

                .. code-block:: python

                    from pasban.db import WordRepo

                    repo = WordRepo()

                    # بررسی وجود واژه
                    persian = repo.get_persian("کامپیوتر")
                    if not persian:
                        # افزودن آن
                        repo.add_word("کامپیوتر", "رایانه")

            .. grid-item-card:: مسئله: بارگذاری نشدن پایگاه‌داده
                :class-card: sd-border-danger

                **علائم:** خطاهای وارد کردن یا پایگاه‌داده گم‌شده

                **راه‌حل‌ها:**

                * از پیوند اینترنت برای بارگیری نخستین اطمینان حاصل کنید
                * نصب را بررسی کنید: ``pip install --upgrade pasban``
                * مجوزهای مسیر پایگاه‌داده را تأیید کنید
                * بارگذاری دستی را امتحان کنید: ``repo.get_all_words(reload=True)``

                .. code-block:: python

                    from pasban.db import WordRepo

                    try:
                        repo = WordRepo()
                        words = repo.get_all_words(reload=True)
                        print(f"{len(words)} واژه بارگذاری شد")
                    except Exception as e:
                        print(f"خطا: {e}")

            .. grid-item-card:: مسئله: مصرف حافظه
                :class-card: sd-border-warning

                **علائم:** مصرف بالای حافظه

                **راه‌حل‌ها:**

                * متن‌های بزرگ را به بخش‌ها پردازش کنید
                * همهٔ اشیاء DetectData را در حافظه ذخیره نکنید
                * فقط اطلاعات مورد نیاز را از نتایج استخراج کنید
                * اگر فقط نگاشت واژگان را نیاز دارید، از ``detect_words()`` به‌جای ``detect()`` استفاده کنید

                .. code-block:: python

                    # ✅ کارآمد در حافظه
                    detector = WordDetector()
                    for text in large_text_list:
                        words = detector.detect_words(text)  # فقط دیکشنری واژگان
                        process(words)
                        # words پس از حلقه جمع‌آوری زباله می‌شود

                    # ❌ پرمصرف حافظه
                    results = []
                    for text in large_text_list:
                        results.append(detector.detect(text))  # همه چیز را ذخیره می‌کند

            .. grid-item-card:: مسئله: مشکلات کدگذاری
                :class-card: sd-border-info

                **علائم:** متن مخدوش یا نویسه‌های نادرست

                **راه‌حل‌ها:**

                * همواره از کدگذاری UTF-8 برای پرونده‌ها استفاده کنید
                * متن را پیش از پردازش نرمال کنید
                * کدگذاری منبع ورودی را بررسی کنید

                .. code-block:: python

                    # ✅ کدگذاری صحیح
                    with open('file.txt', 'r', encoding='utf-8') as f:
                        text = f.read()

                    # نرمال‌سازی برای اطمینان از کدگذاری یکسان
                    from pasban.normalizer.text_normalizer import WordNormalizer
                    text = WordNormalizer.normalize_text(text)


API Reference Summary | خلاصه مرجع API
---------------------------------------

.. tab-set::

    .. tab-item:: English

        *Quick Reference*

        **Detection Engines**

        .. code-block:: python

            from pasban.detector import WordDetector, WordDetectorRegex

            # Fast detection (recommended)
            detector = WordDetector()
            result = detector.detect(text, normalize=True, contextual=True)
            words = detector.detect_words(text)
            detector.reload()

            # Accurate detection
            detector_regex = WordDetectorRegex()
            result = detector_regex.detect(text, normalize=True, contextual=True)
            words_list = detector_regex.find_words_in_text(text)

        **Word Repository**

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()
            all_words = repo.get_all_words(reload=False)
            results = repo.search_word(search_term, limit=5)
            repo.add_word(foreign, persian)
            repo.update_word(foreign, persian)
            repo.remove_word(foreign)
            persian = repo.get_persian(foreign)

        **Normalization**

        .. code-block:: python

            from pasban.normalizer.text_normalizer import WordNormalizer

            normalized = WordNormalizer.normalize_text(text)

        **Contextual Cleaning**

        .. code-block:: python

            from pasban.normalizer.contextual_remover import contextual_cleaner

            cleaned = contextual_cleaner.clean_text(text)

        **DetectData Attributes**

        .. code-block:: python

            result = detector.detect(text)

            result.foreign_words      # list[str]
            result.words              # dict[str, str]
            result.text               # str
            result.count              # int
            result.unique_count       # int
            result.total_words        # int
            result.foreign_percentage # float
            result.to_text            # str
            result.to_summary_text    # str

    .. tab-item:: پارسی

        *مرجع سریع*

        **موتورهای شناسایی**

        .. code-block:: python

            from pasban.detector import WordDetector, WordDetectorRegex

            # شناسایی سریع (پیشنهاد می‌شود)
            detector = WordDetector()
            result = detector.detect(text, normalize=True, contextual=True)
            words = detector.detect_words(text)
            detector.reload()

            # شناسایی دقیق
            detector_regex = WordDetectorRegex()
            result = detector_regex.detect(text, normalize=True, contextual=True)
            words_list = detector_regex.find_words_in_text(text)

        **مخزن واژگان**

        .. code-block:: python

            from pasban.db import WordRepo

            repo = WordRepo()
            all_words = repo.get_all_words(reload=False)
            results = repo.search_word(search_term, limit=5)
            repo.add_word(foreign, persian)
            repo.update_word(foreign, persian)
            repo.remove_word(foreign)
            persian = repo.get_persian(foreign)

        **نرمال‌سازی**

        .. code-block:: python

            from pasban.normalizer.text_normalizer import WordNormalizer

            normalized = WordNormalizer.normalize_text(text)

        **پالایش زمینه‌ای**

        .. code-block:: python

            from pasban.normalizer.contextual_remover import contextual_cleaner

            cleaned = contextual_cleaner.clean_text(text)

        **ویژگی‌های DetectData**

        .. code-block:: python

            result = detector.detect(text)

            result.foreign_words      # list[str]
            result.words              # dict[str, str]
            result.text               # str
            result.count              # int
            result.unique_count       # int
            result.total_words        # int
            result.foreign_percentage # float
            result.to_text            # str
            result.to_summary_text    # str


Contributing | مشارکت
---------------------

.. tab-set::

    .. tab-item:: English

        We welcome contributions to Pasban! Here's how you can help:

        **Ways to Contribute**

        * Report bugs or incorrect detections
        * Improve documentation
        * Submit performance optimizations
        * Add new features
        * Write tests

        **Reporting Issues**

        Please include:

        * Clear description of the issue
        * Example text demonstrating the problem
        * Expected vs actual behavior
        * Python version and Pasban version
        * Full error traceback (if applicable)

        **Code Style**

        * Follow PEP 8 guidelines
        * Write docstrings for all public functions
        * Include type hints
        * Add tests for new features
        * Update documentation

    .. tab-item:: پارسی

        از مشارکت شما در پاسبان استقبال می‌کنیم! راه‌های مشارکت:

        **روش‌های مشارکت**

        * گزارش اشکالات یا شناسایی‌های نادرست
        * بهبود مستندات
        * ارسال بهینه‌سازی‌های کارایی
        * افزودن ویژگی‌های جدید
        * نوشتن آزمون‌ها


        **گزارش مسائل**

        لطفاً شامل باشد:

        * توضیح واضح مسئله
        * متن نمونه نمایش‌دهندهٔ مشکل
        * رفتار مورد انتظار در مقابل رفتار واقعی
        * نسخه پایتون و نسخه پاسبان
        * ردیابی کامل خطا (در صورت وجود)

        **سبک کد**

        * راهنماهای PEP 8 را دنبال کنید
        * برای همهٔ توابع عمومی docstring بنویسید
        * راهنماهای نوع را بیفزایید
        * برای ویژگی‌های جدید آزمون بنویسید
        * مستندات را به‌روزرسانی کنید


License and Credits | مجوز و اعتبارات
--------------------------------------

.. tab-set::

    .. tab-item:: English

        **License**

        Pasban is released under the MIT License.

        **Credits**

        * Developed and maintained by the Persian NLP community
        * Word database curated by contributors
        * Built with Python and love for Persian language

        **Acknowledgments**

        Special thanks to all contributors who help maintain and improve the word database.

    .. tab-item:: پارسی

        **مجوز**

        پاسبان تحت مجوز MIT منتشر شده است.

        **اعتبارات**

        * توسعه و نگهداری توسط انجمن پاسبان سره گرایی ایران
        * پایگاه واژگان گردآوری‌شده توسط مشارکت‌کنندگان
        * ساخته‌شده با پایتون و عشق به زبان پارسی

        **قدردانی**

        سپاس ویژه از همهٔ مشارکت‌کنندگانی که به نگهداری و بهبود پایگاه واژگان کمک می‌کنند.
