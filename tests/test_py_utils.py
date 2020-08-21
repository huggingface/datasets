from unittest import TestCase

from nlp.utils.py_utils import (
    flatten_nest_dict,
    flatten_nested,
    map_nested,
    temporary_assignment,
    zip_dict,
    zip_nested,
)


class PyUtilsTest(TestCase):
    def test_flatten_nest_dict(self):
        d1 = {}
        d2 = {"a": 1, "b": 2}
        d3 = {"a": {"1": 1, "2": 2}, "b": 3}
        expected_flatten_d1 = {}
        expected_flatten_d2 = {"a": 1, "b": 2}
        expected_flatten_d3 = {"a/1": 1, "a/2": 2, "b": 3}
        self.assertDictEqual(flatten_nest_dict(d1), expected_flatten_d1)
        self.assertDictEqual(flatten_nest_dict(d2), expected_flatten_d2)
        self.assertDictEqual(flatten_nest_dict(d3), expected_flatten_d3)

    def test_flatten_nested(self):
        s1 = {}
        s2 = []
        s3 = "foo"
        s4 = ["foo", "bar"]
        s5 = {"a": 1, "b": 2}
        s6 = {"a": [1, 2], "b": [3, 4]}
        s7 = {"a": {"1": 1}, "b": 2}
        expected_flatten_nested_s1 = []
        expected_flatten_nested_s2 = []
        expected_flatten_nested_s3 = ["foo"]
        expected_flatten_nested_s4 = ["foo", "bar"]
        expected_flatten_nested_s5 = [1, 2]
        expected_flatten_nested_s6 = [1, 2, 3, 4]
        expected_flatten_nested_s7 = [1, 2]
        self.assertEqual(flatten_nested(s1), expected_flatten_nested_s1)
        self.assertEqual(flatten_nested(s2), expected_flatten_nested_s2)
        self.assertEqual(flatten_nested(s3), expected_flatten_nested_s3)
        self.assertEqual(flatten_nested(s4), expected_flatten_nested_s4)
        self.assertEqual(flatten_nested(s5), expected_flatten_nested_s5)
        self.assertEqual(flatten_nested(s6), expected_flatten_nested_s6)
        self.assertEqual(flatten_nested(s7), expected_flatten_nested_s7)

    def test_map_mested(self):
        def add_one(i):
            return i + 1

        s1 = {}
        s2 = []
        s3 = 1
        s4 = [1, 2]
        s5 = {"a": 1, "b": 2}
        s6 = {"a": [1, 2], "b": [3, 4]}
        s7 = {"a": {"1": 1}, "b": 2}
        expected_map_nested_s1 = {}
        expected_map_nested_s2 = []
        expected_map_nested_s3 = 2
        expected_map_nested_s4 = [2, 3]
        expected_map_nested_s5 = {"a": 2, "b": 3}
        expected_map_nested_s6 = {"a": [2, 3], "b": [4, 5]}
        expected_map_nested_s7 = {"a": {"1": 2}, "b": 3}
        self.assertEqual(map_nested(add_one, s1), expected_map_nested_s1)
        self.assertEqual(map_nested(add_one, s2), expected_map_nested_s2)
        self.assertEqual(map_nested(add_one, s3), expected_map_nested_s3)
        self.assertEqual(map_nested(add_one, s4), expected_map_nested_s4)
        self.assertEqual(map_nested(add_one, s5), expected_map_nested_s5)
        self.assertEqual(map_nested(add_one, s6), expected_map_nested_s6)
        self.assertEqual(map_nested(add_one, s7), expected_map_nested_s7)

    def test_zip_dict(self):
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 3, "b": 4}
        d3 = {"a": 5, "b": 6}
        expected_zip_dict_result = sorted([("a", (1, 3, 5)), ("b", (2, 4, 6))])
        self.assertEqual(sorted(list(zip_dict(d1, d2, d3))), expected_zip_dict_result)

    def test_zip_nested(self):
        d1 = {"a": {"1": 1}, "b": 2}
        d2 = {"a": {"1": 3}, "b": 4}
        expected_zip_nested_result = {"a": {"1": (1, 3)}, "b": (2, 4)}
        self.assertDictEqual(zip_nested(d1, d2), expected_zip_nested_result)

    def test_temporary_assignment(self):
        class Foo:
            my_attr = "bar"

        foo = Foo()
        self.assertEqual(foo.my_attr, "bar")
        with temporary_assignment(foo, "my_attr", "BAR"):
            self.assertEqual(foo.my_attr, "BAR")
        self.assertEqual(foo.my_attr, "bar")
