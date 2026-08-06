"""Internal caches for lazy Zarr store access.

Two small, thread-safe, read-only-safe LRU caches make patch/ROI reads
cheaper for both local and remote (``hf://buckets``) stores:

- :class:`StoreRegistry`: reuses one open Zarr group/array per
  ``(path, token, storage_options)`` instead of re-opening (and re-reading
  metadata, or re-initializing an ``HfFileSystem`` for remote stores) on
  every decode.
- :class:`ChunkCache`: memoizes *decoded* chunks. The OS page cache can
  save file reads but never decode work — two overlapping patches touching
  the same chunk would otherwise decode it once per patch. Caching decoded
  chunks makes overlapping batch reads decode each shared chunk exactly
  once.

Because stores are always opened read-only, cached chunks and shared
handles can never go stale.
"""

import os
import threading
from collections import OrderedDict
from typing import Any, Dict, Optional, Sequence, Tuple, Union

from .. import config


def _freeze(value) -> tuple:
    """Recursively turn dicts/lists into a hashable tuple for cache keys."""
    if isinstance(value, dict):
        return tuple(sorted((str(k), _freeze(v)) for k, v in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


def _close_store(store) -> None:
    try:
        close = getattr(store, "close", None)
        if close is not None:
            close()
    except Exception:
        pass


class StoreRegistry:
    """Thread-safe LRU registry of open Zarr roots.

    Keyed by ``(path, token, storage_options)``. Read-only roots are safe to
    share between proxies.
    """

    def __init__(self, maxsize: int = 32):
        self._maxsize = maxsize
        self._cache: "OrderedDict[tuple, Any]" = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: tuple):
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]
        return None

    def put(self, key: tuple, root) -> None:
        with self._lock:
            self._cache[key] = root
            self._cache.move_to_end(key)
            while len(self._cache) > self._maxsize:
                _, old = self._cache.popitem(last=False)
                _close_store(old)

    def clear(self) -> None:
        with self._lock:
            for store in self._cache.values():
                _close_store(store)
            self._cache.clear()


STORE_REGISTRY = StoreRegistry()


def store_key(path: str, token: Optional[str], storage_options: Optional[dict]) -> tuple:
    return (path, token, _freeze(storage_options))


class ChunkCache:
    """Thread-safe, bytes-bounded LRU cache of decoded Zarr chunks.

    Keyed by ``(array_path, chunk_coords)``. ``max_bytes <= 0`` disables the
    cache entirely (reads then bypass the cache and go straight to zarr).
    """

    def __init__(self, max_bytes: int):
        self._max_bytes = max_bytes
        self._cache: "OrderedDict[tuple, tuple]" = OrderedDict()  # key -> (nbytes, ndarray)
        self._bytes = 0
        self._lock = threading.Lock()

    @property
    def max_bytes(self) -> int:
        return self._max_bytes

    def get(self, key: tuple):
        if self._max_bytes <= 0:
            return None
        with self._lock:
            item = self._cache.get(key)
            if item is None:
                return None
            self._cache.move_to_end(key)
            return item[1]

    def put(self, key: tuple, chunk) -> None:
        if self._max_bytes <= 0:
            return
        nbytes = chunk.nbytes
        if nbytes > self._max_bytes:
            return
        with self._lock:
            if key in self._cache:
                old_nbytes, _ = self._cache.pop(key)
                self._bytes -= old_nbytes
            self._cache[key] = (nbytes, chunk)
            self._bytes += nbytes
            self._cache.move_to_end(key)
            while self._bytes > self._max_bytes:
                _, (evicted_bytes, _) = self._cache.popitem(last=False)
                self._bytes -= evicted_bytes

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._bytes = 0


CHUNK_CACHE = ChunkCache(config.ZARR_CHUNK_CACHE_SIZE)


def _selection_result_shape(shape: Sequence[int], key) -> Tuple[int, ...]:
    """Compute the output shape of a basic selection without allocating data.

    ``key`` must be a scalar int, a single slice/ellipsis, or a tuple of
    int/slice/Ellipsis/None (no array-like or negative-step entries — those
    are rejected by the caller before this is reached).
    """
    if isinstance(key, (int, slice, type(Ellipsis))) and not isinstance(key, bool):
        key = (key,)
    if not isinstance(key, tuple):
        raise ValueError(f"Unsupported selection {key!r}")
    if any(isinstance(k, (list, tuple, range)) or hasattr(k, "__array__") for k in key):
        raise ValueError(f"Unsupported selection {key!r}")

    ellipses = sum(1 for k in key if k is Ellipsis)
    if ellipses > 1:
        raise ValueError("An index can only have a single ellipsis")
    non_ellipsis = sum(1 for k in key if k is not Ellipsis and k is not None)
    if ellipses == 1:
        fill = len(shape) - non_ellipsis
        if fill < 0:
            raise ValueError("Too many indices")
    else:
        fill = 0

    result = []
    dim = 0
    for k in key:
        if k is Ellipsis:
            for _ in range(fill):
                result.append(shape[dim])
                dim += 1
        elif k is None:
            result.append(1)
        elif isinstance(k, slice):
            result.append(len(range(*k.indices(shape[dim]))))
            dim += 1
        elif isinstance(k, bool):
            raise ValueError("Boolean index not supported in fast path")
        else:  # int
            if k < 0:
                k += shape[dim]
            if k < 0 or k >= shape[dim]:
                raise IndexError("Index out of bounds")
            dim += 1
    while dim < len(shape):
        result.append(shape[dim])
        dim += 1
    return tuple(result)


def _chunk_abs_slice(chunk_coords: Sequence[int], chunks: Sequence[int], shape: Sequence[int]) -> Tuple[slice, ...]:
    slices = []
    for c, cs, s in zip(chunk_coords, chunks, shape):
        start = c * cs
        stop = min(start + cs, s)
        slices.append(slice(start, stop))
    return tuple(slices)


def cached_array_getitem(array, array_path: str, key):
    """Read ``array[key]`` with decoded-chunk caching and a plain fallback.

    Applies the chunk-level fast path only for *simple* selections: scalar
    int, a single slice/Ellipsis, or a tuple of int/slice/Ellipsis with no
    ``None`` and no negative steps. Anything else (or a disabled cache)
    falls back to the exact ``array[key]`` read, preserving semantics.
    """
    if CHUNK_CACHE.max_bytes <= 0:
        return array[key]

    import numpy as np

    shape = array.shape
    try:
        if isinstance(key, tuple):
            if any(k is None for k in key):
                return array[key]
            if any(isinstance(k, slice) and (k.step or 0) < 0 for k in key):
                return array[key]
            for k in key:
                if not isinstance(k, (int, slice, type(Ellipsis))):
                    return array[key]
        else:
            if not isinstance(key, (int, slice, type(Ellipsis))):
                return array[key]
        result_shape = _selection_result_shape(shape, key)
    except (ValueError, IndexError):
        return array[key]

    out = np.empty(result_shape, dtype=array.dtype)
    async_array = array.async_array
    chunk_grid = async_array.metadata.chunk_grid
    chunks = array.chunks

    from zarr.core.indexing import BasicIndexer
    from zarr.core.sync import sync

    for projection in BasicIndexer(key, shape, chunk_grid):
        coords = tuple(int(c) for c in projection.chunk_coords)
        cache_key = (array_path, coords)
        chunk = CHUNK_CACHE.get(cache_key)
        if chunk is None:
            chunk = sync(
                async_array.get_orthogonal_selection(_chunk_abs_slice(coords, chunks, shape))
            )
            CHUNK_CACHE.put(cache_key, chunk)
        try:
            out[projection.out_selection] = chunk[projection.chunk_selection]
        except (IndexError, ValueError):
            return array[key]
    return out


def read_many(reads: Sequence[tuple], max_workers: Optional[int] = None) -> list:
    """Read several ``(array, array_path, key)`` selections concurrently.

    Each read goes through :func:`cached_array_getitem`, so chunks shared
    between selections (e.g. overlapping patches in a batch) are fetched and
    decoded only once across the whole batch. Returns results in input order.
    """
    if len(reads) <= 1:
        return [cached_array_getitem(*r) for r in reads]

    from concurrent.futures import ThreadPoolExecutor

    n = max_workers or min(8, len(reads))
    with ThreadPoolExecutor(max_workers=n) as pool:
        futures = [pool.submit(cached_array_getitem, *r) for r in reads]
        return [f.result() for f in futures]
