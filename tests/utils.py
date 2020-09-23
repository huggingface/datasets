import os
import unittest
from distutils.util import strtobool

from datasets.utils.file_utils import _tf_available, _torch_available


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


def require_beam(test_case):
    """
    Decorator marking a test that requires Apache Beam.

    These tests are skipped when Apache Beam isn't installed.

    """
    if not _torch_available:
        test_case = unittest.skip("test requires PyTorch")(test_case)
    return test_case


def require_faiss(test_case):
    """
    Decorator marking a test that requires Apache Beam.

    These tests are skipped when Faiss isn't installed.

    """
    try:
        import faiss  # noqa
    except ImportError:
        test_case = unittest.skip("test requires faiss")(test_case)
    return test_case

    
def require_regex(test_case):
    """
    Decorator marking a test that requires Apache Beam.

    These tests are skipped when Regex isn't installed.

    """
    try:
        import regex  # noqa
    except ImportError:
        test_case = unittest.skip("test requires regex")(test_case)
    return test_case


def require_torch(test_case):
    """
    Decorator marking a test that requires PyTorch.

    These tests are skipped when PyTorch isn't installed.

    """
    if not _torch_available:
        test_case = unittest.skip("test requires PyTorch")(test_case)
    return test_case


def require_tf(test_case):
    """
    Decorator marking a test that requires TensorFlow.

    These tests are skipped when TensorFlow isn't installed.

    """
    if not _tf_available:
        test_case = unittest.skip("test requires TensorFlow")(test_case)
    return test_case


def require_transformers(test_case):
    """
    Decorator marking a test that requires transformers.

    These tests are skipped when transformers isn't installed.

    """
    try:
        import transformers  # noqa F401
    except ImportError:
        return unittest.skip("test requires transformers")(test_case)
    else:
        return test_case


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
