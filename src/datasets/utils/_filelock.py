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

import inspect
import os

from filelock import FileLock as FileLock_
from filelock import UnixFileLock
from filelock import __version__ as _filelock_version
from packaging import version


# filelock.FileLockMeta compares this sentinel to the instance mode.
_UNSET_FILE_MODE = -1


class FileLock(FileLock_):
    """
    A `filelock.FileLock` initializer that handles long paths.
    It also uses the current umask for lock files.
    """

    MAX_FILENAME_LENGTH = 255

    def __init__(
        self,
        lock_file,
        timeout=-1,
        mode=_UNSET_FILE_MODE,
        thread_local=True,
        blocking=True,
        is_singleton=False,
        poll_interval=0.05,
        lifetime=None,
        *args,
        **kwargs,
    ):
        # Name constructor arguments so filelock.FileLockMeta forwards them.
        # Leave mode unset on singleton locks; the metaclass compares against
        # that sentinel and a concrete umask mode would make reuse fail.
        if (
            mode == _UNSET_FILE_MODE
            and not is_singleton
            and version.parse(_filelock_version) >= version.parse("3.10.0")
        ):
            umask = os.umask(0o666)
            os.umask(umask)
            mode = 0o666 & ~umask
        lock_file = self.hash_filename_if_too_long(lock_file)
        named = {
            "timeout": timeout,
            "mode": mode,
            "thread_local": thread_local,
            "blocking": blocking,
            "is_singleton": is_singleton,
            "poll_interval": poll_interval,
            "lifetime": lifetime,
        }
        parent_params = inspect.signature(FileLock_.__init__).parameters
        accepts_var_kw = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in parent_params.values())
        if accepts_var_kw:
            kwargs.update(named)
        else:
            kwargs.update({key: value for key, value in named.items() if key in parent_params})
        super().__init__(lock_file, *args, **kwargs)

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
