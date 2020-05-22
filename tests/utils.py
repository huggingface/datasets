import os
import unittest
from distutils.util import strtobool

from nlp import cached_path, hf_bucket_url


def parse_flag_from_env(key, default=False):
    try:
        value = os.environ[key]
    except KeyError:
        # KEY isn't set, default to `default`.
        _value = default
    else:
        # KEY is set, convert it to True or False.
        try:
            _value = strtobool(value)
        except ValueError:
            # More values are supported, but let's keep the message simple.
            raise ValueError("If set, {} must be yes or no.".format(key))
    return _value


_run_slow_tests = parse_flag_from_env("RUN_SLOW", default=False)
_run_aws_tests = parse_flag_from_env("RUN_AWS", default=True)
_run_local_tests = parse_flag_from_env("RUN_LOCAL", default=True)


def slow(test_case):
    """
    Decorator marking a test as slow.

    Slow tests are skipped by default. Set the RUN_SLOW environment variable
    to a truthy value to run them.

    """
    if not _run_slow_tests or _run_slow_tests == 0:
        test_case = unittest.skip("test is slow")(test_case)
    return test_case


def local(test_case):
    """
    Decorator marking a test as local

    Local tests are run by default. Set the RUN_LOCAL environment variable
    to a falsy value to not run them.
    """
    if not _run_local_tests or _run_local_tests == 0:
        test_case = unittest.skip("test is local")(test_case)
    return test_case


def aws(test_case):
    """
    Decorator marking a test as one that relies on AWS.

    AWS tests are skipped by default. Set the RUN_AWS environment variable
    to a falsy value to not run them.
    """
    if not _run_aws_tests or _run_aws_tests == 0:
        test_case = unittest.skip("test requires aws")(test_case)
    return test_case


class MockDataLoaderManager(object):
    def __init__(self, dataset_name, config, version, cache_dir, is_local=False, verbose=True):
        self.downloaded_size = 0
        self.dataset_name = dataset_name
        self.cache_dir = cache_dir
        self.verbose = verbose
        self.is_local = is_local
        self.config = config

        # TODO(PVP, QUENTIN) might need to make this more general
        self.version_name = str(version.major) + "." + str(version.minor) + "." + str(version.patch)
        # to be downloaded
        self._dummy_file = None

    @property
    def dummy_file(self):
        if self._dummy_file is None:
            self._dummy_file = self.download_dummy_data()
        return self._dummy_file

    @property
    def dummy_zip_file(self):
        if self.config is not None:
            # structure is dummy / config_name / version_name / dummy_data.zip
            return os.path.join("dummy", self.config.name, self.version_name, "dummy_data.zip")
        return os.path.join("dummy", self.version_name, "dummy_data.zip")

    def download_dummy_data(self):
        if self.is_local is True:
            # extract local data
            path_to_dummy_data_dir = os.path.join("datasets", self.dataset_name, self.dummy_zip_file)
        else:
            # get url to dummy data on AWS S3 bucket
            path_to_dummy_data_dir = hf_bucket_url(self.dataset_name, filename=self.dummy_zip_file)

            # this function will download the dummy data and return the path
        local_path = cached_path(
            path_to_dummy_data_dir, cache_dir=self.cache_dir, extract_compressed_file=True, force_extract=True
        )
        return os.path.join(local_path, "dummy_data")

    @property
    def manual_dir(self):
        # return full path if its a dir
        if os.path.isdir(self.dummy_file):
            return self.dummy_file
        # else cut off path to file -> example `xsum`.
        return "/".join(self.dummy_file.split("/")[:-1])

    # this function has to be in the manager under this name so that testing works
    def download_and_extract(self, data_url, *args):
        # special case when data_url is a dict
        if isinstance(data_url, dict):
            return self.create_dummy_data_dict(self.dummy_file, data_url)
        return self.dummy_file

    # this function has to be in the manager under this name so that testing works
    def download_custom(self, data_url, custom_download):
        return self.download_and_extract(data_url)

    # this function has to be in the manager under this name so that testing works
    def extract(self, path):
        return path

    # this function has to be in the manager under this name so that testing works
    def get_recorded_sizes_checksums(self):
        return {}

    def create_dummy_data_dict(self, path_to_dummy_data, data_url):
        dummy_data_dict = {}
        for key, abs_path in data_url.items():
            # we force the name of each key to be the last file / folder name of the url path
            if isinstance(abs_path, list):
                value = [os.path.join(path_to_dummy_data, x.split("/")[-1]) for x in abs_path]
            else:
                value = os.path.join(path_to_dummy_data, abs_path.split("/")[-1])
            dummy_data_dict[key] = value

        # make sure that values are unique
        first_value = next(iter(dummy_data_dict.values()))
        if isinstance(first_value, str) and len(set(dummy_data_dict.values())) < len(dummy_data_dict.values()):
            # append key to value to make its name unique
            dummy_data_dict = {key: value + key for key, value in dummy_data_dict.items()}

        return dummy_data_dict
