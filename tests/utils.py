import os
import tempfile
import unittest
from contextlib import contextmanager
from distutils.util import strtobool
from enum import Enum
from pathlib import Path
from unittest.mock import patch

import pyarrow as pa

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
            raise ValueError(f"If set, {key} must be yes or no.")
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


def require_jax(test_case):
    """
    Decorator marking a test that requires JAX.

    These tests are skipped when JAX isn't installed.

    """
    if not config.JAX_AVAILABLE:
        test_case = unittest.skip("test requires JAX")(test_case)
    return test_case


def require_pil(test_case):
    """
    Decorator marking a test that requires Pillow.

    These tests are skipped when Pillow isn't installed.

    """
    if not config.PIL_AVAILABLE:
        test_case = unittest.skip("test requires Pillow")(test_case)
    return test_case


def require_zstandard(test_case):
    """
    Decorator marking a test that requires zstandard.

    These tests are skipped when zstandard isn't installed.

    """
    if not config.ZSTANDARD_AVAILABLE:
        test_case = unittest.skip("test requires zstandard")(test_case)
    return test_case


def require_lz4(test_case):
    """
    Decorator marking a test that requires lz4.

    These tests are skipped when lz4 isn't installed.

    """
    if not config.LZ4_AVAILABLE:
        test_case = unittest.skip("test requires lz4")(test_case)
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


def require_s3(test_case):
    """
    Decorator marking a test that requires s3fs and moto to mock s3.

    These tests are skipped when they aren't installed.

    """
    try:
        import moto  # noqa F401
        import s3fs  # noqa F401
    except ImportError:
        return unittest.skip("test requires s3fs and moto")(test_case)
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
    Decorator marking a test as one that relies on GitHub or the Hugging Face Hub.

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


class OfflineSimulationMode(Enum):
    CONNECTION_FAILS = 0
    CONNECTION_TIMES_OUT = 1
    HF_DATASETS_OFFLINE_SET_TO_1 = 2


@contextmanager
def offline(mode=OfflineSimulationMode.CONNECTION_FAILS, timeout=1e-16):
    """
    Simulate offline mode.

    There are three offline simulatiom modes:

    CONNECTION_FAILS (default mode): a ConnectionError is raised for each network call.
        Connection errors are created by mocking socket.socket
    CONNECTION_TIMES_OUT: the connection hangs until it times out.
        The default timeout value is low (1e-16) to speed up the tests.
        Timeout errors are created by mocking requests.request
    HF_DATASETS_OFFLINE_SET_TO_1: the HF_DATASETS_OFFLINE environment variable is set to 1.
        This makes the http/ftp calls of the library instantly fail and raise an OfflineModeEmabled error.
    """
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
        raise OSError("Offline mode is enabled.")

    if mode is OfflineSimulationMode.CONNECTION_FAILS:
        # inspired from https://stackoverflow.com/a/18601897
        with patch("socket.socket", offline_socket):
            yield
    elif mode is OfflineSimulationMode.CONNECTION_TIMES_OUT:
        # inspired from https://stackoverflow.com/a/904609
        with patch("requests.request", timeout_request):
            with patch("requests.api.request", timeout_request):
                yield
    elif mode is OfflineSimulationMode.HF_DATASETS_OFFLINE_SET_TO_1:
        with patch("datasets.config.HF_DATASETS_OFFLINE", True):
            yield
    else:
        raise ValueError("Please use a value from the OfflineSimulationMode enum.")


@contextmanager
def set_current_working_directory_to_temp_dir(*args, **kwargs):
    original_working_dir = str(Path().resolve())
    with tempfile.TemporaryDirectory(*args, **kwargs) as tmp_dir:
        try:
            os.chdir(tmp_dir)
            yield
        finally:
            os.chdir(original_working_dir)


@contextmanager
def assert_arrow_memory_increases():
    import gc

    gc.collect()
    previous_allocated_memory = pa.total_allocated_bytes()
    yield
    assert pa.total_allocated_bytes() - previous_allocated_memory > 0, "Arrow memory didn't increase."


@contextmanager
def assert_arrow_memory_doesnt_increase():
    import gc

    gc.collect()
    previous_allocated_memory = pa.total_allocated_bytes()
    yield
    assert pa.total_allocated_bytes() - previous_allocated_memory <= 0, "Arrow memory wasn't expected to increase."
