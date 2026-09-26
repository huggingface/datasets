import os

from datasets.utils._filelock import FileLock


def test_long_path(tmpdir):
    filename = "a" * 1000 + ".lock"
    lock1 = FileLock(str(tmpdir / filename))
    assert lock1.lock_file.endswith(".lock")
    assert not lock1.lock_file.endswith(filename)
    assert len(os.path.basename(lock1.lock_file)) <= 255


def test_constructor_arguments_reach_filelock(tmpdir):
    # `filelock` forwards only the parameters it can see on the class signature, so a
    # wrapper that takes `*args, **kwargs` silently dropped `timeout` and the rest.
    lock = FileLock(str(tmpdir / "a.lock"), timeout=5)
    assert lock.timeout == 5


def test_singleton_returns_the_cached_instance(tmpdir):
    # The umask `mode` is injected before `filelock` compares singleton arguments, so a
    # second construction with the same arguments must return the existing instance
    # instead of raising because the caller never passed `mode` itself.
    path = str(tmpdir / "c.lock")
    first = FileLock(path, is_singleton=True)
    second = FileLock(path, is_singleton=True)
    assert first is second


def test_umask_mode_is_still_applied(tmpdir):
    umask = os.umask(0o666)
    os.umask(umask)
    lock = FileLock(str(tmpdir / "m.lock"))
    assert lock._context.mode == 0o666 & ~umask
