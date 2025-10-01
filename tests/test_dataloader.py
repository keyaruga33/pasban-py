import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from pasban.core.exceptions import DatabaseNotFound
from pasban.db._data_loader import DataLoader, _DB_PATH


@pytest.fixture(autouse=True)
def temp_dir(monkeypatch):
    """
    Redirect database and TAG paths to a temporary directory for testing.
    Ensures tests do not pollute the real user directory under ~/.pasban.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        monkeypatch.setattr("pasban.db._data_loader._BASE_DIR", tmp_path)
        monkeypatch.setattr("pasban.db._data_loader._DB_PATH", tmp_path / "pasban.db")
        monkeypatch.setattr("pasban.db._data_loader._TAGE_PATH", tmp_path / "TAG")
        yield


class TestDataLoader:
    """
    Unit tests for the DataLoader class.
    Covers reading/writing TAG files, fetching release data,
    resolving database download URLs, and downloading database releases.
    """

    def test_get_lasted_tag_none(self):
        """If TAG file does not exist, _get_lasted_tag should return None."""
        assert DataLoader._get_lasted_tag() is None

    def test_get_lasted_tag_valid(self):
        """If TAG file contains a valid integer, _get_lasted_tag should return int."""
        DataLoader._update_tag("42")
        assert DataLoader._get_lasted_tag() == 42

    def test_get_lasted_tag_invalid(self):
        """If TAG file contains invalid data, _get_lasted_tag should return None."""
        DataLoader._update_tag("invalid")
        assert DataLoader._get_lasted_tag() is None

    @patch("requests.get")
    def test_get_release_data(self, mock_get):
        """_get_release_data should fetch and return JSON data from GitHub API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"tag_name": "1"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = DataLoader._get_release_data()
        assert data["tag_name"] == "1"

    @patch("requests.get")
    def test_get_db_url_success(self, mock_get):
        """_get_db_url should return correct download URL if pasban.db exists in assets."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
                {"name": "pasban.db", "browser_download_url": "http://example.com/db"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = DataLoader._get_db_url("http://fake-url")
        assert url == "http://example.com/db"

    @patch("requests.get")
    def test_get_db_url_not_found(self, mock_get):
        """_get_db_url should raise DatabaseNotFound if pasban.db is not found in assets."""
        mock_response = MagicMock()
        mock_response.json.return_value = [{"name": "other.txt"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(DatabaseNotFound):
            DataLoader._get_db_url("http://fake-url")

    @patch("requests.get")
    def test_download_release(self, mock_get):
        """
        _download_release should:
          - download the pasban.db file,
          - write it to disk,
          - update the TAG file with the provided version.
        """
        # Mock asset API response
        mock_asset_response = MagicMock()
        mock_asset_response.json.return_value = [
                {"name": "pasban.db", "browser_download_url": "http://example.com/db"}
        ]
        mock_asset_response.raise_for_status.return_value = None

        # Mock DB download response
        mock_download_response = MagicMock()
        mock_download_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_download_response.__enter__.return_value = mock_download_response
        mock_download_response.raise_for_status.return_value = None

        def side_effect(url, *args, **kwargs):
            if "db" in url:
                return mock_download_response
            return mock_asset_response

        mock_get.side_effect = side_effect

        DataLoader._download_release("http://fake-assets-url", "123")

        # Assert DB file created
        assert _DB_PATH.exists()
        # Assert TAG updated as integer
        assert DataLoader._get_lasted_tag() == 123
