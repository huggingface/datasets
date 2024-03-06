import os
import tempfile
from pathlib import Path
from unittest import TestCase

import pyarrow as pa
import pytest

from datasets.arrow_dataset import Dataset
from datasets.arrow_reader import ArrowReader, BaseReader, FileInstructions, ReadInstruction, make_file_instructions
from datasets.info import DatasetInfo
from datasets.splits import NamedSplit, Split, SplitDict, SplitInfo

from .utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases


class ReaderTest(BaseReader):
    """
    Build a Dataset object out of Instruction instance(s).
    This reader is made for testing. It mocks file reads.
    """

    def _get_table_from_filename(self, filename_skip_take, in_memory=False):
        """Returns a Dataset instance from given (filename, skip, take)."""
        filename, skip, take = (
            filename_skip_take["filename"],
            filename_skip_take["skip"] if "skip" in filename_skip_take else None,
            filename_skip_take["take"] if "take" in filename_skip_take else None,
        )
        open(os.path.join(filename), "wb").close()
        pa_table = pa.Table.from_pydict({"filename": [Path(filename).name] * 100})
        if take == -1:
            take = len(pa_table) - skip
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

            instructions1 = ["train", "test[:33%]"]
            instructions2 = [Split.TRAIN, ReadInstruction.from_spec("test[:33%]")]
            for instructions in [instructions1, instructions2]:
                datasets_kwargs = [reader.read(name, instr, split_infos) for instr in instructions]
                train_dset, test_dset = (Dataset(**dataset_kwargs) for dataset_kwargs in datasets_kwargs)
                self.assertEqual(train_dset["filename"][0], f"{name}-train")
                self.assertEqual(train_dset.num_rows, 100)
                self.assertEqual(train_dset.num_columns, 1)
                self.assertIsInstance(train_dset.split, NamedSplit)
                self.assertEqual(str(train_dset.split), "train")
                self.assertEqual(test_dset["filename"][0], f"{name}-test")
                self.assertEqual(test_dset.num_rows, 33)
                self.assertEqual(test_dset.num_columns, 1)
                self.assertIsInstance(test_dset.split, NamedSplit)
                self.assertEqual(str(test_dset.split), "test[:33%]")
                del train_dset, test_dset

    def test_read_sharded(self):
        name = "my_name"
        train_info = SplitInfo(name="train", num_examples=1000, shard_lengths=[100] * 10)
        split_infos = [train_info]
        split_dict = SplitDict()
        split_dict.add(train_info)
        info = DatasetInfo(splits=split_dict)

        with tempfile.TemporaryDirectory() as tmp_dir:
            reader = ReaderTest(tmp_dir, info)

            instructions = "train[:33%]"
            dset = Dataset(**reader.read(name, instructions, split_infos))
            self.assertEqual(dset["filename"][0], f"{name}-train-00000-of-00010")
            self.assertEqual(dset["filename"][-1], f"{name}-train-00003-of-00010")
            self.assertEqual(dset.num_rows, 330)
            self.assertEqual(dset.num_columns, 1)

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
            dset = Dataset(**reader.read_files(files, original_instructions="train+test[10:20]"))
            self.assertEqual(dset.num_rows, 110)
            self.assertEqual(dset.num_columns, 1)
            del dset


@pytest.mark.parametrize("in_memory", [False, True])
def test_read_table(in_memory, dataset, arrow_file):
    filename = arrow_file
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        table = ArrowReader.read_table(filename, in_memory=in_memory)
    assert table.shape == dataset.data.shape
    assert set(table.column_names) == set(dataset.data.column_names)
    assert dict(table.to_pydict()) == dict(dataset.data.to_pydict())  # to_pydict returns OrderedDict


@pytest.mark.parametrize("in_memory", [False, True])
def test_read_files(in_memory, dataset, arrow_file):
    filename = arrow_file
    reader = ArrowReader("", None)
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset_kwargs = reader.read_files([{"filename": filename}], in_memory=in_memory)
    assert dataset_kwargs.keys() == {"arrow_table", "info", "split"}
    table = dataset_kwargs["arrow_table"]
    assert table.shape == dataset.data.shape
    assert set(table.column_names) == set(dataset.data.column_names)
    assert dict(table.to_pydict()) == dict(dataset.data.to_pydict())  # to_pydict returns OrderedDict


def test_read_instruction_spec():
    assert ReadInstruction("train", to=10, unit="abs").to_spec() == "train[:10]"
    assert ReadInstruction("train", from_=-80, to=10, unit="%").to_spec() == "train[-80%:10%]"

    spec_train_test = "train+test"
    assert ReadInstruction.from_spec(spec_train_test).to_spec() == spec_train_test

    spec_train_abs = "train[2:10]"
    assert ReadInstruction.from_spec(spec_train_abs).to_spec() == spec_train_abs

    spec_train_pct = "train[15%:-20%]"
    assert ReadInstruction.from_spec(spec_train_pct).to_spec() == spec_train_pct

    spec_train_pct_rounding = "train[:10%](closest)"
    assert ReadInstruction.from_spec(spec_train_pct_rounding).to_spec() == "train[:10%]"

    spec_train_pct_rounding = "train[:10%](pct1_dropremainder)"
    assert ReadInstruction.from_spec(spec_train_pct_rounding).to_spec() == spec_train_pct_rounding

    spec_train_test_pct_rounding = "train[:10%](pct1_dropremainder)+test[-10%:](pct1_dropremainder)"
    assert ReadInstruction.from_spec(spec_train_test_pct_rounding).to_spec() == spec_train_test_pct_rounding


def test_make_file_instructions_basic():
    name = "dummy"
    split_infos = [SplitInfo(name="train", num_examples=100)]
    instruction = "train[:33%]"
    filetype_suffix = "arrow"
    prefix_path = "prefix"

    file_instructions = make_file_instructions(name, split_infos, instruction, filetype_suffix, prefix_path)
    assert isinstance(file_instructions, FileInstructions)
    assert file_instructions.num_examples == 33
    assert file_instructions.file_instructions == [
        {"filename": os.path.join(prefix_path, f"{name}-train.arrow"), "skip": 0, "take": 33}
    ]

    split_infos = [SplitInfo(name="train", num_examples=100, shard_lengths=[10] * 10)]
    file_instructions = make_file_instructions(name, split_infos, instruction, filetype_suffix, prefix_path)
    assert isinstance(file_instructions, FileInstructions)
    assert file_instructions.num_examples == 33
    assert file_instructions.file_instructions == [
        {"filename": os.path.join(prefix_path, f"{name}-train-00000-of-00010.arrow"), "skip": 0, "take": -1},
        {"filename": os.path.join(prefix_path, f"{name}-train-00001-of-00010.arrow"), "skip": 0, "take": -1},
        {"filename": os.path.join(prefix_path, f"{name}-train-00002-of-00010.arrow"), "skip": 0, "take": -1},
        {"filename": os.path.join(prefix_path, f"{name}-train-00003-of-00010.arrow"), "skip": 0, "take": 3},
    ]


@pytest.mark.parametrize(
    "split_name, instruction, shard_lengths, read_range",
    [
        ("train", "train[-20%:]", 100, (80, 100)),
        ("train", "train[:200]", 100, (0, 100)),
        ("train", "train[:-200]", 100, None),
        ("train", "train[-200:]", 100, (0, 100)),
        ("train", "train[-20%:]", [10] * 10, (80, 100)),
        ("train", "train[:200]", [10] * 10, (0, 100)),
        ("train", "train[:-200]", [10] * 10, None),
        ("train", "train[-200:]", [10] * 10, (0, 100)),
    ],
)
def test_make_file_instructions(split_name, instruction, shard_lengths, read_range):
    name = "dummy"
    split_infos = split_infos = [
        SplitInfo(
            name="train",
            num_examples=shard_lengths if not isinstance(shard_lengths, list) else sum(shard_lengths),
            shard_lengths=shard_lengths if isinstance(shard_lengths, list) else None,
        )
    ]
    filetype_suffix = "arrow"
    prefix_path = "prefix"
    file_instructions = make_file_instructions(name, split_infos, instruction, filetype_suffix, prefix_path)
    assert isinstance(file_instructions, FileInstructions)
    assert file_instructions.num_examples == (read_range[1] - read_range[0] if read_range is not None else 0)
    if read_range is None:
        assert file_instructions.file_instructions == []
    else:
        if not isinstance(shard_lengths, list):
            assert file_instructions.file_instructions == [
                {
                    "filename": os.path.join(prefix_path, f"{name}-{split_name}.arrow"),
                    "skip": read_range[0],
                    "take": read_range[1] - read_range[0],
                }
            ]
        else:
            file_instructions_list = []
            shard_offset = 0
            for i, shard_length in enumerate(shard_lengths):
                filename = os.path.join(prefix_path, f"{name}-{split_name}-{i:05d}-of-{len(shard_lengths):05d}.arrow")
                if shard_offset <= read_range[0] < shard_offset + shard_length:
                    file_instructions_list.append(
                        {
                            "filename": filename,
                            "skip": read_range[0] - shard_offset,
                            "take": read_range[1] - read_range[0]
                            if read_range[1] < shard_offset + shard_length
                            else -1,
                        }
                    )
                elif shard_offset < read_range[1] <= shard_offset + shard_length:
                    file_instructions_list.append(
                        {
                            "filename": filename,
                            "skip": 0,
                            "take": read_range[1] - shard_offset
                            if read_range[1] < shard_offset + shard_length
                            else -1,
                        }
                    )
                elif read_range[0] < shard_offset and read_range[1] > shard_offset + shard_length:
                    file_instructions_list.append(
                        {
                            "filename": filename,
                            "skip": 0,
                            "take": -1,
                        }
                    )
                shard_offset += shard_length
            assert file_instructions.file_instructions == file_instructions_list


@pytest.mark.parametrize("name, expected_exception", [(None, TypeError), ("", ValueError)])
def test_make_file_instructions_raises(name, expected_exception):
    split_infos = [SplitInfo(name="train", num_examples=100)]
    instruction = "train"
    filetype_suffix = "arrow"
    prefix_path = "prefix_path"
    with pytest.raises(expected_exception):
        _ = make_file_instructions(name, split_infos, instruction, filetype_suffix, prefix_path)
