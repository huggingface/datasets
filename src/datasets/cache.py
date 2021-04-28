from functools import partial
from typing import Union

from datasets import utils
from datasets.arrow_dataset import Dataset
from datasets.arrow_reader import ArrowReader, ReadInstruction
from datasets.splits import Split


class CacheManager:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir

    def _build_dataset(self, split: Union[str, ReadInstruction, Split], in_memory: bool = False, info=None, name=None):
        # By default, return all splits
        if split is None:
            split = {s: s for s in info.splits}
        # Create a dataset for each of the given splits
        datasets = utils.map_nested(
            partial(
                self._build_a_dataset,
                in_memory=in_memory,
                info=info,
                name=name,
            ),
            split,
            map_tuple=True,
        )
        return datasets

    def _build_a_dataset(
        self,
        split: Union[str, ReadInstruction, Split] = Split.TRAIN,
        in_memory: bool = False,
        info=None,
        name=None,
    ):
        """as_dataset for a single split."""
        if isinstance(split, str):
            split = Split(split)
        # Build base dataset
        dataset_kwargs = ArrowReader(self.cache_dir, info).read(
            name=name,
            instructions=split,
            split_infos=info.splits.values(),
            in_memory=in_memory,
        )
        ds = Dataset(**dataset_kwargs)
        return ds
