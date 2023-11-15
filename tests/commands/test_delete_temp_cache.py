from pathlib import Path

import pytest

from datasets.commands.delete_temp_cache import DeleteTempCacheCommand
from datasets.fingerprint import get_temporary_cache_files_directory


@pytest.mark.integration
def test_delete_temp_cache_command(tmp_path, monkeypatch):
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    hf_temp_cache_dir = Path(get_temporary_cache_files_directory())
    dummy_dir = tmp_path / "dummy_dir"
    dummy_dir.mkdir()
    dummy_file = tmp_path / "dummy.txt"
    with open(dummy_file, "w"):
        pass
    assert hf_temp_cache_dir.exists() and dummy_dir.exists() and dummy_file.exists()
    command = DeleteTempCacheCommand()
    command.run()
    assert not hf_temp_cache_dir.exists() and dummy_dir.exists() and dummy_file.exists()
