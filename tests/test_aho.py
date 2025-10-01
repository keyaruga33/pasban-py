from pasban.core.data_types import AhoCorasickAutomaton


def test_aho_corasick_basic_search():
    """
    Test Aho-Corasick automaton basic functionality.
    """
    words = ["he", "she", "his", "hers"]
    text = "ushers"

    automaton = AhoCorasickAutomaton()
    for word in words:
        automaton.add_word(word)

    automaton.build_failure_links()
    results = automaton.search(text)

    matched_words = sorted([w for w, _, _ in results])
    expected_matches = sorted(["she", "he", "hers"])
    assert matched_words == expected_matches

    positions = {w: (start, end) for w, start, end in results}
    # Correct 0-based indices
    assert positions["she"] == (1, 4)
    assert positions["he"] == (2, 4)
    assert positions["hers"] == (2, 6)


def test_aho_corasick_no_match():
    """
    Test that search returns empty list if no match found.
    """
    automaton = AhoCorasickAutomaton()
    automaton.add_word("abc")
    automaton.build_failure_links()

    results = automaton.search("xyz")
    assert results == []


def test_aho_corasick_partial_overlap():
    """
    Test automaton handles overlapping patterns correctly.
    """
    automaton = AhoCorasickAutomaton()
    automaton.add_word("a")
    automaton.add_word("ab")
    automaton.add_word("bc")
    automaton.build_failure_links()

    text = "abc"
    results = automaton.search(text)

    matched_words = sorted([w for w, _, _ in results])
    expected = sorted(["a", "ab", "bc"])
    assert matched_words == expected

    positions = {w: (start, end) for w, start, end in results}
    assert positions["a"] == (0, 1)
    assert positions["ab"] == (0, 2)
    assert positions["bc"] == (1, 3)
