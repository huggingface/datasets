import os
import subprocess
import sys

import pytest

from datasets.utils._filelock import FileLock


def test_long_path(tmpdir):
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1.lock_file.endswith(".lock")
    assert not lock1.lock_file.endswith(filename)
    assert len(os.path.basename(lock1.lock_file)) <= 255


@pytest.mark.parametrize("max_filename_length", [32, 64])
def test_long_path_with_smaller_filename_limit(tmp_path, monkeypatch, max_filename_length):
    monkeypatch.setattr(FileLock, "MAX_FILENAME_LENGTH", max_filename_length)
    lock = FileLock(str(tmp_path / ("a" * 1000 + ".lock")))
    assert len(os.path.basename(lock.lock_file)) <= max_filename_length
    with lock:
        assert lock.is_locked


@pytest.mark.parametrize("filename_length", [10, 1000])
@pytest.mark.parametrize("hash_seed", ["0", "1"])
def test_filelock_mutual_exclusion_across_processes(tmp_path, filename_length, hash_seed):
    lock_path = str(tmp_path / ("a" * filename_length + ".lock"))
    script = """
import sys

from filelock import Timeout

from datasets.utils._filelock import FileLock

lock = FileLock(sys.argv[1])
try:
    with lock.acquire(timeout=0):
        result = "acquired"
except Timeout:
    result = "blocked"
assert result == sys.argv[2], (result, sys.argv[2])
"""
    command = [sys.executable, "-c", script, lock_path]
    env = dict(os.environ, PYTHONHASHSEED=hash_seed)
    with FileLock(lock_path):
        result = subprocess.run(command + ["blocked"], env=env, capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, result.stderr
    result = subprocess.run(command + ["acquired"], env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
