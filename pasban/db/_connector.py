import sqlite3
from pathlib import Path
from typing import Optional, Tuple, Any, List


class DBConnector:
    """
    A lightweight, read-only SQLite database wrapper.

    This class provides a minimal interface for executing read-only queries
    on a SQLite database file. It ensures that the database is always opened
    in read-only mode and closes the connection automatically when not needed.

    Attributes:
        db_path (Path): Path to the SQLite database file.
        conn (sqlite3.Connection): Active SQLite connection in read-only mode.
    """

    def __init__(self, db_path: Path) -> None:
        """
        Initialize the ReadOnlyDB instance.

        Args:
            db_path (Path): Path to the SQLite database file.
        """
        self.db_path: Path = db_path
        self.conn: sqlite3.Connection = sqlite3.connect(
            db_path, uri=True, check_same_thread=False
        )

    def execute(
            self,
            query: str,
            params: Optional[Tuple[Any, ...]] = None,
            fetch_one: bool = False,
            fetch_all: bool = False,
    ) -> Optional[Tuple[Any, ...] | List[Tuple[Any, ...]]]:
        """
        Execute a read-only SQL query and optionally fetch results.

        Args:
            query (str): SQL query to execute.
            params (tuple, optional): Parameters for the SQL query. Defaults to None.
            fetch_one (bool, optional): If True, return the first row. Defaults to False.
            fetch_all (bool, optional): If True, return all rows. Defaults to False.

        Returns:
            Optional[Tuple[Any, ...] | List[Tuple[Any, ...]]]:
                - A single row if fetch_one is True.
                - A list of rows if fetch_all is True.
                - None otherwise.
        """
        cur = self.conn.cursor()
        try:
            cur.execute(query, params or ())
            if fetch_one:
                return cur.fetchone()
            if fetch_all:
                return cur.fetchall()
            return None
        finally:
            cur.close()

    @classmethod
    def execute_temp(
            cls,
            db_path: Path,
            query: str,
            params: Optional[Tuple[Any, ...]] = None,
            fetch_one: bool = False,
            fetch_all: bool = False,
    ) -> Optional[Tuple[Any, ...] | List[Tuple[Any, ...]]]:
        """
        Execute a query on a temporary read-only connection and close it immediately.

        Args:
            db_path (Path): Path to the SQLite database file.
            query (str): SQL query to execute.
            params (tuple, optional): Parameters for the SQL query. Defaults to None.
            fetch_one (bool, optional): If True, return the first row. Defaults to False.
            fetch_all (bool, optional): If True, return all rows. Defaults to False.

        Returns:
            Optional[Tuple[Any, ...] | List[Tuple[Any, ...]]]:
                - A single row if fetch_one is True.
                - A list of rows if fetch_all is True.
                - None otherwise.
        """
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, check_same_thread=False)
        try:
            cur = conn.cursor()
            cur.execute(query, params or ())
            if fetch_one:
                return cur.fetchone()
            if fetch_all:
                return cur.fetchall()
            return None
        finally:
            cur.close()
            conn.close()

    def close(self) -> None:
        """
        Close the active database connection.
        """
        self.conn.close()
