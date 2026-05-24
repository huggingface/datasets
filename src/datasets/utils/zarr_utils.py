import logging
import math
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union

from datasets.utils import tqdm

logger = logging.getLogger(__name__)

DEFAULT_FILE_LIMIT = 10_000
DEFAULT_LARGE_FOLDER_THRESHOLD = 5_000


def _hub_repo_url(repo_id: str, repo_type: str = "dataset") -> str:
    """Build a canonical Hub URL for a repository."""
    if repo_type == "dataset":
        return f"https://huggingface.co/datasets/{repo_id}"
    if repo_type == "space":
        return f"https://huggingface.co/spaces/{repo_id}"
    return f"https://huggingface.co/{repo_id}"


def load_zarr_dataset(
    data_dir: str,
    drop_labels: bool = True,
    drop_metadata: bool = True,
    split: str = "train",
):
    """Load a Zarr dataset from a local directory, instantly.

    This is the fast alternative to ``load_dataset("zarrfolder", data_dir=...)``
    that avoids scanning every file inside each ``.zarr`` store. Instead it
    directly discovers ``.zarr`` directories and creates a ``Dataset`` with a
    ``Zarr`` feature column.

    For a directory layout like::

        data/
        ├── healthy/
        │   ├── scan1.zarr/
        │   └── scan2.zarr/
        └── diseased/
            ├── scan3.zarr/
            └── scan4.zarr/

    ``load_zarr_dataset("data")`` returns a ``Dataset`` with columns
    ``["zarr", "label"]`` where labels are inferred from parent directory
    names.

    Args:
        data_dir (``str``): Path to a local directory containing ``.zarr``
            directories (possibly nested in subdirectories).
        drop_labels (``bool``, defaults to ``True``): Whether to skip label
            inference from parent directory names. When ``True`` (default), no
            ``label`` column is added. When ``False``, a ``ClassLabel`` column
            is added if multiple label values exist.
        drop_metadata (``bool``, defaults to ``True``): Whether to skip
            metadata files (``metadata.csv``, ``metadata.jsonl``,
            ``metadata.parquet``) in the data directory.
        split (``str``, defaults to ``"train"``): Ignored — included for
            API consistency. All data is always in a single split.

    Returns:
        :class:`Dataset`: A Hugging Face Dataset with a ``zarr`` column
        containing :class:`Zarr` feature values (lazy proxies).

    Example::

        >>> from datasets import load_zarr_dataset
        >>> ds = load_zarr_dataset("/path/to/zarr/data")
        >>> ds[0]["zarr"].shape  # lazily opens the Zarr store on access
        ``(1937, 2048, 2048)``

    Note:
        For local directories, this function is orders of magnitude faster than
        ``load_dataset("zarrfolder", data_dir=...)`` because it discovers
        ``.zarr`` directories directly (O(zarr_stores)) instead of enumerating
        every internal file (O(all_files)). For large OME-Zarr stores with
        hundreds of thousands of chunk files, prefer this function.
    """
    from datasets import ClassLabel, Dataset, Features
    from datasets.features.zarr import Zarr
    from datasets.packaged_modules.zarrfolder.zarrfolder import _discover_zarr_dirs_local

    zarr_roots = _discover_zarr_dirs_local(data_dir)

    if not zarr_roots:
        raise FileNotFoundError(f"No .zarr directories found in {data_dir}")

    all_labels = set()
    if not drop_labels:
        for zarr_path in zarr_roots:
            parent = os.path.basename(os.path.dirname(zarr_path))
            if parent and not parent.startswith((".", "_")):
                if parent not in ("train", "test", "validation", "dev"):
                    all_labels.add(parent)

    add_labels = not drop_labels and len(all_labels) > 1

    if add_labels:
        features = Features(
            {"zarr": Zarr(), "label": ClassLabel(names=sorted(all_labels))}
        )
        data = {
            "zarr": zarr_roots,
            "label": [
                os.path.basename(os.path.dirname(p)) for p in zarr_roots
            ],
        }
    else:
        features = Features({"zarr": Zarr()})
        data = {"zarr": zarr_roots}

    return Dataset.from_dict(data, features=features)


def _count_files(path: str, show_progress: bool = False) -> int:
    """Count the total number of files in a directory tree.

    Args:
        path: Root directory to count files in.
        show_progress: If True, show a tqdm progress bar while counting.
    """
    if not show_progress:
        return sum(len(files) for _, _, files in os.walk(path))

    total = 0
    pbar = tqdm(desc="Counting files", unit="file")
    for _, _, files in os.walk(path):
        total += len(files)
        pbar.update(len(files))
    pbar.close()
    return total


def _total_chunks(shape: tuple, chunks: tuple) -> int:
    """Calculate the total number of chunks for a given array shape and chunk shape."""
    return math.prod(math.ceil(s / c) for s, c in zip(shape, chunks))


def _calculate_shard_shape(
    shape: tuple,
    chunks: tuple,
    file_limit: int = DEFAULT_FILE_LIMIT,
    num_arrays: int = 1,
) -> tuple:
    """Calculate a shard shape that keeps total files below file_limit.

    The shard shape is always a multiple of the chunk shape. We start with
    the chunk shape as the shard shape and increase it shard-by-shard until
    the estimated total file count is below the limit.

    Args:
        shape: Array shape.
        chunks: Inner chunk shape.
        file_limit: Maximum number of files per array.
        num_arrays: Number of arrays in the group (to split the budget).

    Returns:
        Tuple of shard dimensions (always multiples of chunk dimensions).
    """
    per_array_limit = max(file_limit // num_arrays, 1)
    target_chunks = per_array_limit

    # Start with chunks as shard shape
    shard_shape = list(chunks)

    # Iteratively increase shard multiplier until we're under the limit
    # Strategy: double the shard factor in each dimension until under limit
    while True:
        total = _total_chunks(shape, tuple(shard_shape))
        if total <= target_chunks:
            break
        # Find dimension with most room to grow, double it
        dim_to_grow = -1
        max_room = 0
        for i in range(len(shape)):
            room = shape[i] - shard_shape[i]
            if room > max_room:
                max_room = room
                dim_to_grow = i
        if dim_to_grow == -1:
            break  # Can't grow any further
        # Grow by one chunk in that dimension
        shard_shape[dim_to_grow] = min(
            shard_shape[dim_to_grow] + chunks[dim_to_grow],
            shape[dim_to_grow],
        )

    return tuple(shard_shape)


def _rechunk_to_v3(
    src_path: str,
    dst_path: str,
    file_limit: int = DEFAULT_FILE_LIMIT,
    inner_compressors=None,
) -> str:
    """Re-chunk a Zarr store to v3 format with ShardingCodec to reduce file count.

    Opens the source store, re-creates it as a v3 store with sharded chunks
    (fewer, larger files), and copies all data and attributes. Preserves
    group structure and OME-Zarr metadata.

    Args:
        src_path: Path to source Zarr store (v2 or v3).
        dst_path: Path for destination v3 Zarr store.
        file_limit: Target maximum number of files per array.
        inner_compressors: Compressors for inner chunks. Defaults to
            ``[BloscCodec(cname="zstd", clevel=5)]``.

    Returns:
        Path to the re-chunked v3 store.
    """
    import zarr
    from zarr.codecs import BloscCodec

    if inner_compressors is None:
        inner_compressors = [BloscCodec(cname="zstd", clevel=5)]

    src = zarr.open(src_path, mode="r")
    dst = zarr.open(dst_path, mode="w")

    if isinstance(src, zarr.Group):
        _rechunk_group(src, dst, file_limit, inner_compressors)
    else:
        _rechunk_array(src, dst, "data", file_limit, inner_compressors, is_root=True)

    return dst_path


def _rechunk_group(src_group, dst_group, file_limit, inner_compressors):
    """Re-chunk all arrays in a Zarr group, preserving hierarchy and attrs."""
    import zarr

    num_arrays = sum(1 for name in src_group.keys() if isinstance(src_group[name], zarr.Array))
    dst_group.attrs.put(dict(src_group.attrs))

    items = list(src_group.keys())
    for name in tqdm(items, desc="Rechunking arrays"):
        child = src_group[name]
        if isinstance(child, zarr.Array):
            _rechunk_array(child, dst_group, name, file_limit, inner_compressors, num_arrays=num_arrays)
        elif isinstance(child, zarr.Group):
            dst_child = dst_group.create_group(name)
            _rechunk_group(child, dst_child, file_limit, inner_compressors)


def _rechunk_array(
    src_arr,
    dst_group,
    name: str,
    file_limit: int,
    inner_compressors,
    is_root: bool = False,
    num_arrays: int = 1,
):
    """Re-chunk a single array with v3 ShardingCodec."""
    from zarr.codecs import ShardingCodec

    chunks = tuple(src_arr.chunks)
    shape = tuple(src_arr.shape)

    shard_shape = _calculate_shard_shape(shape, chunks, file_limit=file_limit, num_arrays=num_arrays)

    create_kwargs = dict(
        name=name,
        shape=shape,
        chunks=chunks,
        shards=shard_shape,
        dtype=src_arr.dtype,
        compressors=inner_compressors,
    )

    dst_arr = dst_group.create_array(**create_kwargs)

    # Copy data in chunks to avoid loading the entire array into memory
    _copy_array_data(src_arr, dst_arr, name=name)

    # Copy array-level attrs
    dst_arr.attrs.put(dict(src_arr.attrs))


def _copy_array_data(src_arr, dst_arr, name: str = "", chunk_size_mb: float = 64.0):
    """Copy data from source to destination array in manageable chunks.

    Iterates over the array in slices to avoid loading the entire array
    into memory. Each slice covers approximately chunk_size_mb megabytes.

    Args:
        src_arr: Source Zarr array.
        dst_arr: Destination Zarr array.
        name: Array name for progress display.
        chunk_size_mb: Target slice size in megabytes.
    """
    import numpy as np

    dtype_size = np.dtype(src_arr.dtype).itemsize
    elements_per_slice = int(chunk_size_mb * 1024 * 1024 / dtype_size)

    shape = src_arr.shape
    ndim = len(shape)

    if ndim == 0:
        dst_arr[()] = src_arr[()]
        return

    slice_shape = list(shape)
    total = 1
    for d in range(1, ndim):
        total *= slice_shape[d]
    if total > 0:
        slice_shape[0] = max(1, min(shape[0], elements_per_slice // total))
    else:
        slice_shape[0] = shape[0]

    dim0_slice = slice_shape[0]
    total_slices = math.ceil(shape[0] / dim0_slice)
    label = name or "array"
    desc = f"Copying {label} {list(shape)}"
    for start in tqdm(range(0, shape[0], dim0_slice), total=total_slices, desc=desc, leave=False):
        end = min(start + dim0_slice, shape[0])
        slices = tuple([slice(start, end)] + [slice(None)] * (ndim - 1))
        dst_arr[slices] = src_arr[slices]


def push_to_hub_zarr(
    local_path: str,
    repo_id: str,
    path_in_repo: str = "",
    repo_type: str = "dataset",
    token: Optional[str] = None,
    private: bool = False,
    revision: str = "main",
    file_limit: int = DEFAULT_FILE_LIMIT,
    delete_temp: bool = True,
    upload_strategy: str = "auto",
    large_folder_threshold: int = DEFAULT_LARGE_FOLDER_THRESHOLD,
):
    """Upload a Zarr store to HuggingFace Hub.

    If the store exceeds ``file_limit`` files (default 10,000, the Hub's
    per-directory limit), it is automatically re-chunked to Zarr v3 format
    with ShardingCodec, which consolidates many small chunk files into fewer
    shard files. The re-chunked store preserves all data, group structure,
    and metadata (including OME-Zarr multiscales).

    The upload uses ``huggingface_hub.HfApi.upload_folder`` to push the
    store directory to the Hub.

    Args:
        local_path (:obj:`str`):
            Path to the local Zarr store directory (e.g., ``data/image.zarr``).
        repo_id (:obj:`str`):
            HuggingFace Hub repository ID (e.g., ``"username/dataset"``).
        path_in_repo (:obj:`str`, defaults to ``""``):
            Subpath in the repository. If empty, the store
            is uploaded under its directory name.
        repo_type (:obj:`str`, defaults to ``"dataset"``):
            Repository type (``"dataset"``, ``"model"``, or ``"space"``).
        token (:obj:`str`, *optional*):
            HuggingFace Hub authentication token.
        private (:obj:`bool`, defaults to ``False``):
            Whether to create a private repository.
        revision (:obj:`str`, defaults to ``"main"``):
            Git revision to push to.
        file_limit (:obj:`int`, defaults to ``10000``):
            Maximum number of files before triggering automatic re-chunking.
            The HuggingFace Hub imposes a limit of approximately 10,000 files
            per directory. Stores exceeding this limit are re-chunked to Zarr v3
            format with ``ShardingCodec``, which reduces file count substantially.
        delete_temp (:obj:`bool`, defaults to ``True``):
            Whether to delete the temporary directory if re-chunking was needed.
        upload_strategy (:obj:`str`, defaults to ``"auto"``):
            Upload backend to use. One of ``"auto"``, ``"folder"``, or
            ``"large_folder"``.

            - ``"auto"``: uses ``upload_large_folder`` when file count exceeds
              ``large_folder_threshold`` or when re-chunking was performed;
              otherwise uses ``upload_folder``.
            - ``"folder"``: always use ``upload_folder``.
            - ``"large_folder"``: always use ``upload_large_folder``.

            ``upload_large_folder`` is more resilient for large uploads and can
            resume interrupted transfers.

            Note: ``upload_large_folder`` doesn't currently support
            ``path_in_repo``. If ``path_in_repo`` is set, this function falls
            back to ``upload_folder``.
        large_folder_threshold (:obj:`int`, defaults to ``5000``):
            File count threshold used by ``upload_strategy="auto"`` to switch
            from ``upload_folder`` to ``upload_large_folder``.

    Returns:
        :obj:`str`: URL of the uploaded repository.

    Example:

        Upload a small store directly:

        ```python
        push_to_hub_zarr("data/image.zarr", repo_id="username/dataset")
        ```

        Upload a large store (auto re-chunked to v3):

        ```python
        # If image.zarr has >10k files, it's automatically re-chunked
        push_to_hub_zarr("data/large_image.zarr", repo_id="username/dataset")
        ```
    """
    from huggingface_hub import HfApi, create_repo

    local_path = str(local_path)
    if not os.path.isdir(local_path):
        raise ValueError(f"local_path must be a directory, got: {local_path}")

    requested_path_in_repo = path_in_repo

    if upload_strategy not in {"auto", "folder", "large_folder"}:
        raise ValueError(
            f"upload_strategy must be one of 'auto', 'folder', 'large_folder', got: {upload_strategy}"
        )

    tqdm.write(f"Counting files in {local_path} ...")
    file_count = _count_files(local_path, show_progress=True)
    tqdm.write(f"Zarr store has {file_count:,} files (limit: {file_limit:,})")

    upload_path = local_path
    rechunked = False

    if file_count > file_limit:
        tqdm.write(
            f"Store exceeds file limit ({file_count:,} > {file_limit:,}). "
            f"Re-chunking to Zarr v3 format with ShardingCodec ..."
        )
        temp_dir = tempfile.mkdtemp(prefix="zarr_v3_")
        try:
            dst_path = os.path.join(temp_dir, os.path.basename(local_path.rstrip("/\\")))
            _rechunk_to_v3(local_path, dst_path, file_limit=file_limit)
            new_count = _count_files(dst_path, show_progress=False)
            tqdm.write(
                f"Re-chunked: {file_count:,} → {new_count:,} files "
                f"({new_count / file_count:.1%} of original)"
            )
            upload_path = dst_path
            rechunked = True
        except Exception:
            if delete_temp:
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise

    tqdm.write("Creating repository ...")
    api = HfApi(token=token)
    create_repo(repo_id=repo_id, repo_type=repo_type, private=private, exist_ok=True)

    upload_count = _count_files(upload_path, show_progress=False)
    reasons = []

    if upload_strategy == "folder":
        use_large_folder = False
        reasons.append("upload_strategy='folder'")
    elif upload_strategy == "large_folder":
        use_large_folder = True
        reasons.append("upload_strategy='large_folder'")
    else:
        if rechunked:
            reasons.append("re-chunking was performed")
        if upload_count >= large_folder_threshold:
            reasons.append(f"file count {upload_count:,} >= threshold {large_folder_threshold:,}")
        use_large_folder = bool(reasons)

    if use_large_folder and requested_path_in_repo:
        tqdm.write(
            "upload_large_folder does not support path_in_repo. "
            f"Falling back to upload_folder for path_in_repo='{requested_path_in_repo}'."
        )
        use_large_folder = False
        reasons = ["path_in_repo requires upload_folder"]

    if not reasons:
        reasons = ["auto selection for smaller upload"]

    effective_path_in_repo = requested_path_in_repo or os.path.basename(local_path.rstrip("/\\"))

    tqdm.write(f"Uploading {os.path.basename(upload_path)} ...")
    if use_large_folder:
        tqdm.write(f"Using upload_large_folder (resumable): {', '.join(reasons)}")
        api.upload_large_folder(
            repo_id=repo_id,
            folder_path=upload_path,
            repo_type=repo_type,
            revision=revision,
            private=private,
            print_report=True,
        )
        url = _hub_repo_url(repo_id, repo_type)
    else:
        tqdm.write(f"Using upload_folder: {', '.join(reasons)}")
        url = api.upload_folder(
            folder_path=upload_path,
            repo_id=repo_id,
            repo_type=repo_type,
            path_in_repo=effective_path_in_repo,
            revision=revision,
        )

    if file_count > file_limit and delete_temp:
        shutil.rmtree(temp_dir, ignore_errors=True)

    tqdm.write(f"Upload complete: {url}")
    return url


class ZarrCollator:
    """Collation function for PyTorch DataLoader that materializes Zarr patches.

    Designed for training deep learning models on large Zarr-backed datasets.
    Extracts patches from ``ZarrProxy`` objects and converts them to PyTorch
    tensors, enabling batched training without loading entire arrays into memory.

    The collator handles both plain Zarr arrays and OME-Zarr multiscale images.
    For OME-Zarr, a specific resolution level can be selected via the ``level``
    parameter.

    Parameters
    ----------
    patch_size : tuple of int, optional
        Size of patches to extract from each sample. If ``None``, loads the
        entire array (only recommended for small arrays or low resolution levels).
    level : int, optional
        OME-Zarr resolution level to use. Level 0 is highest resolution.
        Defaults to 0. Ignored for plain Zarr arrays.
    label_column : str, optional
        Name of the label column. If provided, labels are collected into a
        tensor. Defaults to ``"label"``.
    column_name : str, optional
        Name of the Zarr column in the dataset. Defaults to ``"zarr"``.
    rng : numpy.random.Generator, optional
        Random number generator for reproducibility. If ``None``, a default
        generator is created.

    Example
    -------
    Using with a PyTorch DataLoader for training:

    ```python
    from datasets import load_dataset
    from datasets.utils.zarr_utils import ZarrCollator

    ds = load_dataset("username/brain-tissue-ome-zarr", streaming=True)
    collator = ZarrCollator(patch_size=(256, 256), level=0)
    loader = DataLoader(ds["train"], batch_size=8, collate_fn=collator)

    for batch in loader:
        # batch = {"pixel_values": torch.Tensor [8, C, 256, 256],
        #          "labels": torch.Tensor [8]}
        loss = model(batch["pixel_values"], batch["labels"])
    ```
    """

    def __init__(
        self,
        patch_size=None,
        level=0,
        label_column="label",
        column_name="zarr",
        rng=None,
    ):
        self.patch_size = patch_size
        self.level = level
        self.label_column = label_column
        self.column_name = column_name
        self._rng = rng

    def __call__(self, batch):
        import numpy as np

        arrays = []
        labels = []
        has_labels = False

        rng = self._rng
        if rng is None:
            rng = np.random.default_rng()

        for sample in batch:
            proxy = sample[self.column_name]

            # Resolve proxy to get the actual array
            if hasattr(proxy, "random_patch"):
                # OmeZarrProxy or ZarrArrayProxy
                if self.patch_size is not None:
                    if hasattr(proxy, "get_level"):
                        # OmeZarrProxy — has level parameter
                        arr = proxy.random_patch(self.patch_size, level=self.level, rng=rng)
                    else:
                        # ZarrArrayProxy — no level parameter
                        arr = proxy.random_patch(self.patch_size, rng=rng)
                else:
                    arr = np.asarray(proxy[:])
            else:
                # ZarrGroupProxy or unresolved ZarrProxy — resolve and try again
                resolved = proxy._resolve() if hasattr(proxy, "_resolve") else proxy
                if hasattr(resolved, "random_patch"):
                    if self.patch_size is not None:
                        arr = resolved.random_patch(self.patch_size, rng=rng)
                    else:
                        arr = np.asarray(resolved[:])
                else:
                    raise TypeError(
                        f"Cannot extract patch from {type(resolved).__name__}. "
                        f"For Zarr groups, specify which array to access "
                        f"(e.g., proxy['array_name']) or use an OME-Zarr "
                        f"multiscale store where iter_patches/random_patch are "
                        f"available on level arrays."
                    )

            arrays.append(np.asarray(arr))

            if self.label_column in sample:
                has_labels = True
                labels.append(sample[self.label_column])

        try:
            import torch

            pixel_values = torch.stack([torch.from_numpy(a) for a in arrays])
        except ImportError:
            pixel_values = np.stack(arrays)

        result = {"pixel_values": pixel_values}

        if has_labels:
            try:
                import torch

                result["labels"] = torch.tensor(labels)
            except ImportError:
                result["labels"] = np.array(labels)

        return result
