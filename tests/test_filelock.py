import inspect
import os

import pytest
from filelock import FileLock as UpstreamFileLock

from datasets.utils._filelock import FileLock


def test_long_path(tmpdir):
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1.lock_file.endswith(".lock")
    assert not lock1.lock_file.endswith(filename)
    assert len(os.path.basename(lock1.lock_file)) <= 255


def test_timeout_is_forwarded(tmpdir):
    lock = FileLock(str(tmpdir / "a.lock"), timeout=5)
    assert lock.timeout == 5


def test_singleton_reuses_instance(tmpdir):
    if "is_singleton" not in inspect.signature(UpstreamFileLock.__init__).parameters:
        pytest.skip("filelock does not support is_singleton")
    path = str(tmpdir / "c.lock")
    first = FileLock(path, is_singleton=True)
    second = FileLock(path, is_singleton=True)
    assert first is second
