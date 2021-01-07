import json
import os
import random
from copy import deepcopy
from dataclasses import asdict
from functools import wraps
from typing import TYPE_CHECKING, Any, List, Union

import numpy as np
import pyarrow as pa
import xxhash

from .info import DatasetInfo
from .utils.logging import get_logger
from .utils.py_utils import dumps


logger = get_logger(__name__)


# Fingerprinting allows to have one deterministic fingerprint per dataset state.
# A dataset fingerprint is updated after each transform.
# Re-running the same transforms on a dataset in a different session results in the same fingerprint.
# Disabling the fingerprinting mechanism makes all the fingerprints random.
_FINGERPRINTING_ENABLED = True


if TYPE_CHECKING:
    from .arrow_dataset import Dataset


def set_fingerprinting_enabled(boolean: bool):
    """
    If disabled, the library will use random dataset fingerprint instead of computing them by hashing the transforms that are applied.
    Since the caching mechanism uses fingerprints to name the cache filescache file names will be different.
    Therefore disabling fingerprinting will prevent the caching mechanism from reloading datasets files that have already been computed.
    """
    global _FINGERPRINTING_ENABLED
    _FINGERPRINTING_ENABLED = bool(boolean)


def hashregister(t):
    def proxy(func):
        Hasher.dispatch[t] = func
        return func

    return proxy


class Hasher:
    """Hasher that accepts python objets as inputs."""

    dispatch = {}

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


@hashregister(pa.Table)
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


def generate_fingerprint(dataset) -> str:
    if not _FINGERPRINTING_ENABLED:
        return generate_random_fingerprint()
    state = dataset.__getstate__()
    hasher = Hasher()
    for key in sorted(state):
        if key == "_fingerprint":
            continue
        hasher.update(key)
        hasher.update(state[key])
    # hash data files last modification timestamps as well
    for data_file in state.get("_data_files", []) + state.get("_indices_data_files", []):
        hasher.update(os.path.getmtime(data_file["filename"]))
    return hasher.hexdigest()


def generate_random_fingerprint(nbits=64) -> str:
    return f"{random.getrandbits(nbits):0{nbits//4}x}"


def update_fingerprint(fingerprint, transform, transform_args):
    if not _FINGERPRINTING_ENABLED:
        return generate_random_fingerprint()
    hasher = Hasher()
    hasher.update(fingerprint)
    try:
        hasher.update(transform)
    except:  # noqa various errors might raise here from pickle or dill
        logger.warning(
            f"Transform {transform} couldn't be hashed properly, a random hash was used instead. "
            "Make sure your transforms and parameters are serializable with pickle or dill for the dataset fingerprinting and caching to work. "
            "If you reuse this transform, the caching mechanism will consider it to be different from the previous calls and recompute everything."
        )
        return generate_random_fingerprint()
    for key in sorted(transform_args):
        hasher.update(key)
        try:
            hasher.update(transform_args[key])
        except:  # noqa various errors might raise here from pickle or dill
            logger.warning(
                f"Parameter '{key}'={transform_args[key]} of the transform {transform} couldn't be hashed properly, a random hash was used instead. "
                "Make sure your transforms and parameters are serializable with pickle or dill for the dataset fingerprinting and caching to work. "
                "If you reuse this transform, the caching mechanism will consider it to be different from the previous calls and recompute everything."
            )
            return generate_random_fingerprint()
    return hasher.hexdigest()


def fingerprint_transform(inplace, use_kwargs=None, ignore_kwargs=None, fingerprint_names=None, randomized_function=None):
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
            if args:
                self: "Dataset" = args[0]
                args = args[1:]
            else:
                self: "Dataset" = kwargs.pop("self")
            kwargs_for_fingerprint = dict(kwargs)
            kwargs_for_fingerprint.update(zip(func.__code__.co_varnames, args))

            # keep the right kwargs to be hashed to generate the fingerprint

            if use_kwargs:
                kwargs_for_fingerprint = {k: v for k, v in kwargs_for_fingerprint.items() if k in use_kwargs}
            if ignore_kwargs:
                kwargs_for_fingerprint = {k: v for k, v in kwargs_for_fingerprint.items() if k not in ignore_kwargs}
            if randomized_function:  # randomized functions have `seed` and `generator` parameters
                if kwargs_for_fingerprint.get("seed") is None and kwargs_for_fingerprint.get("generator") is None:
                    kwargs_for_fingerprint["generator"] = np.random.default_rng(np.random.get_state()[1][0])

            # compute new_fingerprint and add it to the args of not in-place transforms
            transform = func.__module__ + "." + func.__qualname__
            if inplace:
                new_fingerprint = update_fingerprint(self._fingerprint, transform, kwargs_for_fingerprint)
                new_inplace_history_item = (func.__name__, deepcopy(args), deepcopy(kwargs))
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
                for inplace_hist_per_file in self._inplace_history:
                    inplace_hist_per_file["transforms"].append(new_inplace_history_item)

            return out

        wrapper._decorator_name_ = "fingerprint"
        return wrapper

    return _fingerprint
