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
        token: (`str`, *optional*):
            Optional HF token to use to download datasets.
    """

    features: Optional[datasets.Features] = None
    columns: Optional[List[str]] = None
    batch_size: Optional[int] = None
    token: Optional[str] = None

    def __post_init__(self):
        return super().__post_init__()


class _LanceDataset:
    """Reconstruct a Lance dataset from huggingface snapshot or remote files.

    TODO: support sharding
    """

    def __init__(
        self,
        paths: List[datasets.utils.track.tracked_str],
        streaming: bool = False,
        dataset_uri: Optional[str] = None,
        token: Optional[str] = None,
        version: Optional[int] = None,
    ):
        self._paths = paths
        self._dataset_version = version
        self._streaming = streaming
        self._dataset_uri = dataset_uri
        self._hf_token = token

    def __repr__(self):
        return "_HfLanceDataset(uri={}, streaming={})".format(self._dataset_uri, self._streaming)

    def _open_local_dataset(self) -> "lance.LanceDataset":
        import lance

        # Reconstruct a temporary dataset directory
        self.temp_root = tempfile.TemporaryDirectory(delete=True)
        self.dataset_uri = Path(self.temp_root.name)
        (self.dataset_uri / "data").mkdir(parents=True, exist_ok=True)
        (self.dataset_uri / "_versions").mkdir(parents=True, exist_ok=True)
        (self.dataset_uri / "_transactions").mkdir(parents=True, exist_ok=True)

        # Reconstruct the dataset
        for p in self._paths:
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
        return lance.dataset(self.dataset_uri.as_posix(), version=self._dataset_version)

    def _open_streaming_dataset(self) -> "lance.LanceDataset":
        import lance

        storage_opts = {"token": self._hf_token} if self._hf_token else {}
        return lance.dataset(self._dataset_uri, version=self._dataset_version, storage_options=storage_opts)

    def get_fragments(self) -> List["LanceFragment"]:
        if self._streaming:
            ds = self._open_streaming_dataset()
        else:
            ds = self._open_local_dataset()
        # TODO: filter fragments based on the provided data files
        for fragment in ds.get_fragments():
            yield fragment


def _group_by_dataset(files: Iterable[str]) -> Dict[str, List[str]]:
    files_per_dataset = defaultdict(list)
    for file_path in files:
        path = Path(file_path)
        if path.parent.name in {"data", "_transactions", "_indices", "_versions"}:
            dataset_root = path.parent.parent
            files_per_dataset[str(dataset_root)].append(file_path)
    return files_per_dataset


class Lance(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = LanceConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _get_features(self, ds: _LanceDataset) -> datasets.Features:
        if self.info.features is None:
            pa_schema = ds._open_local_dataset().schema if not ds._streaming else ds._open_streaming_dataset().schema
            if self.config.columns:
                fields = [
                    pa_schema.field(name) for name in self.config.columns if pa_schema.get_field_index(name) != -1
                ]
                pa_schema = pa.schema(fields)
            return datasets.Features.from_arrow_schema(pa_schema)
        return self.info.features

    def _split_generators(self, dl_manager):
        dl_manager.download_config.extract_on_the_fly = True

        splits = []
        for split, files in self.config.data_files.items():
            dataset_paths = _group_by_dataset(files)

            is_streaming = getattr(dl_manager, "is_streaming", False)

            datasets_per_split = []
            if is_streaming:
                # STREAMING MODE
                for dataset_root, file_list in dataset_paths.items():
                    data_files = [f for f in file_list if "/data/" in f]
                    # TODO: support revision
                    if "@" in dataset_root:
                        # temporarily remove the revision from the dataset root
                        dataset_root = dataset_root.split("@")[0]

                    streaming_ds = _LanceDataset(
                        data_files,
                        dataset_uri=dataset_root,
                        streaming=True,
                        token=self.config.token,
                    )
                    if self.info.features is None:
                        self.info.features = self._get_features(streaming_ds)
                    datasets_per_split.append(streaming_ds)
            else:
                # NON-STREAMING MODE: Download files (existing behavior)
                all_files_to_download = list(dl_manager.iter_files(list(dataset_paths.keys())))
                local_dataset_paths = _group_by_dataset(
                    dl_manager.iter_files(dl_manager.download(all_files_to_download))
                )
                for paths in local_dataset_paths.values():
                    ds = _LanceDataset(paths, streaming=False, token=self.config.token)
                    datasets_per_split.append(ds)
            splits.append(
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={"datasets": datasets_per_split},
                )
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, datasets: List[_LanceDataset]):
        for ds in datasets:
            for frag_idx, fragment in enumerate(ds.get_fragments()):
                for batch_idx, batch in enumerate(
                    fragment.to_batches(columns=self.config.columns, batch_size=self.config.batch_size)
                ):
                    table = pa.Table.from_batches([batch])
                    yield Key(frag_idx, batch_idx), self._cast_table(table)
