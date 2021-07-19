import os
import time

import pytest

from datasets.utils.filelock import FileLock, Timeout


def test_filelock(tmpdir):
    lock1 = FileLock(str(tmpdir / "foo.lock"))
    lock2 = FileLock(str(tmpdir / "foo.lock"))
    timeout = 0.01
    with lock1.acquire():
        with pytest.raises(Timeout):
            _start = time.time()
            lock2.acquire(timeout)
            assert time.time() - _start > timeout


def test_long_filename(tmpdir):
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1._lock_file.endswith(".lock")
    assert not lock1._lock_file.endswith(filename)
    assert len(os.path.basename(lock1._lock_file)) <= 255
    lock2 = FileLock(tmpdir / filename)
    with lock1.acquire():
        with pytest.raises(Timeout):
            lock2.acquire(0)
