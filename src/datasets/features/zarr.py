import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import pyarrow as pa

from .. import config
from ..table import array_cast


if TYPE_CHECKING:
    from .features import FeatureType


def _open_zarr_store(path: str, token_per_repo_id: Optional[Dict[str, str]] = None):
    """Open a Zarr store from a local or remote path.

    For local paths, opens directly. For ``hf://`` paths, uses HfFileSystem
    with fsspec. For other URLs, delegates to zarr's built-in URL handling.
    """
    import zarr

    token = None
    if token_per_repo_id:
        if path.startswith("hf://"):
            repo_id = _extract_repo_id_from_hf_path(path)
            token = token_per_repo_id.get(repo_id) if repo_id else None
        if token is None:
            token = next(iter(token_per_repo_id.values()), None)

    if path.startswith("hf://"):
        from zarr.storage import FsspecStore

        storage_options = {"token": token} if token is not None else None
        store = FsspecStore.from_url(path, read_only=True, storage_options=storage_options)
        return zarr.open(store=store, mode="r")
    elif os.path.isdir(path):
        return zarr.open(path, mode="r")
    else:
        try:
            from zarr.storage import FsspecStore

            store = FsspecStore.from_url(path, mode="r")
            return zarr.open(store=store, mode="r")
        except Exception:
            return zarr.open(path, mode="r")


def _extract_repo_id_from_hf_path(path: str) -> Optional[str]:
    """Extract repo_id from an hf:// URL path.

    Handles formats like:
    - ``hf://datasets/user/repo/...`` -> ``user/repo``
    - ``hf://datasets/user/repo@revision/...`` -> ``user/repo``
    """
    if not path.startswith("hf://"):
        return None
    stripped = path[len("hf://") :]
    parts = stripped.split("/")
    if len(parts) >= 3:
        org = parts[1]
        repo = parts[2].split("@")[0]
        return f"{org}/{repo}"
    return None


class ZarrProxy:
    """Lazy proxy that auto-detects OME-Zarr vs plain Zarr on first access.

    Stores only the path and optional auth tokens. The underlying Zarr store
    is opened on first property access (shape, dtype, __getitem__, etc.) and
    cached for subsequent use. The proxy is pickle-safe: it drops the opened
    store on serialization and re-opens on deserialization.
    """

    def __init__(self, path: str, token_per_repo_id: Optional[Dict[str, str]] = None):
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}
        self._resolved = None

    def _resolve(self):
        if self._resolved is None:
            import zarr

            root = _open_zarr_store(self._path, self._token_per_repo_id)
            if isinstance(root, zarr.Group):
                if _is_ome_zarr(root):
                    self._resolved = OmeZarrProxy(root, self._path, self._token_per_repo_id)
                else:
                    self._resolved = ZarrGroupProxy(root, self._path, self._token_per_repo_id)
            else:
                self._resolved = ZarrArrayProxy(root, self._path, self._token_per_repo_id)
        return self._resolved

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

    def __contains__(self, key):
        resolved = self._resolve()
        if hasattr(resolved, "__contains__"):
            return key in resolved
        return False

    def __iter__(self):
        resolved = self._resolve()
        if hasattr(resolved, "keys"):
            return iter(resolved.keys())
        raise TypeError(f"'{type(resolved).__name__}' object is not iterable")

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
        return {"path": self._path, "token_per_repo_id": self._token_per_repo_id}

    def __setstate__(self, state):
        self._path = state["path"]
        self._token_per_repo_id = state.get("token_per_repo_id", {})
        self._resolved = None


class ZarrArrayProxy:
    """Lazy proxy for a plain Zarr array.

    Provides attribute access (shape, dtype, chunks, ndim) and subscript
    access (``__getitem__``) without loading the full array into memory.
    Only the chunks needed for a given slice are fetched from the store.
    """

    def __init__(self, array, path: str, token_per_repo_id: Optional[Dict[str, str]] = None):
        # Store the zarr.Array directly — it holds only metadata + store reference,
        # not the data itself. Data is loaded lazily per-chunk on __getitem__.
        self._array = array
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}

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
        return self._array[key]

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

        import numpy as np

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
            yield coords, self._array[slices]

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
        return self._array[leading_slices + spatial_slices]

    def __getstate__(self):
        # Drop the zarr.Array reference on pickle; it will be re-opened
        # by the enclosing ZarrProxy on first access after unpickling.
        return {"path": self._path, "token_per_repo_id": self._token_per_repo_id}

    def __setstate__(self, state):
        self._path = state["path"]
        self._token_per_repo_id = state.get("token_per_repo_id", {})
        self._array = None  # Will be re-opened lazily via ZarrProxy._resolve()


class ZarrGroupProxy:
    """Lazy proxy for a plain Zarr group (non-OME).

    Provides navigation of group members (arrays and sub-groups) without
    loading data. Access individual arrays via subscript notation
    (``group["array_name"]``).
    """

    def __init__(self, group, path: str, token_per_repo_id: Optional[Dict[str, str]] = None):
        self._group = group
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}

    def __getitem__(self, key):
        item = self._group[key]
        if config.ZARR_AVAILABLE:
            import zarr

            if isinstance(item, zarr.Array):
                return ZarrArrayProxy(item, f"{self._path}/{key}", self._token_per_repo_id)
            return ZarrGroupProxy(item, f"{self._path}/{key}", self._token_per_repo_id)
        return item

    def __contains__(self, key):
        return key in self._group

    def keys(self):
        return list(self._group.keys())

    @property
    def attrs(self):
        return dict(self._group.attrs)

    @property
    def shape(self):
        raise ValueError("ZarrGroup does not have a shape. Access individual arrays via group[key].shape")

    @property
    def dtype(self):
        raise ValueError("ZarrGroup does not have a dtype. Access individual arrays via group[key].dtype")

    @property
    def ndim(self):
        raise ValueError("ZarrGroup does not have ndim. Access individual arrays via group[key].ndim")

    def __repr__(self):
        return f"ZarrGroupProxy(path={self._path!r}, members={list(self._group.keys())})"

    def __getstate__(self):
        return {"path": self._path, "token_per_repo_id": self._token_per_repo_id}

    def __setstate__(self, state):
        self._path = state["path"]
        self._token_per_repo_id = state.get("token_per_repo_id", {})
        self._group = None


class OmeZarrProxy:
    """Lazy proxy for an OME-Zarr multiscale image group.

    Provides access to resolution levels, coordinate metadata, and
    region-based reads without loading the full dataset into memory.

    The OME-Zarr specification (NGFF) stores multiscale metadata in the
    group's ``.zattrs`` (v2) or ``zarr.json`` (v3), describing axes,
    coordinate transformations, and resolution level paths.
    """

    def __init__(self, group, path: str, token_per_repo_id: Optional[Dict[str, str]] = None):
        self._group = group
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}
        self._multiscales = None

    @property
    def multiscales(self):
        if self._multiscales is None:
            self._multiscales = _get_ome_attr(self._group.attrs, "multiscales", [])
        return self._multiscales

    @property
    def num_levels(self):
        if self.multiscales:
            return len(self.multiscales[0].get("datasets", []))
        return 0

    @property
    def axes(self):
        if not self.multiscales:
            return []
        return self.multiscales[0].get("axes", [])

    @property
    def scale(self):
        """Voxel-to-physical coordinate scale for level 0."""
        if not self.multiscales:
            return None
        ms = self.multiscales[0]
        datasets = ms.get("datasets", [])
        if datasets:
            transforms = datasets[0].get("coordinateTransformations", [])
            for t in transforms:
                if t.get("type") == "scale":
                    return t["scale"]
        return None

    @property
    def channel_names(self):
        """Channel names from OME-NGFF omero metadata, if present."""
        omero = _get_ome_attr(self._group.attrs, "omero", {})
        if not isinstance(omero, dict):
            omero = {}
        channels = omero.get("channels", [])
        return [ch.get("label", str(i)) for i, ch in enumerate(channels)] if channels else []

    def get_level(self, level: int = 0):
        """Get a ZarrArrayProxy for the specified resolution level.

        Parameters
        ----------
        level : int
            Resolution level index. Level 0 is highest resolution.
            Negative indices are supported (e.g., -1 for lowest resolution).
        """
        if not self.multiscales:
            raise ValueError("No multiscales metadata found in this Zarr group")
        datasets = self.multiscales[0]["datasets"]
        if level < 0:
            level = len(datasets) + level
        if level < 0 or level >= len(datasets):
            raise IndexError(f"Level {level} out of range for {len(datasets)} levels")
        path = datasets[level]["path"]
        array = self._group[path]
        if config.ZARR_AVAILABLE:
            import zarr

            if isinstance(array, zarr.Array):
                return ZarrArrayProxy(array, f"{self._path}/{path}", self._token_per_repo_id)
        return array

    @property
    def levels(self):
        """Get all resolution levels as ZarrArrayProxy objects."""
        return [self.get_level(i) for i in range(self.num_levels)]

    @property
    def shape(self):
        return self.get_level(0).shape

    @property
    def dtype(self):
        return self.get_level(0).dtype

    @property
    def ndim(self):
        return self.get_level(0).ndim

    def __getitem__(self, key):
        """Access level 0 (highest resolution) by default."""
        return self.get_level(0)[key]

    def __len__(self):
        return self.get_level(0).shape[0] if self.get_level(0).ndim > 0 else 1

    def iter_patches(self, patch_size, stride=None, level=0):
        """Iterate over non-overlapping or strided patches at a given resolution level.

        Yields ``(coordinates, patch)`` tuples where ``coordinates`` is a
        tuple of spatial start indices and ``patch`` is a numpy array of
        shape ``patch_size``. Only the chunks needed for each patch are
        loaded, making this efficient for TB-scale arrays.

        Parameters
        ----------
        patch_size : tuple of int
            Size of each patch in spatial dimensions.
        stride : tuple of int, optional
            Stride between patches. Defaults to ``patch_size`` (non-overlapping).
        level : int, optional
            Resolution level. Level 0 is highest resolution. Negative
            indices supported (e.g., -1 for lowest resolution).

        Yields
        ------
        tuple of (tuple, numpy.ndarray)
            ``(start_indices, patch_array)`` pairs.

        Example
        -------
        >>> for (y, x), patch in proxy.iter_patches((256, 256), level=0):
        ...     prediction = model(patch)
        """
        arr = self.get_level(level)
        yield from arr.iter_patches(patch_size, stride=stride)

    def random_patch(self, patch_size, level=0, rng=None):
        """Extract a random patch at the specified resolution level.

        Parameters
        ----------
        patch_size : tuple of int
            Size of the random patch in spatial dimensions.
        level : int, optional
            Resolution level. Level 0 is highest resolution.
        rng : numpy.random.Generator, optional
            Random number generator for reproducibility.

        Returns
        -------
        numpy.ndarray
            Random patch of shape ``(C, *patch_size)`` or ``patch_size``.
        """
        arr = self.get_level(level)
        return arr.random_patch(patch_size, rng=rng)

    def thumbnail(self, level=-1):
        """Get a thumbnail at the lowest (or specified) resolution level.

        Convenience method for visualization and quick inspection. Loads
        the entire array at the specified level, which is typically small.

        Parameters
        ----------
        level : int, optional
            Resolution level for the thumbnail. Defaults to -1 (lowest
            resolution), which is typically small enough to load in full.

        Returns
        -------
        numpy.ndarray
            The full array at the specified resolution level.
        """
        arr = self.get_level(level)
        return arr[:]

    def __repr__(self):
        return (
            f"OmeZarrProxy(path={self._path!r}, "
            f"shape={self.shape}, "
            f"dtype={self.dtype}, "
            f"levels={self.num_levels})"
        )

    def __getstate__(self):
        return {"path": self._path, "token_per_repo_id": self._token_per_repo_id}

    def __setstate__(self, state):
        self._path = state["path"]
        self._token_per_repo_id = state.get("token_per_repo_id", {})
        self._group = None
        self._multiscales = None


def _get_ome_attr(attrs, key, default=None):
    """Get an OME-Zarr metadata key, supporting both v0.4 and v0.5 formats.

    NGFF v0.4 (Zarr v2) stores metadata at the top level of ``.zattrs``::

        {"multiscales": [...], "omero": {...}}

    NGFF v0.5 (Zarr v3) namespaces everything under the ``"ome"`` key::

        {"ome": {"version": "0.5", "multiscales": [...], "omero": {...}}}

    This helper checks both locations and returns the first match.
    """
    if key in attrs:
        return attrs[key]
    ome = attrs.get("ome", {})
    if isinstance(ome, dict) and key in ome:
        return ome[key]
    return default


def _is_ome_zarr(group) -> bool:
    """Check if a Zarr group has OME-Zarr multiscale metadata."""
    if not config.ZARR_AVAILABLE:
        return False
    attrs = getattr(group, "attrs", {})
    return _get_ome_attr(attrs, "multiscales") is not None


@dataclass
class Zarr:
    """Zarr feature for lazy loading of n-dimensional arrays from Zarr stores.

    Supports both plain Zarr arrays and OME-Zarr multiscale images. The
    feature stores only the path to the Zarr store in Arrow format. When
    decoded, it returns a lazy proxy object (``ZarrProxy``) that opens the
    store on first access, enabling efficient streaming of large arrays with
    minimal memory overhead — only the chunks needed for a given slice are
    fetched from the store.

    Input: The Zarr feature accepts as input:

    - A ``str``: Path to the Zarr store directory (local path or ``hf://`` URL).
    - A ``pathlib.Path``: Path to the Zarr store directory.
    - A ``dict`` with the key:

        - ``path``: String with path to the Zarr store.

    - A ``zarr.Array`` or ``zarr.Group`` object.

    Args:
        decode (``bool``, defaults to ``True``):
            Whether to decode the Zarr path into a lazy proxy object. If
            ``False``, the path string is returned as-is.

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
        >>> proxy = ds[0]["zarr"]  # Returns OmeZarrProxy or ZarrArrayProxy
        >>> proxy[0:10, 0:10, 0:10]  # Only loads needed chunks
        array(...)
        ```
    """

    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    dtype: ClassVar[str] = "datasets.features.zarr.ZarrProxy"
    pa_type: ClassVar[Any] = pa.struct({"path": pa.string()})
    _type: str = field(default="Zarr", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, Path, dict]) -> dict:
        """Encode example into the Arrow storage format.

        Args:
            value (``str``, ``pathlib.Path``, ``dict``, ``zarr.Array``, or ``zarr.Group``):
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

            if isinstance(value, (zarr.Array, zarr.Group)):
                path = self._extract_zarr_path(value)
                return {"path": path} if path else {"path": str(value)}
        raise ValueError(
            f"A Zarr sample must be a string path, pathlib.Path, dict with 'path' key, "
            f"or a zarr.Array/zarr.Group object, but got {type(value).__name__}"
        )

    @staticmethod
    def _extract_zarr_path(zarr_obj) -> Optional[str]:
        """Attempt to extract a file path from a zarr.Array or zarr.Group."""
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

        return ZarrProxy(path=path, token_per_repo_id=token_per_repo_id)

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
