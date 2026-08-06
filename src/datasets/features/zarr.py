import html
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
    """Lazy proxy that auto-detects OME-Zarr vs plain Zarr on first access.

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
            if isinstance(root, zarr.Group):
                if _is_ome_zarr(root):
                    self._resolved = OmeZarrProxy(
                        root, self._path, self._token_per_repo_id, self._storage_options
                    )
                else:
                    self._resolved = ZarrGroupProxy(
                        root, self._path, self._token_per_repo_id, self._storage_options
                    )
            else:
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
        if name.startswith("_") and name != "_repr_html_":
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

    def _repr_html_(self):
        """HTML representation with an embedded thumbnail image.

        Renders the array (if it is 2D+ and small enough) as a
        base64-encoded PNG inside an ``<img>`` tag. Returns ``None`` if no
        imaging backend (Pillow/matplotlib) is available, if the array is
        too large to materialize, or if rendering fails — Jupyter then falls
        back to ``__repr__``.
        """
        if self._array.ndim < 2 or self._array.nbytes > 32 * 1024 * 1024:
            return None
        try:
            import base64

            img = _render_array_as_png(self._array[:])
            if img is None:
                return None
            b64 = base64.b64encode(img).decode("ascii")
        except Exception:
            return None
        return (
            "<div style='font-family: monospace; white-space: nowrap;'>"
            f"{html.escape(self._path)}<br>"
            f"shape={self.shape}, dtype={self.dtype}"
            f"<br><img src='data:image/png;base64,{b64}' "
            "style='max-width: 512px; max-height: 512px;'>"
            "</div>"
        )

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
        self._array = None  # Will be re-opened lazily via ZarrProxy._resolve()


class ZarrGroupProxy:
    """Lazy proxy for a plain Zarr group (non-OME).

    Provides navigation of group members (arrays and sub-groups) without
    loading data. Access individual arrays via subscript notation
    (``group["array_name"]``).
    """

    def __init__(
        self,
        group,
        path: str,
        token_per_repo_id: Optional[Dict[str, str]] = None,
        storage_options: Optional[Dict[str, Any]] = None,
    ):
        self._group = group
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}
        self._storage_options = dict(storage_options) if storage_options else None

    def __getitem__(self, key):
        item = self._group[key]
        if config.ZARR_AVAILABLE:
            import zarr

            if isinstance(item, zarr.Array):
                return ZarrArrayProxy(
                    item, f"{self._path}/{key}", self._token_per_repo_id, self._storage_options
                )
            return ZarrGroupProxy(
                item, f"{self._path}/{key}", self._token_per_repo_id, self._storage_options
            )
        return item

    def __contains__(self, key):
        return key in self._group

    def keys(self):
        return list(self._group.keys())

    @property
    def path(self):
        return self._path

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

    def asarray(self):
        raise TypeError(
            "ZarrGroup cannot be converted to a numpy array. "
            "Access individual arrays via group[key].asarray()"
        )

    def __repr__(self):
        return f"ZarrGroupProxy(path={self._path!r}, members={list(self._group.keys())})"

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
        self._group = None


class OmeZarrProxy:
    """Lazy proxy for an OME-Zarr multiscale image group.

    Provides access to resolution levels, coordinate metadata, and
    region-based reads without loading the full dataset into memory.

    The OME-Zarr specification (NGFF) stores multiscale metadata in the
    group's ``.zattrs`` (v2) or ``zarr.json`` (v3), describing axes,
    coordinate transformations, and resolution level paths.
    """

    def __init__(
        self,
        group,
        path: str,
        token_per_repo_id: Optional[Dict[str, str]] = None,
        storage_options: Optional[Dict[str, Any]] = None,
    ):
        self._group = group
        self._path = path
        self._token_per_repo_id = token_per_repo_id or {}
        self._storage_options = dict(storage_options) if storage_options else None
        self._multiscales = None

    @property
    def path(self):
        return self._path

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
    def axis_names(self):
        """Axis names from the multiscales metadata (e.g. ``["c", "z", "y", "x"]``)."""
        return [
            a["name"] if isinstance(a, dict) and "name" in a else a
            for a in self.axes
        ]

    @property
    def axis_types(self):
        """Axis types from the multiscales metadata (e.g. ``["channel", "space", "space"]``).

        Entries without an explicit type (or plain-string axes) map to ``""``.
        """
        return [a.get("type", "") if isinstance(a, dict) else "" for a in self.axes]

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
                return ZarrArrayProxy(
                    array, f"{self._path}/{path}", self._token_per_repo_id, self._storage_options
                )
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

    @property
    def chunks(self):
        return self.get_level(0).chunks

    def __getitem__(self, key):
        """Access level 0 (highest resolution) by default."""
        return self.get_level(0)[key]

    def __len__(self):
        return self.get_level(0).shape[0] if self.get_level(0).ndim > 0 else 1

    def _level_transform(self, level: int = 0):
        """Return the ``(scale, translation)`` coordinate transform for a level.

        ``scale`` and ``translation`` are lists with one entry per array
        axis (physical units per voxel / origin offset), taken from the
        OME-Zarr ``coordinateTransformations`` metadata. Either may be
        ``None`` when the metadata omits it.
        """
        if not self.multiscales:
            return None, None
        datasets = self.multiscales[0].get("datasets", [])
        if level < 0:
            level = len(datasets) + level
        if level < 0 or level >= len(datasets):
            raise IndexError(f"Level {level} out of range for {len(datasets)} levels")
        transforms = datasets[level].get("coordinateTransformations", [])
        scale, translation = None, None
        for t in transforms:
            if t.get("type") == "scale":
                scale = t["scale"]
            elif t.get("type") == "translation":
                translation = t["translation"]
        return scale, translation

    def roi(self, start, stop, level: int = 0):
        """Read a region of interest given in physical (world) coordinates.

        Coordinates are converted to pixel indices with the selected
        level's own ``scale``/``translation`` metadata, so the region is
        independent of the resolution level. Non-spatial axes (e.g. a
        channel axis) usually have scale 1 and translation 0, in which
        case their entries behave like plain pixel indices.

        Parameters
        ----------
        start : tuple of float
            Start of the region per axis, in physical units (e.g.
            micrometers when the OME metadata declares micrometer axes).
            Entries may be ``None`` to start from the array origin.
        stop : tuple of float
            End of the region per axis, in physical units. Entries may be
            ``None`` to extend to the end of the array.
        level : int, optional
            Resolution level. Level 0 is highest resolution; negative
            indices supported (e.g., -1 for lowest resolution).

        Returns
        -------
        numpy.ndarray
            The requested region at the given level. The region is
            clipped to the array extent.

        Example
        -------
        >>> region = proxy.roi((0.0, 100.0, 200.0), (1.0, 300.0, 400.0), level=0)
        """
        import numpy as np

        arr = self.get_level(level)
        shape = arr.shape
        scale, translation = self._level_transform(level)
        if scale is None:
            raise ValueError("No scale coordinate transformation found in multiscales metadata")
        if len(scale) != len(shape):
            raise ValueError(
                f"Scale metadata has {len(scale)} entries but the array has {len(shape)} axes"
            )
        if len(start) != len(stop):
            raise ValueError("start and stop must have the same number of entries")
        if len(start) != len(shape):
            raise ValueError(
                f"start and stop must have one entry per axis ({len(shape)}), got {len(start)}"
            )

        slices = []
        for i, (s, e) in enumerate(zip(start, stop)):
            sc = scale[i]
            tr = translation[i] if translation is not None else 0.0
            start_idx = int(np.floor((s - tr) / sc)) if s is not None else 0
            stop_idx = int(np.ceil((e - tr) / sc)) if e is not None else shape[i]
            start_idx = max(start_idx, 0)
            stop_idx = min(stop_idx, shape[i])
            if stop_idx < start_idx:
                stop_idx = start_idx
            slices.append(slice(start_idx, stop_idx))
        return arr[tuple(slices)]

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

    def asarray(self, level: int = 0):
        """Load a resolution level into memory and return it as a numpy array.

        Parameters
        ----------
        level : int, optional
            Resolution level. Defaults to 0 (highest resolution). Use
            ``-1`` for the lowest resolution (usually small enough to load
            in full).

        Returns
        -------
        numpy.ndarray
            The full array at the specified resolution level.

        Warning: this materializes the entire level. For large stores,
        prefer slicing (``proxy[...]``) or ``iter_patches``/``random_patch``.
        """
        return self.get_level(level).asarray()

    def _repr_html_(self):
        """HTML representation with an embedded thumbnail image.

        Renders the lowest-resolution level as a base64-encoded PNG inside
        an ``<img>`` tag, so large volumes can be previewed without loading
        many chunks. Returns ``None`` if no imaging backend (Pillow/
        matplotlib) is available or if rendering fails — Jupyter then falls
        back to ``__repr__``.
        """
        if self.num_levels == 0:
            return None
        try:
            import base64

            img = _render_array_as_png(self.thumbnail(level=-1))
            if img is None:
                return None
            b64 = base64.b64encode(img).decode("ascii")
        except Exception:
            return None
        return (
            "<div style='font-family: monospace; white-space: nowrap;'>"
            f"{html.escape(self._path)}<br>"
            f"shape={self.shape}, dtype={self.dtype}, levels={self.num_levels}"
            f"<br><img src='data:image/png;base64,{b64}' "
            "style='max-width: 512px; max-height: 512px;'>"
            "</div>"
        )

    def __repr__(self):
        return (
            f"OmeZarrProxy(path={self._path!r}, "
            f"shape={self.shape}, "
            f"dtype={self.dtype}, "
            f"levels={self.num_levels})"
        )

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


def _render_array_as_png(array) -> Optional[bytes]:
    """Render a numpy array as PNG-encoded 2D grayscale bytes.

    Non-spatial leading dimensions (channel/time/z) are collapsed with a
    mean projection, and values are clipped to the 2nd-98th percentiles for
    robust display contrast.

    Returns ``None`` if the array cannot be rendered as an image (less than
    2D, empty) or if no imaging backend (Pillow, then matplotlib) is
    installed.
    """
    import numpy as np

    arr = np.asarray(array)
    if arr.ndim < 2 or arr.size == 0:
        return None

    img = arr.mean(axis=tuple(range(arr.ndim - 2))) if arr.ndim > 2 else arr
    img = np.asarray(img, dtype="float64")
    if img.shape[0] == 0 or img.shape[1] == 0:
        return None

    low, high = np.percentile(img, (2, 98))
    if high > low:
        img = np.clip((img - low) / (high - low), 0.0, 1.0)
    else:
        img = np.zeros_like(img)
    img8 = (img * 255).astype("uint8")

    import io

    try:
        from PIL import Image

        im = Image.fromarray(img8, mode="L")
        im.thumbnail((256, 256), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        pass

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        buf = io.BytesIO()
        fig = plt.figure(figsize=(3, 3))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ax.imshow(img8, cmap="gray", aspect="auto")
        fig.savefig(buf, format="png")
        plt.close(fig)
        return buf.getvalue()
    except Exception:
        return None


@dataclass
class Zarr:
    """Zarr feature for lazy loading of n-dimensional arrays from Zarr stores.

    Supports both plain Zarr arrays and OME-Zarr multiscale images. The
    feature stores only the path to the Zarr store in Arrow format. When
    decoded, it returns a lazy proxy object (``ZarrProxy``) that opens the
    store on first access, enabling efficient streaming of large arrays with
    minimal memory overhead — only the chunks needed for a given slice are
    fetched from the store.

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

    - A ``zarr.Array`` or ``zarr.Group`` object.

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
        >>> proxy = ds[0]["zarr"]  # Returns OmeZarrProxy or ZarrArrayProxy
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
