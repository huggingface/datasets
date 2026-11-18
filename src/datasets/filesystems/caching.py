"""Threadsafe *shared block cache* fsspec filesystem, tuned for random-access reads.

Why not the caches that ship with fsspec
----------------------------------------
`fsspec` ships four caching flavours, and none of them fits "decode random frames
out of big remote videos from many threads":

* ``fsspec.filesystem("blockcache")`` / ``CachingFileSystem`` (a.k.a. ``cached``):
  keeps a JSON index of the cache which is loaded/dumped (and rewritten) around
  ``open()``/``cat()``/``get()``, tracks ``_cache_size`` lazily and mutates
  ``self.storage`` in place. It is documented as *not thread safe*, so using it
  from a ``ThreadPoolExecutor`` is a data race on that index (worst case: a
  corrupted cache dir and duplicated downloads).
* ``ReadCacheFileSystem`` (``readcache``): same JSON index, same problem.
* ``WholeFileCacheFileSystem`` / ``SimpleCacheFileSystem``: thread safe (they only
  check ``os.path.exists``) but they copy *whole* files. The videos here are
  ~500 MB each and one pass touches a few MB of each, so this is unusable.
* ``cache_type="readahead"|"bytes"|"mmap"`` on the file object: a real block
  cache, but it lives on the *file handle* and dies on ``close()`` - opening the
  same video again re-downloads the mp4 headers/moov atom. It is not protected
  against two threads fetching the same block either, and its default block size
  is 5 MB, so a 64 KB read pulls 5 MB.

What this module adds
---------------------
1. **One block store shared by every thread and every ``open()`` of a file.**
   Blocks are keyed by ``(file identity, block number)`` where the file identity
   includes the content hash reported by the backend (``blob_id``/etag), so a
   file that changes server-side can never serve stale blocks.
2. **Single-flight fetching**: when several threads need the same missing block
   at the same time, exactly one range request is issued and the others wait for
   it (see ``_InFlight``).
3. **Run coalescing**: consecutive missing blocks are fetched with one range
   request, so sequential readers (parquet/pyarrow, ffmpeg probing) do not turn
   into a request per block.
4. **A global LRU byte budget** across all files (``max_memory``): the cache
   cannot grow without limit, evicted blocks are simply refetched.
5. **Cached metadata** (``info``/``ls``): opening a file or reading ``size`` does
   not hit the Hub API on every sample.
6. **Whole-file caching for small files** (``cat_file``/``read_text``/parquet):
   one streaming request, served from memory afterwards. Big files keep the
   block path, so you never download a whole video to read its header.
7. No on-disk index and no JSON rewritten under concurrency: the mutable state is
   guarded by one lock (plus per-block ``threading.Event``s), so it is safe to
   use from a thread pool or from asyncio executor threads.

Usage
-----
Importing this module registers the filesystem as the ``sharedblockcache``
protocol, so any fsspec url can be wrapped with the chained syntax fsspec uses
for its own caches (``blockcache::``, ``filecache::``, ``simplecache::``)::

    import sharedblockcache                                 # registers the protocol

    with fsspec.open("sharedblockcache::hf://datasets/.../file-000.mp4") as f:
        ...                                                 # torchcodec, pyarrow, ...

    # per-call options go to the cache, and the target's options are nested
    fsspec.open("sharedblockcache::hf://.../file.mp4", block_size=1 << 20,
                max_memory=4 << 30, hf={"token": "..."})

The inline spelling (``sharedblockcache://hf://...``) is accepted by a filesystem
that already knows its target - exactly like fsspec's own caches, a bare url with
no ``::`` carries no hint of which filesystem to wrap. Or use the object::

    from sharedblockcache import SharedBlockCacheFileSystem

    fs = SharedBlockCacheFileSystem(target_protocol="hf", max_memory=2 << 30)
    with fs.open("hf://datasets/.../file-000.mp4") as f:     # cached + threadsafe
        ...
    fs.read_text("hf://datasets/.../meta/info.json")          # cached too
    print(fs.stats())

All these routes end up in the same place: one block store per
``(block_size, max_memory, max_run_blocks)``, shared by every thread, every file
and every filesystem object created with those options.
"""

from __future__ import annotations

import io
import logging
import threading
import time
from collections import OrderedDict
from hashlib import sha256
from typing import Callable, Optional

import fsspec
from fsspec import AbstractFileSystem


logger = logging.getLogger(__name__)

__all__ = [
    "SharedBlockCache",
    "SharedBlockCacheFileSystem",
    "CachedBlockFile",
]

# Pseudo block number used when the *whole* file is cached as a single entry.
_WHOLE = -1

DEFAULT_BLOCK_SIZE = 1 << 20  # 1 MiB: small enough not to over-fetch, big enough
#                             to keep the number of requests reasonable
DEFAULT_MAX_MEMORY = 2 << 30  # 2 GiB of cached bytes, shared by all files
DEFAULT_WHOLE_FILE_MAX_SIZE = 32 << 20  # cache whole files below 32 MiB
DEFAULT_MAX_RUN_BLOCKS = 8  # coalesce at most 8 missing blocks in one request


class _InFlight:
    """Handshake for a block that is being downloaded right now.

    The first thread that needs a missing block becomes the *owner*, performs the
    download, then wakes every thread that asked for the same block meanwhile.
    ``data``/``exc`` are written before ``event.set()``, which gives the waiters a
    happens-before edge (``threading.Event`` is lock based).
    """

    __slots__ = ("event", "data", "exc")

    def __init__(self) -> None:
        self.event = threading.Event()
        self.data: Optional[bytes] = None
        self.exc: Optional[BaseException] = None


class SharedBlockCache:
    """LRU-capped, threadsafe store of ``{(file_key, block_id): bytes}``.

    Parameters
    ----------
    block_size:
        Block granularity in bytes. Every remote read is aligned on it.
    max_memory:
        Global budget for cached bytes, shared by every file of every thread.
        ``0`` disables caching (every read goes to the network).
    max_run_blocks:
        Maximum number of consecutive missing blocks fetched by one request.
    """

    def __init__(
        self,
        block_size: int = DEFAULT_BLOCK_SIZE,
        max_memory: int = DEFAULT_MAX_MEMORY,
        max_run_blocks: int = DEFAULT_MAX_RUN_BLOCKS,
    ) -> None:
        if block_size <= 0:
            raise ValueError("block_size must be > 0")
        self.block_size = int(block_size)
        self.max_memory = int(max_memory)
        self.max_run_blocks = max(1, int(max_run_blocks))
        # One lock protects _data / _inflight / _nbytes / counters. It is only
        # held for dict gymnastics, never around network I/O.
        self._lock = threading.Lock()
        self._data: OrderedDict[tuple[str, int], bytes] = OrderedDict()
        self._inflight: dict[tuple[str, int], _InFlight] = {}
        self._nbytes = 0
        # stats
        self.hits = 0
        self.misses = 0
        self.deduped = 0
        self.requests = 0
        self.downloaded_bytes = 0
        self.evictions = 0
        self.evicted_bytes = 0

    # ------------------------------------------------------------------- API

    def read(
        self,
        file_key: str,
        size: int,
        start: int,
        end: Optional[int],
        fetch: Callable[[int, int], bytes],
    ) -> bytes:
        """Return the bytes of file ``file_key`` in ``[start, end)``.

        ``fetch(start, end)`` performs the actual remote read of an aligned range.
        """
        size = int(size)
        start = max(0, min(int(start), size))
        end = size if end is None else max(start, min(int(end), size))
        if start == end:
            return b""

        # A whole-file entry covers everything, and it is cheaper to slice.
        whole = self._get_whole(file_key)
        if whole is not None:
            return whole[start:end]

        bs = self.block_size
        first, last = start // bs, (end - 1) // bs
        if self.max_memory <= 0 or (last - first + 1) * bs > self.max_memory:
            # This range can never be assembled out of a cache that is smaller
            # than the read itself: stream it and leave the LRU alone.
            return self._read_uncached(start, end, fetch)

        # `pieces[i]` holds block `first + i` (block aligned, slicing happens at
        # the end). Fetched blocks are kept here as well, so an eviction by
        # another thread cannot force us to download them again.
        pieces: list[Optional[bytes]] = [None] * (last - first + 1)
        while True:
            missing = self._fill_from_store(file_key, first, last, pieces)
            if not missing:
                break
            self._fetch_missing(file_key, missing, size, fetch, pieces, first)
        out = []
        for index, block in enumerate(pieces):
            block_start = (first + index) * bs
            lo = max(start, block_start) - block_start
            hi = min(end, block_start + len(block)) - block_start
            out.append(block[lo:hi])
        return b"".join(out)

    def _read_uncached(self, start: int, end: int, fetch) -> bytes:
        """Read a range that is bigger than the cache, in request-sized chunks."""
        step = self.block_size * self.max_run_blocks
        chunks = []
        for chunk_start in range(start, end, step):
            stop = min(end, chunk_start + step)
            data = fetch(chunk_start, stop)
            with self._lock:
                self.requests += 1
                self.downloaded_bytes += len(data)
            chunks.append(data)
        return b"".join(chunks)

    def read_whole(self, file_key: str, size: int, fetch: Callable[[int, int], bytes]) -> bytes:
        """Read a whole file, caching it as a single entry when it can be kept."""
        whole = self._get_whole(file_key)
        if whole is not None:
            return whole
        if size > self.max_memory:  # would evict everything at once: skip caching
            return self._read_uncached(0, size, fetch)
        key = (file_key, _WHOLE)
        with self._lock:
            infl = self._inflight.get(key)
            owner = infl is None
            if owner:
                infl = self._inflight[key] = _InFlight()
            else:
                self.deduped += 1
        if not owner:
            infl.event.wait()
            if infl.exc is not None:
                raise infl.exc
            return infl.data
        # _download() stores the bytes, wakes the waiters and hands back the data
        return self._download([key], 0, size, fetch, remember=True)

    def clear(self, file_key: Optional[str] = None) -> None:
        """Drop cached blocks (of one file, or everything)."""
        with self._lock:
            if file_key is None:
                self._nbytes -= sum(len(block) for block in self._data.values())
                self._data.clear()
            else:
                for key in [k for k in self._data if k[0] == file_key]:
                    self._nbytes -= len(self._data.pop(key))

    def stats(self) -> dict:
        with self._lock:
            return {
                "block_size": self.block_size,
                "max_memory": self.max_memory,
                "cached_bytes": self._nbytes,
                "cached_blocks": len(self._data),
                "hits": self.hits,
                "misses": self.misses,
                "requests": self.requests,
                "downloaded_bytes": self.downloaded_bytes,
                "deduped_waits": self.deduped,
                "evictions": self.evictions,
                "evicted_bytes": self.evicted_bytes,
            }

    def __repr__(self) -> str:
        s = self.stats()
        return (
            f"<SharedBlockCache {s['cached_bytes'] / 1e6:.1f}/{s['max_memory'] / 1e6:.0f} MB "
            f"in {s['cached_blocks']} blocks | {s['hits']} hits / {s['misses']} misses "
            f"-> {s['requests']} requests, {s['downloaded_bytes'] / 1e6:.1f} MB "
            f"| {s['deduped_waits']} duplicate fetches avoided | {s['evictions']} evictions>"
        )

    # ------------------------------------------------------------- internals

    def _get_whole(self, file_key: str) -> Optional[bytes]:
        with self._lock:
            whole = self._data.get((file_key, _WHOLE))
            if whole is not None:
                self._data.move_to_end((file_key, _WHOLE))
                self.hits += 1
            return whole

    def _fill_from_store(self, file_key, first: int, last: int, pieces) -> list[int]:
        """Fill the empty slots of ``pieces`` from the cache.

        Returns the ids of the blocks that are still missing.
        """
        missing = []
        with self._lock:
            for block_id in range(first, last + 1):
                index = block_id - first
                if pieces[index] is not None:
                    continue
                key = (file_key, block_id)
                block = self._data.get(key)
                if block is None:
                    missing.append(block_id)
                    continue
                self._data.move_to_end(key)  # LRU touch
                self.hits += 1
                pieces[index] = block
        return missing

    def _fetch_missing(self, file_key, missing, size: int, fetch, pieces, first: int) -> None:
        """Download the missing blocks, one request per run of consecutive blocks."""
        bs = self.block_size
        index = 0
        while index < len(missing):
            run = [missing[index]]
            index += 1
            while index < len(missing) and missing[index] == run[-1] + 1 and len(run) < self.max_run_blocks:
                run.append(missing[index])
                index += 1
            # Claim the blocks of this run. Someone else may have fetched (or be
            # fetching) some of them in the meantime - for those we wait instead
            # of downloading again.
            with self._lock:
                mine, waiters = [], []
                shared = None
                for block_id in run:
                    key = (file_key, block_id)
                    if key in self._data:
                        continue
                    infl = self._inflight.get(key)
                    if infl is None:
                        if shared is None:
                            shared = _InFlight()
                        self._inflight[key] = shared
                        mine.append(key)
                    else:
                        waiters.append(infl)
                        self.deduped += 1
                self.misses += len(mine) + len(waiters)
                if mine:
                    owned_range = (mine[0][1] * bs, min(size, (mine[-1][1] + 1) * bs))
                else:
                    owned_range = None
            if owned_range is not None:
                # Download first, then wait: waiting for someone else *before*
                # waking the threads that wait on our own blocks would deadlock
                # when two threads need overlapping runs of blocks.
                self._download(mine, owned_range[0], owned_range[1], fetch, remember=True, pieces=pieces, first=first)
            for infl in waiters:
                # If the owner of those blocks failed they are simply still
                # missing, and the caller's loop retries them - the retry then
                # owns the download itself, so the error surfaces there.
                infl.event.wait()

    def _download(self, keys, start, end, fetch, remember=True, pieces=None, first=0) -> bytes:
        """Fetch ``[start, end)`` outside the lock, store it, wake up waiters.

        ``keys`` are the ``(file_key, block_id)`` entries covered by the range; a
        single :class:`_InFlight` usually backs all of them, which is why the
        wake-up list is deduplicated by identity.
        """
        try:
            data = fetch(start, end)
        except BaseException as exc:  # re-raised below, after waking the waiters
            self._release(keys, start, data=None, exc=exc)
            raise
        with self._lock:
            self.requests += 1
            self.downloaded_bytes += len(data)
        if len(data) != end - start:
            # A truncated block would silently hand ffmpeg/pyarrow short data:
            # fail loudly instead of caching something broken.
            exc = OSError(f"Short read: asked {end - start} bytes at {start}, got {len(data)}")
            self._release(keys, start, data=None, exc=exc)
            raise exc
        self._release(keys, start, data=data, exc=None, store=remember, pieces=pieces, first=first)
        return data

    def _release(self, keys, start, data, exc, store=False, pieces=None, first=0):
        """Drop the in-flight registrations of ``keys``, hand the bytes to ``pieces``
        / the LRU, then wake every thread waiting on them."""
        blocks = {}
        file_key = keys[0][0]  # all keys belong to the same file
        with self._lock:
            if data is not None:
                for key in keys:
                    if key[1] == _WHOLE:
                        blocks[key[1]] = data
                        continue
                    # absolute offsets: `keys` may skip blocks that another
                    # thread filled while we were downloading
                    offset = key[1] * self.block_size - start
                    blocks[key[1]] = data[offset : offset + self.block_size]
                if store:
                    for block_id, block in blocks.items():
                        self._store((file_key, block_id), block)
            inflight = [self._inflight.pop(key, None) for key in keys]
        if pieces is not None:
            # the caller keeps its own reference: eviction cannot take it away
            for block_id, block in blocks.items():
                if block_id != _WHOLE:
                    pieces[block_id - first] = block
        for infl in {id(infl): infl for infl in inflight if infl is not None}.values():
            infl.data = data
            infl.exc = exc
            infl.event.set()

    def _store(self, key, data: bytes) -> None:
        """Insert into the LRU, evicting until back under ``max_memory``.

        Caller holds ``self._lock``.
        """
        if len(data) > self.max_memory:
            return  # larger than the whole budget: useless to remember
        previous = self._data.pop(key, None)
        if previous is not None:
            self._nbytes -= len(previous)
        self._data[key] = data
        self._data.move_to_end(key)
        self._nbytes += len(data)
        while self._nbytes > self.max_memory and self._data:
            _, evicted = self._data.popitem(last=False)
            self._nbytes -= len(evicted)
            self.evictions += 1
            self.evicted_bytes += len(evicted)


class CachedBlockFile(io.IOBase):
    """Random-access read-only file object served by a :class:`SharedBlockCache`.

    Implements the subset of the file protocol that random-access readers
    (ffmpeg/torchcodec, pyarrow, ``io.TextIOWrapper``, ...) use: ``read``,
    ``readinto``, ``read1``, ``seek``, ``tell``, ``close`` and friends. Every read
    is answered block-by-block by the shared store, so concurrent readers of the
    same remote file share both the memory and the in-flight downloads.
    """

    def __init__(self, fs: "SharedBlockCacheFileSystem", path: str, size: int, key: str) -> None:
        self.fs = fs
        self.path = path
        self.name = path
        self.size = int(size)
        self.mode = "rb"
        self._key = key
        self._whole = self.size <= fs.whole_file_max_size
        self._loc = 0
        self._closed_flag = False

    # fsspec's AbstractBufferedFile does the same dance: io.IOBase exposes
    # ``closed`` as a C getset, so override it with a property + setter.
    @property
    def closed(self) -> bool:  # type: ignore[override]
        return self._closed_flag

    @closed.setter
    def closed(self, value: bool) -> None:
        self._closed_flag = bool(value)

    @property
    def loc(self) -> int:
        return self._loc

    def _check_open(self) -> None:
        if self._closed_flag:
            raise ValueError("I/O operation on closed file.")

    # ---------------------------------------------------------------- reading

    def read(self, length: Optional[int] = -1) -> bytes:
        self._check_open()
        length = -1 if length is None else int(length)
        if length < 0:
            length = self.size - self._loc
        if length <= 0 or self._loc >= self.size:
            return b""
        end = min(self._loc + length, self.size)
        fetch = self.fs._fetcher(self.path, self.size)
        if self._whole and self._loc == 0 and end == self.size:
            # small file read in one go: keep it as a single entry, exactly like
            # cat_file() would, instead of fragmenting it into blocks
            data = self.fs.store.read_whole(self._key, self.size, fetch)
        else:
            data = self.fs.store.read(self._key, self.size, self._loc, end, fetch)
        self._loc += len(data)
        return data

    def read1(self, length: Optional[int] = -1) -> bytes:
        # we never buffer more than what a single read returns
        return self.read(length)

    def readall(self) -> bytes:
        return self.read(-1)

    def readinto(self, buffer) -> int:
        view = memoryview(buffer).cast("B")
        data = self.read(view.nbytes)
        view[: len(data)] = data
        return len(data)

    def readinto1(self, buffer) -> int:
        return self.readinto(buffer)

    # ---------------------------------------------------------------- seeking

    def seek(self, offset: int, whence: int = 0) -> int:
        self._check_open()
        offset = int(offset)
        if whence == 0:
            loc = offset
        elif whence == 1:
            loc = self._loc + offset
        elif whence == 2:
            loc = self.size + offset
        else:
            raise ValueError(f"Invalid whence {whence!r}, must be 0, 1 or 2")
        # ffmpeg probes with seek(-1, 2) to ask for the position: clamp rather
        # than raise, like fsspec's own buffered file objects do.
        self._loc = max(loc, 0)
        return self._loc

    def tell(self) -> int:
        self._check_open()
        return self._loc

    def seekable(self) -> bool:
        return True

    def readable(self) -> bool:
        return True

    def writable(self) -> bool:
        return False

    def readline(self, length=-1):
        chunk = self.read(1 << 16 if length in (-1, None) else int(length))
        lines = chunk.splitlines(keepends=True)
        if not lines:
            return b""
        if len(lines) > 1:
            self._loc -= sum(len(line) for line in lines[1:])  # give back the excess
        return lines[0]

    # ---------------------------------------------------------------- closing

    def flush(self) -> None:
        self._check_open()

    def close(self) -> None:
        self._closed_flag = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __repr__(self) -> str:
        return f"<CachedBlockFile {self.path!r} size={self.size} loc={self._loc}>"


class SharedBlockCacheFileSystem(AbstractFileSystem):
    """Caching layer over any fsspec filesystem, sharing blocks across threads.

    Registered as the ``sharedblockcache`` protocol on import, which makes the
    chained url syntax work: ``fsspec.open("sharedblockcache::hf://bucket/key")``.

    Parameters
    ----------
    fs / target_protocol / target_options:
        The wrapped filesystem: provide an instance, or a protocol (plus its
        options). ``fsspec``'s chained-url plumbing provides these.
    block_size:
        Size of a cached block; all remote requests are aligned on it.
    max_memory:
        Global budget of cached bytes, shared across all files and threads.
    whole_file_max_size:
        Files of at most this size read with ``cat_file``/``read_text`` are
        fetched and kept as one entry (one streaming request instead of N range
        requests).
    meta_ttl:
        Seconds after which cached ``info``/``ls`` results expire. ``None``
        (default) caches them for the lifetime of the process - right for
        content-addressed storage such as a pinned Hub revision; set a number if
        the remote tree may change while you read it.
    store:
        Share an existing :class:`SharedBlockCache` between filesystems. By
        default the store is looked up in a process-wide registry keyed by
        ``(block_size, max_memory, max_run_blocks)`` so that two identically
        configured filesystems - including the ones fsspec creates per chained
        url - share one cache.
    fo:
        Path of the wrapped file, as passed by fsspec when a url is written as
        ``sharedblockcache::target://path``. See :meth:`_resolve`.
    """

    protocol = "sharedblockcache"
    _store_registry: dict[tuple, SharedBlockCache] = {}
    _store_registry_lock = threading.Lock()

    def __init__(
        self,
        target_protocol: Optional[str] = None,
        target_options: Optional[dict] = None,
        fs: Optional[AbstractFileSystem] = None,
        block_size: int = DEFAULT_BLOCK_SIZE,
        max_memory: int = DEFAULT_MAX_MEMORY,
        whole_file_max_size: int = DEFAULT_WHOLE_FILE_MAX_SIZE,
        max_run_blocks: int = DEFAULT_MAX_RUN_BLOCKS,
        meta_ttl: Optional[float] = None,
        store: Optional[SharedBlockCache] = None,
        fo: Optional[str] = None,
        **kwargs,
    ) -> None:
        if fs is None:
            if target_protocol is None:
                raise ValueError("Provide `fs` or `target_protocol` (or open a sharedblockcache:: url)")
            fs = fsspec.filesystem(target_protocol, **(target_options or {}))
        self.target = fs
        self.block_size = int(block_size)
        self.whole_file_max_size = int(whole_file_max_size)
        self.meta_ttl = meta_ttl
        self.store = store or self._get_store(block_size, max_memory, max_run_blocks)
        # fsspec hands the wrapped path over as `fo` for chained urls; see _resolve
        self._fo = fo if isinstance(fo, str) else None
        # metadata caches, guarded by their own lock (independent from the block
        # store lock, so a `cat_file` never blocks an `info` and vice versa)
        self._meta_lock = threading.Lock()
        self._info_cache: dict[str, tuple[float, dict]] = {}
        self._ls_cache: dict[str, tuple[float, list]] = {}
        self._fetchers: dict[str, Callable[[int, int], bytes]] = {}
        super().__init__(**kwargs)

    @classmethod
    def _get_store(cls, block_size, max_memory, max_run_blocks) -> SharedBlockCache:
        signature = (int(block_size), int(max_memory), int(max_run_blocks))
        with cls._store_registry_lock:
            store = cls._store_registry.get(signature)
            if store is None:
                store = cls._store_registry[signature] = SharedBlockCache(block_size, max_memory, max_run_blocks)
            return store

    @classmethod
    def default_store(cls, block_size=DEFAULT_BLOCK_SIZE, max_memory=DEFAULT_MAX_MEMORY) -> SharedBlockCache:
        """The store shared by filesystems created with these options."""
        return cls._get_store(block_size, max_memory, DEFAULT_MAX_RUN_BLOCKS)

    # --------------------------------------------------------- path handling

    @classmethod
    def _strip_protocol(cls, path):
        """Strip our own prefix and leave everything else as it was given.

        ``hf://...`` (or any other target url) is meaningful to the wrapped
        filesystem, so it is forwarded verbatim: cache keys then do not depend
        on how the path reached us.
        """
        if isinstance(path, list):
            return [cls._strip_protocol(p) for p in path]
        if hasattr(path, "__fspath__"):
            path = path.__fspath__()
        if not isinstance(path, str):
            return path
        protos = (cls.protocol,) if isinstance(cls.protocol, str) else cls.protocol
        for protocol in protos:
            for prefix in (protocol + "://", protocol + "::"):
                if path.startswith(prefix):
                    return path[len(prefix) :]
        return path

    def _resolve(self, path: str) -> str:
        """Turn whatever the caller passed into a path the target understands.

        Three shapes arrive here:

        * a target url, ``hf://datasets/x`` - used as it stands;
        * a bare target path, ``datasets/x`` - qualified with the target's
          protocol, so that it keys the same cache entries as the url above;
        * the empty string, which is what is left of a chained url
          (``sharedblockcache::hf://datasets/x``): fsspec keeps the inner path
          out of the argument list - except for the three caching protocols it
          knows by name - and passes it as ``fo`` instead, so fall back to that.
        """
        path = self._strip_protocol(path)
        if not path and self._fo is not None:
            path = self._strip_protocol(self._fo)
        if "://" in path:
            return path
        return self.target.unstrip_protocol(path)

    # -------------------------------------------------------------- metadata

    @staticmethod
    def _now() -> float:
        return time.monotonic()

    def _fresh(self, entry) -> bool:
        if entry is None:
            return False
        if self.meta_ttl is None:
            return True
        return (self._now() - entry[0]) < self.meta_ttl

    def info(self, path: str, **kwargs) -> dict:
        path = self._resolve(path)
        with self._meta_lock:
            entry = self._info_cache.get(path)
            if self._fresh(entry):
                return dict(entry[1])
        detail = dict(self.target.info(path, **kwargs))
        # the target names entries in its own namespace (``datasets/x``); qualify
        # them, or fsspec's glob/find/walk - which matches returned names against
        # the requested prefix - stops matching
        if detail.get("name"):
            detail["name"] = self._entry_name(detail["name"])
        with self._meta_lock:
            self._info_cache[path] = (self._now(), detail)
        return dict(detail)

    def ls(self, path: str, detail: bool = True, **kwargs) -> list:
        path = self._resolve(path)
        with self._meta_lock:
            entry = self._ls_cache.get(path)
            if self._fresh(entry):
                out = entry[1]
                return out if detail else [item["name"] for item in out]
        out = [dict(item) for item in self.target.ls(path, detail=True, **kwargs)]
        for item in out:
            if item.get("name"):
                item["name"] = self._entry_name(item["name"])
        with self._meta_lock:
            self._ls_cache[path] = (self._now(), out)
        return out if detail else [item["name"] for item in out]

    def _entry_name(self, name: str) -> str:
        """Qualify a name the target returned in its own namespace.

        ``HfFileSystem.ls`` hands back ``datasets/x``; that goes back out as
        ``hf://datasets/x``, which is what fsspec's ``glob``/``find`` match
        against the requested prefix and what a caller can hand straight back.
        """
        if "://" in name:
            return name
        try:
            return self.target.unstrip_protocol(name)
        except Exception:  # pragma: no cover - exotic targets
            return name

    def invalidate_cache(self, path: Optional[str] = None) -> None:
        path = self._resolve(path) if path else None
        with self._meta_lock:
            if path is None:
                self._info_cache.clear()
                self._ls_cache.clear()
                self._fetchers.clear()
            else:
                self._info_cache.pop(path, None)
                for signature in [s for s in self._fetchers if s[0] == path]:
                    del self._fetchers[signature]
                for cached in [p for p in self._ls_cache if p == path or p.startswith(path + "/")]:
                    del self._ls_cache[cached]
        self.target.invalidate_cache(path)

    def _file_key(self, path: str) -> str:
        """Stable identity of a file *version*: path + size + content hash.

        Keying on ``blob_id``/``etag``/``url`` means a new commit (or any server
        side change) transparently misses the cache instead of serving stale
        bytes. The lookup is cheap because ``info()`` is itself cached (and
        expires with ``meta_ttl``).
        """
        path = self._resolve(path)
        detail = self.info(path)
        version = (
            detail.get("blob_id")
            or detail.get("etag")
            or detail.get("version")
            or detail.get("url")
            or "size=%s" % detail.get("size")
        )
        return sha256(f"{path}|{detail.get('size')}|{version}".encode()).hexdigest()[:32]

    # ------------------------------------------------------------ downloading

    def _fetcher(self, path: str, size: int) -> Callable[[int, int], bytes]:
        """A ``fetch(start, end)`` callable doing a single range read per call."""
        signature = (path, size)
        with self._meta_lock:
            fetch = self._fetchers.get(signature)
            if fetch is not None:
                return fetch

        def fetch(start: int, end: int) -> bytes:
            # `size=` skips a metadata request, `cache_type="none"` keeps the
            # request exactly as long as the range we asked for (fsspec's
            # default readahead cache would pull a whole 5 MB block).
            with self.target.open(path, "rb", cache_type="none", size=size) as f:
                f.seek(start)
                out = f.read(end - start)
            return out[: end - start]  # defensive: backends that overshoot

        with self._meta_lock:
            return self._fetchers.setdefault(signature, fetch)

    # ------------------------------------------------------------------ files

    def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
        path = self._resolve(path)
        if "w" in mode or "a" in mode or "+" in mode or "x" in mode:
            # writes are not cached: hand over to the wrapped filesystem
            return self.target.open(
                path,
                mode=mode,
                block_size=block_size,
                autocommit=autocommit,
                cache_options=cache_options,
                **kwargs,
            )
        # text read modes ("rt") are served as bytes too: AbstractFileSystem.open()
        # wraps the returned object in a TextIOWrapper, so reads still go through
        # the cache and "r" keeps working for both flavours
        size = int(self.info(path)["size"])
        return CachedBlockFile(self, path, size, self._file_key(path))

    def cat_file(self, path, start=None, end=None, **kwargs) -> bytes:
        path = self._resolve(path)
        size = int(self.info(path)["size"])
        key = self._file_key(path)
        fetch = self._fetcher(path, size)
        if start is None and end is None:
            if size <= self.whole_file_max_size:
                return self.store.read_whole(key, size, fetch)
            # big file: cached block by block (the LRU decides what survives) or
            # streamed in chunks if it does not fit the budget at all
            return self.store.read(key, size, 0, None, fetch)
        return self.store.read(key, size, start or 0, end, fetch)

    # --------------------------------------------- statistics / maintenance

    def stats(self) -> dict:
        return self.store.stats()

    def clear_cache(self, path: Optional[str] = None) -> None:
        """Drop the cached bytes of one file (or everything)."""
        self.store.clear(self._file_key(path) if path else None)

    def prefetch(self, path: str, progress_callback=None) -> int:
        """Download a whole file into the cache (useful ahead of a hot loop)."""
        path = self._resolve(path)
        size = int(self.info(path)["size"])
        key = self._file_key(path)
        fetch = self._fetcher(path, size)
        bs = self.store.block_size
        done = 0
        for start in range(0, size, bs):
            end = min(size, start + bs)
            self.store.read(key, size, start, end, fetch)
            done += end - start
            if progress_callback is not None:
                progress_callback(done, size)
        return done

    def __getattr__(self, item: str):
        """Let anything we do not care about (``ukey``, ``url``, ``exists``, ...)
        reach the wrapped filesystem, so this class can stand in for it."""
        if item.startswith("_") or item in ("target", "store"):
            # never resolve private/unknown attributes through the target: that
            # would mask half-initialised instances (e.g. while unpickling)
            raise AttributeError(item)
        return getattr(self.target, item)

    def __dir__(self):
        return sorted(set(super().__dir__()) | set(dir(self.target)))

    def __repr__(self) -> str:
        return f"<SharedBlockCacheFileSystem target={self.target!r} {self.store!r}>"
