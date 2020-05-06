import logging
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


def slow(test_case):
    """
    Decorator marking a test as slow.

    Slow tests are skipped by default. Set the RUN_SLOW environment variable
    to a truthy value to run them.

    """
    if not _run_slow_tests:
        test_case = unittest.skip("test is slow")(test_case)
    return test_case


class MockDataLoaderManager(object):
    dummy_data_folder_name = "dummy"
    dummy_data_file_name = "dummy_data.zip"
    dummy_data_extracted_folder_name = "dummy_data"

    def __init__(self, dataset_name, config, version, cache_dir, verbose=True):
        self.downloaded_size = 0
        self.dataset_name = dataset_name
        self.cache_dir = cache_dir
        self.verbose = True

        self.config_name = config.name if config is not None else ""
        self.version_name = str(version.major) + "." + str(version.minor) + "." + str(version.patch)

        # structure is dummy / config_name / version_name / dummy_data.zip
        self.path_to_dummy_file = os.path.join(
            self.dummy_data_folder_name, self.config_name, self.version_name, self.dummy_data_file_name
        )

    # this function has to be in the manager under this name to work
    def download_and_extract(self, data_url, *args):
        # download dummy data
        path_to_dummy_data = self.download_dummy_data()

        # print expected dummy folder structure
        if self.verbose is True:
            self.print_dummy_data_folder_structure(data_url)

        # special case when data_url is a dict
        if isinstance(data_url, dict):
            return self.create_dummy_data_dict(path_to_dummy_data, data_url)
        return path_to_dummy_data

    def download_dummy_data(self):
        # get url to dummy data on AWS S3 bucket
        url_to_dummy_data_dir = hf_bucket_url(self.dataset_name, filename=self.path_to_dummy_file)

        # this function will download the dummy data and return the path
        local_path = cached_path(
            url_to_dummy_data_dir, cache_dir=self.cache_dir, extract_compressed_file=True, force_extract=True
        )
        return os.path.join(local_path, self.dummy_data_extracted_folder_name)

    def print_dummy_data_folder_structure(self, data_url):
        logging.info(str(20 * "*" + " EXPECTED STRUCTURE OF {} " + 20 * "*").format(self.dummy_data_folder_name))
        logging.info(self.path_to_dummy_file)

        # special case when data_url is a dict
        if isinstance(data_url, dict):
            dummy_data_folder = self.create_dummy_data_dict(self.dummy_data_extracted_folder_name, data_url)
            logging.info(str(20 * "-" + " EXPECTED STRUCTURE OF {} " + 10 * "-").format(self.dummy_data_file_name))
            for key, value in dummy_data_folder.items():
                logging.info(
                    "{} contains folder or file, depending on the `_generate_splits` method called: {} .".format(
                        self.dummy_data_file_name, value
                    )
                )
                if ".zip" in value:
                    logging.info(
                        "data url in `_generate_split` expects a zipped folder. {} should be a directory and match the folder structure of the extracted content of {}".format(
                            value, data_url[key]
                        )
                    )
        else:
            logging.info(
                "{} contains folder a folder or file depending on the `_generate_splits` method that matches names as specified in `_generate_splits`".format(
                    self.dummy_data_file_name,
                )
            )
            if ".zip" in data_url:
                logging.info(
                    "data url in `_generate_split` expects a zipped folder. The dummy folder structure should match the extracted zip file folder structure of {}".format(
                        data_url
                    )
                )
        logging.info(68 * "*")

    def create_dummy_data_dict(self, path_to_dummy_data, data_url):
        dummy_data_dict = {}
        for key, abs_path in data_url.items():
            # we force the name of each key to be the last file / folder name of the url path
            if isinstance(abs_path, list):
                value = [os.path.join(path_to_dummy_data, x.split("/")[-1]) for x in abs_path]
            else:
                value = os.path.join(path_to_dummy_data, abs_path.split("/")[-1])
            dummy_data_dict[key] = value
        return dummy_data_dict

    def check_or_save_checksums(self, *args):
        pass
