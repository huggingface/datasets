import fsspec.asyn
import torch

from ...iterable_dataset import IterableDataset, _apply_feature_types
from ...utils.logging import get_logger


logger = get_logger(__name__)


def _set_fsspec_for_multiprocess() -> None:
    """
    Clear reference to the loop and thread.
    This is necessary otherwise HTTPFileSystem hangs in the ML training loop.
    Only required for fsspec >= 0.9.0
    See https://github.com/fsspec/gcsfs/issues/379
    """
    fsspec.asyn.iothread[0] = None
    fsspec.asyn.loop[0] = None


class TorchIterableDataset(IterableDataset, torch.utils.data.IterableDataset):
    def __iter__(self):
        # fix for fsspec when using multprocess
        _set_fsspec_for_multiprocess()
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:  # single-process data loading, return the full iterator
            yield from IterableDataset.__iter__(self)
        else:  # in a worker process
            # check if there aren't too many workers
            if worker_info.id == 0 and self.n_shards < worker_info.num_workers:
                logger.warning(
                    f"Too many dataloader workers: {worker_info.num_workers} (max is dataset.n_shards={self.n_shards}). "
                    f"Stopping dataloader workers [{self.n_shards}...{worker_info.num_workers -1}]."
                )
                logger.warning(
                    f"To parallelize data loading, we give each process some shards (or data sources) to process. "
                    f"Therefore it's unnecessary to have a number of workers greater than dataset.n_shards={self.n_shards}."
                    f"To enable more parallelism, please split the dataset in more files than {self.n_shards}."
                )
            # split workload
            shards_indices = list(range(worker_info.id, self.n_shards, worker_info.num_workers))
            if shards_indices:
                logger.debug(
                    f"dataloader worker#{worker_info.id}, ': Starting to iterate over {len(shards_indices)}/{self.n_shards} shards."
                )
                for shard_idx in shards_indices:
                    for key, example in self._iter_shard(shard_idx):
                        if self.features:
                            yield _apply_feature_types(
                                example, self.features, token_per_repo_id=self._token_per_repo_id
                            )
                        else:
                            yield example
                logger.debug(
                    f"dataloader worker#{worker_info.id}, ': Finished iterating over {len(shards_indices)}/{self.n_shards} shards."
                )
            else:
                logger.debug(
                    f"dataloader worker#{worker_info.id}, ': Stopping... Number of dataset shards < num_workers ({self.n_shards}<{worker_info.num_workers})."
                )
