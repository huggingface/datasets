import logging
import os
from dataclasses import dataclass
from typing import Iterator, Optional

import datasets
from datasets.builder import BuilderConfig

logger = logging.getLogger(__name__)

ZARR_METADATA_FILENAMES = {"zarr.json", ".zarray", ".zgroup", ".zattrs", ".zmetadata"}


def _find_zarr_roots(file_paths):
    """Given a list of file paths, find unique .zarr directory roots.

    Scans for ``.zarr`` in path components and returns the unique parent
    directory paths. Works with both local paths (``/data/image.zarr/0``)
    and remote URLs (``hf://datasets/user/repo/image.zarr/0``).
    """
    zarr_roots = set()
    for filepath in file_paths:
        parts = filepath.replace("\\", "/").split("/")
        for i, part in enumerate(parts):
            if part.endswith(".zarr"):
                zarr_roots.add("/".join(parts[: i + 1]))
                break
    return sorted(zarr_roots)


def _discover_zarr_dirs_local(base_path):
    """Fast local discovery of .zarr directories by walking the filesystem.

    Instead of enumerating every file inside .zarr stores, this scans
    directory names and stops descending into directories that end with
    ``.zarr``. This is O(zarr_stores) instead of O(all_files).

    Returns a sorted list of absolute paths to .zarr directories.
    """
    zarr_dirs = []
    for dirpath, dirnames, filenames in os.walk(base_path):
        found = []
        for d in dirnames:
            if d.endswith(".zarr"):
                zarr_dirs.append(os.path.join(dirpath, d))
                found.append(d)
        for d in found:
            dirnames.remove(d)
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "__"))]
    return sorted(zarr_dirs)


def _discover_metadata_files_local(base_path, metadata_filenames):
    """Find metadata files (csv, jsonl, parquet) in a local directory."""
    metadata = []
    for fname in metadata_filenames:
        fpath = os.path.join(base_path, fname)
        if os.path.isfile(fpath):
            metadata.append(fpath)
    return metadata


def _parent_dir(path):
    """Get the parent directory name from a path (works for local and hf:// paths)."""
    parts = path.replace("\\", "/").rstrip("/").split("/")
    if len(parts) >= 2:
        return parts[-2]
    return ""


@dataclass
class ZarrFolderConfig(BuilderConfig):
    """BuilderConfig for ZarrFolder."""

    features: Optional[datasets.Features] = None
    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class ZarrFolder(datasets.GeneratorBasedBuilder):
    """ZarrFolder dataset builder for loading Zarr stores.

    Discovers ``.zarr`` directories and creates one dataset row per Zarr
    store, with a ``Zarr`` feature column that lazily opens each store on
    access. Supports plain Zarr arrays, Zarr groups, and OME-Zarr multiscale
    images.

    For local directories, discovery is fast — only ``.zarr`` directory
    names are scanned (O(zarr_stores)) rather than enumerating every
    internal file (O(all_files)). For remote paths, file-level enumeration
    is used as a fallback.

    Labels can be inferred from subdirectory names (e.g.,
    ``data/healthy/scan.zarr`` yields label ``healthy``), or additional
    columns can be provided via metadata files (``metadata.csv``,
    ``metadata.jsonl``, or ``metadata.parquet``).
    """

    BASE_FEATURE = datasets.Zarr
    BASE_COLUMN_NAME = "zarr"
    BUILDER_CONFIG_CLASS = ZarrFolderConfig
    EXTENSIONS: list[str] = [".zarr"]
    METADATA_FILENAMES: list[str] = ["metadata.csv", "metadata.jsonl", "metadata.parquet"]
    METADATA_EXTENSIONS: list[str] = [".zarray", ".zgroup", ".zattrs", ".zmetadata", ".zarr.json"]

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _try_fast_local_discovery(self):
        """Attempt fast local discovery by walking the data_dir directly.

        Returns (zarr_roots_dict, metadata_files_dict) if successful,
        or None if the data_dir is not a local path.
        """
        data_dir = getattr(self.config, "data_dir", None)
        if not data_dir:
            return None

        from datasets.utils.file_utils import is_local_path

        if not is_local_path(str(data_dir)):
            return None

        data_dir = str(data_dir)
        if not os.path.isdir(data_dir):
            return None

        zarr_roots = _discover_zarr_dirs_local(data_dir)
        metadata_files = _discover_metadata_files_local(data_dir, self.METADATA_FILENAMES)

        return {"train": zarr_roots}, {"train": metadata_files}

    def _split_generators(self, dl_manager):
        dl_manager.download_config.extract_on_the_fly = True

        fast_result = self._try_fast_local_discovery()

        if fast_result is not None:
            zarr_roots_by_split, metadata_by_split = fast_result
        elif not self.config.data_files:
            raise ValueError(
                "ZarrFolder datasets require either `data_dir` or `data_files` to be specified. "
                "Neither was provided."
            )
        else:
            zarr_roots_by_split = {}
            metadata_by_split = {}

            for split_name, files in self.config.data_files.items():
                file_paths = [str(f) for f in files]

                metadata = []
                for fp in file_paths:
                    basename = os.path.basename(fp)
                    if basename in self.METADATA_FILENAMES:
                        metadata.append(fp)

                zarr_roots = _find_zarr_roots(file_paths)

                if not zarr_roots:
                    logger.warning(f"No .zarr directories found in split '{split_name}'")

                zarr_roots_by_split[split_name] = zarr_roots
                metadata_by_split[split_name] = metadata

        all_labels = set()
        for zarr_roots in zarr_roots_by_split.values():
            for zarr_path in zarr_roots:
                label = _parent_dir(zarr_path)
                if label and not label.startswith((".", "_")):
                    if label not in ("train", "test", "validation", "dev"):
                        all_labels.add(label)

        add_labels = len(all_labels) > 1 if self.config.drop_labels is None else not self.config.drop_labels
        add_metadata = bool(any(metadata_by_split.values())) if self.config.drop_metadata is None else not self.config.drop_metadata

        if self.config.features is None:
            if add_metadata and any(metadata_by_split.values()):
                self.info.features = datasets.Features({self.BASE_COLUMN_NAME: self.BASE_FEATURE()})
            elif add_labels:
                self.info.features = datasets.Features(
                    {
                        self.BASE_COLUMN_NAME: self.BASE_FEATURE(),
                        "label": datasets.ClassLabel(names=sorted(all_labels)),
                    }
                )
            else:
                self.info.features = datasets.Features({self.BASE_COLUMN_NAME: self.BASE_FEATURE()})

        splits = []
        for split_name, zarr_roots in zarr_roots_by_split.items():
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "zarr_roots": zarr_roots,
                        "metadata_files": metadata_by_split.get(split_name, []),
                        "add_labels": add_labels,
                        "add_metadata": add_metadata,
                    },
                )
            )

        return splits

    def _generate_examples(self, zarr_roots, metadata_files, add_labels, add_metadata):
        if add_metadata and metadata_files:
            yield from self._generate_examples_with_metadata(zarr_roots, metadata_files)
        else:
            for idx, zarr_path in enumerate(zarr_roots):
                sample = {self.BASE_COLUMN_NAME: zarr_path}
                if add_labels:
                    label = _parent_dir(zarr_path)
                    sample["label"] = label
                yield idx, sample

    def _generate_examples_with_metadata(self, zarr_roots, metadata_files):
        zarr_dir = os.path.dirname(zarr_roots[0]) if zarr_roots else ""

        row_idx = 0
        for metadata_file in metadata_files:
            ext = os.path.splitext(metadata_file)[1].lower()
            try:
                if ext == ".csv":
                    import pyarrow.csv as pacsv

                    table = pacsv.read_csv(metadata_file)
                elif ext == ".jsonl":
                    import pyarrow.json as pajson

                    table = pajson.read_json(metadata_file)
                elif ext == ".parquet":
                    import pyarrow.parquet as pq

                    table = pq.read_table(metadata_file)
                else:
                    continue
            except Exception:
                continue

            for row in table.to_pylist():
                file_name = row.pop("file_name", None) or row.pop("zarr_file_name", None)
                if file_name:
                    if not file_name.endswith(".zarr"):
                        base = os.path.splitext(file_name)[0] if os.path.splitext(file_name)[1] else file_name
                        file_name = base.rstrip("/") + ".zarr"
                    zarr_path = os.path.join(zarr_dir, file_name) if not os.path.isabs(file_name) else file_name
                else:
                    continue

                sample = {self.BASE_COLUMN_NAME: zarr_path}
                sample.update(row)
                yield row_idx, sample
                row_idx += 1