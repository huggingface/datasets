# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
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
import pickle
import sys
import types
from io import BytesIO as StringIO
from multiprocessing import Pool, RLock
from shutil import disk_usage
from types import CodeType, FunctionType
from typing import Callable, ClassVar, Generic, Optional, Tuple, Union

import dill
import numpy as np
from tqdm import tqdm

from .logging import INFO, WARNING, get_logger, get_verbosity, set_verbosity_warning


try:  # pragma: no branch
    import typing_extensions as _typing_extensions
    from typing_extensions import Final, Literal
except ImportError:
    _typing_extensions = Literal = Final = None


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

    For example `size_str(1.5 * datasets.units.GiB) == "1.50 GiB"`.

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


def _single_map_nested(args):
    """Apply a function recursively to each element of a nested data struct."""
    function, data_struct, types, rank, disable_tqdm = args

    # Singleton first to spare some computation
    if not isinstance(data_struct, dict) and not isinstance(data_struct, types):
        return function(data_struct)

    # Reduce logging to keep things readable in multiprocessing with tqdm
    if rank is not None and get_verbosity() < WARNING:
        set_verbosity_warning()
    # Print at least one thing to fix tqdm in notebooks in multiprocessing
    # see https://github.com/tqdm/tqdm/issues/485#issuecomment-473338308
    if rank is not None and "notebook" in tqdm.__name__:
        print(" ", end="", flush=True)

    # Loop over single examples or batches and write to buffer/file if examples are to be updated
    pbar_iterable = data_struct.items() if isinstance(data_struct, dict) else data_struct
    pbar_desc = "#" + str(rank) if rank is not None else None
    pbar = tqdm(pbar_iterable, disable=disable_tqdm, position=rank, unit="obj", desc=pbar_desc)

    if isinstance(data_struct, dict):
        return {k: _single_map_nested((function, v, types, None, True)) for k, v in pbar}
    else:
        mapped = [_single_map_nested((function, v, types, None, True)) for v in pbar]
        if isinstance(data_struct, list):
            return mapped
        elif isinstance(data_struct, tuple):
            return tuple(mapped)
        else:
            return np.array(mapped)


def map_nested(
    function,
    data_struct,
    dict_only: bool = False,
    map_list: bool = True,
    map_tuple: bool = False,
    map_numpy: bool = False,
    num_proc: Optional[int] = None,
    types=None,
):
    """Apply a function recursively to each element of a nested data struct.
    If num_proc > 1 and the length of data_struct is longer than num_proc: use multi-processing
    """
    if types is None:
        types = []
        if not dict_only:
            if map_list:
                types.append(list)
            if map_tuple:
                types.append(tuple)
            if map_numpy:
                types.append(np.ndarray)
        types = tuple(types)

    # Singleton
    if not isinstance(data_struct, dict) and not isinstance(data_struct, types):
        return function(data_struct)

    disable_tqdm = bool(logger.getEffectiveLevel() > INFO)
    iterable = list(data_struct.values()) if isinstance(data_struct, dict) else data_struct

    if num_proc is None:
        num_proc = 1
    if num_proc <= 1 or len(iterable) <= num_proc:
        mapped = [
            _single_map_nested((function, obj, types, None, True)) for obj in tqdm(iterable, disable=disable_tqdm)
        ]
    else:
        split_kwds = []  # We organize the splits ourselve (contiguous splits)
        for index in range(num_proc):
            div = len(iterable) // num_proc
            mod = len(iterable) % num_proc
            start = div * index + min(index, mod)
            end = start + div + (1 if index < mod else 0)
            split_kwds.append((function, iterable[start:end], types, index, disable_tqdm))
        assert len(iterable) == sum(len(i[1]) for i in split_kwds), (
            f"Error dividing inputs iterable among processes. "
            f"Total number of objects {len(iterable)}, "
            f"length: {sum(len(i[1]) for i in split_kwds)}"
        )
        logger.info(
            "Spawning {} processes for {} objects in slices of {}".format(
                num_proc, len(iterable), [len(i[1]) for i in split_kwds]
            )
        )
        with Pool(num_proc, initargs=(RLock(),), initializer=tqdm.set_lock) as pool:
            mapped = pool.map(_single_map_nested, split_kwds)
        logger.info("Finished {} processes".format(num_proc))
        mapped = [obj for proc_res in mapped for obj in proc_res]
        logger.info("Unpacked {} objects".format(len(mapped)))

    if isinstance(data_struct, dict):
        return dict(zip(data_struct.keys(), mapped))
    else:
        if isinstance(data_struct, list):
            return mapped
        elif isinstance(data_struct, tuple):
            return tuple(mapped)
        else:
            return np.array(mapped)


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


def datasets_dir():
    """Path to datasets directory."""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class abstractclassmethod(classmethod):  # pylint: disable=invalid-name
    """Decorate a method to mark it as an abstract @classmethod."""

    __isabstractmethod__ = True

    def __init__(self, fn):
        fn.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(fn)


def get_datasets_path(relative_path):
    """Returns absolute path to file given path relative to datasets root."""
    path = os.path.join(datasets_dir(), relative_path)
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

    def save_global(self, obj, name=None):
        if sys.version_info[:2] < (3, 7) and _CloudPickleTypeHintFix._is_parametrized_type_hint(
            obj
        ):  # noqa  # pragma: no branch
            # Parametrized typing constructs in Python < 3.7 are not compatible
            # with type checks and ``isinstance`` semantics. For this reason,
            # it is easier to detect them using a duck-typing-based check
            # (``_is_parametrized_type_hint``) than to populate the Pickler's
            # dispatch with type-specific savers.
            _CloudPickleTypeHintFix._save_parametrized_type_hint(self, obj)
        else:
            dill.Pickler.save_global(self, obj, name=name)


def dump(obj, file):
    """pickle an object to a file"""
    Pickler(file, recurse=True).dump(obj)
    return


@contextlib.contextmanager
def _no_cache_fields(obj):
    try:
        import transformers as tr

        if (
            hasattr(tr, "PreTrainedTokenizerBase")
            and isinstance(obj, tr.PreTrainedTokenizerBase)
            and hasattr(obj, "cache")
            and isinstance(obj.cache, dict)
        ):
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


class _CloudPickleTypeHintFix:
    """
    Type hints can't be properly pickled in python < 3.7
    CloudPickle provided a way to make it work in older versions.
    This class provide utilities to fix pickling of type hints in older versions.
    from https://github.com/cloudpipe/cloudpickle/pull/318/files
    """

    def _is_parametrized_type_hint(obj):
        # This is very cheap but might generate false positives.
        origin = getattr(obj, "__origin__", None)  # typing Constructs
        values = getattr(obj, "__values__", None)  # typing_extensions.Literal
        type_ = getattr(obj, "__type__", None)  # typing_extensions.Final
        return origin is not None or values is not None or type_ is not None

    def _create_parametrized_type_hint(origin, args):
        return origin[args]

    def _save_parametrized_type_hint(pickler, obj):
        # The distorted type check sematic for typing construct becomes:
        # ``type(obj) is type(TypeHint)``, which means "obj is a
        # parametrized TypeHint"
        if type(obj) is type(Literal):  # pragma: no branch
            initargs = (Literal, obj.__values__)
        elif type(obj) is type(Final):  # pragma: no branch
            initargs = (Final, obj.__type__)
        elif type(obj) is type(ClassVar):
            initargs = (ClassVar, obj.__type__)
        elif type(obj) in [type(Union), type(Tuple), type(Generic)]:
            initargs = (obj.__origin__, obj.__args__)
        elif type(obj) is type(Callable):
            args = obj.__args__
            if args[0] is Ellipsis:
                initargs = (obj.__origin__, args)
            else:
                initargs = (obj.__origin__, (list(args[:-1]), args[-1]))
        else:  # pragma: no cover
            raise pickle.PicklingError("Datasets pickle Error: Unknown type {}".format(type(obj)))
        pickler.save_reduce(_CloudPickleTypeHintFix._create_parametrized_type_hint, initargs, obj=obj)


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


@pklregister(FunctionType)
def save_function(pickler, obj):
    """
    From dill._dill.save_function
    This is a modified version that make globs deterministic since the order of
    the keys in the output dictionary of globalvars can change.
    """
    if not dill._dill._locate_function(obj):
        dill._dill.log.info("F1: %s" % obj)
        if getattr(pickler, "_recurse", False):
            # recurse to get all globals referred to by obj
            globalvars = dill.detect.globalvars
            globs = globalvars(obj, recurse=True, builtin=True)
            if id(obj) in dill._dill.stack:
                globs = obj.__globals__ if dill._dill.PY3 else obj.func_globals
        else:
            globs = obj.__globals__ if dill._dill.PY3 else obj.func_globals
        # globs is a dictionary with keys = var names (str) and values = python objects
        # however the dictionary is not always loaded in the same order
        # therefore we have to sort the keys to make deterministic.
        # This is important to make `dump` deterministic.
        # Only this line is different from the original implementation:
        globs = {k: globs[k] for k in sorted(globs.keys())}
        # The rest is the same as in the original dill implementation
        _byref = getattr(pickler, "_byref", None)
        _recurse = getattr(pickler, "_recurse", None)
        _memo = (id(obj) in dill._dill.stack) and (_recurse is not None)
        dill._dill.stack[id(obj)] = len(dill._dill.stack), obj
        if dill._dill.PY3:
            _super = ("super" in getattr(obj.__code__, "co_names", ())) and (_byref is not None)
            if _super:
                pickler._byref = True
            if _memo:
                pickler._recurse = False
            fkwdefaults = getattr(obj, "__kwdefaults__", None)
            pickler.save_reduce(
                dill._dill._create_function,
                (obj.__code__, globs, obj.__name__, obj.__defaults__, obj.__closure__, obj.__dict__, fkwdefaults),
                obj=obj,
            )
        else:
            _super = (
                ("super" in getattr(obj.func_code, "co_names", ()))
                and (_byref is not None)
                and getattr(pickler, "_recurse", False)
            )
            if _super:
                pickler._byref = True
            if _memo:
                pickler._recurse = False
            pickler.save_reduce(
                dill._dill._create_function,
                (obj.func_code, globs, obj.func_name, obj.func_defaults, obj.func_closure, obj.__dict__),
                obj=obj,
            )
        if _super:
            pickler._byref = _byref
        if _memo:
            pickler._recurse = _recurse
        if (
            dill._dill.OLDER
            and not _byref
            and (_super or (not _super and _memo) or (not _super and not _memo and _recurse))
        ):
            pickler.clear_memo()
        dill._dill.log.info("# F1")
    else:
        dill._dill.log.info("F2: %s" % obj)
        name = getattr(obj, "__qualname__", getattr(obj, "__name__", None))
        dill._dill.StockPickler.save_global(pickler, obj, name=name)
        dill._dill.log.info("# F2")
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
