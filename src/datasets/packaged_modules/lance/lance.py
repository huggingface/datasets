import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class LanceConfig(datasets.BuilderConfig):
    """
    BuilderConfig for Lance format.

    Args:
        features: (`Features`, *optional*):
            Cast the data to `features`.
        columns: (`List[str]`, *optional*):
            List of columns to load, the other ones are ignored.
        batch_size: (`int`, *optional*):
            Size of the RecordBatches to iterate on.
    """

    features: Optional[datasets.Features] = None
    columns: Optional[List[str]] = None
    batch_size: Optional[int] = None

    def __post_init__(self):
        return super().__post_init__()


class _LanceSnapshotDataset:
    """Reconstruct a Lance dataset from huggingface snapshot"""

    def __init__(self, paths: List[datasets.utils.track.tracked_str], version: Optional[int] = None):
        self._dataset_version = version

        # Reconstruct a temporary dataset directory
        self.temp_root = tempfile.TemporaryDirectory(delete=True)
        self.dataset_uri = Path(self.temp_root.name)
        (self.dataset_uri / "data").mkdir(parents=True, exist_ok=True)
        (self.dataset_uri / "_versions").mkdir(parents=True, exist_ok=True)
        (self.dataset_uri / "_transactions").mkdir(parents=True, exist_ok=True)

        # Reconstruct the dataset
        for p in paths:
            original_path = Path(p.get_origin())
            parent_dir = original_path.parent.name
            if parent_dir == "data":
                (self.dataset_uri / "data" / original_path.name).symlink_to(p)
            elif parent_dir == "_transactions":
                (self.dataset_uri / "_transactions" / original_path.name).symlink_to(p)
            elif parent_dir == "_indices":
                (self.dataset_uri / "_indices" / original_path.name).symlink_to(p)
            elif parent_dir == "_versions":
                shutil.copyfile(p, self.dataset_uri / "_versions" / original_path.name)

    def get_fragments(self) -> List["LanceFragment"]:
        import lance

        ds = lance.LanceDataset(self.dataset_uri.as_posix(), version=self._dataset_version)
        for fragment in ds.get_fragments():
            yield fragment


def _group_by_dataset(files: Iterable[str]) -> Dict[str, List[str]]:
    files_per_dataset = defaultdict(list)
    for file_path in files:
        path = Path(file_path)
        dataset_root = path.parent.parent
        if dataset_root.suffix == ".lance":
            files_per_dataset[str(dataset_root)].append(file_path)
    return files_per_dataset


class Lance(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = LanceConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        dl_manager.download_config.extract_on_the_fly = True

        splits = []
        # if not speficied, treat whole data_files as a single split
        for split, files in self.config.data_files.items():
            dataset_paths = _group_by_dataset(files)

            all_files_to_download = list(dl_manager.iter_files(list(dataset_paths.keys())))
            local_dataset_paths = _group_by_dataset(dl_manager.iter_files(dl_manager.download(all_files_to_download)))
            local_datasets = []
            for paths in local_dataset_paths.values():
                ds = _LanceSnapshotDataset(paths)
                local_datasets.append(ds)
            splits.append(datasets.SplitGenerator(name=split, gen_kwargs={"paths": local_datasets}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, paths: List[_LanceSnapshotDataset]):
        for ds in paths:
            for frag_idx, fragment in enumerate(ds.get_fragments()):
                for batch_idx, batch in enumerate(
                    fragment.to_batches(columns=self.config.columns, batch_size=self.config.batch_size)
                ):
                    table = pa.Table.from_batches([batch])
                    table = self._cast_table(table)
                    yield Key(frag_idx, batch_idx), table
