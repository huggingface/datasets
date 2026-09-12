import copyreg
import enum
import inspect
import json
import math
import os
import pickle
import subprocess
import sys
import threading
import warnings
from contextlib import nullcontext
from datetime import date
from functools import partial
from pathlib import Path
from tempfile import gettempdir
from textwrap import dedent
from types import FunctionType
from unittest import TestCase
from unittest.mock import patch

import dill
import numpy as np
import pytest
from multiprocess import Pool
from multiprocess.reduction import ForkingPickler

import datasets
from datasets import config
from datasets.fingerprint import Hasher, fingerprint_transform
from datasets.table import InMemoryTable
from datasets.utils._dill import Pickler, dumps

from .utils import (
    require_not_windows,
    require_numpy1_on_windows,
    require_regex,
    require_spacy,
    require_tiktoken,
    require_torch,
    require_torch_compile,
    require_transformers,
)


class Foo:
    def __init__(self, foo):
        self.foo = foo

    def __call__(self):
        return self.foo


class ImportableEnumBase(enum.Enum):
    pass


class ImportableEnum(ImportableEnumBase):
    first = "first"


class EnumValueWithUndefinedEquality:
    def __init__(self, equality):
        self.equality = equality
        self.code = 7

    def __eq__(self, other):
        if self.equality == "raises":
            raise ValueError("equality is undefined")
        return NotImplemented

    def __hash__(self):
        return 7


class BlockingEnumValue(int):
    def __reduce__(self):
        entered, release = self.events[int(self)]
        entered.set()
        if not release.wait(10):
            raise RuntimeError("Enum dump release timed out")
        return type(self), (int(self),)


ENUM_TYPES = [enum.Enum, enum.IntEnum, enum.Flag, enum.IntFlag]
if hasattr(enum, "StrEnum"):
    ENUM_TYPES.append(enum.StrEnum)


@pytest.mark.parametrize("enum_type", ENUM_TYPES)
def test_dill_local_enum_roundtrip(enum_type):
    class Choice(enum_type):
        second = enum.auto()
        first = enum.auto()
        alias = second

        def label(self):
            return self.name

    member = Choice.second

    def transform():
        return Choice, member

    restored_class, restored_member = dill.loads(dumps(transform))()
    assert list(restored_class.__members__) == ["second", "first", "alias"]
    assert restored_class.__bases__ == Choice.__bases__
    assert restored_class.__qualname__ == Choice.__qualname__
    assert restored_member is restored_class.second
    assert restored_class.alias is restored_class.second
    assert restored_member.value == member.value
    assert restored_member.label() == "second"


def test_dill_importable_enum_roundtrip():
    assert dill.loads(dumps(ImportableEnum)) is ImportableEnum
    assert dill.loads(ForkingPickler.dumps(ImportableEnum.first)) is ImportableEnum.first


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_concurrent_dumps_preserve_warning_filters(serialize, monkeypatch):
    events = {n: (threading.Event(), threading.Event()) for n in (1, 2)}
    monkeypatch.setattr(BlockingEnumValue, "events", events, raising=False)

    class Choice1(enum.Enum):
        A = BlockingEnumValue(1)

    class Choice2(enum.Enum):
        A = BlockingEnumValue(2)

    errors = []

    def worker(choice):
        try:
            serialize(choice)
        except BaseException as error:
            errors.append(error)

    threads = [threading.Thread(target=worker, args=(choice,)) for choice in (Choice1, Choice2)]
    # The test owns this context; worker dumps must leave its filters alone.
    pickling_warning = getattr(dill, "PicklingWarning", UserWarning)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pickling_warning)
        filters = warnings.filters
        before = list(filters)
        try:
            for n, thread in enumerate(threads, 1):
                thread.start()
                assert events[n][0].wait(10)
            during = list(warnings.filters)
            # Exit in entry order to expose overlapping catch_warnings contexts.
            for n, thread in enumerate(threads, 1):
                events[n][1].set()
                thread.join(20)
                assert not thread.is_alive()
            assert not errors
            assert warnings.filters is filters
            assert before == during == warnings.filters
            warnings.warn("After both Enum dumps finished", pickling_warning)
        finally:
            for _, release in events.values():
                release.set()
            for thread in threads:
                if thread.ident is not None:
                    thread.join(20)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("importable", [False, True])
@pytest.mark.parametrize("raises", [False, True])
def test_dill_enum_instance_reduce_ex(serialize, importable, raises, monkeypatch):
    class Choice(enum.Enum):
        A = 1

    choice = ImportableEnum if importable else Choice
    member = next(iter(choice))

    def reduce_member(protocol):
        if raises:
            raise TypeError("custom instance rejected")
        return str, ("custom-instance",)

    monkeypatch.setitem(member.__dict__, "__reduce_ex__", reduce_member)
    # Serializing the class alone must not invoke a member's explicit contract.
    restored = dill.loads(serialize(choice))
    assert list(restored.__members__) == list(choice.__members__)
    if raises:
        with pytest.raises(TypeError, match="custom instance rejected"):
            serialize(member)
    else:
        assert dill.loads(serialize(member)) == "custom-instance"
        restored, result = dill.loads(serialize((choice, member)))
        assert result == "custom-instance"


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("importable", [False, True])
def test_dill_enum_instance_reduce_ex_bound_to_another_member(serialize, importable, monkeypatch):
    choice = enum.Enum("InstanceReducerChoice", {"A": 1, "B": 2})
    if importable:
        monkeypatch.setitem(globals(), "InstanceReducerChoice", choice)
    choice.A.__reduce_ex__ = choice.B.__reduce_ex__
    if importable:
        assert pickle.loads(pickle.dumps(choice.A)) is choice.B
    restored, member = dill.loads(serialize((choice, choice.A)))
    assert member is restored.B
    assert restored.A.__reduce_ex__.__self__ is restored.B


@pytest.mark.skipif(sys.version_info < (3, 13), reason="Value aliases require Python 3.13+")
@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("alias", [["alias"], {"alias": 1}])
def test_dill_enum_unhashable_value_alias(serialize, alias):
    class Choice(enum.Enum):
        A = 1
        B = ["primary"]

    Choice.A._add_value_alias_(alias)
    assert Choice(alias) is Choice.A
    restored = dill.loads(serialize(Choice))
    assert restored(alias) is restored.A
    assert restored(["primary"]) is restored.B
    assert restored._unhashable_values_map_ == Choice._unhashable_values_map_


@pytest.mark.skipif(sys.version_info < (3, 13), reason="Value aliases require Python 3.13+")
def test_dill_enum_validation_detects_lost_unhashable_value_alias():
    from datasets.utils._dill import _check_enum

    original = enum.Enum("Choice", {"A": 1})
    restored = enum.Enum("Choice", {"A": 1})
    original.A._add_value_alias_(["alias"])
    with pytest.raises(ValueError, match="value aliases changed"):
        _check_enum(original, restored)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("size", [1000, 4000])
def test_dill_large_enum_dump_scales_linearly(serialize, size):
    from datasets.utils._dill import _enum_slots

    choice = enum.Enum("Choice", {f"V{i}": i for i in range(size)})
    # Discovery scans a class dictionary that grows with the member count.
    # Repeating it for every member makes serialization quadratic.
    with patch("datasets.utils._dill._enum_slots", wraps=_enum_slots) as discover_slots:
        assert serialize(choice)
    # One scan for the validation dump, two for its original/rebuilt comparison,
    # and one for the final dump, independent of the number of members.
    assert discover_slots.call_count == 4


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("accessor", ["name", "value"])
def test_dill_enum_raising_public_accessor(serialize, accessor):
    class Choice(enum.Enum):
        A = 1

        @property
        def code(self):
            return self._value_

    def unavailable(self):
        raise AttributeError("use code instead")

    setattr(Choice, accessor, property(unavailable))
    assert Hasher.hash(Choice)
    restored = dill.loads(serialize(Choice))
    assert restored.A.code == 1
    assert restored.A._name_ == "A"
    with pytest.raises(AttributeError, match="use code instead"):
        getattr(restored.A, accessor)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("shared_value", [False, True])
def test_dill_enum_alias_with_nan_value(serialize, shared_value):
    class Choice(enum.Enum):
        first = float("nan")
        alias = first if shared_value else float("nan")

    restored = dill.loads(serialize(Choice))
    # Before Python 3.11, even a shared NaN creates two distinct members.
    assert (restored.alias is restored.first) == (Choice.alias is Choice.first)
    assert (restored.alias.value is restored.first.value) == shared_value
    assert restored._member_names_ == Choice._member_names_
    for name in Choice.__members__:
        assert restored(restored[name].value) is restored[Choice(Choice[name].value).name]


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("hook", ["__init__", "__new__", "_generate_next_value_"])
def test_dill_enum_constructor_references_class(serialize, hook):
    if hook == "__init__":

        class Choice(enum.Enum):
            A = 1

            def __init__(self, value):
                self.get = lambda: Choice

    elif hook == "__new__":

        class Choice(enum.Enum):
            A = 1

            def __new__(cls, value):
                member = object.__new__(cls)
                member._value_ = value
                member.get = lambda: Choice
                return member

    else:

        class Choice(enum.Enum):
            def _generate_next_value_(name, start, count, last_values):
                return count + len((lambda: Choice,))

            A = enum.auto()

    restored, member = dill.loads(serialize((Choice, Choice.A)))
    assert member is restored.A
    assert member.value == 1
    if hook == "_generate_next_value_":
        assert restored._generate_next_value_("B", 1, 1, [1]) == 2
    else:
        assert member.get() is restored


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_numpy_value(serialize):
    class Choice(enum.Enum):
        A = np.array([1, 2, 3])

    restored, member = dill.loads(serialize((Choice, Choice.A)))
    assert member is restored.A
    np.testing.assert_array_equal(member.value, [1, 2, 3])


def test_map_enum_numpy_value():
    class Choice(enum.Enum):
        A = np.array([1, 2, 3])

    def transform(row):
        return {"value": int(Choice.A.value.sum())}

    result = datasets.Dataset.from_dict({"text": ["one", "two"]}).map(transform, num_proc=2)
    assert result["value"] == [6, 6]


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("equality", ["not_implemented", "raises"])
@pytest.mark.parametrize("importable", [False, True])
@pytest.mark.parametrize("as_key", [False, True])
def test_dill_enum_undefined_value_equality(serialize, equality, importable, as_key):
    if not importable and config.DILL_VERSION.release < (0, 3, 5):
        pytest.skip("Local non-Enum classes require dill>=0.3.5")

    class Value:
        def __init__(self):
            self.code = 7

        def __eq__(self, other):
            if equality == "raises":
                raise ValueError("equality is undefined")
            return NotImplemented

        def __hash__(self):
            return 7

    value = EnumValueWithUndefinedEquality(equality) if importable else Value()

    class Choice(enum.Enum):
        A = {value: 42} if as_key else value

    restored, member = dill.loads(serialize((Choice, Choice.A)))
    assert member is restored.A
    if as_key:
        assert list(member.value.values()) == [42]
        assert next(iter(member.value)).code == 7
    else:
        assert member.value.code == 7


@pytest.mark.skipif(config.DILL_VERSION.release < (0, 3, 5), reason="Local non-Enum classes require dill>=0.3.5")
@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_defined_local_value_equality(serialize):
    class Value:
        def __init__(self, code):
            self.code = code

        def __eq__(self, other):
            return self.code == other.code

        def __reduce__(self):
            return type(self), (99,)

    class Choice(enum.Enum):
        A = Value(7)

    with pytest.raises(pickle.PicklingError, match="member A changed during reconstruction"):
        serialize(Choice)


def test_map_enum_requires_worker_dispatch(monkeypatch):
    class Choice(enum.Enum):
        A = 1

    def transform(row):
        return {"value": Choice.A.value}

    dataset = datasets.Dataset.from_dict({"text": ["one", "two"]})
    assert dataset.map(transform, num_proc=2, load_from_cache_file=False)["value"] == [1, 1]
    # Hashing still succeeds with datasets' private pickler. The real pool
    # task, however, is serialized by multiprocess.connection.ForkingPickler.
    # Full-suite collection also imports src.datasets via test_nifti, so the
    # shared table can have multiple Enum wrappers. Remove every wrapper.
    fallback = ForkingPickler.dispatch
    while hasattr(fallback, "fallback"):
        fallback = fallback.fallback
    monkeypatch.setattr(ForkingPickler, "dispatch", fallback)
    assert Hasher.hash(transform)
    # Older dill raises directly, without emitting a PicklingWarning first.
    warning = pytest.warns(dill.PicklingWarning) if hasattr(dill, "PicklingWarning") else nullcontext()
    with warning, pytest.raises(pickle.PicklingError, match="Can't pickle.*Choice"):
        dataset.map(transform, num_proc=2, load_from_cache_file=False)


def test_dill_main_guard_enum_spawn(tmp_path):
    script = tmp_path / "spawn_enum.py"
    script.write_text(
        dedent(
            """
            import enum
            import dill
            import multiprocess
            from datasets.utils._dill import dumps

            def child(payload, queue):
                import dill

                assert "Label" not in globals()
                restored, member = dill.loads(payload)
                assert member is restored.A
                assert restored.A.value == "a"
                queue.put([m.name for m in restored])

            if __name__ == "__main__":
                class Label(str, enum.Enum):
                    A = "a"
                    B = "b"

                ctx = multiprocess.get_context("spawn")
                queue = ctx.Queue()
                process = ctx.Process(target=child, args=(dumps((Label, Label.A)), queue))
                process.start()
                try:
                    assert queue.get(timeout=60) == ["A", "B"]
                    process.join(timeout=60)
                    assert process.exitcode == 0
                finally:
                    if process.is_alive():
                        process.terminate()
                        process.join(timeout=10)
                    queue.close()
                    queue.join_thread()
            """
        )
    )
    subprocess.run([sys.executable, str(script)], check=True, timeout=150)


def _make_adversarial_enum(case):
    if case == "constructor":

        class Choice(int, enum.Enum):
            def __new__(cls, code):
                member = int.__new__(cls, code * 10)
                member._value_ = code
                return member

            A = 1

    elif case == "slots":

        class Choice(enum.Enum):
            __slots__ = ("label",)

            def __init__(self, value):
                self.label = "initial"

            A = 1

        Choice.A.label = "updated"
    elif case == "value_alias":

        class Choice(enum.Enum):
            A = 1

        Choice.A._add_value_alias_(2)
    elif case == "name":

        class Choice(enum.Enum):
            A = 1

            @property
            def name(self):
                return self._name_.lower()

    elif case == "value":

        class Choice(enum.Enum):
            A = 1

            @property
            def value(self):
                return self._value_ * 10

    elif case == "nan":

        class Choice(enum.Enum):
            A = float("nan")

    elif case == "metaclass":

        class Meta(enum.EnumMeta):
            pass

        class Choice(enum.Enum, metaclass=Meta):
            A = 1

    elif case == "date":

        class Choice(date, enum.Enum):
            A = 2012, 1, 31

    elif case == "changed_value":

        class Choice(int, enum.Enum):
            def __new__(cls, code):
                member = int.__new__(cls, code)
                member._value_ = code + 1
                return member

            A = 1

    elif case == "float_payload":

        class Choice(float, enum.Enum):
            def __new__(cls, code):
                member = float.__new__(cls, code)
                member._value_ = int(code)
                return member

            A = 1.5

    elif case == "redirected_metaclass":

        class Meta(enum.EnumMeta):
            def __getattribute__(cls, name):
                return super().__getattribute__("B" if name == "A" else name)

        class Choice(enum.Enum, metaclass=Meta):
            A = 1
            B = 2

    elif case == "inherited_slots":

        class Base(enum.Enum):
            __slots__ = ("label",)

        class Choice(Base):
            __slots__ = ("label",)

            def __init__(self, value):
                Base.label.__set__(self, "base")
                self.label = "child"

            A = 1

        Base.label.__set__(Choice.A, "updated")

    elif case == "super":

        class Choice(enum.Enum):
            A = 1

            def label(self):
                return super().__str__()

    elif case == "self_reference":

        class Choice(enum.Enum):
            A = 1

            def label(self):
                return Choice.A

            @classmethod
            def class_ref(cls):
                return Choice

            @staticmethod
            def static_ref():
                return Choice

            @property
            def member_ref(self):
                return Choice.A

    elif case == "constructor_method":

        class Choice(enum.Enum):
            A = 1

            def __init__(self, value):
                self.label = self.make_label()

            def make_label(self):
                return "label"

    elif case in {
        "flag_invert",
        "flag_negative",
        "flag_composite",
        "intflag_invert",
        "intflag_negative",
        "intflag_composite",
    }:

        class Choice(enum.IntFlag if case.startswith("intflag") else enum.Flag):
            A = 1
            B = 2

        fingerprint = Hasher.hash(Choice)
        if case.endswith("invert"):
            _ = ~Choice.A
        elif case.endswith("negative"):
            _ = Choice(-2)
        else:
            assert Choice(3) == Choice.A | Choice.B
        assert Hasher.hash(Choice) == fingerprint

    else:
        raise AssertionError(case)
    return Choice


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("case", ["super", "self_reference"])
def test_dill_enum_recursive_method(serialize, case):
    choice = _make_adversarial_enum(case)
    restored = dill.loads(serialize(choice))
    assert restored.A.label() == ("Choice.A" if case == "super" else restored.A)
    method, restored = dill.loads(serialize((choice.label, choice)))
    assert method(restored.A) == ("Choice.A" if case == "super" else restored.A)
    if case == "self_reference":
        assert restored.class_ref() is restored
        assert restored.static_ref() is restored
        assert restored.A.member_ref is restored.A


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_constructor_calls_method(serialize):
    restored = dill.loads(serialize(_make_adversarial_enum("constructor_method")))
    assert restored.A.label == "label"


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("enum_type", [enum.Flag, enum.IntFlag])
@pytest.mark.parametrize(
    "lookup",
    [lambda choice: ~choice.A, lambda choice: choice(-2), lambda choice: choice.A | choice.B],
    ids=["invert", "negative", "composite"],
)
def test_dill_enum_lookup_cache(serialize, enum_type, lookup):
    class Choice(enum_type):
        A = 1
        B = 2

    before = bytes(serialize(Choice))
    fresh = dill.loads(before)
    fingerprint = Hasher.hash(Choice)
    expected = lookup(Choice)
    after = bytes(serialize(Choice))
    assert after == before
    assert Hasher.hash(Choice) == fingerprint
    restored = dill.loads(after)
    assert list(restored._value2member_map_) == [1, 2]
    assert "_inverted_" not in restored.A.__dict__
    for rebuilt in (fresh, restored):
        member = lookup(rebuilt)
        assert (member.name, member.value) == (expected.name, expected.value)
        assert (member is rebuilt.B) == (expected is Choice.B)
        assert member is rebuilt(member.value)


@pytest.mark.skipif(sys.version_info < (3, 13), reason="Value aliases require Python 3.13+")
@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("enum_type", [enum.Enum, enum.Flag, enum.IntFlag])
def test_dill_enum_explicit_negative_value_alias(serialize, enum_type):
    class Choice(enum_type):
        A = 1
        B = 2

    Choice.A._add_value_alias_(-2)
    restored = dill.loads(serialize(Choice))
    assert restored(-2) is restored.A


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("method", ["__reduce_ex__", "__reduce__"])
@pytest.mark.parametrize("inherited", [False, True])
@pytest.mark.parametrize("importable", [False, True])
def test_dill_enum_explicit_member_reducer_raises(serialize, method, inherited, importable, monkeypatch):
    class Base(enum.Enum):
        pass

    class Choice(Base):
        A = 1

    def reject(self, *args):
        raise TypeError("explicit Enum reduction rejected")

    choice = ImportableEnum if importable else Choice
    owner = choice.__bases__[0] if inherited else choice
    monkeypatch.setattr(owner, method, reject)
    with pytest.raises(TypeError, match="explicit Enum reduction rejected"):
        serialize(next(iter(choice)))
    # Serializing the class itself must not invoke an instance-only contract.
    restored = dill.loads(serialize(choice))
    assert list(restored.__members__) == list(choice.__members__)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
@pytest.mark.parametrize("registration", ["dill", "copyreg", "__reduce__", "__reduce_ex__"])
@pytest.mark.parametrize("importable", [False, True])
def test_dill_enum_registered_member_reducer(serialize, registration, importable, monkeypatch):
    class Choice(enum.Enum):
        A = 1

    choice = ImportableEnum if importable else Choice

    def reduce_member(member, *args):
        return str, ("custom",)

    def save_member(pickler, member):
        pickler.save_reduce(*reduce_member(member), obj=member)

    if registration.startswith("__reduce"):
        monkeypatch.setattr(choice, registration, reduce_member)
    else:
        table = dill.Pickler.dispatch if registration == "dill" else copyreg.dispatch_table
        monkeypatch.setitem(table, choice, None)
        if registration == "dill":
            dill.register(choice)(save_member)
        else:
            copyreg.pickle(choice, reduce_member)
    assert dill.loads(serialize(next(iter(choice)))) == "custom"
    restored, member = dill.loads(serialize((choice, next(iter(choice)))))
    assert list(restored.__members__) == list(choice.__members__)
    assert member == "custom"


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_constructor_replay(serialize, monkeypatch):
    monkeypatch.setenv("DATASETS_ENUM_CONSTRUCTIONS", "0")

    class Choice(enum.Enum):
        A = 1

        def __init__(self, value):
            os.environ["DATASETS_ENUM_CONSTRUCTIONS"] = str(int(os.environ["DATASETS_ENUM_CONSTRUCTIONS"]) + 1)

    assert os.environ["DATASETS_ENUM_CONSTRUCTIONS"] == "1"
    Hasher.hash(Choice)
    # Validation rebuilds once during hashing/dumping; loading rebuilds again.
    assert os.environ["DATASETS_ENUM_CONSTRUCTIONS"] == "2"
    payload = serialize(Choice)
    assert os.environ["DATASETS_ENUM_CONSTRUCTIONS"] == "3"
    restored = dill.loads(payload)
    assert os.environ["DATASETS_ENUM_CONSTRUCTIONS"] == "4"
    assert restored.A.value == 1


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_custom_new(serialize):
    choice = _make_adversarial_enum("constructor")
    restored = dill.loads(serialize(choice))
    assert int(restored.A) == 10
    assert restored.A.value == 1
    assert str(restored.A) == str(choice.A)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_slots(serialize):
    choice = _make_adversarial_enum("slots")
    restored = dill.loads(serialize(choice))
    assert restored.__slots__ == ("label",)
    assert restored.A.label == "updated"
    assert set(restored.A.__dict__) == set(choice.A.__dict__)
    assert "label" not in restored.A.__dict__


@pytest.mark.skipif(sys.version_info < (3, 13), reason="Value aliases require Python 3.13+")
@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_value_alias(serialize):
    choice = _make_adversarial_enum("value_alias")
    assert choice(2) is choice.A
    restored = dill.loads(serialize(choice))
    assert restored(2) is restored.A


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_overridden_name(serialize):
    restored = dill.loads(serialize(_make_adversarial_enum("name")))
    assert list(restored.__members__) == ["A"]
    assert restored.A._name_ == "A"
    assert restored.A.name == "a"


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_overridden_value(serialize):
    restored = dill.loads(serialize(_make_adversarial_enum("value")))
    assert restored.A._value_ == 1
    assert restored.A.value == 10
    assert restored(1) is restored.A


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_nan_member_closure(serialize):
    choice = _make_adversarial_enum("nan")
    member = choice.A

    def transform():
        return choice, member

    restored, restored_member = dill.loads(serialize(transform))()
    assert restored_member is restored.A
    assert math.isnan(restored_member.value)


@pytest.mark.skipif(config.DILL_VERSION.release < (0, 3, 5), reason="Local non-Enum classes require dill>=0.3.5")
@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_metaclass_subclass(serialize):
    choice = _make_adversarial_enum("metaclass")
    restored = dill.loads(serialize(choice))
    assert type(restored).__name__ == "Meta"
    assert type(restored).__bases__ == (enum.EnumMeta,)
    assert restored.A.value == 1


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps, Hasher.hash])
def test_dill_enum_date_fails_at_dump(serialize):
    choice = _make_adversarial_enum("date")
    assert choice.A.value == date(2012, 1, 31)
    with pytest.raises(pickle.PicklingError, match=r"Cannot faithfully pickle Enum .*Choice"):
        serialize(choice)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps, Hasher.hash])
def test_dill_enum_changed_value_fails_at_dump(serialize):
    choice = _make_adversarial_enum("changed_value")
    assert int(choice.A) == 1
    assert choice.A.value == 2
    with pytest.raises(pickle.PicklingError, match=r"Cannot faithfully pickle Enum .*Choice"):
        serialize(choice)


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps, Hasher.hash])
def test_dill_enum_float_payload_fails_at_dump(serialize):
    choice = _make_adversarial_enum("float_payload")
    assert float(choice.A) == 1.5
    assert choice.A.value == 1
    with pytest.raises(pickle.PicklingError, match=r"Cannot faithfully pickle Enum .*Choice"):
        serialize(choice)


@pytest.mark.skipif(config.DILL_VERSION.release < (0, 3, 5), reason="Local non-Enum classes require dill>=0.3.5")
@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_member_ignores_metaclass_attribute_override(serialize):
    choice = _make_adversarial_enum("redirected_metaclass")
    member = choice["A"]
    assert choice.A is choice.B

    def transform():
        return choice, member

    restored, restored_member = dill.loads(serialize(transform))()
    assert restored_member is restored["A"]
    assert restored_member.value == 1


@pytest.mark.parametrize("serialize", [dumps, ForkingPickler.dumps])
def test_dill_enum_shadowed_inherited_slots(serialize):
    choice = _make_adversarial_enum("inherited_slots")
    restored = dill.loads(serialize(choice))
    assert restored.A.label == "child"
    assert restored.__bases__[0].label.__get__(restored.A) == "updated"


def test_dill_dispatch_retains_registered_type_membership():
    # Pickler.save uses membership to skip costly optional-library discovery.
    assert all(kind in Pickler.dispatch for kind in (str, int, dict, list))


def test_adversarial_enum_in_separate_processes(tmp_path):
    script = tmp_path / "adversarial_enums.py"
    script.write_text(
        "import enum\nimport json\nimport pickle\nimport sys\nfrom datetime import date\n"
        "import dill\nfrom multiprocess.reduction import ForkingPickler\n"
        "from datasets import Dataset, config\nfrom datasets.fingerprint import Hasher\n"
        "from datasets.utils._dill import dumps\n"
        + inspect.getsource(_make_adversarial_enum)
        + dedent(
            """
            class MainMeta(enum.EnumMeta):
                pass

            class MainChoice(enum.Enum, metaclass=MainMeta):
                A = 1

            def make_transform(choice):
                member = choice["A"]

                def transform(row):
                    assert member is choice["A"]
                    label = getattr(member, "label", None)
                    if callable(label):
                        label = label()
                        assert label == "Choice.A" or label is member
                    return {"label": str((member._name_, member.name, str(member.value),
                                          str(member), int(member) if isinstance(member, int) else None,
                                          label))}

                return transform

            if __name__ == "__main__":
                results = {}
                cases = ["constructor", "slots", "name", "value", "nan", "metaclass", "date", "changed_value",
                         "float_payload", "redirected_metaclass", "inherited_slots", "main_metaclass",
                         "super", "self_reference", "flag_invert", "flag_negative", "flag_composite",
                         "intflag_invert", "intflag_negative", "intflag_composite", "constructor_method"]
                if sys.version_info >= (3, 13):
                    cases.append("value_alias")
                if config.DILL_VERSION.release < (0, 3, 5):
                    # Local non-Enum metaclasses are unsupported by upstream dill.
                    cases = [case for case in cases if case not in ("metaclass", "redirected_metaclass")]
                for case in cases:
                    choice = MainChoice if case == "main_metaclass" else _make_adversarial_enum(case)
                    transform = make_transform(choice)
                    if case in ("date", "changed_value", "float_payload"):
                        errors = []
                        for serialize in (dumps, ForkingPickler.dumps, Hasher.hash):
                            try:
                                serialize(transform)
                            except pickle.PicklingError as error:
                                assert "Cannot faithfully pickle Enum" in str(error)
                                assert "Choice" in str(error)
                                errors.append(str(error))
                            else:
                                raise AssertionError("Expected dump-time error: " + case)
                        results[case] = errors
                        continue
                    expected = transform({})
                    for serialize in (dumps, ForkingPickler.dumps):
                        assert dill.loads(serialize(transform))({}) == expected
                        restored = dill.loads(serialize(choice))
                        if case == "value_alias":
                            assert restored(2) is restored.A
                        if case == "inherited_slots":
                            assert restored.__bases__[0].label.__get__(restored.A) == "updated"
                    result = Dataset.from_dict({"text": ["one", "two"]}).map(transform, num_proc=2)
                    assert result["label"] == [expected["label"]] * 2
                    results[case] = [Hasher.hash(choice), Hasher.hash(transform), result._fingerprint]
                print(json.dumps(results, sort_keys=True))
            """
        )
    )
    outputs = [subprocess.check_output([sys.executable, str(script)], timeout=120) for _ in range(2)]
    assert json.loads(outputs[0]) == json.loads(outputs[1])


def test_hash_enum_depends_on_values():
    def make_transform(value):
        class Choice(enum.Enum):
            first = value

        def transform():
            return Choice.first.value

        return transform

    assert Hasher.hash(make_transform("one")) == Hasher.hash(make_transform("one"))
    assert Hasher.hash(make_transform("one")) != Hasher.hash(make_transform("two"))


def test_multiprocess_keeps_late_dill_registrations():
    class Payload:
        def __reduce__(self):
            raise TypeError("The registered reducer must be used")

    with patch.dict(dill.Pickler.dispatch):

        @dill.register(Payload)
        def save_payload(pickler, obj):
            pickler.save_reduce(str, ("custom",), obj=obj)

        assert dill.loads(ForkingPickler.dumps(Payload())) == "custom"


@pytest.mark.parametrize("enum_type", ENUM_TYPES)
@pytest.mark.parametrize("scope", ["main", "local"])
@pytest.mark.parametrize("num_proc", [None, 2])
def test_map_enum_in_separate_processes(tmp_path, enum_type, scope, num_proc):
    # Run a real script: an importable test-module Enum would be saved by reference.
    enum_code = f"class Choice(enum.{enum_type.__name__}):\n    second = enum.auto()\n    first = enum.auto()\n"
    if scope == "local":
        enum_code = "def make_enum():\n" + "\n".join("    " + line for line in enum_code.splitlines())
        enum_code += "\n    return Choice\nChoice = make_enum()\n"
    script = tmp_path / "enum_map.py"
    script.write_text(
        "import enum\nimport json\nfrom datasets import Dataset\nfrom datasets.fingerprint import Hasher\n"
        + enum_code
        + dedent(
            f"""
            def make_transform():
                choice = Choice
                member = Choice.second

                def transform(row):
                    assert member is choice.second
                    return {{"label": member.name}}

                return transform

            if __name__ == "__main__":
                transform = make_transform()
                function_hash = Hasher.hash(transform)
                result = Dataset.from_dict({{"text": ["one", "two"]}}).map(transform, num_proc={num_proc!r})
                assert result["label"] == ["second", "second"]
                print(json.dumps([function_hash, result._fingerprint]))
            """
        )
    )
    outputs = [subprocess.check_output([sys.executable, str(script)], timeout=60) for _ in range(2)]
    assert json.loads(outputs[0]) == json.loads(outputs[1])


class DatasetChild(datasets.Dataset):
    @fingerprint_transform(inplace=False)
    def func1(self, new_fingerprint, *args, **kwargs):
        return DatasetChild(self.data, fingerprint=new_fingerprint)

    @fingerprint_transform(inplace=False)
    def func2(self, new_fingerprint, *args, **kwargs):
        return DatasetChild(self.data, fingerprint=new_fingerprint)


class UnpicklableCallable:
    def __init__(self, callable):
        self.callable = callable

    def __call__(self, *args, **kwargs):
        if self.callable is not None:
            return self.callable(*args, **kwargs)

    def __getstate__(self):
        raise pickle.PicklingError()


if config.TORCH_AVAILABLE:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class TorchModule(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(1, 20, 5)
            self.conv2 = nn.Conv2d(20, 20, 5)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            return F.relu(self.conv2(x))
else:
    TorchModule = None


class TokenizersHashTest(TestCase):
    @require_transformers
    @pytest.mark.integration
    def test_hash_tokenizer(self):
        from transformers import AutoTokenizer

        def encode(x):
            return tokenizer(x)

        # TODO: add hash consistency tests across sessions
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        hash1 = Hasher.hash(tokenizer)
        hash1_lambda = Hasher.hash(lambda x: tokenizer(x))
        hash1_encode = Hasher.hash(encode)
        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        hash2 = Hasher.hash(tokenizer)
        hash2_lambda = Hasher.hash(lambda x: tokenizer(x))
        hash2_encode = Hasher.hash(encode)
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        hash3 = Hasher.hash(tokenizer)
        hash3_lambda = Hasher.hash(lambda x: tokenizer(x))
        hash3_encode = Hasher.hash(encode)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)
        self.assertEqual(hash1_lambda, hash3_lambda)
        self.assertNotEqual(hash1_lambda, hash2_lambda)
        self.assertEqual(hash1_encode, hash3_encode)
        self.assertNotEqual(hash1_encode, hash2_encode)

    @require_transformers
    @pytest.mark.integration
    def test_hash_tokenizer_with_cache(self):
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        hash1 = Hasher.hash(tokenizer)
        tokenizer("Hello world !")  # call once to change the tokenizer's cache
        hash2 = Hasher.hash(tokenizer)
        self.assertEqual(hash1, hash2)

    @require_regex
    def test_hash_regex(self):
        import regex

        pat = regex.Regex("foo")
        hash1 = Hasher.hash(pat)
        pat = regex.Regex("bar")
        hash2 = Hasher.hash(pat)
        pat = regex.Regex("foo")
        hash3 = Hasher.hash(pat)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)


class RecurseHashTest(TestCase):
    def test_recurse_hash_for_function(self):
        def func():
            return foo

        foo = [0]
        hash1 = Hasher.hash(func)
        foo = [1]
        hash2 = Hasher.hash(func)
        foo = [0]
        hash3 = Hasher.hash(func)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_hash_ignores_line_definition_of_function(self):
        def func():
            pass

        hash1 = Hasher.hash(func)

        def func():
            pass

        hash2 = Hasher.hash(func)
        self.assertEqual(hash1, hash2)

    def test_recurse_hash_for_class(self):
        hash1 = Hasher.hash(Foo([0]))
        hash2 = Hasher.hash(Foo([1]))
        hash3 = Hasher.hash(Foo([0]))
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_recurse_hash_for_method(self):
        hash1 = Hasher.hash(Foo([0]).__call__)
        hash2 = Hasher.hash(Foo([1]).__call__)
        hash3 = Hasher.hash(Foo([0]).__call__)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_hash_ipython_function(self):
        def create_ipython_func(co_filename, returned_obj):
            def func():
                return returned_obj

            code = func.__code__
            # Use _create_code from dill in order to make it work for different python versions
            code = code.replace(co_filename=co_filename)
            return FunctionType(code, func.__globals__, func.__name__, func.__defaults__, func.__closure__)

        co_filename, returned_obj = "<ipython-input-2-e0383a102aae>", [0]
        hash1 = Hasher.hash(create_ipython_func(co_filename, returned_obj))
        co_filename, returned_obj = "<ipython-input-2-e0383a102aae>", [1]
        hash2 = Hasher.hash(create_ipython_func(co_filename, returned_obj))
        co_filename, returned_obj = "<ipython-input-5-713f6613acf3>", [0]
        hash3 = Hasher.hash(create_ipython_func(co_filename, returned_obj))
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

        co_filename, returned_obj = os.path.join(gettempdir(), "ipykernel_12345", "321456789.py"), [0]
        hash4 = Hasher.hash(create_ipython_func(co_filename, returned_obj))
        co_filename, returned_obj = os.path.join(gettempdir(), "ipykernel_12345", "321456789.py"), [1]
        hash5 = Hasher.hash(create_ipython_func(co_filename, returned_obj))
        co_filename, returned_obj = os.path.join(gettempdir(), "ipykernel_12345", "654123987.py"), [0]
        hash6 = Hasher.hash(create_ipython_func(co_filename, returned_obj))
        self.assertEqual(hash4, hash6)
        self.assertNotEqual(hash4, hash5)

    def test_recurse_hash_for_function_with_shuffled_globals(self):
        foo, bar = [0], [1]

        def func():
            return foo, bar

        func.__module__ = "__main__"

        def globalvars_mock1_side_effect(func, *args, **kwargs):
            return {"foo": foo, "bar": bar}

        def globalvars_mock2_side_effect(func, *args, **kwargs):
            return {"bar": bar, "foo": foo}

        with patch("dill.detect.globalvars", side_effect=globalvars_mock1_side_effect) as globalvars_mock1:
            hash1 = Hasher.hash(func)
            self.assertGreater(globalvars_mock1.call_count, 0)
        with patch("dill.detect.globalvars", side_effect=globalvars_mock2_side_effect) as globalvars_mock2:
            hash2 = Hasher.hash(func)
            self.assertGreater(globalvars_mock2.call_count, 0)
        self.assertEqual(hash1, hash2)


class HashingTest(TestCase):
    def test_hash_simple(self):
        hash1 = Hasher.hash("hello")
        hash2 = Hasher.hash("hello")
        hash3 = Hasher.hash("there")
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)

    def test_hash_class_instance(self):
        hash1 = Hasher.hash(Foo("hello"))
        hash2 = Hasher.hash(Foo("hello"))
        hash3 = Hasher.hash(Foo("there"))
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)

    def test_hash_arrow_table_is_independent_of_chunking(self):
        import pyarrow as pa

        def table_with_chunks(num_chunks, num_rows=600):
            rows_per_chunk = num_rows // num_chunks
            values = pa.array(["a" * 40] * num_rows)
            chunks = [values.slice(i * rows_per_chunk, rows_per_chunk) for i in range(num_chunks)]
            return pa.table({"text": pa.chunked_array(chunks)})

        hash_few_chunks = Hasher.hash(InMemoryTable(table_with_chunks(2)))
        hash_many_chunks = Hasher.hash(InMemoryTable(table_with_chunks(600)))
        hash_other_data = Hasher.hash(InMemoryTable(pa.table({"text": pa.array(["b" * 40] * 600)})))
        self.assertEqual(hash_few_chunks, hash_many_chunks)
        self.assertNotEqual(hash_few_chunks, hash_other_data)

    def test_hash_update(self):
        hasher = Hasher()
        for x in ["hello", Foo("hello")]:
            hasher.update(x)
        hash1 = hasher.hexdigest()
        hasher = Hasher()
        for x in ["hello", Foo("hello")]:
            hasher.update(x)
        hash2 = hasher.hexdigest()
        hasher = Hasher()
        for x in ["there", Foo("there")]:
            hasher.update(x)
        hash3 = hasher.hexdigest()
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)

    def test_hash_unpicklable(self):
        with self.assertRaises(pickle.PicklingError):
            Hasher.hash(UnpicklableCallable(Foo("hello")))

    def test_hash_same_strings(self):
        string = "abc"
        obj1 = [string, string]  # two strings have the same ids
        obj2 = [string, string]
        obj3 = json.loads(f'["{string}", "{string}"]')  # two strings have different ids
        self.assertIs(obj1[0], string)
        self.assertIs(obj1[0], obj1[1])
        self.assertIs(obj2[0], string)
        self.assertIs(obj2[0], obj2[1])
        self.assertIsNot(obj3[0], string)
        self.assertIsNot(obj3[0], obj3[1])
        hash1 = Hasher.hash(obj1)
        hash2 = Hasher.hash(obj2)
        hash3 = Hasher.hash(obj3)
        self.assertEqual(hash1, hash2)
        self.assertEqual(hash1, hash3)

    def test_set_stable(self):
        rng = np.random.default_rng(42)
        set_ = {rng.random() for _ in range(10_000)}
        expected_hash = Hasher.hash(set_)
        assert expected_hash == Pool(1).apply_async(partial(Hasher.hash, set(set_))).get()

    def test_set_doesnt_depend_on_order(self):
        set_ = set("abc")
        hash1 = Hasher.hash(set_)
        set_ = set("def")
        hash2 = Hasher.hash(set_)
        set_ = set("cba")
        hash3 = Hasher.hash(set_)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    @require_tiktoken
    def test_hash_tiktoken_encoding(self):
        import tiktoken

        enc = tiktoken.get_encoding("gpt2")
        hash1 = Hasher.hash(enc)
        enc = tiktoken.get_encoding("r50k_base")
        hash2 = Hasher.hash(enc)
        enc = tiktoken.get_encoding("gpt2")
        hash3 = Hasher.hash(enc)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    @require_numpy1_on_windows
    @require_torch
    def test_hash_torch_tensor(self):
        import torch

        t = torch.tensor([1.0])
        hash1 = Hasher.hash(t)
        t = torch.tensor([2.0])
        hash2 = Hasher.hash(t)
        t = torch.tensor([1.0])
        hash3 = Hasher.hash(t)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    @require_numpy1_on_windows
    @require_torch
    def test_hash_torch_generator(self):
        import torch

        t = torch.Generator(device="cpu").manual_seed(42)
        hash1 = Hasher.hash(t)
        t = t = torch.Generator(device="cpu").manual_seed(50)
        hash2 = Hasher.hash(t)
        t = t = torch.Generator(device="cpu").manual_seed(42)
        hash3 = Hasher.hash(t)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    @require_spacy
    @pytest.mark.integration
    def test_hash_spacy_model(self):
        import spacy

        nlp = spacy.blank("en")
        hash1 = Hasher.hash(nlp)
        nlp = spacy.blank("fr")
        hash2 = Hasher.hash(nlp)
        nlp = spacy.blank("en")
        hash3 = Hasher.hash(nlp)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    @require_not_windows
    @require_torch_compile
    def test_hash_torch_compiled_function(self):
        import torch

        def f(x):
            return torch.sin(x) + torch.cos(x)

        hash1 = Hasher.hash(f)
        f = torch.compile(f)
        hash2 = Hasher.hash(f)
        self.assertEqual(hash1, hash2)

    @require_not_windows
    @require_torch_compile
    def test_hash_torch_compiled_module(self):
        m = TorchModule()
        next(iter(m.parameters())).data.fill_(1.0)
        mc = torch.compile(m)
        hash1 = Hasher.hash(m)
        hash2 = Hasher.hash(mc)
        m = TorchModule()
        next(iter(m.parameters())).data.fill_(2.0)
        mc = torch.compile(m)
        hash3 = Hasher.hash(mc)
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)
        self.assertNotEqual(hash2, hash3)


@pytest.mark.integration
def test_move_script_doesnt_change_hash(tmp_path: Path):
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()
    script_filename = "script.py"
    code = dedent(
        """
    from datasets.fingerprint import Hasher
    def foo():
        pass
    print(Hasher.hash(foo))
    """
    )
    script_path1 = dir1 / script_filename
    script_path2 = dir2 / script_filename
    with script_path1.open("w") as f:
        f.write(code)
    with script_path2.open("w") as f:
        f.write(code)
    fingerprint1 = subprocess.check_output(["python", str(script_path1)])
    fingerprint2 = subprocess.check_output(["python", str(script_path2)])
    assert fingerprint1 == fingerprint2


def test_fingerprint_in_multiprocessing():
    data = {"a": [0, 1, 2]}
    dataset = DatasetChild(InMemoryTable.from_pydict(data))
    expected_fingerprint = dataset.func1()._fingerprint
    with Pool(2) as pool:
        fingerprints = pool.map(
            lambda _: DatasetChild(InMemoryTable.from_pydict(data)).func1()._fingerprint, range(10)
        )
    assert all(f == expected_fingerprint for f in fingerprints)


def test_temp_cache_dir_with_tmpdir_nonexistent(tmp_path, caplog):
    """Test that _TempCacheDir creates TMPDIR if it doesn't exist."""
    import os

    # Set TMPDIR to a non-existent directory
    tmpdir_path = tmp_path / "custom_tmpdir"
    assert not tmpdir_path.exists(), "TMPDIR should not exist initially"

    # Save original TMPDIR and set new one
    original_tmpdir = os.environ.get("TMPDIR")
    try:
        os.environ["TMPDIR"] = str(tmpdir_path)

        # Clear any existing temp cache dir to force recreation
        import datasets.fingerprint

        datasets.fingerprint._TEMP_DIR_FOR_TEMP_CACHE_FILES = None

        # Import and test _TempCacheDir directly
        from datasets.fingerprint import _TempCacheDir

        with caplog.at_level("INFO", logger="datasets.fingerprint"):
            temp_cache = _TempCacheDir()
            cache_dir = temp_cache.name

        # The key test: verify the cache directory is within the TMPDIR we set
        # This proves that TMPDIR was respected and the directory was created
        tmpdir_path_str = str(tmpdir_path)
        assert cache_dir.startswith(tmpdir_path_str), (
            f"Cache dir {cache_dir} should be in TMPDIR {tmpdir_path_str}. TMPDIR env var: {os.environ.get('TMPDIR')}"
        )
        # Verify the directory was created
        assert tmpdir_path.exists(), (
            f"TMPDIR directory {tmpdir_path} should have been created. Cache dir is: {cache_dir}"
        )
        # Verify logging
        assert f"Created TMPDIR directory: {tmpdir_path_str}" in caplog.text

        # Cleanup
        temp_cache.cleanup()
    finally:
        # Restore original TMPDIR
        if original_tmpdir is not None:
            os.environ["TMPDIR"] = original_tmpdir
        elif "TMPDIR" in os.environ:
            del os.environ["TMPDIR"]


def test_temp_cache_dir_with_tmpdir_existing(tmp_path, monkeypatch):
    """Test that _TempCacheDir works correctly when TMPDIR exists."""
    from datasets.fingerprint import get_temporary_cache_files_directory

    # Set TMPDIR to an existing directory
    tmpdir_path = tmp_path / "existing_tmpdir"
    tmpdir_path.mkdir()
    monkeypatch.setenv("TMPDIR", str(tmpdir_path))

    # Clear any existing temp cache dir
    import datasets.fingerprint

    datasets.fingerprint._TEMP_DIR_FOR_TEMP_CACHE_FILES = None

    cache_dir = get_temporary_cache_files_directory()

    # Verify the cache directory is within the TMPDIR
    assert cache_dir.startswith(str(tmpdir_path)), f"Cache dir {cache_dir} should be in TMPDIR {tmpdir_path}"


def test_temp_cache_dir_without_tmpdir(monkeypatch):
    """Test that _TempCacheDir works correctly when TMPDIR is not set."""
    from datasets.fingerprint import get_temporary_cache_files_directory

    # Remove TMPDIR if it exists
    monkeypatch.delenv("TMPDIR", raising=False)

    # Clear any existing temp cache dir
    import datasets.fingerprint

    datasets.fingerprint._TEMP_DIR_FOR_TEMP_CACHE_FILES = None

    cache_dir = get_temporary_cache_files_directory()

    # Verify it uses the default temp directory
    from tempfile import gettempdir

    default_temp = gettempdir()
    assert cache_dir.startswith(default_temp), f"Cache dir {cache_dir} should be in default temp {default_temp}"


def test_temp_cache_dir_tmpdir_creation_failure(tmp_path, monkeypatch, caplog):
    """Test that _TempCacheDir raises if TMPDIR cannot be created."""
    from unittest.mock import patch

    from datasets.fingerprint import _TempCacheDir

    # Set TMPDIR to a path that will fail to create (e.g., invalid permissions)
    # Use a path that's likely to fail on creation
    tmpdir_path = tmp_path / "nonexistent" / "nested" / "path"
    monkeypatch.setenv("TMPDIR", str(tmpdir_path))

    # Mock os.makedirs to raise an error
    with patch("datasets.fingerprint.os.makedirs", side_effect=OSError("Permission denied")):
        with pytest.raises(OSError) as excinfo:
            _TempCacheDir()

    # Verify the error message gives clear context about TMPDIR
    msg = str(excinfo.value)
    assert "TMPDIR is set to" in msg
    assert "could not be created" in msg


def test_temp_cache_dir_tmpdir_not_directory(tmp_path, monkeypatch):
    """Test that _TempCacheDir raises if TMPDIR points to a non-directory."""
    from datasets.fingerprint import _TempCacheDir

    # Create a regular file and point TMPDIR to it
    file_path = tmp_path / "not_a_dir"
    file_path.write_text("not a directory")
    monkeypatch.setenv("TMPDIR", str(file_path))

    with pytest.raises(OSError) as excinfo:
        _TempCacheDir()

    msg = str(excinfo.value)
    assert "TMPDIR is set to" in msg
    assert "is not a directory" in msg


def test_fingerprint_when_transform_version_changes():
    data = {"a": [0, 1, 2]}

    class DummyDatasetChild(datasets.Dataset):
        @fingerprint_transform(inplace=False)
        def func(self, new_fingerprint):
            return DummyDatasetChild(self.data, fingerprint=new_fingerprint)

    fingeprint_no_version = DummyDatasetChild(InMemoryTable.from_pydict(data)).func()

    class DummyDatasetChild(datasets.Dataset):
        @fingerprint_transform(inplace=False, version="1.0.0")
        def func(self, new_fingerprint):
            return DummyDatasetChild(self.data, fingerprint=new_fingerprint)

    fingeprint_1 = DummyDatasetChild(InMemoryTable.from_pydict(data)).func()

    class DummyDatasetChild(datasets.Dataset):
        @fingerprint_transform(inplace=False, version="2.0.0")
        def func(self, new_fingerprint):
            return DummyDatasetChild(self.data, fingerprint=new_fingerprint)

    fingeprint_2 = DummyDatasetChild(InMemoryTable.from_pydict(data)).func()

    assert len({fingeprint_no_version, fingeprint_1, fingeprint_2}) == 3


def test_dependency_on_dill():
    # AttributeError: module 'dill._dill' has no attribute 'stack'
    hasher = Hasher()
    hasher.update(lambda x: x)
