from datasets.utils._filelock import FileLock


def test_long_path(tmpdir):
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1._lock_file.endswith(".lock")
    assert not lock1._lock_file.endswith(filename)
