import os
import tempfile
from pathlib import Path
from unittest import TestCase

import pyarrow as pa

from datasets.arrow_dataset import Dataset
from datasets.arrow_reader import BaseReader
from datasets.info import DatasetInfo
from datasets.splits import SplitDict, SplitInfo


class ReaderTest(BaseReader):
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
        open(os.path.join(filename), "wb").close()
        pa_table = pa.Table.from_pydict({"filename": [Path(filename).name] * 100})
        if skip is not None and take is not None:
            pa_table = pa_table.slice(skip, take)
        return pa_table


class BaseReaderTest(TestCase):
    def test_read(self):
        name = "my_name"
        train_info = SplitInfo(name="train", num_examples=100)
        test_info = SplitInfo(name="test", num_examples=100)
        split_infos = [train_info, test_info]
        split_dict = SplitDict()
        split_dict.add(train_info)
        split_dict.add(test_info)
        info = DatasetInfo(splits=split_dict)

        with tempfile.TemporaryDirectory() as tmp_dir:
            reader = ReaderTest(tmp_dir, info)

            instructions = "test[:33%]"
            dset = Dataset(**reader.read(name, instructions, split_infos))
            self.assertEqual(dset["filename"][0], f"{name}-test")
            self.assertEqual(dset.num_rows, 33)
            self.assertEqual(dset.num_columns, 1)

            instructions = ["train", "test[:33%]"]
            datasets_kwargs = [reader.read(name, instr, split_infos) for instr in instructions]
            train_dset, test_dset = [Dataset(**dataset_kwargs) for dataset_kwargs in datasets_kwargs]
            self.assertEqual(train_dset["filename"][0], f"{name}-train")
            self.assertEqual(train_dset.num_rows, 100)
            self.assertEqual(train_dset.num_columns, 1)
            self.assertEqual(test_dset["filename"][0], f"{name}-test")
            self.assertEqual(test_dset.num_rows, 33)
            self.assertEqual(test_dset.num_columns, 1)
            del train_dset, test_dset

    def test_read_files(self):
        train_info = SplitInfo(name="train", num_examples=100)
        test_info = SplitInfo(name="test", num_examples=100)
        split_dict = SplitDict()
        split_dict.add(train_info)
        split_dict.add(test_info)
        info = DatasetInfo(splits=split_dict)

        with tempfile.TemporaryDirectory() as tmp_dir:
            reader = ReaderTest(tmp_dir, info)

            files = [
                {"filename": os.path.join(tmp_dir, "train")},
                {"filename": os.path.join(tmp_dir, "test"), "skip": 10, "take": 10},
            ]
            dset = Dataset(**reader.read_files(files, original_instructions=""))
            self.assertEqual(dset.num_rows, 110)
            self.assertEqual(dset.num_columns, 1)
            self.assertEqual(dset._data_files, files)
            del dset
