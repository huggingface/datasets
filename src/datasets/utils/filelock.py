# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

"""
A platform independent file lock that supports the with-statement.
"""


# Modules
# ------------------------------------------------
import logging
import os
import threading
import time


try:
    import warnings
except ImportError:
    warnings = None

try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import fcntl
except ImportError:
    fcntl = None


# Backward compatibility
# ------------------------------------------------
try:
    TimeoutError
except NameError:
    TimeoutError = OSError


# Data
# ------------------------------------------------
__all__ = [
    "Timeout",
    "BaseFileLock",
    "WindowsFileLock",
    "UnixFileLock",
    "SoftFileLock",
    "FileLock",
]

__version__ = "3.0.12"


_logger = None


def logger():
    """Returns the logger instance used in this module."""
    global _logger
    _logger = _logger or logging.getLogger(__name__)
    return _logger


# Exceptions
# ------------------------------------------------
class Timeout(TimeoutError):
    """
    Raised when the lock could not be acquired in *timeout*
    seconds.
    """

    def __init__(self, lock_file):
        """ """
        #: The path of the file lock.
        self.lock_file = lock_file
        return None

    def __str__(self):
        temp = f"The file lock '{self.lock_file}' could not be acquired."
        return temp


# Classes
# ------------------------------------------------


# This is a helper class which is returned by :meth:`BaseFileLock.acquire`
# and wraps the lock to make sure __enter__ is not called twice when entering
# the with statement.
# If we would simply return *self*, the lock would be acquired again
# in the *__enter__* method of the BaseFileLock, but not released again
# automatically.
#
# :seealso: issue #37 (memory leak)
class _Acquire_ReturnProxy:
    def __init__(self, lock):
        self.lock = lock
        return None

    def __enter__(self):
        return self.lock

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
        return None


class BaseFileLock:
    """
    Implements the base class of a file lock.
    """

    def __init__(self, lock_file, timeout=-1, max_filename_length=None):
        """ """
        max_filename_length = max_filename_length if max_filename_length is not None else 255
        # Hash the filename if it's too long
        lock_file = self.hash_filename_if_too_long(lock_file, max_filename_length)
        # The path to the lock file.
        self._lock_file = lock_file

        # The file descriptor for the *_lock_file* as it is returned by the
        # os.open() function.
        # This file lock is only NOT None, if the object currently holds the
        # lock.
        self._lock_file_fd = None

        # The default timeout value.
        self.timeout = timeout

        # We use this lock primarily for the lock counter.
        self._thread_lock = threading.Lock()

        # The lock counter is used for implementing the nested locking
        # mechanism. Whenever the lock is acquired, the counter is increased and
        # the lock is only released, when this value is 0 again.
        self._lock_counter = 0
        return None

    @property
    def lock_file(self):
        """
        The path to the lock file.
        """
        return self._lock_file

    @property
    def timeout(self):
        """
        You can set a default timeout for the filelock. It will be used as
        fallback value in the acquire method, if no timeout value (*None*) is
        given.

        If you want to disable the timeout, set it to a negative value.

        A timeout of 0 means, that there is exactly one attempt to acquire the
        file lock.

        *New in version 2.0.0*
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """ """
        self._timeout = float(value)
        return None

    # Platform dependent locking
    # --------------------------------------------

    def _acquire(self):
        """
        Platform dependent. If the file lock could be
        acquired, self._lock_file_fd holds the file descriptor
        of the lock file.
        """
        raise NotImplementedError()

    def _release(self):
        """
        Releases the lock and sets self._lock_file_fd to None.
        """
        raise NotImplementedError()

    # Platform independent methods
    # --------------------------------------------

    @property
    def is_locked(self):
        """
        True, if the object holds the file lock.

            This was previously a method and is now a property.
        """
        return self._lock_file_fd is not None

    def acquire(self, timeout=None, poll_intervall=0.05):
        """
        Acquires the file lock or fails with a :exc:`Timeout` error.

        ```py
        # You can use this method in the context manager (recommended)
        with lock.acquire():
            pass

        # Or use an equivalent try-finally construct:
        lock.acquire()
        try:
            pass
        finally:
            lock.release()
        ```

        :arg float timeout:
            The maximum time waited for the file lock.
            If ``timeout < 0``, there is no timeout and this method will
            block until the lock could be acquired.
            If ``timeout`` is None, the default :attr:`~timeout` is used.

        :arg float poll_intervall:
            We check once in *poll_intervall* seconds if we can acquire the
            file lock.

        :raises Timeout:
            if the lock could not be acquired in *timeout* seconds.

            This method returns now a *proxy* object instead of *self*,
            so that it can be used in a with statement without side effects.
        """
        # Use the default timeout, if no timeout is provided.
        if timeout is None:
            timeout = self.timeout

        # Increment the number right at the beginning.
        # We can still undo it, if something fails.
        with self._thread_lock:
            self._lock_counter += 1

        lock_id = id(self)
        lock_filename = self._lock_file
        start_time = time.time()
        try:
            while True:
                with self._thread_lock:
                    if not self.is_locked:
                        logger().debug(f"Attempting to acquire lock {lock_id} on {lock_filename}")
                        self._acquire()

                if self.is_locked:
                    logger().debug(f"Lock {lock_id} acquired on {lock_filename}")
                    break
                elif timeout >= 0 and time.time() - start_time > timeout:
                    logger().debug(f"Timeout on acquiring lock {lock_id} on {lock_filename}")
                    raise Timeout(self._lock_file)
                else:
                    logger().debug(
                        f"Lock {lock_id} not acquired on {lock_filename}, waiting {poll_intervall} seconds ..."
                    )
                    time.sleep(poll_intervall)
        except:  # noqa
            # Something did go wrong, so decrement the counter.
            with self._thread_lock:
                self._lock_counter = max(0, self._lock_counter - 1)

            raise
        return _Acquire_ReturnProxy(lock=self)

    def release(self, force=False):
        """
        Releases the file lock.

        Please note, that the lock is only completly released, if the lock
        counter is 0.

        Also note, that the lock file itself is not automatically deleted.

        :arg bool force:
            If true, the lock counter is ignored and the lock is released in
            every case.
        """
        with self._thread_lock:
            if self.is_locked:
                self._lock_counter -= 1

                if self._lock_counter == 0 or force:
                    lock_id = id(self)
                    lock_filename = self._lock_file

                    logger().debug(f"Attempting to release lock {lock_id} on {lock_filename}")
                    self._release()
                    self._lock_counter = 0
                    logger().debug(f"Lock {lock_id} released on {lock_filename}")

        return None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return None

    def __del__(self):
        self.release(force=True)
        return None

    def hash_filename_if_too_long(self, path: str, max_length: int) -> str:
        filename = os.path.basename(path)
        if len(filename) > max_length and max_length > 0:
            dirname = os.path.dirname(path)
            hashed_filename = str(hash(filename))
            new_filename = filename[: max_length - len(hashed_filename) - 8] + "..." + hashed_filename + ".lock"
            return os.path.join(dirname, new_filename)
        else:
            return path


# Windows locking mechanism
# ~~~~~~~~~~~~~~~~~~~~~~~~~


class WindowsFileLock(BaseFileLock):
    """
    Uses the :func:`msvcrt.locking` function to hard lock the lock file on
    windows systems.
    """

    def __init__(self, lock_file, timeout=-1, max_filename_length=None):
        from .file_utils import relative_to_absolute_path

        super().__init__(lock_file, timeout=timeout, max_filename_length=max_filename_length)
        self._lock_file = "\\\\?\\" + relative_to_absolute_path(self.lock_file)

    def _acquire(self):
        open_mode = os.O_RDWR | os.O_CREAT | os.O_TRUNC

        try:
            fd = os.open(self._lock_file, open_mode)
        except OSError:
            pass
        else:
            try:
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            except OSError:
                os.close(fd)
            else:
                self._lock_file_fd = fd
        return None

    def _release(self):
        fd = self._lock_file_fd
        self._lock_file_fd = None
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        os.close(fd)

        try:
            os.remove(self._lock_file)
        # Probably another instance of the application
        # that acquired the file lock.
        except OSError:
            pass
        return None


# Unix locking mechanism
# ~~~~~~~~~~~~~~~~~~~~~~


class UnixFileLock(BaseFileLock):
    """
    Uses the :func:`fcntl.flock` to hard lock the lock file on unix systems.
    """

    def __init__(self, lock_file, timeout=-1, max_filename_length=None):
        max_filename_length = os.statvfs(os.path.dirname(lock_file)).f_namemax
        super().__init__(lock_file, timeout=timeout, max_filename_length=max_filename_length)

    def _acquire(self):
        open_mode = os.O_RDWR | os.O_CREAT | os.O_TRUNC
        fd = os.open(self._lock_file, open_mode)

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
        else:
            self._lock_file_fd = fd
        return None

    def _release(self):
        # Do not remove the lockfile:
        #
        #   https://github.com/benediktschmitt/py-filelock/issues/31
        #   https://stackoverflow.com/questions/17708885/flock-removing-locked-file-without-race-condition
        fd = self._lock_file_fd
        self._lock_file_fd = None
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
        return None


# Soft lock
# ~~~~~~~~~


class SoftFileLock(BaseFileLock):
    """
    Simply watches the existence of the lock file.
    """

    def _acquire(self):
        open_mode = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC
        try:
            fd = os.open(self._lock_file, open_mode)
        except OSError:
            pass
        else:
            self._lock_file_fd = fd
        return None

    def _release(self):
        os.close(self._lock_file_fd)
        self._lock_file_fd = None

        try:
            os.remove(self._lock_file)
        # The file is already deleted and that's what we want.
        except OSError:
            pass
        return None


# Platform filelock
# ~~~~~~~~~~~~~~~~~

#: Alias for the lock, which should be used for the current platform. On
#: Windows, this is an alias for :class:`WindowsFileLock`, on Unix for
#: :class:`UnixFileLock` and otherwise for :class:`SoftFileLock`.
FileLock = None

if msvcrt:
    FileLock = WindowsFileLock
elif fcntl:
    FileLock = UnixFileLock
else:
    FileLock = SoftFileLock

    if warnings is not None:
        warnings.warn("only soft file lock is available")
