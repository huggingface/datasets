import os
import stat
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import filelock
import pytest

from datasets import config
from datasets.utils._filelock import FileLock


@pytest.fixture(params=[False, True], ids=["hard", "soft"])
def use_soft_filelock(request, monkeypatch):
    monkeypatch.setattr(config, "HF_DATASETS_USE_SOFT_FILELOCK", request.param)
    return request.param


def test_isinstance(tmp_path, use_soft_filelock):
    lock = FileLock(tmp_path / "test.lock")
    assert isinstance(lock, FileLock)


def test_deprecated_import(tmp_path, use_soft_filelock):
    from datasets.utils.filelock import FileLock as DeprecatedFileLock

    assert DeprecatedFileLock is FileLock
    assert isinstance(DeprecatedFileLock(tmp_path / "test.lock"), FileLock)


def test_classmethod(tmp_path, use_soft_filelock):
    path = str(tmp_path / "test.lock")
    assert callable(FileLock.hash_filename_if_too_long)
    assert FileLock.hash_filename_if_too_long(path) == path


def test_issubclass(tmp_path, use_soft_filelock):
    assert issubclass(FileLock, object)
    assert issubclass(type(FileLock(tmp_path / "test.lock")), FileLock)


def test_subclass(tmp_path, use_soft_filelock):
    class MyLock(FileLock):
        pass

    assert issubclass(MyLock, FileLock)
    lock = MyLock(tmp_path / "custom.lock", 0.1, 0o600)
    assert type(lock) is MyLock
    assert isinstance(lock, FileLock)
    assert isinstance(lock, filelock.FileLock)
    # Upstream filters positional constructor arguments too, matching main.
    assert lock.timeout == -1
    with lock:
        assert lock.is_locked


def test_concrete_subclass(tmp_path, use_soft_filelock, monkeypatch):
    lock = FileLock(tmp_path / "test.lock")

    class MyLock(type(lock)):
        def __init__(self, lock_file):
            super().__init__(lock_file)
            self.initialized = True

    monkeypatch.setattr(config, "HF_DATASETS_USE_SOFT_FILELOCK", not use_soft_filelock)
    custom_lock = MyLock(tmp_path / "custom.lock")
    assert type(custom_lock) is MyLock
    assert isinstance(custom_lock, FileLock)
    assert isinstance(custom_lock, filelock.SoftFileLock if use_soft_filelock else filelock.FileLock)
    assert custom_lock.initialized
    with custom_lock:
        assert custom_lock.is_locked


def test_current_upstream_filtered_arguments_match_main(tmp_path, use_soft_filelock):
    # Pin today's upstream signature filtering for parity, not as desired behavior.
    # Fixing dropped constructor arguments belongs in a separate change.
    assert FileLock(tmp_path / "timeout.lock", timeout=5).timeout == -1
    path = tmp_path / "singleton.lock"
    lock = FileLock(path, is_singleton=True)
    assert not lock.is_singleton
    with pytest.raises(ValueError, match="^Singleton lock instances cannot be initialized with differing arguments"):
        FileLock(path, is_singleton=True)


def test_long_path(tmpdir, use_soft_filelock, monkeypatch):
    if use_soft_filelock:
        monkeypatch.setattr(
            os, "statvfs", Mock(side_effect=AssertionError("Soft locks must not call statvfs")), raising=False
        )
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1.lock_file.endswith(".lock")
    assert not lock1.lock_file.endswith(filename)
    assert len(os.path.basename(lock1.lock_file)) <= 255
    with lock1:
        assert lock1.is_locked


def test_filesystem_filename_limit(tmp_path, use_soft_filelock, monkeypatch):
    statvfs = Mock(return_value=SimpleNamespace(f_namemax=100))
    monkeypatch.setattr(os, "statvfs", statvfs, raising=False)
    filename = "a" * 200 + ".lock"
    lock = FileLock(tmp_path / filename)
    if not use_soft_filelock and isinstance(lock, filelock.UnixFileLock):
        assert len(os.path.basename(lock.lock_file)) <= 100
        statvfs.assert_called_once_with(str(tmp_path))
    else:
        assert os.path.basename(lock.lock_file) == filename
        statvfs.assert_not_called()


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX file permissions")
@pytest.mark.parametrize("umask", [0o022, 0o027, 0o077])
@pytest.mark.parametrize("mode", [None, 0o600])
def test_mode(tmp_path, use_soft_filelock, umask, mode):
    previous_umask = os.umask(umask)
    try:
        kwargs = {} if mode is None else {"mode": mode}
        lock = FileLock(tmp_path / "test.lock", **kwargs)
        assert os.umask(umask) == umask
        with lock:
            # Explicit mode is currently filtered upstream; preserve main's umask behavior.
            expected_mode = 0o666 & ~umask
            assert stat.S_IMODE(os.stat(lock.lock_file).st_mode) == expected_mode
    finally:
        os.umask(previous_umask)


def test_positional_mode(tmp_path, use_soft_filelock):
    lock = FileLock(tmp_path / "test.lock", 0.1, 0o600)
    # Upstream filters positional constructor arguments too, matching main.
    assert lock.timeout == -1
    if sys.platform != "win32":
        previous_umask = os.umask(0)
        try:
            with lock:
                # Mode was derived from the umask at construction, as on main.
                assert stat.S_IMODE(os.stat(lock.lock_file).st_mode) == 0o666 & ~previous_umask
        finally:
            os.umask(previous_umask)


def test_flavour_and_release(tmp_path, use_soft_filelock):
    lock = FileLock(tmp_path / "test.lock")
    expected_class = filelock.SoftFileLock if use_soft_filelock else filelock.FileLock
    assert isinstance(lock, expected_class)
    if use_soft_filelock:
        assert not isinstance(lock, filelock.UnixFileLock)
    with lock:
        assert lock.is_locked
        assert os.path.isfile(lock.lock_file)
    assert not lock.is_locked
    if use_soft_filelock:
        assert not os.path.exists(lock.lock_file)
    else:
        # Older filelock releases leave hard lock files behind. Preserve the
        # installed backend's release behaviour (newer releases remove them).
        reference_path = tmp_path / "reference.lock"
        with filelock.FileLock(reference_path):
            pass
        assert os.path.exists(lock.lock_file) == reference_path.exists()


def test_mutual_exclusion_across_processes(tmp_path, use_soft_filelock):
    script = """
import sys
import filelock
import pytest
from datasets import config
from datasets.utils._filelock import FileLock

config.HF_DATASETS_USE_SOFT_FILELOCK = sys.argv[2] == "True"
lock = FileLock(sys.argv[1])
if sys.argv[3] == "blocked":
    with pytest.raises(filelock.Timeout):
        lock.acquire(timeout=0.1)
else:
    with lock.acquire(timeout=0.1):
        assert lock.is_locked
print(sys.argv[3])
"""
    lock = FileLock(tmp_path / "test.lock")
    command = [sys.executable, "-c", script, lock.lock_file, str(use_soft_filelock)]
    with lock:
        result = subprocess.run(command + ["blocked"], capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "blocked"
    result = subprocess.run(command + ["acquired"], capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "acquired"


@pytest.mark.parametrize(
    "value, expected_soft",
    [
        (None, False),
        ("", False),
        ("0", False),
        ("false", False),
        ("true", True),
        ("1", True),
        ("On", True),
        ("yes", True),
    ],
)
def test_environment_switch(tmp_path, monkeypatch, value, expected_soft):
    monkeypatch.delenv("HF_DATASETS_USE_SOFT_FILELOCK", raising=False)
    if value is not None:
        monkeypatch.setenv("HF_DATASETS_USE_SOFT_FILELOCK", value)
    script = """
import sys
import filelock
from datasets import config
from datasets.utils._filelock import FileLock

expected_soft = sys.argv[2] == "True"
assert config.HF_DATASETS_USE_SOFT_FILELOCK is expected_soft
lock = FileLock(sys.argv[1])
assert isinstance(lock, filelock.SoftFileLock if expected_soft else filelock.FileLock)
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(tmp_path / "test.lock"), str(expected_soft)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr


def test_switch_is_read_per_construction(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "HF_DATASETS_USE_SOFT_FILELOCK", False)
    hard_lock = FileLock(tmp_path / "hard.lock")
    monkeypatch.setattr(config, "HF_DATASETS_USE_SOFT_FILELOCK", True)
    soft_lock = FileLock(tmp_path / "soft.lock")
    assert isinstance(hard_lock, filelock.FileLock)
    assert isinstance(soft_lock, filelock.SoftFileLock)
    monkeypatch.setattr(config, "HF_DATASETS_USE_SOFT_FILELOCK", False)
    assert isinstance(FileLock(tmp_path / "hard-again.lock"), filelock.FileLock)
