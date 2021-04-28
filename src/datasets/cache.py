from typing import Union

from datasets.arrow_dataset import Dataset
from datasets.arrow_reader import ArrowReader, ReadInstruction
from datasets.splits import Split


class CacheManager:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir

    def _as_dataset(
        self,
        split: Union[ReadInstruction, Split] = Split.TRAIN,
        in_memory: bool = False,
        info=None,
        name=None,
    ) -> Dataset:
        """Constructs a `Dataset`.

        This is the internal implementation to overwrite called when user calls
        `as_dataset`. It should read the pre-processed datasets files and generate
        the `Dataset` object.

        Args:
            split: `datasets.Split` which subset of the data to read.
            in_memory (bool, default False): Whether to copy the data in-memory.

        Returns:
            `Dataset`
        """

        dataset_kwargs = ArrowReader(self.cache_dir, info).read(
            name=name,
            instructions=split,
            split_infos=info.splits.values(),
            in_memory=in_memory,
        )
        return Dataset(**dataset_kwargs)
