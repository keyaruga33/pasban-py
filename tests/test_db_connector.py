import sqlite3
from pathlib import Path
import pytest

from pasban.db._connector import DBConnector


@pytest.fixture
def temp_db(tmp_path: Path) -> Path:
    """
    Fixture: create a temporary SQLite database file with sample data.
    Returns the path to the database file.
    """
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
    cur.executemany("INSERT INTO users (name) VALUES (?)", [("Alice",), ("Bob",), ("Charlie",)])
    conn.commit()
    conn.close()
    return db_path


class TestDBConnector:
    """Test suite for the DBConnector class."""

    def test_connection_initialization(self, temp_db: Path):
        """Ensure DBConnector initializes correctly in read-only mode."""
        db = DBConnector(temp_db)
        assert isinstance(db.conn, sqlite3.Connection)
        db.close()

    def test_fetch_one(self, temp_db: Path):
        """Test fetching a single row using fetch_one."""
        db = DBConnector(temp_db)
        row = db.execute("SELECT name FROM users WHERE id = ?", (1,), fetch_one=True)
        assert row == ("Alice",)
        db.close()

    def test_fetch_all(self, temp_db: Path):
        """Test fetching all rows using fetch_all."""
        db = DBConnector(temp_db)
        rows = db.execute("SELECT name FROM users ORDER BY id", fetch_all=True)
        assert rows == [("Alice",), ("Bob",), ("Charlie",)]
        db.close()

    def test_no_fetch(self, temp_db: Path):
        """Test executing a query without fetching results."""
        db = DBConnector(temp_db)
        result = db.execute("SELECT name FROM users WHERE id = ?", (2,))
        assert result is None
        db.close()

    def test_execute_temp_fetch(self, temp_db: Path):
        """Test executing a query with a temporary read-only connection."""
        row = DBConnector.execute_temp(temp_db, "SELECT name FROM users WHERE id = ?", (3,), fetch_one=True)
        assert row == ("Charlie",)

    def test_read_only_violation(self, temp_db: Path):
        """Ensure write attempts raise an error in read-only mode."""
        db = DBConnector(temp_db)
        with pytest.raises(sqlite3.OperationalError):
            db.execute("INSERT INTO users (name) VALUES (?)", ("David",))
        db.close()

    def test_connection_close(self, temp_db: Path):
        """Ensure close() properly closes the connection."""
        db = DBConnector(temp_db)
        db.close()
        with pytest.raises(sqlite3.ProgrammingError):
            db.execute("SELECT 1", fetch_one=True)
