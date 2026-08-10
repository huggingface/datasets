import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import pyarrow as pa

from .. import config
from ..table import array_cast
from .zarr_cache import STORE_REGISTRY, cached_array_getitem, store_key


if TYPE_CHECKING:
    from .features import FeatureType


def _open_zarr_store(
    path: str,
    token_per_repo_id: Optional[Dict[str, str]] = None,
    storage_options: Optional[Dict[str, Any]] = None,
):
    """Open a Zarr store from a local or remote path.

    For local paths, opens directly. For ``hf://`` paths, uses HfFileSystem
    with fsspec. For other URLs, delegates to zarr's built-in URL handling.

    Token resolution:
    - ``hf://datasets/...`` paths look up the token for the dataset repo in
      ``token_per_repo_id`` (e.g. to access private Zarr stores hosted in
      other dataset repositories).
    - ``hf://buckets/...`` paths have no repo id; they fall back to the
      first token in ``token_per_repo_id``. Public buckets require no token.

    Extra ``storage_options`` are forwarded to the fsspec filesystem (e.g.
    ``{"anon": True}`` for public object stores). Resolved tokens take
    precedence over any user-supplied ``"token"`` option.
    """
    import zarr

    token = None
    if token_per_repo_id:
        if path.startswith("hf://datasets/"):
            repo_id = _extract_repo_id_from_hf_path(path)
            token = token_per_repo_id.get(repo_id) if repo_id else None
        if token is None:
            token = next(iter(token_per_repo_id.values()), None)

    key = store_key(path, token, storage_options)
    cached = STORE_REGISTRY.get(key)
    if cached is not None:
        return cached

    if path.startswith("hf://"):
        from zarr.storage import FsspecStore

        options = dict(storage_options) if storage_options else {}
        if token is not None:
            options["token"] = token
        store = FsspecStore.from_url(path, read_only=True, storage_options=options or None)
        root = zarr.open(store=store, mode="r")
    elif os.path.isdir(path):
        root = zarr.open(path, mode="r")
    else:
        try:
            from zarr.storage import FsspecStore

            store = FsspecStore.from_url(path, mode="r", storage_options=storage_options)
            root = zarr.open(store=store, mode="r")
        except Exception:
            root = zarr.open(path, mode="r")

    STORE_REGISTRY.put(key, root)
    return root


def _reopen_zarr_node(path: str, token_per_repo_id, storage_options):
    """Re-open a Zarr array by path, used when unpickling resolved proxies.

    Raises a clear error if the node at ``path`` is no longer an array.
    """
    import zarr

    root = _open_zarr_store(path, token_per_repo_id, storage_options)
    if isinstance(root, zarr.Array):
        return root
    raise ValueError(
        f"Cannot reopen {path!r} as a Zarr array (got {type(root).__name__}); "
        f"the store may have been renamed or removed"
    )


def _extract_repo_id_from_hf_path(path: str) -> Optional[str]:
    """Extract repo_id from an ``hf://datasets/...`` URL path.

    Handles formats like:
    - ``hf://datasets/user/repo/...`` -> ``user/repo``
    - ``hf://datasets/user/repo@revision/...`` -> ``user/repo``

    Returns ``None`` for non-dataset paths such as ``hf://buckets/...``.
    """
    if not path.startswith("hf://datasets/"):
        return None
    stripped = path[len("hf://datasets/") :]
    parts = stripped.split("/")
    if len(parts) >= 2:
        org = parts[0]
        repo = parts[1].split("@")[0]
        return f"{org}/{repo}"
    return None


class ZarrProxy:
    """Lazy proxy for a Zarr array store.

    Stores only the path and optional auth tokens. The underlying Zarr store
    is opened on first property access (shape, dtype, __getitem__, etc.) and
    cached for subsequent use. The proxy is pickle-safe: it drops the opened
    store on serialization and re-opens on deserialization.
    """

    def __init__(
        self,
        path: str,
        token_per_repo_id: Optional[Dict[str, str]] = None,
        storage_options: Optional[Dict[str, Any]] = None,
    ):
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}
        self._storage_options = dict(storage_options) if storage_options else None
        self._resolved = None

    def _resolve(self):
        if self._resolved is None:
            import zarr

            root = _open_zarr_store(self._path, self._token_per_repo_id, self._storage_options)
            if not isinstance(root, zarr.Array):
                raise ValueError(
                    f"The default Zarr feature only supports Zarr arrays, but {self._path!r} "
                    f"is a {type(root).__name__}. Point the feature at the array inside the "
                    f"store (e.g. '{self._path}/array_name'), or use load_dataset('zarr', ...) "
                    f"to load a whole store as a table; OME-Zarr (multiscale) stores are "
                    f"supported in a separate integration."
                )
            self._resolved = ZarrArrayProxy(
                root, self._path, self._token_per_repo_id, self._storage_options
            )
        return self._resolved

    @property
    def path(self):
        return self._path

    @property
    def shape(self):
        return self._resolve().shape

    @property
    def dtype(self):
        return self._resolve().dtype

    @property
    def ndim(self):
        return self._resolve().ndim

    @property
    def chunks(self):
        return self._resolve().chunks

    def __getitem__(self, key):
        return self._resolve().__getitem__(key)

    def __len__(self):
        return len(self._resolve())

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self._resolve(), name)

    def __repr__(self):
        if self._resolved is not None:
            return repr(self._resolved)
        return f"ZarrProxy(path={self._path!r})"

    def __getstate__(self):
        return {
            "path": self._path,
            "token_per_repo_id": self._token_per_repo_id,
            "storage_options": self._storage_options,
        }

    def __setstate__(self, state):
        self._path = state["path"]
        self._token_per_repo_id = state.get("token_per_repo_id", {})
        self._storage_options = state.get("storage_options")
        self._resolved = None


class ZarrArrayProxy:
    """Lazy proxy for a plain Zarr array.

    Provides attribute access (shape, dtype, chunks, ndim) and subscript
    access (``__getitem__``) without loading the full array into memory.
    Only the chunks needed for a given slice are fetched from the store.
    """

    def __init__(
        self,
        array,
        path: str,
        token_per_repo_id: Optional[Dict[str, str]] = None,
        storage_options: Optional[Dict[str, Any]] = None,
    ):
        # Store the zarr.Array directly — it holds only metadata + store reference,
        # not the data itself. Data is loaded lazily per-chunk on __getitem__.
        self._array = array
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}
        self._storage_options = dict(storage_options) if storage_options else None

    @property
    def path(self):
        return self._path

    @property
    def shape(self):
        return self._array.shape

    @property
    def dtype(self):
        return self._array.dtype

    @property
    def ndim(self):
        return self._array.ndim

    @property
    def chunks(self):
        return self._array.chunks

    @property
    def attrs(self):
        return dict(self._array.attrs)

    def __getitem__(self, key):
        return cached_array_getitem(self._array, self._path, key)

    def asarray(self):
        """Load the full array into memory and return it as a numpy array.

        Warning: this materializes the entire array. For large stores,
        prefer slicing (``proxy[...]``) or ``iter_patches``/``random_patch``,
        which only fetch the needed chunks.
        """
        import numpy as np

        return np.asarray(self._array)

    def __len__(self):
        return self._array.shape[0] if self._array.ndim > 0 else 1

    def __repr__(self):
        return (
            f"ZarrArrayProxy(path={self._path!r}, "
            f"shape={self._array.shape}, "
            f"dtype={self._array.dtype})"
        )

    def iter_patches(self, patch_size, stride=None):
        """Iterate over non-overlapping or strided patches of the array.

        Yields ``(coordinates, patch)`` tuples where ``coordinates`` is a
        tuple of start indices and ``patch`` is a numpy array of shape
        ``patch_size``. Only the chunks needed for each patch are loaded
        from the store, making this efficient for TB-scale arrays.

        For arrays with leading non-spatial dimensions (e.g., time or
        channel), those dimensions are yielded in full and ``patch_size``
        applies to the trailing spatial dimensions.

        Parameters
        ----------
        patch_size : tuple of int
            Size of each patch. Must match the number of spatial dimensions.
            For a 2D array, use ``(height, width)``. For a 3D array,
            use ``(depth, height, width)``.
        stride : tuple of int, optional
            Stride between patches. Defaults to ``patch_size`` (non-overlapping).
            Use a smaller stride for overlapping patches (e.g., half of
            ``patch_size`` for 50% overlap).

        Yields
        ------
        tuple of (tuple, numpy.ndarray)
            ``(start_indices, patch_array)`` pairs.

        Example
        -------
        >>> for (y, x), patch in proxy.iter_patches((256, 256), stride=(128, 128)):
        ...     prediction = model(patch)
        """
        import itertools

        shape = self._array.shape
        ndim = self._array.ndim
        n_spatial = len(patch_size)

        if n_spatial > ndim:
            raise ValueError(
                f"patch_size has {n_spatial} dimensions but array has {ndim} dimensions"
            )

        n_leading = ndim - n_spatial
        if stride is None:
            stride = patch_size

        leading_ranges = [range(s) for s in shape[:n_leading]]
        spatial_ranges = [
            range(0, shape[n_leading + i], stride[i]) for i in range(n_spatial)
        ]

        all_ranges = leading_ranges + spatial_ranges

        for indices in itertools.product(*all_ranges):
            spatial_starts = indices[n_leading:]
            slices = tuple(
                slice(indices[i], min(indices[i] + patch_size[i - n_leading], shape[i]))
                if i >= n_leading
                else slice(None)
                for i in range(ndim)
            )
            coords = tuple(int(s) for s in spatial_starts)
            yield coords, self[slices]

    def random_patch(self, patch_size, rng=None):
        """Extract a random patch from the array.

        Useful for data augmentation during training. Only the chunks
        needed for the patch are loaded from the store.

        Parameters
        ----------
        patch_size : tuple of int
            Size of the random patch. Must match the number of spatial
            dimensions (trailing dimensions of the array).
        rng : numpy.random.Generator, optional
            Random number generator for reproducibility. If ``None``,
            a default generator is created with ``numpy.random.default_rng()``.

        Returns
        -------
        numpy.ndarray
            Random patch of shape ``patch_size``.

        Example
        -------
        >>> patch = proxy.random_patch((256, 256))
        """
        import numpy as np

        shape = self._array.shape
        ndim = self._array.ndim
        n_spatial = len(patch_size)

        if n_spatial > ndim:
            raise ValueError(
                f"patch_size has {n_spatial} dimensions but array has {ndim} dimensions"
            )

        n_leading = ndim - n_spatial
        if rng is None:
            rng = np.random.default_rng()

        leading_slices = tuple(slice(None) for _ in range(n_leading))
        spatial_starts = tuple(
            rng.integers(0, max(shape[n_leading + i] - ps + 1, 1))
            for i, ps in enumerate(patch_size)
        )
        spatial_slices = tuple(
            slice(int(s), min(int(s) + ps, shape[n_leading + i]))
            for i, (s, ps) in enumerate(zip(spatial_starts, patch_size))
        )
        return self[leading_slices + spatial_slices]

    def __getstate__(self):
        # Drop the zarr.Array reference on pickle; it will be re-opened
        # by the enclosing ZarrProxy on first access after unpickling.
        return {
            "path": self._path,
            "token_per_repo_id": self._token_per_repo_id,
            "storage_options": self._storage_options,
        }

    def __setstate__(self, state):
        self._path = state["path"]
        self._token_per_repo_id = state.get("token_per_repo_id", {})
        self._storage_options = state.get("storage_options")
        self._array = _reopen_zarr_node(
            self._path, self._token_per_repo_id, self._storage_options
        )


@dataclass
class Zarr:
    """Zarr feature for lazy loading of n-dimensional arrays from Zarr stores.

    Supports plain Zarr arrays. The feature stores only the path to the Zarr
    store in Arrow format. When decoded, it returns a lazy proxy object
    (``ZarrProxy``) that opens the store on first access, enabling efficient
    streaming of large arrays with minimal memory overhead — only the chunks
    needed for a given slice are fetched from the store.

    Reads are optimized with two internal, read-only-safe caches:

    - Open stores are reused per ``(path, token, storage_options)`` instead
      of being re-opened (and re-reading metadata) on every decode.
    - Decoded chunks are memoized in a bytes-bounded LRU cache (256 MiB by
      default, configurable via the ``DATASETS_ZARR_CHUNK_CACHE_SIZE``
      environment variable in bytes; ``0`` disables it), so overlapping
      patch/ROI reads decode each shared chunk exactly once.

    Input: The Zarr feature accepts as input:

    - A ``str``: Path to the Zarr store directory (local path or ``hf://`` URL).
    - A ``pathlib.Path``: Path to the Zarr store directory.
    - A ``dict`` with the key:

        - ``path``: String with path to the Zarr store.

    - A ``zarr.Array`` object.

    Args:
        decode (``bool``, defaults to ``True``):
            Whether to decode the Zarr path into a lazy proxy object. If
            ``False``, the path string is returned as-is.
        storage_options (``dict``, *optional*):
            Extra options forwarded to the fsspec filesystem when opening
            remote stores (e.g. ``{"anon": True}`` for anonymous access to
            public object stores). Resolved access tokens take precedence
            over any ``"token"`` entry here.

            Note: fsspec caching wrappers (``simplecache``) do not support
            the suffix byte-range reads used by the sharding codec, so they
            should not be used for chunk caching of Zarr v3 stores.

    Examples:

        Loading a local Zarr store:

        ```py
        >>> from datasets import Dataset, Zarr
        >>> ds = Dataset.from_dict({"zarr": ["path/to/store.zarr"]}).cast_column("zarr", Zarr())
        >>> ds.features["zarr"]
        Zarr(decode=True, id=None)
        >>> proxy = ds[0]["zarr"]
        >>> proxy.shape
        (120, 120, 139)
        >>> proxy.dtype
        dtype('uint8')
        ```

        Streaming from HuggingFace Hub:

        ```py
        >>> proxy = ds[0]["zarr"]  # Returns a lazy ZarrProxy
        >>> proxy[0:10, 0:10, 0:10]  # Only loads needed chunks
        array(...)
        ```
    """

    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)
    storage_options: Optional[Dict[str, Any]] = field(default=None, repr=False)

    dtype: ClassVar[str] = "datasets.features.zarr.ZarrProxy"
    pa_type: ClassVar[Any] = pa.struct({"path": pa.string()})
    _type: str = field(default="Zarr", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, Path, dict]) -> dict:
        """Encode example into the Arrow storage format.

        Args:
            value (``str``, ``pathlib.Path``, ``dict``, or ``zarr.Array``):
                Data passed as input to Zarr feature.

        Returns:
            ``dict`` with "path" field
        """
        if isinstance(value, str):
            return {"path": value}
        elif isinstance(value, Path):
            return {"path": str(value.absolute())}
        elif isinstance(value, dict):
            if value.get("path") is not None:
                return {"path": value["path"]}
            else:
                raise ValueError(f"A Zarr sample must have a 'path' key, but got {value}")
        elif config.ZARR_AVAILABLE:
            import zarr

            if isinstance(value, zarr.Array):
                path = self._extract_zarr_path(value)
                if path:
                    return {"path": path}
                raise ValueError(
                    f"Cannot encode a zarr {type(value).__name__} without an extractable "
                    f"store path (its store has no 'path'/'root'); pass a string path instead"
                )
        raise ValueError(
            f"A Zarr sample must be a string path, pathlib.Path, dict with 'path' key, "
            f"or a zarr.Array object, but got {type(value).__name__}"
        )

    @staticmethod
    def _extract_zarr_path(zarr_obj) -> Optional[str]:
        """Attempt to extract a file path from a zarr.Array."""
        store = getattr(zarr_obj, "store", None)
        if store is not None:
            path = getattr(store, "path", None)
            if path is not None:
                return str(path)
            root = getattr(store, "root", None)
            if root is not None:
                return str(root)
        return None

    def decode_example(self, value: dict, token_per_repo_id=None) -> Union["ZarrProxy", dict]:
        """Decode a Zarr path into a lazy proxy object.

        Args:
            value (``dict``):
                Dictionary with "path" key pointing to a Zarr store.
            token_per_repo_id (``dict``, *optional*):
                Mapping of repo_id to access tokens for private repositories.

        Returns:
            :class:`ZarrProxy` if ``decode=True``, otherwise the input dict.
        """
        if not self.decode:
            return value

        if not config.ZARR_AVAILABLE:
            raise ImportError("To support decoding Zarr features, please install 'zarr': pip install zarr>=3.0.0")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path = value["path"]
        if path is None:
            raise ValueError(f"A Zarr sample must have a 'path' key, but got {value}")

        return ZarrProxy(
            path=path,
            token_per_repo_id=token_per_repo_id,
            storage_options=self.storage_options,
        )

    def embed_storage(self, storage: pa.StructArray, token_per_repo_id=None) -> pa.StructArray:
        """Embed Zarr stores into the Arrow array.

        Since Zarr stores are directories (not single files), they cannot be
        embedded as bytes. The path reference is preserved as-is for lazy
        access.

        Args:
            storage (:class:`pa.StructArray`):
                PyArrow array to embed.

        Returns:
            :class:`pa.StructArray`: Unchanged storage with path references.
        """
        return storage

    def flatten(self) -> Union["FeatureType", Dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from .features import Value

        return self if self.decode else {"path": Value("string")}

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Zarr Arrow storage type.

        The Arrow types that can be converted to the Zarr pyarrow storage type are:

        - ``pa.string()`` — it must contain the "path" data
        - ``pa.struct({"path": pa.string()})`` — order doesn't matter

        Args:
            storage (:class:`pa.StringArray` or :class:`pa.StructArray`):
                PyArrow array to cast.

        Returns:
            :class:`pa.StructArray`: Array in the Zarr Arrow storage type,
                that is ``pa.struct({"path": pa.string()})``.
        """
        if pa.types.is_string(storage.type):
            storage = pa.StructArray.from_arrays([storage], ["path"], mask=storage.is_null())
        elif pa.types.is_struct(storage.type):
            if storage.type.get_field_index("path") >= 0:
                path_array = storage.field("path")
            else:
                path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([path_array], ["path"], mask=storage.is_null())
        return array_cast(storage, self.pa_type)
