import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_tmpdir(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        monkeypatch.setattr("pasban.db._data_loader._BASE_DIR", tmp_path)
        monkeypatch.setattr("pasban.db._data_loader._DB_PATH", tmp_path / "pasban.db")
        monkeypatch.setattr("pasban.db._data_loader._TAGE_PATH", tmp_path / "TAG")
        yield
