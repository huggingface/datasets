import re
import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional

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


class _StreamingLanceDataset:
    """Handle Lance dataset access for streaming mode using hf:// URI."""

    def __init__(self, hf_dataset_uri: str, data_files: List[str], token: Optional[str] = None):
        self.hf_dataset_uri = hf_dataset_uri
        self.data_files = data_files
        self.token = token

    def _try_native_lance_open(self):
        """Try to open dataset using native Lance remote support with hf:// URI."""
        import lance

        try:
            storage_opts = {"token": self.token} if self.token else {}
            return lance.dataset(self.hf_dataset_uri, storage_options=storage_opts)
        except Exception:
            return None

    def get_fragments(self, columns: Optional[List[str]] = None, batch_size: Optional[int] = None) -> Iterator[pa.RecordBatch]:
        """Yield batches from fragments - try native hf:// first, then fallback."""
        ds = self._try_native_lance_open()
        if ds is not None:
            for fragment in ds.get_fragments():
                for batch in fragment.to_batches(columns=columns, batch_size=batch_size):
                    yield batch
            return

        # Fallback: read individual .lance files
        yield from self._read_files_directly(columns, batch_size)

    def _read_files_directly(self, columns: Optional[List[str]] = None, batch_size: Optional[int] = None) -> Iterator[pa.RecordBatch]:
        """Fallback: Read individual .lance files using LanceFileReader or Arrow IPC."""
        for file_url in self.data_files:
            if not file_url.endswith(".lance"):
                continue
            with open(file_url, "rb") as f:  # Patched to xopen in streaming mode
                content = f.read()
                yield from self._read_lance_content(content, columns)

    def _read_lance_content(self, content: bytes, columns: Optional[List[str]] = None) -> Iterator[pa.RecordBatch]:
        """Read lance file content, try LanceFileReader then Arrow IPC."""
        try:
            from lance.file import LanceFileReader

            reader = LanceFileReader.from_bytes(content)
            table = reader.read_all(columns=columns) if columns else reader.read_all()
            for batch in table.to_batches():
                yield batch
        except (ImportError, AttributeError, Exception):
            # Fallback to Arrow IPC
            reader = pa.ipc.open_file(pa.BufferReader(content))
            for i in range(reader.num_record_batches):
                batch = reader.get_batch(i)
                if columns:
                    table = pa.Table.from_batches([batch]).select(columns)
                    batch = table.to_batches()[0]
                yield batch


def _extract_hf_uri(dataset_root: str) -> str:
    """Convert HF Hub URL to hf:// URI format for Lance."""
    if dataset_root.startswith("hf://"):
        return dataset_root
    # https://huggingface.co/datasets/org/repo/resolve/rev/path -> hf://datasets/org/repo@rev/path
    match = re.match(
        r"https://huggingface\.co/datasets/([^/]+/[^/]+)/resolve/([^/]+)/(.*)",
        dataset_root,
    )
    if match:
        repo_id, revision, path = match.groups()
        return f"hf://datasets/{repo_id}@{revision}/{path}"
    return dataset_root


def _group_by_dataset(files: Iterable[str]) -> Dict[str, List[str]]:
    files_per_dataset = defaultdict(list)
    for file_path in files:
        path = Path(file_path)
        if path.parent.name in {"data", "_transactions", "_indices"}:
            dataset_root = path.parent.parent
            files_per_dataset[str(dataset_root)].append(file_path)
    return files_per_dataset


class Lance(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = LanceConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        dl_manager.download_config.extract_on_the_fly = True

        splits = []
        for split, files in self.config.data_files.items():
            dataset_paths = _group_by_dataset(files)

            print(dl_manager, "is_streaming:", getattr(dl_manager, "is_streaming", False))

            if getattr(dl_manager, "is_streaming", False):
                # STREAMING MODE: Use _StreamingLanceDataset with hf:// URI
                streaming_datasets = []
                for dataset_root, file_list in dataset_paths.items():
                    print("dataset_root:", dataset_root)
                    hf_uri = _extract_hf_uri(dataset_root)

                    data_files = [f for f in file_list if "/data/" in f]
                    streaming_ds = _StreamingLanceDataset(
                        hf_dataset_uri=hf_uri,
                        data_files=data_files,
                        token=dl_manager.download_config.token,
                    )
                    streaming_datasets.append(streaming_ds)
                splits.append(
                    datasets.SplitGenerator(
                        name=split,
                        gen_kwargs={"streaming_datasets": streaming_datasets, "streaming": True},
                    )
                )
            else:
                # NON-STREAMING MODE: Download files (existing behavior)
                all_files_to_download = list(dl_manager.iter_files(list(dataset_paths.keys())))
                local_dataset_paths = _group_by_dataset(dl_manager.iter_files(dl_manager.download(all_files_to_download)))
                local_datasets = []
                for paths in local_dataset_paths.values():
                    ds = _LanceSnapshotDataset(paths)
                    local_datasets.append(ds)
                splits.append(
                    datasets.SplitGenerator(
                        name=split,
                        gen_kwargs={"paths": local_datasets, "streaming": False},
                    )
                )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, paths=None, streaming_datasets=None, streaming=False):
        if streaming:
            # Streaming mode: use _StreamingLanceDataset (tries hf:// first, then fallback)
            for ds_idx, streaming_ds in enumerate(streaming_datasets):
                for batch_idx, batch in enumerate(
                    streaming_ds.get_fragments(
                        columns=self.config.columns,
                        batch_size=self.config.batch_size,
                    )
                ):
                    table = pa.Table.from_batches([batch])
                    yield Key(ds_idx, batch_idx), self._cast_table(table)
        else:
            # Non-streaming mode: existing behavior
            for ds in paths:
                for frag_idx, fragment in enumerate(ds.get_fragments()):
                    for batch_idx, batch in enumerate(
                        fragment.to_batches(columns=self.config.columns, batch_size=self.config.batch_size)
                    ):
                        table = pa.Table.from_batches([batch])
                        yield Key(frag_idx, batch_idx), self._cast_table(table)
