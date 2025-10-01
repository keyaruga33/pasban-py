import sqlite3
import tempfile
from pathlib import Path
from typing import List, Tuple, Dict

import pytest

from pasban.core.exceptions import WordAlreadyExistsError, WordNotFoundError
from pasban.db import WordRepo, DataLoader


class TestWordRepoBase:
    """
    Base class for WordRepo integration tests using a temporary SQLite database.

    Sets up:
    - Temporary SQLite file database
    - Words table compatible with WordRepo (`words` table with columns `word` and `parsi`)
    - WordRepo instance connected to this database
    """

    @pytest.fixture(autouse=True)
    def setup_repo(self, request):
        """
        Fixture to setup temporary database and WordRepo instance.

        Ensures cleanup after tests by deleting the temporary file.
        """
        tmpfile = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = Path(tmpfile.name)
        tmpfile.close()

        # Create words table
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
                     CREATE TABLE words
                     (
                         word  TEXT PRIMARY KEY,
                         parsi TEXT
                     )
                     """)
        conn.commit()
        conn.close()

        # Patch DataLoader to return our temporary DB path
        self.original_get_db_path = DataLoader.get_db_path
        DataLoader.get_db_path = staticmethod(lambda: self.db_path)

        # Initialize WordRepo
        self.repo = WordRepo()

        # Cleanup after test
        def fin():
            import os
            DataLoader.get_db_path = self.original_get_db_path
            if self.db_path.exists():
                os.remove(self.db_path)

        request.addfinalizer(fin)
        yield


class TestWordRepo(TestWordRepoBase):
    """Integration tests for the updated WordRepo class."""

    # -------- get_all_words & search_word --------

    def test_get_all_words_returns_inserted_data(self):
        """Test that get_all_words returns all rows inserted into the words table."""
        conn = sqlite3.connect(self.db_path)
        test_data: List[Tuple[str, str]] = [("سلام", "درود"), ("خانه", "مسکن")]
        conn.executemany("INSERT INTO words (word, parsi) VALUES (?, ?)", test_data)
        conn.commit()
        conn.close()

        results: Dict[str, str] = self.repo.get_all_words(reload=True)
        assert results == dict(test_data), "All inserted words should be returned by get_all_words"

    def test_search_word_by_word_column(self):
        """Test that searching by partial word matches correctly."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO words VALUES (?, ?)", ("دوست", "یار"))
        conn.commit()
        conn.close()

        results: List[Tuple[str, str]] = self.repo.search_word("دو")
        assert ("دوست", "یار") in results, "Partial search should match the word column"

    def test_search_word_by_parsi_column(self):
        """Test that searching by partial equivalent (parsi) matches correctly."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO words VALUES (?, ?)", ("خانه", "مسکن"))
        conn.commit()
        conn.close()

        results: List[Tuple[str, str]] = self.repo.search_word("مسک")
        assert ("خانه", "مسکن") in results, "Partial search should match the parsi column"

    def test_search_word_respects_limit(self):
        """Test that the limit parameter is respected in search results."""
        conn = sqlite3.connect(self.db_path)
        conn.executemany(
            "INSERT INTO words VALUES (?, ?)",
            [("الف", "A"), ("ب", "B"), ("پ", "P")]
        )
        conn.commit()
        conn.close()

        results = self.repo.search_word("ا", limit=1)
        assert len(results) == 1, "Search should respect the provided limit"

    def test_search_word_sanitizes_wildcards(self):
        """Test that % and _ characters in search input are sanitized."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO words VALUES (?, ?)", ("zacd", "xyz"))
        conn.commit()
        conn.close()

        results = self.repo.search_word("a%c")  # % should be stripped -> "ac"
        assert ("zacd", "xyz") in results, "Sanitized input should still find matching words"

    # -------- add_word --------

    def test_add_word_inserts_new_entry(self):
        """Test that add_word inserts a new entry into the database."""
        self.repo.add_word("test", "آزمایش")
        result = self.repo.get_persian("test")
        assert result == "آزمایش", "Word should be added and retrievable"

    def test_add_word_raises_if_exists(self):
        """Test that add_word raises WordAlreadyExistsError if word already exists."""
        self.repo.add_word("test", "آزمایش")
        with pytest.raises(WordAlreadyExistsError):
            self.repo.add_word("test", "دیگری")

    # -------- remove_word --------

    def test_remove_word_deletes_entry(self):
        """Test that remove_word deletes the word from database and cache."""
        self.repo.add_word("delete_me", "پاک")
        self.repo.remove_word("delete_me")
        result = self.repo.get_persian("delete_me")
        assert result is None, "Removed word should not be found in database"

    def test_remove_word_raises_if_not_found(self):
        """Test that remove_word raises WordNotFoundError if word does not exist."""
        with pytest.raises(WordNotFoundError):
            self.repo.remove_word("not_there")

    # -------- update_word --------

    def test_update_word_changes_equivalent(self):
        """Test that update_word successfully changes the Persian equivalent."""
        self.repo.add_word("update_me", "قدیم")
        self.repo.update_word("update_me", "جدید")
        result = self.repo.get_persian("update_me")
        assert result == "جدید", "Word's Persian equivalent should be updated"

    def test_update_word_raises_if_not_found(self):
        """Test that update_word raises WordNotFoundError if word does not exist."""
        with pytest.raises(WordNotFoundError):
            self.repo.update_word("missing", "چیزی")

    # -------- get_persian --------

    def test_get_persian_returns_none_if_not_found(self):
        """Test that get_persian returns None if the word is not in the database."""
        result = self.repo.get_persian("ghost")
        assert result is None, "Nonexistent word should return None"
