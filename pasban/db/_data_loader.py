import os
from pathlib import Path
from typing import Optional

import requests

from pasban.core.exceptions import DatabaseNotFound

# Determine base directory for storing database and tag file (depending on OS)
if os.name == "nt":  # Windows
    _BASE_DIR = Path(os.getenv("LOCALAPPDATA", Path.home())) / "Pasban"
else:  # Linux / macOS
    _BASE_DIR = Path.home() / ".pasban"

# Create base directory if it does not exist
_BASE_DIR.mkdir(parents=True, exist_ok=True)

# File path for storing the last downloaded tag/version
_TAGE_PATH: Path = _BASE_DIR / "TAG"

# File path for storing the database
_DB_PATH: Path = _BASE_DIR / "pasban.db"


class DataLoader:
    """
    DataLoader handles database management:
    - Fetches the latest database release from GitHub
    - Compares the local version with the latest available one
    - Downloads and updates the database when needed
    """

    # GitHub repository containing the database releases
    _REPO: str = "keyaruga33/pasban_db"

    # GitHub API endpoint for the latest release
    _URL: str = f"https://api.github.com/repos/{_REPO}/releases/latest"

    @staticmethod
    def _get_lasted_tag() -> Optional[int]:
        """
        Read the last stored version (tag) from the TAG file.

        Returns:
            int | None: The stored tag as an integer, or None if the
            TAG file does not exist or contains invalid data.
        """
        if not _TAGE_PATH.exists():
            return None
        tag = _TAGE_PATH.read_text().strip()
        return int(tag) if tag.isdigit() else None

    @classmethod
    def _get_release_data(cls):
        """
        Fetch metadata of the latest release from GitHub.

        Returns:
            dict: JSON response with release information.

        Raises:
            requests.HTTPError: If the request fails.
        """
        res = requests.get(cls._URL)
        res.raise_for_status()
        return res.json()

    @staticmethod
    def _update_tag(tag: str) -> None:
        """
        Update the TAG file with the provided release tag.

        Args:
            tag (str): Release version string.
        """
        _TAGE_PATH.write_text(tag, encoding="utf-8")

    @staticmethod
    def _get_db_url(assets_url: str) -> str:
        """
        Retrieve the download URL for the database file from GitHub assets.

        Args:
            assets_url (str): API URL pointing to release assets.

        Returns:
            str: Direct browser download URL for the database file.

        Raises:
            DatabaseNotFound: If `pasban.db` is not found among assets.
        """
        res = requests.get(assets_url)
        res.raise_for_status()
        data = res.json()
        for asset in data:
            if asset["name"] == "pasban.db":
                return asset["browser_download_url"]
        raise DatabaseNotFound()

    @classmethod
    def _download_release(cls, assets_url: str, tag: str) -> None:
        """
        Download the latest database release and store it locally.
        Also updates the TAG file with the new version.

        Args:
            assets_url (str): API URL pointing to release assets.
            tag (str): Release version tag.
        """
        print("Downloading latest release...")
        db_url = cls._get_db_url(assets_url)

        # Stream download to avoid loading the entire file into memory
        with requests.get(db_url, stream=True) as r:
            r.raise_for_status()
            with _DB_PATH.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        # Update the TAG file with the latest version
        cls._update_tag(tag)
        print("Download completed.")

    @classmethod
    def update(cls, force_update: bool = False):
        """
        Check for database updates and download if necessary.

        Args:
            force_update (bool, optional): If True, always download the
            latest version regardless of local version. Defaults to False.
        """
        print("Fetching release data...")
        data = cls._get_release_data()
        assets_url = data.get("assets_url")
        last_tag = cls._get_lasted_tag()

        if force_update or (last_tag is None) or (last_tag < int(data["tag_name"])):
            cls._download_release(assets_url, data["tag_name"])
        else:
            print("Your database is already up-to-date.")

    @classmethod
    def initialize(cls):
        """
        Ensure the database exists locally.
        If not, trigger an initial download of the latest version.
        """
        if _DB_PATH.exists():
            return
        print("Database not found. Starting initial download...")
        cls.update(force_update=True)

    @classmethod
    def get_db_path(cls) -> Path:
        """
        Get the path to the local database.
        Automatically initializes the database if it does not exist.

        Returns:
            Path: Path to the database file.
        """
        if not _DB_PATH.exists():
            cls.initialize()
        return _DB_PATH
