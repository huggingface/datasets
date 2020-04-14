# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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
"""Data downloads using the Kaggle CLI."""

import collections
import os
import subprocess as sp

import logging

from .. import utils

logger = logging.getLogger(__name__)

_ERR_MSG = """\
To download Kaggle data, follow the instructions to install the \
kaggle API and get API credentials:
https://github.com/Kaggle/kaggle-api#installation

Additionally, you must join the competition through the Kaggle competition's \
website:
https://www.kaggle.com/c/%s
"""

_NOT_FOUND_ERR_MSG = """\
Competition %s not found. Please ensure you have spelled the competition name \
correctly.
"""

KaggleType = collections.namedtuple(
        "KaggleType",
        ["prefix", "download_cmd", "dl_flag", "extra_flag"])

_KAGGLE_TYPES = {
        "dataset": KaggleType(
                prefix="dataset",
                download_cmd="datasets",
                dl_flag="-d",
                extra_flag="--unzip"),
        "competition": KaggleType(
                prefix="competition",
                download_cmd="competitions",
                dl_flag="-c",
                extra_flag="")
}


def _get_kaggle_type(competition_name):
    if "/" in competition_name:
        return _KAGGLE_TYPES["dataset"]
    else:
        return _KAGGLE_TYPES["competition"]


class KaggleFile(object):
    """Represents a Kaggle competition file."""
    _URL_PREFIX = "kaggle://"

    def __init__(self, competition_name, filename):
        self._competition_name = competition_name
        self._filename = filename
        self.type = _get_kaggle_type(competition_name)

    @property
    def competition(self):
        return self._competition_name

    @property
    def filename(self):
        return self._filename

    @classmethod
    def from_url(cls, url):
        if not KaggleFile.is_kaggle_url(url):
            raise TypeError("Not a valid kaggle URL")
        download_type, competition_name, filename = (
                url[len(cls._URL_PREFIX):].split("/", 2))
        if download_type == "dataset":
            dataset_name, filename = filename.split("/", 1)
            competition_name = "%s/%s" % (competition_name, dataset_name)
        return cls(competition_name, filename)

    @staticmethod
    def is_kaggle_url(url):
        return url.startswith(KaggleFile._URL_PREFIX)

    def to_url(self):
        return "%s%s/%s/%s" % (self._URL_PREFIX,
                                                     self.type.prefix,
                                                     self._competition_name,
                                                     self._filename)


class KaggleCompetitionDownloader(object):
    """Downloader for a Kaggle competition.

    Usage:
    You can download with dataset or competition name like `zillow/zecon`
    or `titanic`.

    ```
    downloader = KaggleCompetitionDownloader(competition_name)
    for fname in downloader.competition_files:
        downloader.download_file(fname, make_file_output_path(fname))
    ```
    """

    def __init__(self, competition_name):
        self._competition_name = competition_name
        self._kaggle_type = _get_kaggle_type(self._competition_name)

    @utils.memoized_property
    def competition_files(self):
        """List of competition files."""
        command = [
                "kaggle",
                self._kaggle_type.download_cmd,
                "files",
                "-v",
                self._competition_name,
        ]
        output = _run_kaggle_command(command, self._competition_name)
        return sorted([
                line.split(",")[0] for line in output.split("\n")[1:] if line
        ])

    @utils.memoized_property
    def competition_urls(self):
        """Returns 'kaggle://' urls."""
        return [
                KaggleFile(self._competition_name, fname).to_url()
                for fname in self.competition_files  # pylint: disable=not-an-iterable
        ]

    def download_file(self, fname, output_dir):
        """Downloads competition file to output_dir."""
        if fname not in self.competition_files:  # pylint: disable=unsupported-membership-test
            raise ValueError("%s is not one of the competition's "
                                             "files: %s" % (fname, self.competition_files))
        command = [
                "kaggle",
                self._kaggle_type.download_cmd,
                "download",
                "--file",
                fname,
                "--path",
                output_dir,
                self._kaggle_type.dl_flag,
                self._competition_name
        ]
        if self._kaggle_type.extra_flag:
            command.append(self._kaggle_type.extra_flag)
        _run_kaggle_command(command, self._competition_name)
        return os.path.join(output_dir, fname)


def _run_kaggle_command(command_args, competition_name):
    """Run kaggle command with subprocess."""
    try:
        output = sp.check_output(command_args)
        return str(output)
    except sp.CalledProcessError as err:
        output = err.output
        _log_command_output(output, error=True)
        if output.startswith(b"404"):
            logger.error(_NOT_FOUND_ERR_MSG, competition_name)
            raise
        logger.error(_ERR_MSG, competition_name)
        raise


def _log_command_output(output, error=False):
    log = logger.error if error else logger.info
    log("kaggle command output:\n%s", str(output))
