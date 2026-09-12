# Copyright 2023 The HuggingFace Team. All rights reserved.
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
"""Extends `dill` to support pickling more types and produce more consistent dumps."""

import copyreg
import math
import os
import sys
from enum import Enum, EnumMeta
from io import BytesIO
from pickle import PicklingError
from types import CodeType, FunctionType, MemberDescriptorType, MethodType

import dill
import numpy as np
import pyarrow as pa
from multiprocess.reduction import ForkingPickler
from packaging import version

from .. import config


class Pickler(dill.Pickler):
    dispatch = dill._dill.MetaCatchingDict(dill.Pickler.dispatch.copy())
    _legacy_no_dict_keys_sorting = False

    def save(self, obj, save_persistent_id=True):
        obj_type = type(obj)
        if obj_type not in self.dispatch:
            if "regex" in sys.modules:
                import regex  # type: ignore

                if obj_type is regex.Pattern:
                    pklregister(obj_type)(_save_regexPattern)
            if "spacy" in sys.modules:
                import spacy  # type: ignore

                if issubclass(obj_type, spacy.Language):
                    pklregister(obj_type)(_save_spacyLanguage)
            if "tiktoken" in sys.modules:
                import tiktoken  # type: ignore

                if obj_type is tiktoken.Encoding:
                    pklregister(obj_type)(_save_tiktokenEncoding)
            if "torch" in sys.modules:
                import torch  # type: ignore

                if issubclass(obj_type, torch.Tensor):
                    pklregister(obj_type)(_save_torchTensor)

                if obj_type is torch.Generator:
                    pklregister(obj_type)(_save_torchGenerator)

                # Unwrap `torch.compile`-ed modules
                if issubclass(obj_type, torch.nn.Module):
                    obj = getattr(obj, "_orig_mod", obj)
            if "transformers" in sys.modules:
                import transformers  # type: ignore

                if issubclass(obj_type, transformers.PreTrainedTokenizerBase):
                    pklregister(obj_type)(_save_transformersPreTrainedTokenizerBase)

        # Unwrap `torch.compile`-ed functions
        if obj_type is FunctionType:
            obj = getattr(obj, "_torchdynamo_orig_callable", obj)
        dill.Pickler.save(self, obj, save_persistent_id=save_persistent_id)

    def _batch_setitems(self, items, *args, **kwargs):
        # Ignore the order of keys in a dict
        try:
            # Faster, but fails for unorderable elements
            items = sorted(items)
        except Exception:  # TypeError, decimal.InvalidOperation, etc.
            from datasets.fingerprint import Hasher

            items = sorted(items, key=lambda x: Hasher.hash(x[0]))
        return super()._batch_setitems(items, *args, **kwargs)

    def memoize(self, obj):
        # Don't memoize strings since two identical strings can have different Python ids
        if type(obj) is not str:  # noqa: E721
            dill.Pickler.memoize(self, obj)


def pklregister(t):
    """Register a custom reducer for the type."""

    def proxy(func):
        Pickler.dispatch[t] = func
        return func

    return proxy


def _is_supported_dill_version():
    """Check if the current dill version is in the supported range."""
    return config.DILL_VERSION.release[:3] in [
        version.parse("0.3.6").release,
        version.parse("0.3.7").release,
        version.parse("0.3.8").release,
        version.parse("0.3.9").release,
        version.parse("0.4.0").release,
        version.parse("0.4.1").release,
    ]


def dump(obj, file):
    """Pickle an object to a file."""
    Pickler(file, recurse=True).dump(obj)


def dumps(obj):
    """Pickle an object to a string."""
    file = BytesIO()
    dump(obj, file)
    return file.getvalue()


if config.DILL_VERSION < version.parse("0.3.6"):

    def log(pickler, msg):
        dill._dill.log.info(msg)

elif _is_supported_dill_version():

    def log(pickler, msg):
        dill._dill.logger.trace(pickler, msg)


@pklregister(set)
def _save_set(pickler, obj):
    log(pickler, f"Se: {obj}")
    try:
        # Faster, but fails for unorderable elements
        args = (sorted(obj),)
    except Exception:  # TypeError, decimal.InvalidOperation, etc.
        from datasets.fingerprint import Hasher

        args = (sorted(obj, key=Hasher.hash),)

    pickler.save_reduce(set, args, obj=obj)
    log(pickler, "# Se")


def _create_enum(metaclass, name, bases, attributes, members, boundary):
    namespace = metaclass.__prepare__(name, bases)
    for key, value in attributes:
        namespace[key] = value
    for key, canonical_name, value in members:
        namespace[key] = value if key == canonical_name else namespace[canonical_name]
    return metaclass(name, bases, namespace, **boundary)


def _set_enum_state(enum_class, state):
    attributes, member_attributes, value_aliases, unhashable_values = state
    for name, value in attributes.items():
        setattr(enum_class, name, value)
    for name, (attributes, slots) in member_attributes.items():
        member = _get_enum_member(enum_class, name)
        member.__dict__.update(attributes)
        for base_index, key, value in slots:
            enum_class.__mro__[base_index].__dict__[key].__set__(member, value)
    for value, name in value_aliases:
        _get_enum_member(enum_class, name)._add_value_alias_(value)
    if unhashable_values is not None:
        enum_class._unhashable_values_, enum_class._unhashable_values_map_ = unhashable_values


def _enum_slots(enum_class):
    # Discover descriptors once for all members: an Enum's class dictionary
    # itself grows with its member count, even when there are no slots.
    return [
        (base_index, name, descriptor)
        for base_index, base in enumerate(enum_class.__mro__)
        for name, descriptor in base.__dict__.items()
        if isinstance(descriptor, MemberDescriptorType)
    ]


def _enum_slot_values(member, descriptors):
    slots = []
    for base_index, name, descriptor in descriptors:
        try:
            value = descriptor.__get__(member, type(member))
        except AttributeError:
            continue
        # A subclass can shadow a slot without replacing its storage.
        slots.append((base_index, name, value))
    return slots


def _enum_equal(left, right):
    # None means replay cannot be checked: identity need not survive loading,
    # and undefined/raising equality must not make a picklable value fail.
    if left is right:
        return True
    if isinstance(left, Enum) and isinstance(right, Enum):
        return type(left).__qualname__ == type(right).__qualname__ and left._name_ == right._name_
    if isinstance(left, MethodType) and isinstance(right, MethodType) and isinstance(left.__self__, Enum):
        # Explicit instance reducers can be bound to another Enum member.
        # Its reconstructed owner has a new identity, just like the class.
        return _enum_equal(left.__func__, right.__func__) is not False and _enum_equal(left.__self__, right.__self__)
    if type(left) is not type(right):
        # Local value classes are reconstructed too; still try their equality.
        if (type(left).__module__, type(left).__qualname__) != (type(right).__module__, type(right).__qualname__):
            return False
    try:
        if isinstance(left, float) and math.isnan(left):
            return math.isnan(right)
        if isinstance(left, (tuple, list)):
            return len(left) == len(right) and all(_enum_equal(a, b) is not False for a, b in zip(left, right))
        if isinstance(left, dict):
            if len(left) != len(right):
                return False
            for key, value in left.items():
                try:
                    other = right[key]
                except Exception:
                    # A reconstructed key may support neither identity lookup
                    # nor equality. Skip that check unless every key differs.
                    return None if any(_enum_equal(key, candidate) is not False for candidate in right) else False
                if _enum_equal(value, other) is False:
                    return False
            return True
        if isinstance(left, np.ndarray):
            try:
                return bool(np.array_equal(left, right, equal_nan=True))
            except TypeError:
                return bool(np.array_equal(left, right))
        equal = left.__eq__(right)
        if equal is NotImplemented:
            equal = right.__eq__(left)
        return bool(equal) if equal is not NotImplemented else None
    except Exception:
        return None


def _enum_conversion(convert, member):
    try:
        return convert(member)
    except Exception as error:
        return type(error), str(error)


def _enum_payload_equal(original, restored):
    member_type = type(original)._member_type_
    if member_type is object:
        return True
    if member_type is float:
        return _enum_equal(float.__float__(original), float.__float__(restored))
    try:
        equal = member_type.__eq__(original, restored)
        return bool(equal) if equal is not NotImplemented else None
    except Exception:
        return None


def _check_enum(original, restored):
    if (
        original.__name__ != restored.__name__
        or original.__qualname__ != restored.__qualname__
        or original.__module__ != restored.__module__
        or original.__dict__.keys() != restored.__dict__.keys()
        or list(original.__members__) != list(restored.__members__)
        or original._member_names_ != restored._member_names_
    ):
        raise ValueError("class attributes or member names changed")
    original_slots, restored_slots = _enum_slots(original), _enum_slots(restored)
    for name, member in original.__members__.items():
        other = restored[name]
        if (
            member._name_ != other._name_
            or other is not restored[member._name_]
            or _enum_equal(member._value_, other._value_) is False
            or _enum_payload_equal(member, other) is False
            or _enum_equal(_enum_conversion(int, member), _enum_conversion(int, other)) is False
            or _enum_equal(_enum_conversion(str, member), _enum_conversion(str, other)) is False
            or member.__dict__.keys() - {"_inverted_"} != other.__dict__.keys() - {"_inverted_"}
            or _enum_equal(_enum_slot_values(member, original_slots), _enum_slot_values(other, restored_slots))
            is False
            or any(
                _enum_equal(value, other.__dict__[key]) is False
                for key, value in member.__dict__.items()
                if key not in {"__objclass__", "_inverted_"}
            )
        ):
            raise ValueError(f"member {name} changed during reconstruction")

    # Explicit value aliases are recorded in _hashable_values_ (Python 3.13+).
    # Lookup caches, including Flag's negative keys, are only in the value map.
    def aliases(enum_class):
        return [
            (value, member._name_)
            for value, member in enum_class._value2member_map_.items()
            if member._name_ in enum_class.__members__
            and (
                value is member._value_
                or any(value is alias for alias in getattr(enum_class, "_hashable_values_", ()))
            )
        ]

    if (
        _enum_equal(aliases(original), aliases(restored)) is False
        or _enum_equal(
            getattr(original, "_unhashable_values_map_", {}), getattr(restored, "_unhashable_values_map_", {})
        )
        is False
    ):
        raise ValueError("value aliases changed during reconstruction")


def _validate_enum(pickler, obj):
    # Use the actual serializer, including its protocol and recursion settings.
    # Track all enums in the trial graph so nested classes are checked as well.
    buffer = BytesIO()
    trial = type(pickler)(buffer, protocol=pickler.proto, recurse=pickler._recurse, byref=pickler._byref)
    trial._enum_validation = []
    if hasattr(pickler, "dispatch_table"):
        trial.dispatch_table = pickler.dispatch_table.copy()
    # Only the default member reducer promises canonical identity. Explicit
    # instance contracts must not be invoked merely to validate the class.
    members = (
        [
            member
            for member in obj.__members__.values()
            if "__reduce_ex__" not in member.__dict__
            and getattr(member.__reduce_ex__, "__func__", None) is Enum.__reduce_ex__
        ]
        if trial.dispatch.get(obj) is _save_enum_member
        and obj.__reduce__ is object.__reduce__
        and obj not in getattr(trial, "dispatch_table", copyreg.dispatch_table)
        else []
    )
    trial.dump((obj, members, trial._enum_validation))
    rebuilt_class, rebuilt_members, restored = dill.loads(buffer.getvalue())
    for original, member in zip(members, rebuilt_members):
        if member is not _get_enum_member(rebuilt_class, original._name_):
            raise ValueError(f"captured member {original._name_} changed during reconstruction")
    for original, rebuilt in zip(trial._enum_validation, restored):
        _check_enum(original, rebuilt)


def _enum_method_references_class(value, enum_class):
    if isinstance(value, (staticmethod, classmethod)):
        value = value.__func__
    functions = (value.fget, value.fset, value.fdel) if isinstance(value, property) else (value,)
    return any(
        isinstance(function, FunctionType)
        and (
            any(reference is enum_class for reference in dill.detect.freevars(function).values())
            or any(
                function.__globals__.get(name) is enum_class for name in dill.detect.nestedglobals(function.__code__)
            )
        )
        for function in functions
    )


def _save_enum(pickler, obj):
    """Rebuild nonimportable Enums through their metaclass.

    Nonrecursive constructors rerun on load and during dump/hash validation;
    class-referencing hooks are restored after construction instead.
    """
    if dill._dill._locate_function(obj, pickler):
        return dill._dill.save_type(pickler, obj)

    label = f"{obj.__module__}.{obj.__qualname__}"
    active = pickler.__dict__.setdefault("_enum_in_progress", set())
    if id(obj) in active:
        raise PicklingError(f"Cannot faithfully pickle Enum {label}: recursive construction namespace")
    active.add(id(obj))
    try:
        if hasattr(pickler, "_enum_validation"):
            pickler._enum_validation.append(obj)
        else:
            _validate_enum(pickler, obj)

        log(pickler, f"En: {obj}")
        # EnumMeta transforms the class body. Rebuild the recoverable body, not
        # its generated member maps/descriptors. The saved constructor is the
        # original __new__; EnumMeta has replaced __new__ with value lookup.
        generated = set(obj.__members__) | {
            "__dict__",
            "__weakref__",
            "__new__",
            "__new_member__",
            "_member_names_",
            "_member_map_",
            "_value2member_map_",
            "_member_type_",
            "_new_member_",
            "_use_args_",
            "_value_repr_",
            "_unhashable_values_",
            "_hashable_values_",
            "_unhashable_values_map_",
            "_boundary_",
            "_flag_mask_",
            "_singles_mask_",
            "_all_bits_",
            "_inverted_",
        }
        attributes = {
            name: value
            for name, value in obj.__dict__.items()
            if name not in generated and not isinstance(value, MemberDescriptorType)
        }
        # Attributes attached after class creation must not become new members.
        # Methods that reference this class follow memoization in state, even
        # construction hooks: their saved member state replaces unsafe replay.
        # Keep other methods in the body: member constructors may call them.
        body = [
            (name, value)
            for name, value in attributes.items()
            if (name.startswith("_") or hasattr(value, "__get__")) and not _enum_method_references_class(value, obj)
        ]
        body.append(("__qualname__", obj.__qualname__))
        if "__new_member__" in obj.__dict__:
            new = obj.__dict__["__new_member__"]
            if _enum_method_references_class(new, obj):
                # Constructor closures can refer to the completed class without
                # using it during construction. Restore the hook and saved
                # member state after memoization instead of replaying it.
                attributes["__new_member__"] = new
            else:
                body.append(("__new__", new))
        members = [
            (name, member._name_, member._value_ if name == member._name_ else None)
            for name, member in obj.__members__.items()
        ]
        slots = _enum_slots(obj)
        member_attributes = {
            name: (
                {
                    key: value
                    for key, value in member.__dict__.items()
                    if key not in {"_value_", "_name_", "__objclass__", "_sort_order_", "_inverted_"}
                },
                _enum_slot_values(member, slots),
            )
            for name, member in obj.__members__.items()
            if name == member._name_
        }
        value_aliases = [
            (value, member._name_)
            for value, member in obj._value2member_map_.items()
            if member._name_ in obj.__members__
            and value is not member._value_
            and any(value is alias for alias in getattr(obj, "_hashable_values_", ()))
        ]
        # Python 3.13+ keeps unhashable aliases outside _value2member_map_.
        # Preserve both indexes directly, including ordinary unhashable values.
        unhashable_values = (
            (obj._unhashable_values_, obj._unhashable_values_map_) if hasattr(obj, "_unhashable_values_map_") else None
        )
        boundary = {"boundary": obj._boundary_} if hasattr(obj, "_boundary_") else {}
        # Ordered lists keep the construction order even in the fingerprint
        # pickler, which sorts dictionaries. Runtime state follows memoization.
        pickler.save_reduce(
            _create_enum,
            (type(obj), obj.__name__, obj.__bases__, body, members, boundary),
            state=(attributes, member_attributes, value_aliases, unhashable_values),
            state_setter=_set_enum_state,
            obj=obj,
        )
        log(pickler, "# En")
    except Exception as error:
        raise PicklingError(f"Cannot faithfully pickle Enum {label}: {type(error).__name__}: {error}") from error
    finally:
        active.remove(id(obj))


def _get_enum_member(enum_class, name):
    return type.__getattribute__(enum_class, "_member_map_")[name]


def _save_enum_member(pickler, obj):
    enum_class = type(obj)
    # Private worker registrations precede instance contracts, just as in
    # pickle. Resolve __reduce_ex__ on the member, which can override its class.
    reduce = getattr(pickler, "dispatch_table", copyreg.dispatch_table).get(enum_class)
    if reduce is not None:
        reduction = reduce(obj)
    else:
        reduce_ex = obj.__reduce_ex__
        if "__reduce_ex__" in obj.__dict__ or getattr(reduce_ex, "__func__", None) is not Enum.__reduce_ex__:
            reduction = reduce_ex(pickler.proto)
        elif enum_class.__reduce__ is not object.__reduce__:
            reduction = obj.__reduce__()
        else:
            # Value lookup cannot recover a separately serialized NaN. Use
            # canonical names; unnamed Flag combinations still use values.
            if obj._name_ in enum_class.__members__ and _get_enum_member(enum_class, obj._name_) is obj:
                pickler.save_reduce(_get_enum_member, (enum_class, obj._name_), obj=obj)
            else:
                pickler.save_reduce(enum_class, (obj._value_,), obj=obj)
            return

    if isinstance(reduction, str):
        pickler.save_global(obj, reduction)
    else:
        pickler.save_reduce(*reduction, obj=obj)


class _EnumDispatch(dill._dill.MetaCatchingDict):
    def __init__(self, fallback):
        super().__init__()
        self.fallback = fallback

    def __contains__(self, key):
        return super().__contains__(key) or key in self.fallback or issubclass(key, (EnumMeta, Enum))

    def __missing__(self, key):
        # Explicit registrations and member contracts take precedence over
        # Enum dispatch, including dill registrations made after this import.
        if issubclass(key, (EnumMeta, Enum)):
            if key in dill.Pickler.dispatch:
                return dill.Pickler.dispatch[key]
            if key in self.fallback:
                return self.fallback[key]
            if key in copyreg.dispatch_table:
                raise KeyError(key)
        if issubclass(key, EnumMeta):
            return _save_enum
        if issubclass(key, Enum):
            if key.__reduce_ex__ is not Enum.__reduce_ex__:
                raise KeyError(key)
            return _save_enum_member
        return self.fallback[key]


# Both serializers need subclass dispatch. Dataset.map uses multiprocess.Pool,
# whose queue/connection modules bind the shared ForkingPickler: the pool has no
# per-instance pickler, and even context.reducer changes a module global. Thus
# the current pool transport needs this process-wide assignment, which also
# affects other multiprocess users. test_map_enum_requires_worker_dispatch
# demonstrates that private fingerprint dispatch alone leaves map unpicklable.
# Keep dill's table as fallback so later third-party registrations still work.
Pickler.dispatch = _EnumDispatch(Pickler.dispatch)
ForkingPickler.dispatch = _EnumDispatch(ForkingPickler.dispatch)


@pklregister(pa.Table)
def _save_arrowTable(pickler, obj):
    # pyarrow's default pickle serializes each chunk's buffers separately, so the
    # pickled size (and therefore the fingerprint cost) scales with the number of
    # chunks rather than the amount of data. Serialize a chunk-count-independent
    # form instead: combine each column's chunks one at a time (bounded memory,
    # never a full-table copy) so identical data produces identical bytes
    # regardless of chunking. See
    # https://github.com/huggingface/datasets/issues/8327.
    def create_arrowTable(schema, columns):
        return pa.Table.from_arrays(columns, schema=schema)

    log(pickler, f"Ta: {obj}")
    args = (obj.schema, [column.combine_chunks() for column in obj.columns])
    pickler.save_reduce(create_arrowTable, args, obj=obj)
    log(pickler, "# Ta")


@pklregister(pa.ChunkedArray)
def _save_arrowChunkedArray(pickler, obj):
    # Same rationale as _save_arrowTable: hash a chunk-count-independent form by
    # combining the chunks into a single array.
    def create_arrowChunkedArray(array):
        return pa.chunked_array([array])

    log(pickler, f"Ca: {obj}")
    args = (obj.combine_chunks(),)
    pickler.save_reduce(create_arrowChunkedArray, args, obj=obj)
    log(pickler, "# Ca")


def _save_regexPattern(pickler, obj):
    import regex  # type: ignore

    log(pickler, f"Re: {obj}")
    args = (obj.pattern, obj.flags)
    pickler.save_reduce(regex.compile, args, obj=obj)
    log(pickler, "# Re")


def _save_tiktokenEncoding(pickler, obj):
    import tiktoken  # type: ignore

    log(pickler, f"Enc: {obj}")
    args = (obj.name, obj._pat_str, obj._mergeable_ranks, obj._special_tokens)
    pickler.save_reduce(tiktoken.Encoding, args, obj=obj)
    log(pickler, "# Enc")


def _save_torchTensor(pickler, obj):
    import torch  # type: ignore

    # `torch.from_numpy` is not picklable in `torch>=1.11.0`
    def create_torchTensor(np_array, dtype=None):
        tensor = torch.from_numpy(np_array)
        if dtype:
            tensor = tensor.type(dtype)
        return tensor

    log(pickler, f"To: {obj}")
    if obj.dtype == torch.bfloat16:
        args = (obj.detach().to(torch.float).cpu().numpy(), torch.bfloat16)
    else:
        args = (obj.detach().cpu().numpy(),)
    pickler.save_reduce(create_torchTensor, args, obj=obj)
    log(pickler, "# To")


def _save_torchGenerator(pickler, obj):
    import torch  # type: ignore

    def create_torchGenerator(state):
        generator = torch.Generator()
        generator.set_state(state)
        return generator

    log(pickler, f"Ge: {obj}")
    args = (obj.get_state(),)
    pickler.save_reduce(create_torchGenerator, args, obj=obj)
    log(pickler, "# Ge")


def _save_spacyLanguage(pickler, obj):
    import spacy  # type: ignore

    def create_spacyLanguage(config, bytes):
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        lang_inst = lang_cls.from_config(config)
        return lang_inst.from_bytes(bytes)

    log(pickler, f"Sp: {obj}")
    args = (obj.config, obj.to_bytes())
    pickler.save_reduce(create_spacyLanguage, args, obj=obj)
    log(pickler, "# Sp")


def _save_transformersPreTrainedTokenizerBase(pickler, obj):
    log(pickler, f"Tok: {obj}")
    # Ignore the `cache` attribute and make hashing stable.
    #
    # Some tokenizers backed by the `tokenizers` library mutate their internal `_tokenizer` state when called
    # (e.g. by enabling truncation/padding). This can change the serialized bytes across runs and make dataset
    # fingerprints unstable, which prevents `.map(load_from_cache_file=True)` from reusing cache files.
    #
    # For hashing/fingerprinting, we temporarily disable backend truncation/padding to avoid these runtime settings
    # affecting the fingerprint, then restore the original settings.
    state = obj.__dict__.copy()
    if "cache" in state and isinstance(state["cache"], dict):
        state["cache"] = {}
    if "deprecation_warnings" in state and isinstance(state["deprecation_warnings"], dict):
        state["deprecation_warnings"] = {}

    backend_tokenizer = obj.__dict__.get("_tokenizer")
    truncation = padding = None
    if (
        backend_tokenizer is not None
        and hasattr(backend_tokenizer, "truncation")
        and hasattr(backend_tokenizer, "padding")
    ):
        truncation = backend_tokenizer.truncation
        padding = backend_tokenizer.padding
        try:
            if truncation is not None and hasattr(backend_tokenizer, "no_truncation"):
                backend_tokenizer.no_truncation()
            if padding is not None and hasattr(backend_tokenizer, "no_padding"):
                backend_tokenizer.no_padding()
        except Exception:
            truncation = padding = None

    try:
        pickler.save_reduce(type(obj), (), state=state, obj=obj)
    finally:
        try:
            if backend_tokenizer is not None:
                if truncation is not None and hasattr(backend_tokenizer, "enable_truncation"):
                    backend_tokenizer.enable_truncation(**truncation)
                if padding is not None and hasattr(backend_tokenizer, "enable_padding"):
                    backend_tokenizer.enable_padding(**padding)
        except Exception:
            pass
    log(pickler, "# Tok")


if config.DILL_VERSION < version.parse("0.3.6"):

    @pklregister(CodeType)
    def _save_code(pickler, obj):
        """
        From dill._dill.save_code
        This is a modified version that removes the origin (filename + line no.)
        of functions created in notebooks or shells for example.
        """
        dill._dill.log.info(f"Co: {obj}")
        # The filename of a function is the .py file where it is defined.
        # Filenames of functions created in notebooks or shells start with '<'
        # ex: <ipython-input-13-9ed2afe61d25> for ipython, and <stdin> for shell
        # Filenames of functions created in ipykernel the filename
        # look like f"{tempdir}/ipykernel_{id1}/{id2}.py"
        # Moreover lambda functions have a special name: '<lambda>'
        # ex: (lambda x: x).__code__.co_name == "<lambda>"  # True
        #
        # For the hashing mechanism we ignore where the function has been defined
        # More specifically:
        # - we ignore the filename of special functions (filename starts with '<')
        # - we always ignore the line number
        # - we only use the base name of the file instead of the whole path,
        # to be robust in case a script is moved for example.
        #
        # Only those two lines are different from the original implementation:
        co_filename = (
            ""
            if obj.co_filename.startswith("<")
            or (
                len(obj.co_filename.split(os.path.sep)) > 1
                and obj.co_filename.split(os.path.sep)[-2].startswith("ipykernel_")
            )
            or obj.co_name == "<lambda>"
            else os.path.basename(obj.co_filename)
        )
        co_firstlineno = 1
        # The rest is the same as in the original dill implementation (with also a version check for 3.10)
        if dill._dill.PY3:
            if hasattr(obj, "co_posonlyargcount"):  # python 3.8 (16 args)
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
                    obj.co_linetable if sys.version_info >= (3, 10) else obj.co_lnotab,
                    obj.co_freevars,
                    obj.co_cellvars,
                )
            else:  # python 3.7 (15 args)
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

elif _is_supported_dill_version():
    # From: https://github.com/uqfoundation/dill/blob/dill-0.3.6/dill/_dill.py#L1104
    @pklregister(CodeType)
    def save_code(pickler, obj):
        dill._dill.logger.trace(pickler, "Co: %s", obj)

        ############################################################################################################
        # Modification here for huggingface/datasets
        # The filename of a function is the .py file where it is defined.
        # Filenames of functions created in notebooks or shells start with '<'
        # ex: <ipython-input-13-9ed2afe61d25> for ipython, and <stdin> for shell
        # Filenames of functions created in ipykernel the filename
        # look like f"{tempdir}/ipykernel_{id1}/{id2}.py"
        # Moreover lambda functions have a special name: '<lambda>'
        # ex: (lambda x: x).__code__.co_name == "<lambda>"  # True
        #
        # For the hashing mechanism we ignore where the function has been defined
        # More specifically:
        # - we ignore the filename of special functions (filename starts with '<')
        # - we always ignore the line number
        # - we only use the base name of the file instead of the whole path,
        # to be robust in case a script is moved for example.
        #
        # Only those two lines are different from the original implementation:
        co_filename = (
            ""
            if obj.co_filename.startswith("<")
            or (
                len(obj.co_filename.split(os.path.sep)) > 1
                and obj.co_filename.split(os.path.sep)[-2].startswith("ipykernel_")
            )
            or obj.co_name == "<lambda>"
            else os.path.basename(obj.co_filename)
        )
        co_firstlineno = 1
        # The rest is the same as in the original dill implementation, except for the replacements:
        # - obj.co_filename => co_filename
        # - obj.co_firstlineno => co_firstlineno
        # - obj.co_lnotab => obj.co_linetable for >= 3.10 since co_lnotab was deprecated
        ############################################################################################################

        if hasattr(obj, "co_endlinetable"):  # python 3.11a (20 args)
            args = (
                obj.co_linetable,  # Modification for huggingface/datasets ############################################
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
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                obj.co_qualname,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_linetable,
                obj.co_endlinetable,
                obj.co_columntable,
                obj.co_exceptiontable,
                obj.co_freevars,
                obj.co_cellvars,
            )
        elif hasattr(obj, "co_exceptiontable"):  # python 3.11 (18 args)
            args = (
                obj.co_linetable,  # Modification for huggingface/datasets #######################################
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
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                obj.co_qualname,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_linetable,
                obj.co_exceptiontable,
                obj.co_freevars,
                obj.co_cellvars,
            )
        elif hasattr(obj, "co_linetable"):  # python 3.10 (16 args)
            args = (
                obj.co_linetable,  # Modification for huggingface/datasets #######################################
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
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_linetable,
                obj.co_freevars,
                obj.co_cellvars,
            )
        elif hasattr(obj, "co_posonlyargcount"):  # python 3.8 (16 args)
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
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )
        else:  # python 3.7 (15 args)
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
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )

        pickler.save_reduce(dill._dill._create_code, args, obj=obj)
        dill._dill.logger.trace(pickler, "# Co")
        return
