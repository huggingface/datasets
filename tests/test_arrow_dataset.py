from unittest import TestCase

import pyarrow as pa
import numpy as np

from nlp.arrow_reader import BaseReader
from nlp.info import DatasetInfo
from nlp.splits import SplitDict, SplitInfo


class ReaderTester(BaseReader):
    """
    Build a Dataset object out of Instruction instance(s).
    This reader is made for testing. It mocks file reads.
    """

    def _get_dataset_from_filename(self, filename_skip_take):
        """Returns a Dataset instance from given (filename, skip, take)."""
        filename, skip, take = (
            filename_skip_take["filename"],
            filename_skip_take["skip"] if "skip" in filename_skip_take else None,
            filename_skip_take["take"] if "take" in filename_skip_take else None,
        )
        pa_table = pa.Table.from_pydict({"filename": [filename + "_" + str(x) for x in np.arange(100).tolist()]})
        if skip is not None and take is not None:
            pa_table = pa_table.slice(skip, take)
        return pa_table


class BaseDatasetTest(TestCase):
    def _create_dummy_dataset(self):
        name = "my_name"
        train_info = SplitInfo(name="train", num_examples=30)
        test_info = SplitInfo(name="test", num_examples=30)
        split_infos = [train_info, test_info]
        split_dict = SplitDict()
        split_dict.add(train_info)
        split_dict.add(test_info)
        info = DatasetInfo(splits=split_dict)
        reader = ReaderTester("", info)
        dset = reader.read(name, "train", split_infos)
        return dset

    def test_map(self):
        dset = self._create_dummy_dataset()
        dset_test = dset.map(lambda x: {"name": x["filename"][:-2], "id": int(x["filename"][-1])})
        self.assertEqual(len(dset_test), 30)
        dset_test_with_indices = dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True)
        self.assertEqual(len(dset_test_with_indices), 30)

    def test_map_batched(self):
        dset = self._create_dummy_dataset()

        def map_batched(example):
            return {"filename_new": [x + "_extension" for x in example["filename"]]}

        dset_test_batched = dset.map(map_batched, batched=True)
        self.assertEqual(len(dset_test_batched), 30)

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        dset_test_with_indices_batched = dset.map(map_batched_with_indices, batched=True, with_indices=True)
        self.assertEqual(len(dset_test_with_indices_batched), 30)

    def test_remove_colums(self):
        dset = self._create_dummy_dataset()
        dset = dset.map(lambda x, i: {"name": x["filename"][:-2], "id": i}, with_indices=True)
        self.assertTrue("id" in dset[0])
        dset = dset.map(lambda x: x, remove_columns=["id"])
        self.assertTrue("id" not in dset[0])

        def map_batched_with_indices(example, idx):
            return {"filename_new": [x + "_extension_" + str(idx) for x in example["filename"]]}

        dset_test_with_indices_batched = dset.map(map_batched_with_indices, batched=True, with_indices=True)
        self.assertEqual(len(dset_test_with_indices_batched), 30)

    def test_filter(self):
        dset = self._create_dummy_dataset()
        # keep only first five examples
        dset_filter_first_five = dset.filter(lambda x, i: i < 5, with_indices=True)
        self.assertEqual(len(dset_filter_first_five), 5)

        # filter filenames with even id at the end
        dset_filter_even_num = dset.filter(lambda x: (int(x["filename"][-1]) % 2 == 0))
        self.assertEqual(len(dset_filter_even_num), 15)
