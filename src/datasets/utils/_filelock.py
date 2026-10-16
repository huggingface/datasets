#!/usr/bin/env python
# Copyright 2023 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
"""Utilities to handle file locking in `datasets`."""

import os

from filelock import FileLock as FileLock_
from filelock import UnixFileLock
from filelock import __version__ as _filelock_version
from packaging import version


class _FileLockMeta(type(FileLock_)):
    """
    Applies the umask and long-path handling before `filelock` sees the arguments.

    `filelock` decides which constructor arguments to forward by inspecting the
    signature of `cls.__init__`, and it compares the arguments passed for a singleton
    lock against the existing instance. Both happen in its metaclass, before
    `__init__` runs, so an `__init__` override that takes `*args, **kwargs` hides
    every named parameter from the first check and injects a `mode` the second
    never sees. Doing the work here keeps the parent's real signature visible and
    makes the injected `mode` part of what the singleton check compares.
    """

    def __call__(cls, lock_file, *args, **kwargs):
        # The "mode" argument is required if we want to use the current umask in filelock >= 3.10
        # In previous versions it was already using the current umask.
        if "mode" not in kwargs and version.parse(_filelock_version) >= version.parse("3.10.0"):
            umask = os.umask(0o666)
            os.umask(umask)
            kwargs["mode"] = 0o666 & ~umask
        lock_file = cls.hash_filename_if_too_long(lock_file)
        return super().__call__(lock_file, *args, **kwargs)


class FileLock(FileLock_, metaclass=_FileLockMeta):
    """
    A `filelock.FileLock` initializer that handles long paths.
    It also uses the current umask for lock files.
    """

    MAX_FILENAME_LENGTH = 255

    @classmethod
    def hash_filename_if_too_long(cls, path: str) -> str:
        path = os.path.abspath(os.path.expanduser(path))
        filename = os.path.basename(path)
        max_filename_length = cls.MAX_FILENAME_LENGTH
        if issubclass(cls, UnixFileLock):
            max_filename_length = min(max_filename_length, os.statvfs(os.path.dirname(path)).f_namemax)
        if len(filename) > max_filename_length:
            dirname = os.path.dirname(path)
            hashed_filename = str(hash(filename))
            new_filename = (
                filename[: max_filename_length - len(hashed_filename) - 8] + "..." + hashed_filename + ".lock"
            )
            return os.path.join(dirname, new_filename)
        else:
            return path
