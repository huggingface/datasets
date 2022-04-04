import torch

from ...iterable_dataset import IterableDataset
from ...utils.logging import get_logger


logger = get_logger(__name__)


class TorchIterableDataset(IterableDataset, torch.utils.data.IterableDataset):
    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:  # single-process data loading, return the full iterator
            yield from IterableDataset.__iter__(self)
        else:  # in a worker process
            # split workload
            shards_indices = list(range(worker_info.id, self.n_shards, worker_info.num_workers))
            if shards_indices:
                for shard_idx in shards_indices:
                    for key, example in self._iter_shard(shard_idx):
                        yield self._apply_feature_types(example)
                logger.warning(
                    f"worker#{worker_info.id}, ': Stopping... Finished iterating over {len(shards_indices)} shards."
                )
            else:
                logger.warning(f"worker#{worker_info.id}, ': Stopping... Number of shards < num_workers.")
