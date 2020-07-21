from unittest import TestCase

from nlp.arrow_dataset import Dataset
from nlp.features import Features, Sequence, Value


class FeaturesTest(TestCase):
    def test_from_arrow_schema_simple(self):
        data = {"a": [{"b": {"c": "text"}}] * 10, "foo": [1] * 10}
        original_features = Features({"a": {"b": {"c": Value("string")}}, "foo": Value("int64")})
        dset = Dataset.from_dict(data, features=original_features)
        new_features = Features.from_arrow_schema(dset.schema)
        new_dset = Dataset.from_dict(data, features=new_features)
        self.assertDictEqual(dset[0], new_dset[0])
        self.assertDictEqual(dset[:], new_dset[:])

    def test_from_arrow_schema_with_sequence(self):
        data = {"a": [{"b": {"c": ["text"]}}] * 10, "foo": [1] * 10}
        original_features = Features({"a": {"b": Sequence({"c": Value("string")})}, "foo": Value("int64")})
        dset = Dataset.from_dict(data, features=original_features)
        new_features = Features.from_arrow_schema(dset.schema)
        new_dset = Dataset.from_dict(data, features=new_features)
        self.assertDictEqual(dset[0], new_dset[0])
        self.assertDictEqual(dset[:], new_dset[:])
