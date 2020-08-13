# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
""" Arrow ArrowReader."""

import copy
import logging
import math
import os
import re
import shutil
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

import pyarrow as pa
import pyarrow.parquet

from .naming import filename_for_dataset_split
from .utils import cached_path


if TYPE_CHECKING:
    from .info import DatasetInfo  # noqa: F401


logger = logging.getLogger(__name__)

_BUFFER_SIZE = 8 << 20  # 8 MiB per file.
HF_GCP_BASE_URL = "https://storage.googleapis.com/huggingface-nlp/cache/datasets"

_SUB_SPEC_RE = re.compile(
    r"""
^
 (?P<split>\w+)
 (\[
    ((?P<from>-?\d+)
     (?P<from_pct>%)?)?
    :
    ((?P<to>-?\d+)
     (?P<to_pct>%)?)?
 \])?
$
""",
    re.X,
)

_ADDITION_SEP_RE = re.compile(r"\s*\+\s*")


class DatasetNotOnHfGcs(ConnectionError):
    """When you can't get the dataset from the Hf google cloud storage"""

    pass


class MissingFilesOnHfGcs(ConnectionError):
    """When some files are missing on the Hf oogle cloud storage"""

    pass


@dataclass(frozen=True)
class FileInstructions:
    """The file instructions associated with a split ReadInstruction.

    Attributes:
        num_examples: `int`, The total number of examples
        file_instructions: List[dict(filename, skip, take)], the files information.
            The filenames contains the relative path, not absolute.
            skip/take indicates which example read in the file: `ds.slice(skip, take)`
    """

    num_examples: int
    file_instructions: List[dict]


def make_file_instructions(name, split_infos, instruction, filetype_suffix=None):
    """Returns instructions of the split dict.

    Args:
        name: Name of the dataset.
        split_infos: `List[SplitInfo]`, Dataset splits information
        instruction: `ReadInstruction` or `str`
        filetype_suffix: `Optional[str]` suffix of dataset files, e.g. 'arrow' or 'parquet'

    Returns:
        file_intructions: FileInstructions instance
    """
    name2len = {info.name: info.num_examples for info in split_infos}
    if not isinstance(instruction, ReadInstruction):
        instruction = ReadInstruction.from_spec(instruction)
    # Create the absolute instruction (per split)
    absolute_instructions = instruction.to_absolute(name2len)

    return _make_file_instructions_from_absolutes(
        name=name, name2len=name2len, absolute_instructions=absolute_instructions, filetype_suffix=filetype_suffix
    )


def _make_file_instructions_from_absolutes(name, name2len, absolute_instructions, filetype_suffix=None):
    """Returns the files instructions from the absolute instructions list."""
    # For each split, return the files instruction (skip/take)
    file_instructions = []
    num_examples = 0
    for abs_instr in absolute_instructions:
        length = name2len[abs_instr.splitname]
        filename = filename_for_dataset_split(
            dataset_name=name, split=abs_instr.splitname, filetype_suffix=filetype_suffix
        )
        from_ = 0 if abs_instr.from_ is None else abs_instr.from_
        to = length if abs_instr.to is None else abs_instr.to
        num_examples += to - from_
        single_file_instructions = [{"filename": filename, "skip": from_, "take": to - from_}]
        file_instructions.extend(single_file_instructions)
    return FileInstructions(num_examples=num_examples, file_instructions=file_instructions,)


class BaseReader:
    """
    Build a Dataset object out of Instruction instance(s).
    """

    def __init__(self, path: str, info: Optional["DatasetInfo"]):
        """Initializes ArrowReader.

        Args:
            path (str): path where tfrecords are stored.
            info (DatasetInfo): info about the dataset.
        """
        self._path: str = path
        self._info: Optional["DatasetInfo"] = info
        self._filetype_suffix: Optional[str] = None

    def _get_dataset_from_filename(self, filename_skip_take):
        """Returns a Dataset instance from given (filename, skip, take)."""
        raise NotImplementedError

    def _read_files(self, files, info, original_instructions) -> dict:
        """Returns Dataset for given file instructions.

        Args:
            files: List[dict(filename, skip, take)], the files information.
                The filenames contain the absolute path, not relative.
                skip/take indicates which example read in the file: `ds.slice(skip, take)`
            original_instructions: store the original instructions used to build the dataset split in the dataset
        """
        pa_batches = []
        for f_dict in files:
            pa_table: pa.Table = self._get_dataset_from_filename(f_dict)
            pa_batches.extend(pa_table.to_batches())
        if pa_batches:
            pa_table = pa.Table.from_batches(pa_batches)
        dataset_kwargs = dict(arrow_table=pa_table, data_files=files, info=info, split=original_instructions)
        return dataset_kwargs

    def get_file_instructions(self, name, instruction, split_infos):
        """Return list of dict {'filename': str, 'skip': int, 'take': int}"""
        file_instructions = make_file_instructions(
            name, split_infos, instruction, filetype_suffix=self._filetype_suffix
        )
        files = file_instructions.file_instructions
        return files

    def read(
        self, name, instructions, split_infos,
    ):
        """Returns Dataset instance(s).

        Args:
            name (str): name of the dataset.
            instructions (ReadInstruction): instructions to read.
                Instruction can be string and will then be passed to the Instruction
                constructor as it.
            split_infos (list of SplitInfo proto): the available splits for dataset.

        Returns:
             kwargs to build a single Dataset instance.
        """

        files = self.get_file_instructions(name, instructions, split_infos)
        if not files:
            msg = 'Instruction "%s" corresponds to no data!' % instructions
            raise AssertionError(msg)
        return self.read_files(files=tuple(files), original_instructions=instructions)

    def read_files(
        self, files, original_instructions=None,
    ):
        """Returns single Dataset instance for the set of file instructions.

        Args:
            files: List[dict(filename, skip, take)], the files information.
                The filenames contains the relative path, not absolute.
                skip/take indicates which example read in the file: `ds.skip().take()`
            original_instructions: store the original instructions used to build the dataset split in the dataset

        Returns:
            kwargs to build a Dataset instance.
        """
        # Prepend path to filename
        files = copy.deepcopy(files)
        for f in files:
            f.update(filename=os.path.join(self._path, f["filename"]))
        dataset_kwargs = self._read_files(files=files, info=self._info, original_instructions=original_instructions)
        return dataset_kwargs

    def download_from_hf_gcs(self, cache_dir, relative_data_dir):
        """
        Download the dataset files from the Hf GCS

        Args:
            cache_dir: `str`, the local cache directory where to save the dataset
            relative_data_dir: `str`, the relative directory of the remote files from
                the `datasets` directory on GCS.

        """
        remote_cache_dir = os.path.join(HF_GCP_BASE_URL, relative_data_dir)
        try:
            remote_dataset_info = os.path.join(remote_cache_dir, "dataset_info.json")
            downloaded_dataset_info = cached_path(remote_dataset_info)
            shutil.move(downloaded_dataset_info, os.path.join(cache_dir, "dataset_info.json"))
            if self._info is not None:
                self._info.update(self._info.from_directory(cache_dir))
        except ConnectionError:
            raise DatasetNotOnHfGcs()
        try:
            for split in self._info.splits:
                file_instructions = self.get_file_instructions(
                    name=self._info.builder_name, instruction=split, split_infos=self._info.splits.values(),
                )
                for file_instruction in file_instructions:
                    remote_prepared_filename = os.path.join(remote_cache_dir, file_instruction["filename"])
                    downloaded_prepared_filename = cached_path(remote_prepared_filename)
                    shutil.move(downloaded_prepared_filename, os.path.join(cache_dir, file_instruction["filename"]))
        except ConnectionError:
            raise MissingFilesOnHfGcs()


class ArrowReader(BaseReader):
    """
    Build a Dataset object out of Instruction instance(s).
    This Reader uses memory mapping on arrow files.
    """

    def __init__(self, path: str, info: Optional["DatasetInfo"]):
        """Initializes ArrowReader.

        Args:
            path (str): path where tfrecords are stored.
            info (DatasetInfo): info about the dataset.
        """
        super().__init__(path, info)
        self._filetype_suffix = "arrow"

    def _get_dataset_from_filename(self, filename_skip_take):
        """Returns a Dataset instance from given (filename, skip, take)."""
        filename, skip, take = (
            filename_skip_take["filename"],
            filename_skip_take["skip"] if "skip" in filename_skip_take else None,
            filename_skip_take["take"] if "take" in filename_skip_take else None,
        )
        mmap = pa.memory_map(filename)
        f = pa.ipc.open_stream(mmap)
        pa_table = f.read_all()
        if skip is not None and take is not None:
            pa_table = pa_table.slice(skip, take)
        return pa_table


class ParquetReader(BaseReader):
    """
    Build a Dataset object out of Instruction instance(s).
    This Reader uses memory mapping on parquet files.
    """

    def __init__(self, path: str, info: Optional["DatasetInfo"]):
        """Initializes ParquetReader.

        Args:
            path (str): path where tfrecords are stored.
            info (DatasetInfo): info about the dataset.
        """
        super().__init__(path, info)
        self._filetype_suffix = "parquet"

    def _get_dataset_from_filename(self, filename_skip_take):
        """Returns a Dataset instance from given (filename, skip, take)."""
        filename, skip, take = (
            filename_skip_take["filename"],
            filename_skip_take["skip"] if "skip" in filename_skip_take else None,
            filename_skip_take["take"] if "take" in filename_skip_take else None,
        )
        pa_table = pa.parquet.read_table(filename, memory_map=True)
        if skip is not None and take is not None:
            pa_table = pa_table.slice(skip, take)
        return pa_table


@dataclass(frozen=True)
class _AbsoluteInstruction:
    """A machine friendly slice: defined absolute positive boundaries."""

    splitname: str
    from_: int  # uint (starting index).
    to: int  # uint (ending index).


@dataclass(frozen=True)
class _RelativeInstruction:
    """Represents a single parsed slicing instruction, can use % and negatives."""

    splitname: str
    from_: Optional[int] = None  # int (starting index) or None if no lower boundary.
    to: Optional[int] = None  # int (ending index) or None if no upper boundary.
    unit: Optional[str] = None
    rounding: Optional[str] = None

    def __post_init__(self):
        assert self.unit is None or self.unit in ["%", "abs"]
        assert self.rounding is None or self.rounding in ["closest", "pct1_dropremainder"]
        if self.unit == "%" and self.from_ is not None and abs(self.from_) > 100:
            raise AssertionError("Percent slice boundaries must be > -100 and < 100.")
        if self.unit == "%" and self.to is not None and abs(self.to) > 100:
            raise AssertionError("Percent slice boundaries must be > -100 and < 100.")


def _str_to_relative_instruction(spec):
    """Returns ReadInstruction for given string."""
    res = _SUB_SPEC_RE.match(spec)
    if not res:
        raise AssertionError("Unrecognized instruction format: %s" % spec)
    unit = "%" if res.group("from_pct") or res.group("to_pct") else "abs"
    return ReadInstruction(
        split_name=res.group("split"),
        rounding="closest",
        from_=int(res.group("from")) if res.group("from") else None,
        to=int(res.group("to")) if res.group("to") else None,
        unit=unit,
    )


def _pct_to_abs_pct1(boundary, num_examples):
    # Using math.trunc here, since -99.5% should give -99%, not -100%.
    if num_examples < 100:
        msg = (
            'Using "pct1_dropremainder" rounding on a split with less than 100 '
            "elements is forbidden: it always results in an empty dataset."
        )
        raise AssertionError(msg)
    return boundary * math.trunc(num_examples / 100.0)


def _pct_to_abs_closest(boundary, num_examples):
    return int(round(boundary * num_examples / 100.0))


def _rel_to_abs_instr(rel_instr, name2len):
    """Returns _AbsoluteInstruction instance for given RelativeInstruction.

    Args:
        rel_instr: RelativeInstruction instance.
        name2len: dict {split_name: num_examples}.
    """
    pct_to_abs = _pct_to_abs_closest if rel_instr.rounding == "closest" else _pct_to_abs_pct1
    split = rel_instr.splitname
    if split not in name2len:
        raise ValueError('Unknown split "{}". Should be one of {}.'.format(split, list(name2len)))
    num_examples = name2len[split]
    from_ = rel_instr.from_
    to = rel_instr.to
    if rel_instr.unit == "%":
        from_ = 0 if from_ is None else pct_to_abs(from_, num_examples)
        to = num_examples if to is None else pct_to_abs(to, num_examples)
    else:
        from_ = 0 if from_ is None else from_
        to = num_examples if to is None else to
    if abs(from_) > num_examples or abs(to) > num_examples:
        msg = "Requested slice [%s:%s] incompatible with %s examples." % (from_ or "", to or "", num_examples)
        raise AssertionError(msg)
    if from_ < 0:
        from_ = num_examples + from_
    elif from_ == 0:
        from_ = None
    if to < 0:
        to = num_examples + to
    elif to == num_examples:
        to = None
    return _AbsoluteInstruction(split, from_, to)


class ReadInstruction(object):
    """Reading instruction for a dataset.

    Examples of usage:

    ```
    # The following lines are equivalent:
    ds = nlp.load_dataset('mnist', split='test[:33%]')
    ds = nlp.load_dataset('mnist', split=ReadInstruction.from_spec('test[:33%]'))
    ds = nlp.load_dataset('mnist', split=ReadInstruction('test', to=33, unit='%'))
    ds = nlp.load_dataset('mnist', split=ReadInstruction(
            'test', from_=0, to=33, unit='%'))

    # The following lines are equivalent:
    ds = nlp.load_dataset('mnist', split='test[:33%]+train[1:-1]')
    ds = nlp.load_dataset('mnist', split=ReadInstruction.from_spec(
            'test[:33%]+train[1:-1]'))
    ds = nlp.load_dataset('mnist', split=(
            ReadInstruction.('test', to=33, unit='%') +
            ReadInstruction.('train', from_=1, to=-1, unit='abs')))

    # 10-fold validation:
    tests = nlp.load_dataset(
            'mnist',
            [ReadInstruction('train', from_=k, to=k+10, unit='%')
             for k in range(0, 100, 10)])
    trains = nlp.load_dataset(
            'mnist',
            [RI('train', to=k, unit='%') + RI('train', from_=k+10, unit='%')
             for k in range(0, 100, 10)])
    ```

    """

    def _init(self, relative_instructions):
        # Private initializer.
        self._relative_instructions = relative_instructions

    @classmethod
    def _read_instruction_from_relative_instructions(cls, relative_instructions):
        """Returns ReadInstruction obj initialized with relative_instructions."""
        # Use __new__ to bypass __init__ used by public API and not conveniant here.
        result = cls.__new__(cls)
        result._init(relative_instructions)  # pylint: disable=protected-access
        return result

    def __init__(self, split_name, rounding="closest", from_=None, to=None, unit=None):
        """Initialize ReadInstruction.

        Args:
            split_name (str): name of the split to read. Eg: 'train'.
            rounding (str): The rounding behaviour to use when percent slicing is
                used. Ignored when slicing with absolute indices.
                Possible values:
                 - 'closest' (default): The specified percentages are rounded to the
                     closest value. Use this if you want specified percents to be as
                     much exact as possible.
                 - 'pct1_dropremainder': the specified percentages are treated as
                     multiple of 1%. Use this option if you want consistency. Eg:
                         len(5%) == 5 * len(1%).
                     Using this option, one might not be able to use the full set of
                     examples, if the number of those is not a multiple of 100.
            from_ (int):
            to (int): alternative way of specifying slicing boundaries. If any of
                {from_, to, unit} argument is used, slicing cannot be specified as
                string.
            unit (str): optional, one of:
                '%': to set the slicing unit as percents of the split size.
                'abs': to set the slicing unit as absolute numbers.
        """
        # This constructor is not always called. See factory method
        # `_read_instruction_from_relative_instructions`. Common init instructions
        # MUST be placed in the _init method.
        self._init([_RelativeInstruction(split_name, from_, to, unit, rounding)])

    @classmethod
    def from_spec(cls, spec):
        """Creates a ReadInstruction instance out of a string spec.

        Args:
            spec (str): split(s) + optional slice(s) to read. A slice can be
                        specified, using absolute numbers (int) or percentages (int). E.g.
                            `test`: test split.
                            `test + validation`: test split + validation split.
                            `test[10:]`: test split, minus its first 10 records.
                            `test[:10%]`: first 10% records of test split.
                            `test[:-5%]+train[40%:60%]`: first 95% of test + middle 20% of
                                                                                     train.

        Returns:
            ReadInstruction instance.
        """
        spec = str(spec)  # Need to convert to str in case of NamedSplit instance.
        subs = _ADDITION_SEP_RE.split(spec)
        if not subs:
            raise AssertionError("No instructions could be built out of %s" % spec)
        instruction = _str_to_relative_instruction(subs[0])
        return sum([_str_to_relative_instruction(sub) for sub in subs[1:]], instruction)

    def __add__(self, other):
        """Returns a new ReadInstruction obj, result of appending other to self."""
        if not isinstance(other, ReadInstruction):
            msg = "ReadInstruction can only be added to another ReadInstruction obj."
            raise AssertionError(msg)
        other_ris = other._relative_instructions  # pylint: disable=protected-access
        if self._relative_instructions[0].rounding != other_ris[0].rounding:
            raise AssertionError("It is forbidden to sum ReadInstruction instances " "with different rounding values.")
        return self._read_instruction_from_relative_instructions(self._relative_instructions + other_ris)

    def __str__(self):
        return "ReadInstruction(%s)" % self._relative_instructions

    def to_absolute(self, name2len):
        """Translate instruction into a list of absolute instructions.

        Those absolute instructions are then to be added together.

        Args:
            name2len: dict associating split names to number of examples.

        Returns:
            list of _AbsoluteInstruction instances (corresponds to the + in spec).
        """
        return [_rel_to_abs_instr(rel_instr, name2len) for rel_instr in self._relative_instructions]
