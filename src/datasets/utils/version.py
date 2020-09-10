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
"""Version utils."""

import dataclasses
import re
from dataclasses import dataclass


_VERSION_TMPL = r"^(?P<major>{v})" r"\.(?P<minor>{v})" r"\.(?P<patch>{v})$"
_VERSION_WILDCARD_REG = re.compile(_VERSION_TMPL.format(v=r"\d+|\*"))
_VERSION_RESOLVED_REG = re.compile(_VERSION_TMPL.format(v=r"\d+"))


@dataclass()
class Version:
    """Dataset version MAJOR.MINOR.PATCH.
    Args:
        version_str: string. Eg: "1.2.3".
        description: string, a description of what is new in this version.
    """

    version_str: str
    description: str = None
    major: str = None
    minor: str = None
    patch: str = None

    def __post_init__(self):
        self.major, self.minor, self.patch = _str_to_version(self.version_str)

    def __repr__(self):
        return "{}.{}.{}".format(*self.tuple)

    @property
    def tuple(self):
        return self.major, self.minor, self.patch

    def _validate_operand(self, other):
        if isinstance(other, str):
            return Version(other)
        elif isinstance(other, Version):
            return other
        raise AssertionError("{} (type {}) cannot be compared to version.".format(other, type(other)))

    def __eq__(self, other):
        other = self._validate_operand(other)
        return self.tuple == other.tuple

    def __ne__(self, other):
        other = self._validate_operand(other)
        return self.tuple != other.tuple

    def __lt__(self, other):
        other = self._validate_operand(other)
        return self.tuple < other.tuple

    def __le__(self, other):
        other = self._validate_operand(other)
        return self.tuple <= other.tuple

    def __gt__(self, other):
        other = self._validate_operand(other)
        return self.tuple > other.tuple

    def __ge__(self, other):
        other = self._validate_operand(other)
        return self.tuple >= other.tuple

    def match(self, other_version):
        """Returns True if other_version matches.

        Args:
            other_version: string, of the form "x[.y[.x]]" where {x,y,z} can be a
                number or a wildcard.
        """
        major, minor, patch = _str_to_version(other_version, allow_wildcard=True)
        return major in [self.major, "*"] and minor in [self.minor, "*"] and patch in [self.patch, "*"]

    @classmethod
    def from_dict(cls, dic):
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in dic.items() if k in field_names})


def _str_to_version(version_str, allow_wildcard=False):
    """Return the tuple (major, minor, patch) version extracted from the str."""
    reg = _VERSION_WILDCARD_REG if allow_wildcard else _VERSION_RESOLVED_REG
    res = reg.match(version_str)
    if not res:
        msg = "Invalid version '{}'. Format should be x.y.z".format(version_str)
        if allow_wildcard:
            msg += " with {x,y,z} being digits or wildcard."
        else:
            msg += " with {x,y,z} being digits."
        raise ValueError(msg)
    return tuple(v if v == "*" else int(v) for v in [res.group("major"), res.group("minor"), res.group("patch")])
