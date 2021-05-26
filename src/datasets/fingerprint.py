import inspect
import json
import os
import random
import shutil
import tempfile
import weakref
from dataclasses import asdict
from functools import wraps
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import numpy as np
import pyarrow as pa
import xxhash

from datasets.table import ConcatenationTable, InMemoryTable, MemoryMappedTable, Table

from .info import DatasetInfo
from .utils.logging import get_logger
from .utils.py_utils import dumps


if TYPE_CHECKING:
    from .arrow_dataset import Dataset


logger = get_logger(__name__)


# Fingerprinting allows to have one deterministic fingerprint per dataset state.
# A dataset fingerprint is updated after each transform.
# Re-running the same transforms on a dataset in a different session results in the same fingerprint.
# This is possible thanks to a custom hashing function that works with most python objects.

# Fingerprinting is the main mechanism that enables caching.
# The caching mechanism allows to reload an existing cache file if it's already been computed.


#################
# Caching
#################

_CACHING_ENABLED = True
_TEMP_DIR_FOR_TEMP_CACHE_FILES: Optional["_TempDirWithCustomCleanup"] = None
_DATASETS_WITH_TABLE_IN_TEMP_DIR: Optional[weakref.WeakSet] = None


class _TempDirWithCustomCleanup:
    """
    A temporary directory with a custom cleanup function.
    We need a custom temporary directory cleanup in order to delete the dataset objects that have
    cache files in the temporary directory before deleting the dorectory itself.
    """

    def __init__(self, cleanup_func=None, *cleanup_func_args, **cleanup_func_kwargs):
        self.name = tempfile.mkdtemp()
        self._finalizer = weakref.finalize(self, self._cleanup)
        self._cleanup_func = cleanup_func
        self._cleanup_func_args = cleanup_func_args
        self._cleanup_func_kwargs = cleanup_func_kwargs

    def _cleanup(self):
        self._cleanup_func(*self._cleanup_func_args, **self._cleanup_func_kwargs)
        if os.path.exists(self.name):
            shutil.rmtree(self.name)

    def cleanup(self):
        if self._finalizer.detach():
            self._cleanup()


def maybe_register_dataset_for_temp_dir_deletion(dataset):
    """
    This function registers the datasets that have cache files in _TEMP_DIR_FOR_TEMP_CACHE_FILES in order
    to properly delete them before deleting the temporary directory.
    The temporary directory _TEMP_DIR_FOR_TEMP_CACHE_FILES is used when caching is disabled.
    """
    if _TEMP_DIR_FOR_TEMP_CACHE_FILES is None:
        return

    global _DATASETS_WITH_TABLE_IN_TEMP_DIR
    if _DATASETS_WITH_TABLE_IN_TEMP_DIR is None:
        _DATASETS_WITH_TABLE_IN_TEMP_DIR = weakref.WeakSet()
    if any(
        os.path.samefile(os.path.dirname(cache_file["filename"]), _TEMP_DIR_FOR_TEMP_CACHE_FILES.name)
        for cache_file in dataset.cache_files
    ):
        _DATASETS_WITH_TABLE_IN_TEMP_DIR.add(dataset)


def get_datasets_with_cache_file_in_temp_dir():
    return list(_DATASETS_WITH_TABLE_IN_TEMP_DIR) if _DATASETS_WITH_TABLE_IN_TEMP_DIR is not None else []


def set_caching_enabled(boolean: bool):
    """
    When applying transforms on a dataset, the data are stored in cache files.
    The caching mechanism allows to reload an existing cache file if it's already been computed.

    Reloading a dataset is possible since the cache files are named using the dataset fingerprint, which is updated
    after each transform.

    If disabled, the library will no longer reload cached datasets files when applying transforms to the datasets.
    More precisely, if the caching is disabled:
    - cache files are always recreated
    - cache files are written to a temporary directory that is deleted when session closes
    - cache files are named using a random hash instead of the dataset fingerprint
    - use :func:`datasets.Dataset.save_to_disk` to save a transformed dataset or it will be deleted when session closes
    - caching doesn't affect :func:`datasets.load_dataset`. If you want to regenerate a dataset from scratch you should use
    the ``download_mode`` parameter in :func:`datasets.load_dataset`.
    """
    global _CACHING_ENABLED
    _CACHING_ENABLED = bool(boolean)


def is_caching_enabled() -> bool:
    """
    When applying transforms on a dataset, the data are stored in cache files.
    The caching mechanism allows to reload an existing cache file if it's already been computed.

    Reloading a dataset is possible since the cache files are named using the dataset fingerprint, which is updated
    after each transform.

    If disabled, the library will no longer reload cached datasets files when applying transforms to the datasets.
    More precisely, if the caching is disabled:
    - cache files are always recreated
    - cache files are written to a temporary directory that is deleted when session closes
    - cache files are named using a random hash instead of the dataset fingerprint
    - use :func:`datasets.Dataset.save_to_disk` to save a transformed dataset or it will be deleted when session closes
    - caching doesn't affect :func:`datasets.load_dataset`. If you want to regenerate a dataset from scratch you should use
    the ``download_mode`` parameter in :func:`datasets.load_dataset`.
    """
    global _CACHING_ENABLED
    return bool(_CACHING_ENABLED)


def get_temporary_cache_files_directory() -> str:
    """Return a directory that is deleted when session closes."""
    global _TEMP_DIR_FOR_TEMP_CACHE_FILES
    if _TEMP_DIR_FOR_TEMP_CACHE_FILES is None:

        # Avoids a PermissionError on Windows caused by the datasets referencing
        # the files from the cache directory on clean-up
        def cleanup_func():
            for dset in get_datasets_with_cache_file_in_temp_dir():
                dset.__del__()

        _TEMP_DIR_FOR_TEMP_CACHE_FILES = _TempDirWithCustomCleanup(cleanup_func=cleanup_func)
    return _TEMP_DIR_FOR_TEMP_CACHE_FILES.name


#################
# Hashing
#################


def hashregister(*types):
    def proxy(func):
        for t in types:
            Hasher.dispatch[t] = func
        return func

    return proxy


class Hasher:
    """Hasher that accepts python objets as inputs."""

    dispatch: Dict = {}

    def __init__(self):
        self.m = xxhash.xxh64()

    @classmethod
    def hash_bytes(cls, value: Union[bytes, List[bytes]]) -> str:
        value = [value] if isinstance(value, bytes) else value
        m = xxhash.xxh64()
        for x in value:
            m.update(x)
        return m.hexdigest()

    @classmethod
    def hash_default(cls, value: Any) -> str:
        return cls.hash_bytes(dumps(value))

    @classmethod
    def hash(cls, value: Any) -> str:
        if type(value) in cls.dispatch:
            return cls.dispatch[type(value)](cls, value)
        else:
            return cls.hash_default(value)

    def update(self, value: Any) -> None:
        header_for_update = f"=={type(value)}=="
        value_for_update = self.hash(value)
        self.m.update(header_for_update.encode("utf8"))
        self.m.update(value_for_update.encode("utf-8"))

    def hexdigest(self) -> str:
        return self.m.hexdigest()


# Register a new hasher can be useful for two possible reasons:
# 1 - optimize the hashing of large amount of data (e.g. pa.Table)
# 2 - take advantage of a custom serialization method (e.g. DatasetInfo)


@hashregister(pa.Table, Table, InMemoryTable, MemoryMappedTable, ConcatenationTable)
def _hash_pa_table(hasher, value):
    def _hash_pa_array(value):
        if isinstance(value, pa.ChunkedArray):
            return hasher.hash_bytes(c.to_string().encode("utf-8") for c in value.chunks)
        else:
            return hasher.hash_bytes(value.to_string().encode("utf-8"))

    value = "-".join(col + "-" + _hash_pa_array(value[col]) for col in sorted(value.column_names))
    return hasher.hash_bytes(value.encode("utf-8"))


@hashregister(DatasetInfo)
def _hash_dataset_info(hasher, value):
    return hasher.hash_bytes(json.dumps(asdict(value), sort_keys=True).encode("utf-8"))


#################
# Fingerprinting
#################

# we show a warning only once when fingerprinting fails to avoid spam
fingerprint_warnings: Dict[str, bool] = {}


def generate_fingerprint(dataset) -> str:
    state = dataset.__dict__
    hasher = Hasher()
    for key in sorted(state):
        if key == "_fingerprint":
            continue
        hasher.update(key)
        hasher.update(state[key])
    # hash data files last modification timestamps as well
    for cache_file in dataset.cache_files:
        hasher.update(os.path.getmtime(cache_file["filename"]))
    return hasher.hexdigest()


def generate_random_fingerprint(nbits=64) -> str:
    return f"{random.getrandbits(nbits):0{nbits//4}x}"


def update_fingerprint(fingerprint, transform, transform_args):
    global fingerprint_warnings
    hasher = Hasher()
    hasher.update(fingerprint)
    try:
        hasher.update(transform)
    except:  # noqa various errors might raise here from pickle or dill
        if _CACHING_ENABLED:
            if not fingerprint_warnings.get("update_fingerprint_transform_hash_failed", False):
                logger.warning(
                    f"Transform {transform} couldn't be hashed properly, a random hash was used instead. "
                    "Make sure your transforms and parameters are serializable with pickle or dill for the dataset fingerprinting and caching to work. "
                    "If you reuse this transform, the caching mechanism will consider it to be different from the previous calls and recompute everything. "
                    "This warning is only showed once. Subsequent hashing failures won't be showed."
                )
                fingerprint_warnings["update_fingerprint_transform_hash_failed"] = True
            else:
                logger.info(f"Transform {transform} couldn't be hashed properly, a random hash was used instead.")
        else:
            logger.info(
                f"Transform {transform} couldn't be hashed properly, a random hash was used instead. This doesn't affect caching since it's disabled."
            )

        return generate_random_fingerprint()
    for key in sorted(transform_args):
        hasher.update(key)
        try:
            hasher.update(transform_args[key])
        except:  # noqa various errors might raise here from pickle or dill
            if _CACHING_ENABLED:
                if not fingerprint_warnings.get("update_fingerprint_transform_hash_failed", False):
                    logger.warning(
                        f"Parameter '{key}'={transform_args[key]} of the transform {transform} couldn't be hashed properly, a random hash was used instead. "
                        "Make sure your transforms and parameters are serializable with pickle or dill for the dataset fingerprinting and caching to work. "
                        "If you reuse this transform, the caching mechanism will consider it to be different from the previous calls and recompute everything. "
                        "This warning is only showed once. Subsequent hashing failures won't be showed."
                    )
                    fingerprint_warnings["update_fingerprint_transform_hash_failed"] = True
                else:
                    logger.info(
                        f"Parameter '{key}'={transform_args[key]} of the transform {transform} couldn't be hashed properly, a random hash was used instead."
                    )
            else:
                logger.info(
                    f"Parameter '{key}'={transform_args[key]} of the transform {transform} couldn't be hashed properly, a random hash was used instead. This doesn't affect caching since it's disabled."
                )
            return generate_random_fingerprint()
    return hasher.hexdigest()


def fingerprint_transform(
    inplace: bool,
    use_kwargs: Optional[List[str]] = None,
    ignore_kwargs: Optional[List[str]] = None,
    fingerprint_names: Optional[List[str]] = None,
    randomized_function: bool = False,
):
    """
    Wrapper for dataset transforms to update the dataset fingerprint using ``update_fingerprint``

    Args:
        inplace (``bool``):  If inplace is True, the fingerprint of the dataset is updated inplace.
            Otherwise, a parameter "new_fingerprint" is passed to the wrapped method that should take care of
            setting the fingerprint of the returned Dataset.
        use_kwargs (Optional ``List[str]``): optional white list of argument names to take into account
            to update the fingerprint to the wrapped method that should take care of
            setting the fingerprint of the returned Dataset. By default all the arguments are used.
        ignore_kwargs (Optional ``List[str]``): optional black list of argument names to take into account
            to update the fingerprint. Note that ignore_kwargs prevails on use_kwargs.
        fingerprint_names (Optional ``List[str]``, defaults to ["new_fingerprint"]):
            If the dataset transforms is not inplace and returns a DatasetDict, then it can require
            several fingerprints (one per dataset in the DatasetDict). By specifying fingerprint_names,
            one fingerprint named after each element of fingerprint_names is going to be passed.
        randomized_function (``bool``, defaults to False): If the dataset transform is random and has
            optional parameters "seed" and "generator", then you can set randomized_function to True.
            This way, even if users set "seed" and "generator" to None, then the fingerprint is
            going to be randomly generated depending on numpy's current state. In this case, the
            generator is set to np.random.default_rng(np.random.get_state()[1][0]).
    """

    assert use_kwargs is None or isinstance(use_kwargs, list), "use_kwargs is supposed to be a list, not {}".format(
        type(use_kwargs)
    )
    assert ignore_kwargs is None or isinstance(
        ignore_kwargs, list
    ), "ignore_kwargs is supposed to be a list, not {}".format(type(use_kwargs))
    assert not inplace or not fingerprint_names, "fingerprint_names are only used when inplace is False"
    fingerprint_names = fingerprint_names if fingerprint_names is not None else ["new_fingerprint"]

    def _fingerprint(func):

        assert inplace or all(  # check that not in-place functions require fingerprint parameters
            name in func.__code__.co_varnames for name in fingerprint_names
        ), "function {} is missing parameters {} in signature".format(func, fingerprint_names)
        if randomized_function:  # randomized function have seed and generator parameters
            assert "seed" in func.__code__.co_varnames, "'seed' must be in {}'s signature".format(func)
            assert "generator" in func.__code__.co_varnames, "'generator' must be in {}'s signature".format(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs_for_fingerprint = kwargs.copy()
            if args:
                params = [p.name for p in inspect.signature(func).parameters.values() if p != p.VAR_KEYWORD]
                self: "Dataset" = args[0]
                args = args[1:]
                params = params[1:]
                kwargs_for_fingerprint.update(zip(params, args))
            else:
                self: "Dataset" = kwargs.pop("self")

            # keep the right kwargs to be hashed to generate the fingerprint

            if use_kwargs:
                kwargs_for_fingerprint = {k: v for k, v in kwargs_for_fingerprint.items() if k in use_kwargs}
            if ignore_kwargs:
                kwargs_for_fingerprint = {k: v for k, v in kwargs_for_fingerprint.items() if k not in ignore_kwargs}
            if randomized_function:  # randomized functions have `seed` and `generator` parameters
                if kwargs_for_fingerprint.get("seed") is None and kwargs_for_fingerprint.get("generator") is None:
                    kwargs_for_fingerprint["generator"] = np.random.default_rng(np.random.get_state()[1][0])

            # remove kwargs that are the default values

            default_values = {
                p.name: p.default for p in inspect.signature(func).parameters.values() if p.default != inspect._empty
            }
            for default_varname, default_value in default_values.items():
                if (
                    default_varname in kwargs_for_fingerprint
                    and kwargs_for_fingerprint[default_varname] == default_value
                ):
                    kwargs_for_fingerprint.pop(default_varname)

            # compute new_fingerprint and add it to the args of not in-place transforms
            transform = func.__module__ + "." + func.__qualname__
            if inplace:
                new_fingerprint = update_fingerprint(self._fingerprint, transform, kwargs_for_fingerprint)
            else:
                for fingerprint_name in fingerprint_names:  # transforms like `train_test_split` have several hashes
                    if kwargs.get(fingerprint_name) is None:
                        kwargs_for_fingerprint["fingerprint_name"] = fingerprint_name
                        kwargs[fingerprint_name] = update_fingerprint(
                            self._fingerprint, transform, kwargs_for_fingerprint
                        )

            # Call actual function

            out = func(self, *args, **kwargs)

            # Update fingerprint of in-place transforms + update in-place history of transforms

            if inplace:  # update after calling func so that the fingerprint doesn't change if the function fails
                self._fingerprint = new_fingerprint

            return out

        wrapper._decorator_name_ = "fingerprint"
        return wrapper

    return _fingerprint
