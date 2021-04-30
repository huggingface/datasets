import os
from functools import partial
from typing import Union

from datasets import utils
from datasets.arrow_dataset import Dataset
from datasets.arrow_reader import ArrowReader, ReadInstruction
from datasets.arrow_writer import ArrowWriter
from datasets.splits import Split
from datasets.utils.logging import WARNING, get_logger


logger = get_logger(__name__)


class DatasetCacheManager:
    def __init__(self, cache_dir=None, writer_batch_size=None):
        self.cache_dir = cache_dir
        self.writer_batch_size = writer_batch_size

    def load(self, split: Union[str, ReadInstruction, Split], in_memory: bool = False, info=None, name=None):
        """
        Load cached preprocessed Dataset.

        Args:
            split (:class:`Split` or :class:`ReadInstruction` or :obj:`str`): Which split of the Dataset to load.
            in_memory (:obj:`bool`, default ``False``): Whether to copy the dataset in-memory.
            info (:class:`DatasetInfo`, optional): Information about the Dataset.
            name (:obj:`str`, optional): Dataset name.

        Returns:
            :class:`DatasetDict`
        """
        # By default, return all splits
        if split is None:
            split = {s: s for s in info.splits}
        # Load a dataset for each of the given splits
        datasets = utils.map_nested(
            partial(
                self._load_one,
                in_memory=in_memory,
                info=info,
                name=name,
            ),
            split,
            map_tuple=True,
        )
        return datasets

    def _load_one(
        self,
        split: Union[str, ReadInstruction, Split] = Split.TRAIN,
        in_memory: bool = False,
        info=None,
        name=None,
    ):
        """Load a single split."""
        if isinstance(split, str):
            split = Split(split)
        # Read Arrow dataset
        dataset_kwargs = ArrowReader(self.cache_dir, info).read(
            name=name,
            instructions=split,
            split_infos=info.splits.values(),
            in_memory=in_memory,
        )
        ds = Dataset(**dataset_kwargs)
        return ds

    def save(self, generator, split_generator_name, total=None, name=None, info=None, tmp_cache_dir=None):
        # TODO: tmp_cache_dir instead of self.cache_dir because of:
        #  with utils.temporary_assignment(self, "_cache_dir", tmp_data_dir)
        fname = "{}-{}.arrow".format(name, split_generator_name)
        fpath = os.path.join(tmp_cache_dir, fname)
        not_verbose = bool(logger.getEffectiveLevel() > WARNING)
        with ArrowWriter(features=info.features, path=fpath, writer_batch_size=self.writer_batch_size) as writer:
            try:
                for key, record in utils.tqdm(
                    generator, unit=" examples", total=total, leave=False, disable=not_verbose
                ):
                    example = info.features.encode_example(record)
                    writer.write(example)
            finally:
                num_examples, num_bytes = writer.finalize()
        return num_bytes, num_examples
