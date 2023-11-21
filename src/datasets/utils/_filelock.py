#!/usr/bin/env python
# coding=utf-8
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


class FileLock(FileLock_):
    """
    Class to format `lock_file` argument on Windows as an extended path in case the string has more than 255 characthers.
    """

    def __init__(self, lock_file, *args, **kwargs):
        if os.name == "nt" and len(os.path.abspath(lock_file)) > 255:
            lock_file = "\\\\?\\" + os.path.abspath(lock_file)
        super().__init__(lock_file, *args, **kwargs)
