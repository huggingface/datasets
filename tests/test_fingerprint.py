import json
import os
import pickle
import subprocess
from functools import partial
from pathlib import Path
from tempfile import gettempdir
from textwrap import dedent
from types import FunctionType
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pytest
from multiprocess import Pool

import datasets
from datasets import config
from datasets.fingerprint import Hasher, fingerprint_transform
from datasets.table import InMemoryTable

from .utils import (
    require_not_windows,
    require_numpy1_on_windows,
    require_regex,
    require_spacy,
    require_tiktoken,
    require_torch,
    require_transformers,
)


class Foo:
    def __init__(self, foo):
        self.foo = foo

    def __call__(self):
        return self.foo


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
    @require_torch
    def test_hash_torch_compiled_function(self):
        import torch

        def f(x):
            return torch.sin(x) + torch.cos(x)

        hash1 = Hasher.hash(f)
        f = torch.compile(f)
        hash2 = Hasher.hash(f)
        self.assertEqual(hash1, hash2)

    @require_not_windows
    @require_torch
    def test_hash_torch_compiled_module(self):
        m = TorchModule()
        next(iter(m.parameters())).data.fill_(1.0)
        hash1 = Hasher.hash(m)
        m = torch.compile(m)
        hash2 = Hasher.hash(m)
        m = TorchModule()
        next(iter(m.parameters())).data.fill_(2.0)
        m = torch.compile(m)
        hash3 = Hasher.hash(m)
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
    assert expected_fingerprint == dataset.func1()._fingerprint
    assert expected_fingerprint != dataset.func2()._fingerprint

    with Pool(2) as p:
        assert expected_fingerprint == p.apply_async(dataset.func1).get()._fingerprint
        assert expected_fingerprint != p.apply_async(dataset.func2).get()._fingerprint


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
