# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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
"""Some python utils function and classes.

"""

import contextlib
import functools
import itertools
import os
import types
from functools import partial
from io import BytesIO as StringIO
from multiprocessing import Pool, RLock
from shutil import disk_usage
from types import CodeType

import dill
import numpy as np
from tqdm import tqdm

from .logging import INFO, get_logger


# NOTE: When used on an instance method, the cache is shared across all
# instances and IS NOT per-instance.
# See
# https://stackoverflow.com/questions/14946264/python-lru-cache-decorator-per-instance
# For @property methods, use @memoized_property below.
memoize = functools.lru_cache

logger = get_logger(__name__)


def size_str(size_in_bytes):
    """Returns a human readable size string.

    If size_in_bytes is None, then returns "Unknown size".

    For example `size_str(1.5 * nlp.units.GiB) == "1.50 GiB"`.

    Args:
        size_in_bytes: `int` or `None`, the size, in bytes, that we want to
            format as a human-readable size string.
    """
    if not size_in_bytes:
        return "Unknown size"

    _NAME_LIST = [("PiB", 2 ** 50), ("TiB", 2 ** 40), ("GiB", 2 ** 30), ("MiB", 2 ** 20), ("KiB", 2 ** 10)]

    size_in_bytes = float(size_in_bytes)
    for (name, size_bytes) in _NAME_LIST:
        value = size_in_bytes / size_bytes
        if value >= 1.0:
            return "{:.2f} {}".format(value, name)
    return "{} {}".format(int(size_in_bytes), "bytes")


def is_notebook():
    """Returns True if running in a notebook (Colab, Jupyter) environement."""
    # Inspired from the tfdm autonotebook code
    try:
        from IPython import get_ipython  # pylint: disable=import-outside-toplevel,g-import-not-at-top

        if "IPKernelApp" not in get_ipython().config:
            return False  # Run in a IPython terminal
    except:  # noqa: E722
        return False
    else:
        return True


@contextlib.contextmanager
def temporary_assignment(obj, attr, value):
    """Temporarily assign obj.attr to value."""
    original = getattr(obj, attr, None)
    setattr(obj, attr, value)
    try:
        yield
    finally:
        setattr(obj, attr, original)


def zip_dict(*dicts):
    """Iterate over items of dictionaries grouped by their keys."""
    for key in set(itertools.chain(*dicts)):  # set merge all keys
        # Will raise KeyError if the dict don't have the same keys
        yield key, tuple(d[key] for d in dicts)


class NonMutableDict(dict):
    """Dict where keys can only be added but not modified.

    Will raise an error if the user try to overwrite one key. The error message
    can be customized during construction. It will be formatted using {key} for
    the overwritten key.
    """

    def __init__(self, *args, **kwargs):
        self._error_msg = kwargs.pop(
            "error_msg",
            "Try to overwrite existing key: {key}",
        )
        if kwargs:
            raise ValueError("NonMutableDict cannot be initialized with kwargs.")
        super(NonMutableDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in self:
            raise ValueError(self._error_msg.format(key=key))
        return super(NonMutableDict, self).__setitem__(key, value)

    def update(self, other):
        if any(k in self for k in other):
            raise ValueError(self._error_msg.format(key=set(self) & set(other)))
        return super(NonMutableDict, self).update(other)


class classproperty(property):  # pylint: disable=invalid-name
    """Descriptor to be used as decorator for @classmethods."""

    def __get__(self, obj, objtype=None):
        return self.fget.__get__(None, objtype)()


class memoized_property(property):  # pylint: disable=invalid-name
    """Descriptor that mimics @property but caches output in member variable."""

    def __get__(self, obj, objtype=None):
        # See https://docs.python.org/3/howto/descriptor.html#properties
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        attr = "__cached_" + self.fget.__name__
        cached = getattr(obj, attr, None)
        if cached is None:
            cached = self.fget(obj)
            setattr(obj, attr, cached)
        return cached


def _parallel_map_nested(
    args, dict_only=False, map_list=True, map_tuple=False, map_numpy=False, disable_tqdm=True
):
    """Apply a function recursively to each element of a nested data struct."""
    function, data_struct = args
    if isinstance(data_struct, dict):
        return {
            k: _parallel_map_nested(
                (function, v), dict_only=dict_only, map_list=map_list, map_tuple=map_tuple, map_numpy=map_numpy
            )
            for k, v in tqdm(data_struct.items(), disable=disable_tqdm)
        }
    elif not dict_only:
        types = []
        if map_list:
            types.append(list)
        if map_tuple:
            types.append(tuple)
        if map_numpy:
            types.append(np.ndarray)
        if isinstance(data_struct, tuple(types)):
            mapped = [
                _parallel_map_nested(
                    (function, v), dict_only=dict_only, map_list=map_list, map_tuple=map_tuple, map_numpy=map_numpy
                )
                for v in tqdm(data_struct, disable=disable_tqdm)
            ]
            if isinstance(data_struct, list):
                return mapped
            elif isinstance(data_struct, tuple):
                return tuple(mapped)
            else:
                return np.array(mapped)
    # Singleton
    return function(data_struct)


def map_nested(
    function,
    data_struct,
    dict_only: bool = False,
    map_list: bool = True,
    map_tuple: bool = False,
    map_numpy: bool = False,
    num_proc: int = 1,
):
    """Apply a function recursively to each element of a nested data struct."""
    disable_tqdm = bool(logger.getEffectiveLevel() > INFO)
    if num_proc <= 1:
        map_func = partial(
            map_nested,
            dict_only=dict_only,
            map_list=map_list,
            map_tuple=map_tuple,
            map_numpy=map_numpy,
            num_proc=num_proc,
        )
    else:
        map_func = partial(
            _parallel_map_nested,
            dict_only=dict_only,
            map_list=map_list,
            map_tuple=map_tuple,
            map_numpy=map_numpy,
            disable_tqdm=disable_tqdm,
        )

    # Could add support for more exotic data_struct, like OrderedDict
    if isinstance(data_struct, dict):
        if num_proc <= 1:
            return {k: map_func(function, v) for k, v in tqdm(data_struct.items(), disable=disable_tqdm)}
        else:
            kwds = [(function, data_struct) for sub_struct in data_struct.values()]
            with Pool(num_proc, initargs=(RLock(),), initializer=tqdm.set_lock) as pool:
                results = pool.map(map_func, kwds)
            return {k: v for k, v in zip(data_struct.keys(), results)}

    elif not dict_only:
        types = []
        if map_list:
            types.append(list)
        if map_tuple:
            types.append(tuple)
        if map_numpy:
            types.append(np.ndarray)
        if isinstance(data_struct, tuple(types)):
            if num_proc <= 1:
                mapped = [map_func(function, v) for v in tqdm(data_struct, disable=disable_tqdm)]
            else:
                kwds = [(function, data_struct) for sub_struct in data_struct]
                with Pool(num_proc, initargs=(RLock(),), initializer=tqdm.set_lock) as pool:
                    results = pool.map(map_func, kwds)
            if isinstance(data_struct, list):
                return mapped
            elif isinstance(data_struct, tuple):
                return tuple(mapped)
            else:
                return np.array(mapped)
    # Singleton
    return function(data_struct)


def zip_nested(arg0, *args, **kwargs):
    """Zip data struct together and return a data struct with the same shape."""
    # Python 2 do not support kwargs only arguments
    dict_only = kwargs.pop("dict_only", False)
    assert not kwargs

    # Could add support for more exotic data_struct, like OrderedDict
    if isinstance(arg0, dict):
        return {k: zip_nested(*a, dict_only=dict_only) for k, a in zip_dict(arg0, *args)}
    elif not dict_only:
        if isinstance(arg0, list):
            return [zip_nested(*a, dict_only=dict_only) for a in zip(arg0, *args)]
    # Singleton
    return (arg0,) + args


def flatten_nest_dict(d):
    """Return the dict with all nested keys flattened joined with '/'."""
    # Use NonMutableDict to ensure there is no collision between features keys
    flat_dict = NonMutableDict()
    for k, v in d.items():
        if isinstance(v, dict):
            flat_dict.update({"{}/{}".format(k, k2): v2 for k2, v2 in flatten_nest_dict(v).items()})
        else:
            flat_dict[k] = v
    return flat_dict


def flatten_nested(data_struct):
    """Flatten data struct of obj or `list`/`dict` of obj"""
    if isinstance(data_struct, dict):
        data_struct = list(flatten_nest_dict(data_struct).values())
        if data_struct and isinstance(data_struct[0], (list, tuple)):
            data_struct = [x for sublist in data_struct for x in sublist]
    if isinstance(data_struct, (list, tuple)):
        return data_struct
    # Singleton
    return [data_struct]


def nlp_dir():
    """Path to nlp directory."""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class abstractclassmethod(classmethod):  # pylint: disable=invalid-name
    """Decorate a method to mark it as an abstract @classmethod."""

    __isabstractmethod__ = True

    def __init__(self, fn):
        fn.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(fn)


def get_nlp_path(relative_path):
    """Returns absolute path to file given path relative to nlp root."""
    path = os.path.join(nlp_dir(), relative_path)
    return path


def has_sufficient_disk_space(needed_bytes, directory="."):
    try:
        free_bytes = disk_usage(os.path.abspath(directory)).free
    except OSError:
        return True
    return needed_bytes < free_bytes


class Pickler(dill.Pickler):
    """Same Pickler as the one from dill, but improved for notebooks and shells"""

    dispatch = dill._dill.MetaCatchingDict(dill.Pickler.dispatch.copy())


def dump(obj, file):
    """pickle an object to a file"""
    Pickler(file, recurse=True).dump(obj)
    return


@contextlib.contextmanager
def _no_cache_fields(obj):
    try:
        import transformers as tr

        if isinstance(obj, tr.PreTrainedTokenizerBase) and hasattr(obj, "cache") and isinstance(obj.cache, dict):
            with temporary_assignment(obj, "cache", {}):
                yield
        else:
            yield

    except ImportError:
        yield


def dumps(obj):
    """pickle an object to a string"""
    file = StringIO()
    with _no_cache_fields(obj):
        dump(obj, file)
    return file.getvalue()


def pklregister(t):
    def proxy(func):
        Pickler.dispatch[t] = func
        return func

    return proxy


@pklregister(CodeType)
def _save_code(pickler, obj):
    """
    From dill._dill.save_code
    This is a modified version that removes the origin (filename + line no.)
    of functions created in notebooks or shells for example.
    """
    dill._dill.log.info("Co: %s" % obj)
    # Filenames of functions created in notebooks or shells start with '<'
    # ex: <ipython-input-13-9ed2afe61d25> for ipython, and <stdin> for shell
    # Moreover lambda functions have a special name: '<lambda>'
    # ex: (lambda x: x).__code__.co_name == "<lambda>"  # True
    # Only those two lines are different from the original implementation:
    co_filename = "" if obj.co_filename.startswith("<") or obj.co_name == "<lambda>" else obj.co_filename
    co_firstlineno = 1 if obj.co_filename.startswith("<") or obj.co_name == "<lambda>" else obj.co_firstlineno
    # The rest is the same as in the original dill implementation
    if dill._dill.PY3:
        if hasattr(obj, "co_posonlyargcount"):
            args = (
                obj.co_argcount,
                obj.co_posonlyargcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,
                obj.co_name,
                co_firstlineno,
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )
        else:
            args = (
                obj.co_argcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,
                obj.co_name,
                co_firstlineno,
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )
    else:
        args = (
            obj.co_argcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            obj.co_names,
            obj.co_varnames,
            co_filename,
            obj.co_name,
            co_firstlineno,
            obj.co_lnotab,
            obj.co_freevars,
            obj.co_cellvars,
        )
    pickler.save_reduce(CodeType, args, obj=obj)
    dill._dill.log.info("# Co")
    return


def copyfunc(func):
    return types.FunctionType(func.__code__, func.__globals__, func.__name__, func.__defaults__, func.__closure__)


try:
    import regex

    @pklregister(type(regex.Regex("", 0)))
    def _save_regex(pickler, obj):
        dill._dill.log.info("Re: %s" % obj)
        args = (
            obj.pattern,
            obj.flags,
        )
        pickler.save_reduce(regex.compile, args, obj=obj)
        dill._dill.log.info("# Re")
        return


except ImportError:
    pass
