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
import hashlib
import io
import itertools
import os
import sys
import uuid


from .file_utils import INCOMPLETE_SUFFIX

from shutil import disk_usage

import functools


# NOTE: When used on an instance method, the cache is shared across all
# instances and IS NOT per-instance.
# See
# https://stackoverflow.com/questions/14946264/python-lru-cache-decorator-per-instance
# For @property methods, use @memoized_property below.
memoize = functools.lru_cache


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

    _NAME_LIST = [("PiB", 2**50), ("TiB", 2**40), ("GiB",  2**30), ("MiB", 2**20),
                                ("KiB", 2**10)]

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
    except:  # pylint: disable=bare-except
        return False
    else:
        return True


@contextlib.contextmanager
def temporary_assignment(obj, attr, value):
    """Temporarily assign obj.attr to value."""
    original = getattr(obj, attr, None)
    setattr(obj, attr, value)
    yield
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
        return super(NonMutableDict, self). __setitem__(key, value)

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


def map_nested(function, data_struct, dict_only=False, map_tuple=False):
    """Apply a function recursively to each element of a nested data struct."""

    # Could add support for more exotic data_struct, like OrderedDict
    if isinstance(data_struct, dict):
        return {
                k: map_nested(function, v, dict_only, map_tuple)
                for k, v in data_struct.items()
        }
    elif not dict_only:
        types = [list]
        if map_tuple:
            types.append(tuple)
        if isinstance(data_struct, tuple(types)):
            mapped = [map_nested(function, v, dict_only, map_tuple)
                                for v in data_struct]
            if isinstance(data_struct, list):
                return mapped
            else:
                return tuple(mapped)
    # Singleton
    return function(data_struct)


def zip_nested(arg0, *args, **kwargs):
    """Zip data struct together and return a data struct with the same shape."""
    # Python 2 do not support kwargs only arguments
    dict_only = kwargs.pop("dict_only", False)
    assert not kwargs

    # Could add support for more exotic data_struct, like OrderedDict
    if isinstance(arg0, dict):
        return {
                k: zip_nested(*a, dict_only=dict_only) for k, a in zip_dict(arg0, *args)
        }
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
            flat_dict.update({
                    "{}/{}".format(k, k2): v2 for k2, v2 in flatten_nest_dict(v).items()
            })
        else:
            flat_dict[k] = v
    return flat_dict


def pack_as_nest_dict(flat_d, nest_d):
    """Pack a 1-lvl dict into a nested dict with same structure as `nest_d`."""
    nest_out_d = {}
    for k, v in nest_d.items():
        if isinstance(v, dict):
            v_flat = flatten_nest_dict(v)
            sub_d = {
                    k2: flat_d.pop("{}/{}".format(k, k2)) for k2, _ in v_flat.items()
            }
            # Recursivelly pack the dictionary
            nest_out_d[k] = pack_as_nest_dict(sub_d, v)
        else:
            nest_out_d[k] = flat_d.pop(k)
    if flat_d:  # At the end, flat_d should be empty
        raise ValueError(
                "Flat dict strucure do not match the nested dict. Extra keys: "
                "{}".format(list(flat_d.keys())))
    return nest_out_d


def nlp_dir():
    """Path to nlp directory."""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


@contextlib.contextmanager
def atomic_write(path, mode):
    """Writes to path atomically, by writing to temp file and renaming it."""
    tmp_path = "%s%s_%s" % (path, INCOMPLETE_SUFFIX, uuid.uuid4().hex)
    with open(tmp_path, mode) as file_:
        yield file_
    os.rename(tmp_path, path)


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


def read_checksum_digest(path, checksum_cls=hashlib.sha256):
    """Given a hash constructor, returns checksum digest and size of file."""
    checksum = checksum_cls()
    size = 0
    with open(path, "rb") as f:
        while True:
            block = f.read(io.DEFAULT_BUFFER_SIZE)
            size += len(block)
            if not block:
                break
            checksum.update(block)
    return checksum.hexdigest(), size


def reraise(prefix=None, suffix=None):
    """Reraise an exception with an additional message."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    prefix = prefix or ""
    suffix = "\n" + suffix if suffix else ""
    msg = prefix + str(exc_value) + suffix
    raise(exc_type, exc_type(msg), exc_traceback)


@contextlib.contextmanager
def try_reraise(*args, **kwargs):
    """Reraise an exception with an additional message."""
    try:
        yield
    except Exception:   # pylint: disable=broad-except
        reraise(*args, **kwargs)


def rgetattr(obj, attr, *args):
    """Get attr that handles dots in attr name."""
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split("."))


def has_sufficient_disk_space(needed_bytes, directory="."):
    try:
        free_bytes = disk_usage(os.path.abspath(directory)).free
    except OSError:
        return True
    return needed_bytes < free_bytes
