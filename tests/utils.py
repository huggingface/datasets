import os
import tempfile
import unittest
from contextlib import contextmanager
from distutils.util import strtobool
from pathlib import Path
from unittest.mock import patch

from datasets import config


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
_run_remote_tests = parse_flag_from_env("RUN_REMOTE", default=False)
_run_local_tests = parse_flag_from_env("RUN_LOCAL", default=True)
_run_packaged_tests = parse_flag_from_env("RUN_PACKAGED", default=True)


def require_beam(test_case):
    """
    Decorator marking a test that requires Apache Beam.

    These tests are skipped when Apache Beam isn't installed.

    """
    if not config.TORCH_AVAILABLE:
        test_case = unittest.skip("test requires PyTorch")(test_case)
    return test_case


def require_faiss(test_case):
    """
    Decorator marking a test that requires Faiss.

    These tests are skipped when Faiss isn't installed.

    """
    try:
        import faiss  # noqa
    except ImportError:
        test_case = unittest.skip("test requires faiss")(test_case)
    return test_case


def require_regex(test_case):
    """
    Decorator marking a test that requires regex.

    These tests are skipped when Regex isn't installed.

    """
    try:
        import regex  # noqa
    except ImportError:
        test_case = unittest.skip("test requires regex")(test_case)
    return test_case


def require_elasticsearch(test_case):
    """
    Decorator marking a test that requires ElasticSearch.

    These tests are skipped when ElasticSearch isn't installed.

    """
    try:
        import elasticsearch  # noqa
    except ImportError:
        test_case = unittest.skip("test requires elasticsearch")(test_case)
    return test_case


def require_torch(test_case):
    """
    Decorator marking a test that requires PyTorch.

    These tests are skipped when PyTorch isn't installed.

    """
    if not config.TORCH_AVAILABLE:
        test_case = unittest.skip("test requires PyTorch")(test_case)
    return test_case


def require_tf(test_case):
    """
    Decorator marking a test that requires TensorFlow.

    These tests are skipped when TensorFlow isn't installed.

    """
    if not config.TF_AVAILABLE:
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


def packaged(test_case):
    """
    Decorator marking a test as packaged

    Packaged tests are run by default. Set the RUN_PACKAGED environment variable
    to a falsy value to not run them.
    """
    if not _run_packaged_tests or _run_packaged_tests == 0:
        test_case = unittest.skip("test is packaged")(test_case)
    return test_case


def remote(test_case):
    """
    Decorator marking a test as one that relies on github or aws.

    Remote tests are skipped by default. Set the RUN_REMOTE environment variable
    to a falsy value to not run them.
    """
    if not _run_remote_tests or _run_remote_tests == 0:
        test_case = unittest.skip("test requires remote")(test_case)
    return test_case


def for_all_test_methods(*decorators):
    def decorate(cls):
        for name, fn in cls.__dict__.items():
            if callable(fn) and name.startswith("test"):
                for decorator in decorators:
                    fn = decorator(fn)
                setattr(cls, name, fn)
        return cls

    return decorate


class RequestWouldHangIndefinitelyError(Exception):
    pass


@contextmanager
def offline(connection_times_out=False, timeout=1e-16):
    """
    Simulate offline mode.

    By default a ConnectionError is raised for each network call.
    With connection_times_out=True on the other hand, the connection hangs until it times out.
    The default timeout value is low (1e-16) to speed up the tests.

    Connection errors are created by mocking socket.socket,
    while the timeout errors are created by mocking requests.request.
    """
    import socket

    from requests import request as online_request

    def timeout_request(method, url, **kwargs):
        # Change the url to an invalid url so that the connection hangs
        invalid_url = "https://10.255.255.1"
        if kwargs.get("timeout") is None:
            raise RequestWouldHangIndefinitelyError(
                f"Tried a call to {url} in offline mode with no timeout set. Please set a timeout."
            )
        kwargs["timeout"] = timeout
        try:
            return online_request(method, invalid_url, **kwargs)
        except Exception as e:
            # The following changes in the error are just here to make the offline timeout error prettier
            e.request.url = url
            max_retry_error = e.args[0]
            max_retry_error.args = (max_retry_error.args[0].replace("10.255.255.1", f"OfflineMock[{url}]"),)
            e.args = (max_retry_error,)
            raise

    def offline_socket(*args, **kwargs):
        raise socket.error("Offline mode is enabled.")

    if connection_times_out:
        # inspired from https://stackoverflow.com/a/904609
        with patch("requests.request", timeout_request):
            yield
    else:
        # inspired from https://stackoverflow.com/a/18601897
        with patch("socket.socket", offline_socket):
            yield


@contextmanager
def set_current_working_directory_to_temp_dir(*args, **kwargs):
    original_working_dir = str(Path().resolve())
    with tempfile.TemporaryDirectory(*args, **kwargs) as tmp_dir:
        os.chdir(tmp_dir)
        yield
        os.chdir(original_working_dir)
