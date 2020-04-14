# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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

import enum
import re



_VERSION_TMPL = (
        r"^(?P<major>{v})"
        r"\.(?P<minor>{v})"
        r"\.(?P<patch>{v})$")
_VERSION_WILDCARD_REG = re.compile(_VERSION_TMPL.format(v=r"\d+|\*"))
_VERSION_RESOLVED_REG = re.compile(_VERSION_TMPL.format(v=r"\d+"))


class Experiment(enum.Enum):
    """Experiments which can be enabled/disabled on a per version basis.

    Experiments are designed to gradually apply changes to datasets while
    maintaining backward compatibility with previous versions. All experiments
    should eventually be deleted, once used by all versions of all datasets.

    Eg:
    class Experiment(enum.Enum):
        EXP_A = enum.auto()  # Short description of experiment.

    class MyBuilder(...):
        VERSION = nlp.Version('1.2.3', experiments={
                nlp.Experiment.EXP_A: True,
                })
    """
    # A Dummy experiment, which should NOT be used, except for testing.
    DUMMY = 1

    # New Shuffling, sharding and slicing mechanism.
    S3 = 2

    # Experiment to update the dataset metadata files without making the
    # new dataset version the default.
    METADATA = 3


class Version(object):
    """Dataset version MAJOR.MINOR.PATCH."""

    _DEFAULT_EXPERIMENTS = {
            Experiment.DUMMY: False,
            Experiment.S3: True,
            Experiment.METADATA: False,
    }

    def __init__(self, version_str, description=None, experiments=None,
                             nlp_version_to_prepare=None):
        """Version init.

        Args:
            version_str: string. Eg: "1.2.3".
            description: string, a description of what is new in this version.
            experiments: dict of experiments. See Experiment.
            nlp_version_to_prepare: string, defaults to None. If set, indicates that
                current version cannot be used to `download_and_prepare` the
                dataset, but that at version {nlp_version_to_prepare} should be
                used instead.
        """
        if description is not None and not isinstance(description, str):
            raise TypeError(
                    "Description should be a string. Got {}".format(description))
        self.description = description
        self._experiments = self._DEFAULT_EXPERIMENTS.copy()
        self.nlp_version_to_prepare = nlp_version_to_prepare
        if experiments:
            self._experiments.update(experiments)
        self.major, self.minor, self.patch = _str_to_version(version_str)

    def implements(self, experiment):
        """Returns True if version implements given experiment."""
        return self._experiments[experiment]

    def __str__(self):
        return "{}.{}.{}".format(*self.tuple)

    @property
    def tuple(self):
        return self.major, self.minor, self.patch

    def _validate_operand(self, other):
        if isinstance(other, str):
            return Version(other)
        elif isinstance(other, Version):
            return other
        raise AssertionError("{} (type {}) cannot be compared to version.".format(
                other, type(other)))

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
        return (major in [self.major, "*"] and minor in [self.minor, "*"]
                        and patch in [self.patch, "*"])


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
    return tuple(
            v if v == "*" else int(v)
            for v in [res.group("major"), res.group("minor"), res.group("patch")])
