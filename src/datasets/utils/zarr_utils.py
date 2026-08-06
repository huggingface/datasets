import logging
import os
from typing import Dict, List, Optional, Union

from datasets.utils import tqdm

try:
    from huggingface_hub.errors import BucketNotFoundError
except ImportError:  # huggingface_hub < 1.6.0
    BucketNotFoundError = None

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


def push_to_hub_zarr(
    local_path: str,
    repo_id: str,
    path_in_repo: str = "",
    repo_type: str = "dataset",
    token: Optional[str] = None,
    private: bool = False,
    revision: str = "main",
    file_limit: int = DEFAULT_FILE_LIMIT,
    upload_strategy: str = "auto",
    large_folder_threshold: int = DEFAULT_LARGE_FOLDER_THRESHOLD,
):
    """Upload a Zarr store to HuggingFace Hub.

    Two destinations are supported:

    - **Storage Bucket** (recommended for large stores): pass a
      ``repo_id`` of the form ``"buckets/<namespace>/<bucket_name>"`` (optionally
      followed by a subpath). The store directory is synced to the bucket with
      ``huggingface_hub.HfApi.sync_bucket``, which handles thousands of chunk
      files and resumes interrupted transfers. Buckets have no revisions and no
      per-directory file limits.
    - **Dataset repository**: any other ``repo_id`` uploads the store directory
      as-is with ``huggingface_hub.HfApi.upload_folder`` (or
      ``upload_large_folder``). Zarr stores are never re-chunked by this
      function: if the store contains more than ``file_limit`` files, a warning
      is printed recommending a Storage Bucket.

    Args:
        local_path (:obj:`str`):
            Path to the local Zarr store directory (e.g., ``data/image.zarr``).
        repo_id (:obj:`str`):
            HuggingFace Hub repository ID (e.g., ``"username/dataset"``) or a
            Storage Bucket destination (e.g., ``"buckets/username/my-bucket"``).
        path_in_repo (:obj:`str`, defaults to ``""``):
            Subpath in the repository or bucket. If empty, the store
            is uploaded under its directory name.
        repo_type (:obj:`str`, defaults to ``"dataset"``):
            Repository type (``"dataset"``, ``"model"``, or ``"space"``).
            Ignored for bucket destinations.
        token (:obj:`str`, *optional*):
            HuggingFace Hub authentication token.
        private (:obj:`bool`, defaults to ``False``):
            Whether to create a private repository or bucket.
        revision (:obj:`str`, defaults to ``"main"``):
            Git revision to push to. Ignored for bucket destinations (buckets
            have no revisions).
        file_limit (:obj:`int`, defaults to ``10000``):
            File count above which a warning is printed recommending a
            Storage Bucket for the upload. Ignored for bucket destinations.
        upload_strategy (:obj:`str`, defaults to ``"auto"``):
            Upload backend to use for dataset repositories. One of ``"auto"``,
            ``"folder"``, or ``"large_folder"``. Ignored for bucket
            destinations.

            - ``"auto"``: uses ``upload_large_folder`` when file count exceeds
              ``large_folder_threshold``; otherwise uses ``upload_folder``.
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
        :obj:`str`: URL of the uploaded store, either a Hub repository URL or
        an ``hf://buckets/...`` path.

    Example:

        Upload a Zarr store to a dataset repository:

        ```python
        push_to_hub_zarr("data/image.zarr", repo_id="username/dataset")
        ```

        Upload a large store to a Storage Bucket (recommended for stores with
        many chunk files):

        ```python
        push_to_hub_zarr("data/large_image.zarr", repo_id="buckets/username/my-bucket")
        ```

        Upload a large store to a dataset repository, which prints a warning
        recommending a bucket:

        ```python
        # If image.zarr has >10k files, a warning suggests a Storage Bucket
        push_to_hub_zarr("data/large_image.zarr", repo_id="username/dataset")
        ```
    """
    from huggingface_hub import HfApi, create_repo

    local_path = str(local_path)
    if not os.path.isdir(local_path):
        raise ValueError(f"local_path must be a directory, got: {local_path}")

    if repo_id.startswith("buckets/"):
        return _push_to_hub_bucket(
            local_path=local_path,
            repo_id=repo_id,
            path_in_repo=path_in_repo,
            token=token,
            private=private,
        )

    requested_path_in_repo = path_in_repo

    if upload_strategy not in {"auto", "folder", "large_folder"}:
        raise ValueError(
            f"upload_strategy must be one of 'auto', 'folder', 'large_folder', got: {upload_strategy}"
        )

    tqdm.write(f"Counting files in {local_path} ...")
    file_count = _count_files(local_path, show_progress=True)
    tqdm.write(f"Zarr store has {file_count:,} files")

    if file_count > file_limit:
        tqdm.write(
            f"WARNING: Zarr store has {file_count:,} files "
            f"(recommended limit: {file_limit:,}). "
            "Large file counts strain dataset repositories; consider uploading "
            "to a Storage Bucket instead (see huggingface_hub.create_bucket)."
        )

    upload_path = local_path

    tqdm.write("Creating repository ...")
    api = HfApi(token=token)
    create_repo(repo_id=repo_id, repo_type=repo_type, private=private, exist_ok=True)

    reasons = []

    if upload_strategy == "folder":
        use_large_folder = False
        reasons.append("upload_strategy='folder'")
    elif upload_strategy == "large_folder":
        use_large_folder = True
        reasons.append("upload_strategy='large_folder'")
    else:
        if file_count >= large_folder_threshold:
            reasons.append(f"file count {file_count:,} >= threshold {large_folder_threshold:,}")
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

    tqdm.write(f"Upload complete: {url}")
    return url


def _push_to_hub_bucket(
    local_path: str,
    repo_id: str,
    path_in_repo: str = "",
    token: Optional[str] = None,
    private: bool = False,
) -> str:
    """Upload a Zarr store to a Storage Bucket.

    ``repo_id`` must have the form ``buckets/<namespace>/<bucket_name>``,
    optionally followed by a subpath: ``buckets/<namespace>/<bucket_name>/<subpath>``.
    The bucket is created if it doesn't exist yet. Files are synced with
    ``HfApi.sync_bucket``, which supports resumable uploads.

    Args:
        local_path (:obj:`str`): Path to the local Zarr store directory.
        repo_id (:obj:`str`): Bucket destination, e.g. ``"buckets/username/my-bucket"``.
        path_in_repo (:obj:`str`, defaults to ``""``): Subpath within the bucket.
        token (:obj:`str`, *optional*): HuggingFace Hub authentication token.
        private (:obj:`bool`, defaults to ``False``): Whether to create a private bucket.

    Returns:
        :obj:`str`: ``hf://buckets/...`` URL of the uploaded store.
    """
    from huggingface_hub import HfApi

    if BucketNotFoundError is None:
        raise ImportError("Pushing Zarr stores to buckets requires huggingface_hub>=1.6.0")

    _, _namespace, _bucket_name, *_path_segments = repo_id.split("/")
    api = HfApi(token=token)
    try:
        bucket_id = api.bucket_info(_namespace + "/" + _bucket_name).id
    except BucketNotFoundError:
        bucket_url = api.create_bucket(_namespace + "/" + _bucket_name, private=private, exist_ok=True)
        bucket_id = bucket_url.bucket_id

    subpath = "/".join(s for s in _path_segments if s)
    subpath = "/".join(
        s for s in [subpath, path_in_repo or os.path.basename(local_path.rstrip("/\\"))] if s
    )

    dest = f"hf://buckets/{bucket_id}"
    if subpath:
        dest += "/" + subpath

    tqdm.write(f"Syncing {local_path} to {dest} ...")
    api.sync_bucket(source=local_path, dest=dest, token=token)
    tqdm.write(f"Upload complete: {dest}")
    return dest


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
    Using with a streaming dataset and ``IterableDataset.batch`` for training:

    ```python
    from datasets import load_dataset
    from datasets.utils.zarr_utils import ZarrCollator

    ds = load_dataset("username/brain-tissue-ome-zarr", streaming=True)
    collator = ZarrCollator(patch_size=(256, 256), level=0)

    for batch in ds["train"].batch(batch_size=8):
        # batch = {"pixel_values": torch.Tensor [8, C, 256, 256],
        #          "labels": torch.Tensor [8]}
        loss = model(batch["pixel_values"], batch["labels"])
    ```

    The collator extracts patches concurrently across the batch (up to 8
    workers); reads go through a shared decoded-chunk cache, so overlapping
    patches fetch each chunk only once.

    For map-style datasets the same collator works as a ``collate_fn`` for a
    PyTorch ``DataLoader`` (without ``streaming=True``).
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

    def _extract(self, sample, rng):
        """Extract a (patch, label-or-None) pair from a single sample."""
        import numpy as np

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

        label = sample.get(self.label_column, None) if self.label_column in sample else None
        return np.asarray(arr), label

    def __call__(self, batch):
        import numpy as np

        if isinstance(batch, dict):
            # Columnar batch (e.g. from ``IterableDataset.batch`` or
            # ``iter(batch_size=...)``): {"zarr": [p1, p2], "label": [0, 1]}
            first = next(iter(batch.values()))
            if isinstance(first, (list, tuple)):
                lengths = {len(values) for values in batch.values()}
                if len(lengths) != 1:
                    raise ValueError(
                        f"Columnar batch columns have mismatched lengths: {lengths}"
                    )
                n = next(iter(lengths))
                batch = [{key: batch[key][i] for key in batch} for i in range(n)]
            else:
                # A single sample, not a columnar batch
                batch = [batch]

        rng = self._rng
        if rng is None:
            rng = np.random.default_rng()

        if self.patch_size is not None and len(batch) > 1:
            # Concurrent batch pass: spawn a deterministic child rng per
            # sample (Generator is not thread-safe) and extract patches in
            # parallel. Reads go through the shared decoded-chunk cache, so
            # overlapping chunks across the batch are fetched/decoded once.
            child_rngs = [np.random.default_rng(int(rng.integers(0, 2**32))) for _ in batch]
            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor(max_workers=min(8, len(batch))) as pool:
                extras = list(pool.map(self._extract, batch, child_rngs))
        else:
            extras = [self._extract(sample, rng) for sample in batch]

        arrays = [arr for arr, _ in extras]
        labels = [label for _, label in extras]
        present_labels = [label for label in labels if label is not None]
        has_labels = bool(present_labels)

        try:
            # On Windows, torch's bundled libomp.dll conflicts with the copy
            # bundled by numcodecs.blosc (zarr reads load it first). Allow
            # both runtimes to coexist instead of aborting on import.
            if os.name == "nt":
                os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
            import torch

            pixel_values = torch.stack([torch.from_numpy(a) for a in arrays])
        except ImportError:
            pixel_values = np.stack(arrays)

        result = {"pixel_values": pixel_values}

        if has_labels:
            try:
                if os.name == "nt":
                    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
                import torch

                result["labels"] = torch.tensor(present_labels)
            except ImportError:
                result["labels"] = np.array(present_labels)

        return result
