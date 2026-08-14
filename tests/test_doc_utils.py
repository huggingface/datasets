import unittest

from datasets.utils.doc_utils import is_documented_by


class DocUtilsTest(unittest.TestCase):
    def test_is_documented_by_copies_docstring(self):
        def source_func():
            """This is a sample docstring for testing."""
            pass

        @is_documented_by(source_func)
        def target_func():
            pass

        self.assertEqual(target_func.__doc__, source_func.__doc__)

    def test_is_documented_by_callable(self):
        def source_func():
            """Calculate sum of two numbers."""
            pass

        @is_documented_by(source_func)
        def add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(add.__doc__, "Calculate sum of two numbers.")
        self.assertEqual(add(2, 3), 5)

    def test_is_documented_by_none_docstring(self):
        def source_without_doc():
            pass

        @is_documented_by(source_without_doc)
        def target_func():
            """Initial docstring"""
            pass

        self.assertIsNone(target_func.__doc__)
