import os

from datasets.utils._filelock import FileLock


def test_long_path(tmpdir):
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1.lock_file.endswith(".lock")
    assert not lock1.lock_file.endswith(filename)
    assert len(os.path.basename(lock1.lock_file)) <= 255


def test_long_dirname_windows(tmpdir):
    # The lock filename may duplicate the whole parent path (e.g. the builder lock),
    # so on Windows the total path must also stay within MAX_PATH (260), not just
    # the 255-character filename limit. See https://github.com/huggingface/datasets/issues/8702.
    dirname = str(tmpdir / ("d" * 100))
    os.makedirs(dirname, exist_ok=True)
    filename = dirname.replace(os.sep, "_").replace(":", "_") + ".lock"
    lock = FileLock(os.path.join(dirname, filename))
    assert lock.lock_file.endswith(".lock")
    if os.name == "nt":
        assert len(lock.lock_file) <= 259
