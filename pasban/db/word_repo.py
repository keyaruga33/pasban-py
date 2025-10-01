from pathlib import Path
from typing import List, Tuple, Dict, Optional

from pasban.core.exceptions import WordAlreadyExistsError, WordNotFoundError
from ._connector import DBConnector
from ._data_loader import DataLoader

words_cache: Dict[str, str] = {}


class WordRepo:
    """
    Repository class for managing word lookups in the database.

    This class provides high-level methods to query and modify the `words` table,
    including fetching, searching, adding, updating, and removing words.

    Attributes:
        db_path (Path): Path to the SQLite database file.
        db (DBConnector): Persistent DBConnector instance for executing queries.
    """

    def __init__(self):
        """
        Initialize the WordRepo with a database path.
        """
        self.db_path: Path = DataLoader.get_db_path()
        self.db: DBConnector = DBConnector(self.db_path)

    @staticmethod
    def get_all_words(reload: bool = False) -> Dict[str, str]:
        """
        Get all words and their Persian equivalents from the database or cache.

        Args:
            reload (bool): If True, reload the cache from the database.

        Returns:
            Dict[str, str]: Dictionary mapping foreign word -> Persian equivalent.
        """
        if reload and words_cache:
            words_cache.clear()

        if words_cache:
            return words_cache

        data = DBConnector.execute_temp(
            DataLoader.get_db_path(),
            "SELECT word, parsi FROM words",
            fetch_all=True
        )

        words_cache.update({w: m for w, m in data})
        return words_cache

    def search_word(self, search_term: str, limit: int = 5) -> List[Tuple[str, str]]:
        """
        Search for words or equivalents containing the given search term.

        Input is sanitized to prevent misuse of SQL wildcards (`%` and `_`),
        ensuring safe and predictable LIKE matches.

        Args:
            search_term (str): Term to search for in the `word` or `parsi` columns.
            limit (int, optional): Maximum number of results to return. Defaults to 5.

        Returns:
            List[Tuple[str, str]]: List of matching (word, equivalent) tuples.
        """
        sanitized_term = search_term.replace("%", "").replace("_", "")
        like_pattern = f"%{sanitized_term}%"

        return self.db.execute(
            """
            SELECT word, parsi
            FROM words
            WHERE word LIKE ?
               OR parsi LIKE ?
            LIMIT ?
            """,
            params=(like_pattern, like_pattern, limit),
            fetch_all=True
        )

    def add_word(self, foreign: str, persian: str) -> None:
        """
        Add a new word to the database.

        Args:
            foreign (str): Foreign (non-Persian) word to add.
            persian (str): Persian equivalent.

        Raises:
            WordAlreadyExistsError: If the foreign word already exists in the database.
        """
        # Check if word already exists
        existing = self.db.execute(
            "SELECT 1 FROM words WHERE word = ?",
            params=(foreign,),
            fetch_one=True
        )
        if existing:
            raise WordAlreadyExistsError(f"Word '{foreign}' already exists.")

        self.db.execute(
            "INSERT INTO words (word, parsi) VALUES (?, ?)",
            params=(foreign, persian)
        )

        # Update cache
        words_cache[foreign] = persian

    def remove_word(self, foreign: str) -> None:
        """
        Remove a word from the database.

        Args:
            foreign (str): Foreign word to remove.

        Raises:
            WordNotFoundError: If the word is not found in the database.
        """
        existing = self.db.execute(
            "SELECT 1 FROM words WHERE word = ?",
            params=(foreign,),
            fetch_one=True
        )
        if not existing:
            raise WordNotFoundError(f"Word '{foreign}' not found.")

        self.db.execute(
            "DELETE FROM words WHERE word = ?",
            params=(foreign,),
        )
        words_cache.pop(foreign, None)

    def update_word(self, foreign: str, persian: str) -> None:
        """
        Update a word’s Persian equivalent.

        Args:
            foreign (str): Foreign word to update.
            persian (str): New Persian equivalent.

        Raises:
            WordNotFoundError: If the foreign word does not exist in the database.
        """
        existing = self.db.execute(
            "SELECT 1 FROM words WHERE word = ?",
            params=(foreign,),
            fetch_one=True
        )
        if not existing:
            raise WordNotFoundError(f"Word '{foreign}' not found.")

        self.db.execute(
            "UPDATE words SET parsi = ? WHERE word = ?",
            params=(persian, foreign)
        )
        words_cache[foreign] = persian

    def get_persian(self, foreign: str) -> Optional[str]:
        """
        Get the Persian equivalent of a foreign word.

        Args:
            foreign (str): Foreign word to look up.

        Returns:
            Optional[str]: Persian equivalent, or None if not found.
        """
        if foreign in words_cache:
            return words_cache[foreign]

        row = self.db.execute(
            "SELECT parsi FROM words WHERE word = ?",
            params=(foreign,),
            fetch_one=True
        )

        return row[0] if row else None
