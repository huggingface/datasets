import unittest
import warnings

from datasets.utils import experimental


@experimental
def dummy_function():
    return "success"


class TestExperimentalFlag(unittest.TestCase):
    def test_experimental_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(dummy_function(), "success")
        self.assertEqual(len(w), 1)
