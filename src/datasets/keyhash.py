# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
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
# limitations under the License.

# Lint as: python3

"""
Hashing function for dataset keys using `hashlib.md5`

Requirements for the hash function:

- Provides a uniformly distributed hash from random space
- Adequately fast speed
- Working with multiple input types (in this case, `str`, `int` or `bytes`)
- Should be platform independent (generates same hash on different OS and systems)

The hashing function provides a unique 128-bit integer hash of the key provided.

The split name is being used here as the hash salt to avoid having same hashes
in different splits due to same keys
"""

import hashlib
from typing import Union

class KeyHasher(object):
    """KeyHasher class for providing hash using md5"""

    def __init__(self, hash_salt: str):
        self._split_md5 = hashlib.md5(_as_bytes(hash_salt))

    def _as_bytes(self, hash_data: Union[str, int, bytes]) -> bytes:
        """
        Returns the input hash_data in its bytes form

        Args:
        hash_data: the hash salt/key to be converted to bytes
        """
        if instance(hash_data, bytes):
            #Data already in bytes, returns as it as
            return hash_data
        elif isinstance(hash_data, str):
            #We keep the data as it as for it ot be later encoded to UTF-8
            #However replace `\\` with `/` for Windows compatibility
            hash_data = hash_data.replace('\\', '/')
        elif isinstance(hash_data, int):
            hash_data = str(hash_data)
        else:
            #If data is not of the required type, raise error
            prefix = "Invalid key type detected: "
            err_msg = f"Found {type(hash_data)}"
            suffix = "\nKeys should be either str, int or bytes type"
            raise TypeError(f'{prefix}{err_msg}{suffix}')
        return hash_data.encode('utf-8')

    def hash(self, key: Union[str, int, bytes]) -> int:
        """ Returns 128-bits unique hash of input key

        Args:
        key: the input key to be hashed (should be str, int or bytes)

        Returns: 128-bit int hash key"""
        md5 = self._split_md5.copy()
        byte_key = _to_bytes(key)
        md5.update(byte_key)
        #Convert to integer with hexadecimal conversion
        return int(md5.hexdigest(), 16)
