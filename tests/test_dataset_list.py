from unittest import TestCase

from datasets import List, Value
from datasets.arrow_dataset import Dataset


class DatasetListTest(TestCase):
    def _create_example_records(self):
        return [
            {"col_1": 3, "col_2": "a"},
            {"col_1": 2, "col_2": "b"},
            {"col_1": 1, "col_2": "c"},
            {"col_1": 0, "col_2": "d"},
        ]

    def _create_example_dict(self):
        data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
        return Dataset.from_dict(data)

    def test_create(self):
        example_records = self._create_example_records()
        dset = Dataset.from_list(example_records)
        self.assertListEqual(dset.column_names, ["col_1", "col_2"])
        for i, r in enumerate(dset):
            self.assertDictEqual(r, example_records[i])

    def test_list_dict_equivalent(self):
        example_records = self._create_example_records()
        dset = Dataset.from_list(example_records)
        dset_from_dict = Dataset.from_dict({k: [r[k] for r in example_records] for k in example_records[0]})
        self.assertEqual(dset.info, dset_from_dict.info)

    def test_uneven_records(self):  # checks what happens with missing columns
        uneven_records = [{"col_1": 1}, {"col_2": "x"}]
        dset = Dataset.from_list(uneven_records)
        self.assertDictEqual(dset[0], {"col_1": 1})
        self.assertDictEqual(dset[1], {"col_1": None})  # NB: first record is used for columns

    def test_variable_list_records(self):  # checks if the type can be inferred from the second record
        list_records = [{"col_1": []}, {"col_1": [1, 2]}]
        dset = Dataset.from_list(list_records)
        self.assertEqual(dset.info.features["col_1"], List(Value("int64")))

    def test_create_empty(self):
        dset = Dataset.from_list([])
        self.assertEqual(len(dset), 0)
        self.assertListEqual(dset.column_names, [])

    def test_create_empty_records(self):
        dset = Dataset.from_list([{}, {}])
        self.assertEqual(len(dset), 2)
        self.assertListEqual(dset.column_names, [])
        self.assertListEqual(dset.to_list(), [{}, {}])

    def test_create_single_empty_record(self):
        dset = Dataset.from_list([{}])
        self.assertEqual(len(dset), 1)
        self.assertDictEqual(dset[0], {})

    def test_create_empty_records_map_and_filter(self):
        dset = Dataset.from_list([{}, {}, {}])
        self.assertEqual(len(dset.map(lambda example: {})), 3)
        self.assertEqual(len(dset.map(lambda example: {"a": 1})), 3)
        self.assertEqual(len(dset.filter(lambda example: True)), 3)
        self.assertEqual(len(dset.filter(lambda example: False)), 0)

    def test_create_empty_records_save_and_load(self):
        import tempfile

        dset = Dataset.from_list([{}, {}, {}])
        with tempfile.TemporaryDirectory() as temp_dir:
            dset.save_to_disk(temp_dir)
            reloaded = Dataset.load_from_disk(temp_dir)
        self.assertEqual(len(reloaded), 3)
        self.assertListEqual(reloaded.to_list(), [{}, {}, {}])
