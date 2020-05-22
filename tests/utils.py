import os
import unittest
from distutils.util import strtobool


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
