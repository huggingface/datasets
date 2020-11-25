from hashlib import md5
from types import CodeType, FunctionType
from unittest import TestCase
from unittest.mock import patch

import datasets

from .utils import require_regex, require_transformers


class Foo:
    def __init__(self, foo):
        self.foo = foo

    def __call__(self):
        return self.foo


class TokenizersCachingTest(TestCase):
    @require_transformers
    def test_hash_tokenizer(self):
        from transformers import AutoTokenizer

        def encode(x):
            return tokenizer(x)

        # TODO: add hash consistency tests across sessions
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        hash1 = md5(datasets.utils.dumps(tokenizer)).hexdigest()
        hash1_lambda = md5(datasets.utils.dumps(lambda x: tokenizer(x))).hexdigest()
        hash1_encode = md5(datasets.utils.dumps(encode)).hexdigest()
        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        hash2 = md5(datasets.utils.dumps(tokenizer)).hexdigest()
        hash2_lambda = md5(datasets.utils.dumps(lambda x: tokenizer(x))).hexdigest()
        hash2_encode = md5(datasets.utils.dumps(encode)).hexdigest()
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        hash3 = md5(datasets.utils.dumps(tokenizer)).hexdigest()
        hash3_lambda = md5(datasets.utils.dumps(lambda x: tokenizer(x))).hexdigest()
        hash3_encode = md5(datasets.utils.dumps(encode)).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)
        self.assertEqual(hash1_lambda, hash3_lambda)
        self.assertNotEqual(hash1_lambda, hash2_lambda)
        self.assertEqual(hash1_encode, hash3_encode)
        self.assertNotEqual(hash1_encode, hash2_encode)

    @require_transformers
    def test_hash_tokenizer_with_cache(self):
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        hash1 = md5(datasets.utils.dumps(tokenizer)).hexdigest()
        tokenizer("Hello world !")  # call once to change the tokenizer's cache
        hash2 = md5(datasets.utils.dumps(tokenizer)).hexdigest()
        self.assertEqual(hash1, hash2)

    @require_regex
    def test_hash_regex(self):
        import regex

        pat = regex.Regex("foo")
        hash1 = md5(datasets.utils.dumps(pat)).hexdigest()
        pat = regex.Regex("bar")
        hash2 = md5(datasets.utils.dumps(pat)).hexdigest()
        pat = regex.Regex("foo")
        hash3 = md5(datasets.utils.dumps(pat)).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)


class RecurseDumpTest(TestCase):
    def test_recurse_dump_for_function(self):
        def func():
            return foo

        foo = [0]
        hash1 = md5(datasets.utils.dumps(func)).hexdigest()
        foo = [1]
        hash2 = md5(datasets.utils.dumps(func)).hexdigest()
        foo = [0]
        hash3 = md5(datasets.utils.dumps(func)).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_recurse_dump_for_class(self):

        hash1 = md5(datasets.utils.dumps(Foo([0]))).hexdigest()
        hash2 = md5(datasets.utils.dumps(Foo([1]))).hexdigest()
        hash3 = md5(datasets.utils.dumps(Foo([0]))).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_recurse_dump_for_method(self):

        hash1 = md5(datasets.utils.dumps(Foo([0]).__call__)).hexdigest()
        hash2 = md5(datasets.utils.dumps(Foo([1]).__call__)).hexdigest()
        hash3 = md5(datasets.utils.dumps(Foo([0]).__call__)).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_dump_ipython_function(self):

        code_args = (
            "co_argcount",
            "co_kwonlyargcount",
            "co_nlocals",
            "co_stacksize",
            "co_flags",
            "co_code",
            "co_consts",
            "co_names",
            "co_varnames",
            "co_filename",
            "co_name",
            "co_firstlineno",
            "co_lnotab",
            "co_freevars",
            "co_cellvars",
        )

        def create_ipython_func(co_filename, returned_obj):
            def func():
                return returned_obj

            code = func.__code__
            code = CodeType(*[getattr(code, k) if k != "co_filename" else co_filename for k in code_args])
            return FunctionType(code, func.__globals__, func.__name__, func.__defaults__, func.__closure__)

        co_filename, returned_obj = "<ipython-input-2-e0383a102aae>", [0]
        hash1 = md5(datasets.utils.dumps(create_ipython_func(co_filename, returned_obj))).hexdigest()
        co_filename, returned_obj = "<ipython-input-2-e0383a102aae>", [1]
        hash2 = md5(datasets.utils.dumps(create_ipython_func(co_filename, returned_obj))).hexdigest()
        co_filename, returned_obj = "<ipython-input-5-713f6613acf3>", [0]
        hash3 = md5(datasets.utils.dumps(create_ipython_func(co_filename, returned_obj))).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_recurse_dump_for_function_with_shuffled_globals(self):
        foo, bar = [0], [1]

        def func():
            return foo, bar

        func.__module__ = "__main__"

        def globalvars_mock1_side_effect(func, *args, **kwargs):
            return {"foo": foo, "bar": bar}

        def globalvars_mock2_side_effect(func, *args, **kwargs):
            return {"bar": bar, "foo": foo}

        with patch("dill.detect.globalvars", side_effect=globalvars_mock1_side_effect) as globalvars_mock1:
            hash1 = md5(datasets.utils.dumps(func)).hexdigest()
            self.assertGreater(globalvars_mock1.call_count, 0)
        with patch("dill.detect.globalvars", side_effect=globalvars_mock2_side_effect) as globalvars_mock2:
            hash2 = md5(datasets.utils.dumps(func)).hexdigest()
            self.assertGreater(globalvars_mock2.call_count, 0)
        self.assertEqual(hash1, hash2)


class TypeHintDumpTest(TestCase):
    def test_dump_type_hint(self):
        from typing import Union

        t1 = Union[str, None]  # this type is not picklable in python 3.6
        # let's check that we can pickle it anyway using our pickler, even in 3.6
        hash1 = md5(datasets.utils.dumps(t1)).hexdigest()
        t2 = Union[str]  # this type is picklable in python 3.6
        hash2 = md5(datasets.utils.dumps(t2)).hexdigest()
        t3 = Union[str, None]
        hash3 = md5(datasets.utils.dumps(t3)).hexdigest()
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)
