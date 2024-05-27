import asyncio
import importlib.metadata
import os
import re
import sys
import tempfile
import unittest
from contextlib import contextmanager
from copy import deepcopy
from distutils.util import strtobool
from enum import Enum
from importlib.util import find_spec
from pathlib import Path
from unittest.mock import patch

import pyarrow as pa
import pytest
import requests
from packaging import version

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

# Compression
require_lz4 = pytest.mark.skipif(not config.LZ4_AVAILABLE, reason="test requires lz4")
require_py7zr = pytest.mark.skipif(not config.PY7ZR_AVAILABLE, reason="test requires py7zr")
require_zstandard = pytest.mark.skipif(not config.ZSTANDARD_AVAILABLE, reason="test requires zstandard")

# Audio
require_sndfile = pytest.mark.skipif(
    # On Windows and OS X, soundfile installs sndfile
    find_spec("soundfile") is None or version.parse(importlib.metadata.version("soundfile")) < version.parse("0.12.0"),
    reason="test requires sndfile>=0.12.1: 'pip install \"soundfile>=0.12.1\"'; ",
)

# Beam
require_beam = pytest.mark.skipif(
    not config.BEAM_AVAILABLE or config.DILL_VERSION >= version.parse("0.3.2"),
    reason="test requires apache-beam and a compatible dill version",
)

# Dill-cloudpickle compatibility
require_dill_gt_0_3_2 = pytest.mark.skipif(
    config.DILL_VERSION <= version.parse("0.3.2"),
    reason="test requires dill>0.3.2 for cloudpickle compatibility",
)

# Windows
require_not_windows = pytest.mark.skipif(
    sys.platform == "win32",
    reason="test should not be run on Windows",
)


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


def require_sqlalchemy(test_case):
    """
    Decorator marking a test that requires SQLAlchemy.

    These tests are skipped when SQLAlchemy isn't installed.

    """
    try:
        import sqlalchemy  # noqa
    except ImportError:
        test_case = unittest.skip("test requires sqlalchemy")(test_case)
    return test_case


def require_torch(test_case):
    """
    Decorator marking a test that requires PyTorch.

    These tests are skipped when PyTorch isn't installed.

    """
    if not config.TORCH_AVAILABLE:
        test_case = unittest.skip("test requires PyTorch")(test_case)
    return test_case


def require_polars(test_case):
    """
    Decorator marking a test that requires Polars.

    These tests are skipped when Polars isn't installed.

    """
    if not config.POLARS_AVAILABLE:
        test_case = unittest.skip("test requires Polars")(test_case)
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


def require_tiktoken(test_case):
    """
    Decorator marking a test that requires tiktoken.

    These tests are skipped when transformers isn't installed.

    """
    try:
        import tiktoken  # noqa F401
    except ImportError:
        return unittest.skip("test requires tiktoken")(test_case)
    else:
        return test_case


def require_spacy(test_case):
    """
    Decorator marking a test that requires spacy.

    These tests are skipped when they aren't installed.

    """
    try:
        import spacy  # noqa F401
    except ImportError:
        return unittest.skip("test requires spacy")(test_case)
    else:
        return test_case


def require_pyspark(test_case):
    """
    Decorator marking a test that requires pyspark.

    These tests are skipped when pyspark isn't installed.

    """
    try:
        import pyspark  # noqa F401
    except ImportError:
        return unittest.skip("test requires pyspark")(test_case)
    else:
        return test_case


def require_joblibspark(test_case):
    """
    Decorator marking a test that requires joblibspark.

    These tests are skipped when pyspark isn't installed.

    """
    try:
        import joblibspark  # noqa F401
    except ImportError:
        return unittest.skip("test requires joblibspark")(test_case)
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
    online_request = requests.Session().request

    def timeout_request(session, method, url, **kwargs):
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

    def raise_connection_error(session, prepared_request, **kwargs):
        raise requests.ConnectionError("Offline mode is enabled.", request=prepared_request)

    if mode is OfflineSimulationMode.CONNECTION_FAILS:
        with patch("requests.Session.send", raise_connection_error):
            yield
    elif mode is OfflineSimulationMode.CONNECTION_TIMES_OUT:
        # inspired from https://stackoverflow.com/a/904609
        with patch("requests.Session.request", timeout_request):
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


def is_rng_equal(rng1, rng2):
    return deepcopy(rng1).integers(0, 100, 10).tolist() == deepcopy(rng2).integers(0, 100, 10).tolist()


def xfail_if_500_502_http_error(func):
    import decorator
    from requests.exceptions import HTTPError

    def _wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as err:
            if str(err).startswith("500") or str(err).startswith("502"):
                pytest.xfail(str(err))
            raise err

    return decorator.decorator(_wrapper, func)


# --- distributed testing functions --- #

# copied from transformers
# originally adapted from https://stackoverflow.com/a/59041913/9201239


class _RunOutput:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


async def _read_stream(stream, callback):
    while True:
        line = await stream.readline()
        if line:
            callback(line)
        else:
            break


async def _stream_subprocess(cmd, env=None, stdin=None, timeout=None, quiet=False, echo=False) -> _RunOutput:
    if echo:
        print("\nRunning: ", " ".join(cmd))

    p = await asyncio.create_subprocess_exec(
        cmd[0],
        *cmd[1:],
        stdin=stdin,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    # note: there is a warning for a possible deadlock when using `wait` with huge amounts of data in the pipe
    # https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process.wait
    #
    # If it starts hanging, will need to switch to the following code. The problem is that no data
    # will be seen until it's done and if it hangs for example there will be no debug info.
    # out, err = await p.communicate()
    # return _RunOutput(p.returncode, out, err)

    out = []
    err = []

    def tee(line, sink, pipe, label=""):
        line = line.decode("utf-8").rstrip()
        sink.append(line)
        if not quiet:
            print(label, line, file=pipe)

    # XXX: the timeout doesn't seem to make any difference here
    await asyncio.wait(
        [
            _read_stream(p.stdout, lambda line: tee(line, out, sys.stdout, label="stdout:")),
            _read_stream(p.stderr, lambda line: tee(line, err, sys.stderr, label="stderr:")),
        ],
        timeout=timeout,
    )
    return _RunOutput(await p.wait(), out, err)


def execute_subprocess_async(cmd, env=None, stdin=None, timeout=180, quiet=False, echo=True) -> _RunOutput:
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        _stream_subprocess(cmd, env=env, stdin=stdin, timeout=timeout, quiet=quiet, echo=echo)
    )

    cmd_str = " ".join(cmd)
    if result.returncode > 0:
        stderr = "\n".join(result.stderr)
        raise RuntimeError(
            f"'{cmd_str}' failed with returncode {result.returncode}\n\n"
            f"The combined stderr from workers follows:\n{stderr}"
        )

    # check that the subprocess actually did run and produced some output, should the test rely on
    # the remote side to do the testing
    if not result.stdout and not result.stderr:
        raise RuntimeError(f"'{cmd_str}' produced no output.")

    return result


def pytest_xdist_worker_id():
    """
    Returns an int value of worker's numerical id under `pytest-xdist`'s concurrent workers `pytest -n N` regime, or 0
    if `-n 1` or `pytest-xdist` isn't being used.
    """
    worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
    worker = re.sub(r"^gw", "", worker, 0, re.M)
    return int(worker)


def get_torch_dist_unique_port():
    """
    Returns a port number that can be fed to `torchrun`'s `--master_port` argument.

    Under `pytest-xdist` it adds a delta number based on a worker id so that concurrent tests don't try to use the same
    port at once.
    """
    port = 29500
    uniq_delta = pytest_xdist_worker_id()
    return port + uniq_delta
