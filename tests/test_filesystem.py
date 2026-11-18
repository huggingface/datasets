import concurrent.futures as cf
import hashlib
import os
import random
import threading
import time

import fsspec
import pytest
from fsspec.core import url_to_fs
from fsspec.registry import _registry as _fsspec_registry

from datasets.filesystems import COMPRESSION_FILESYSTEMS, is_remote_filesystem
from datasets.filesystems.caching import (
    CachedBlockFile,
    SharedBlockCache,
    SharedBlockCacheFileSystem,
)

from .utils import require_lz4, require_zstandard


def test_mockfs(mockfs):
    assert "mock" in _fsspec_registry
    assert "bz2" in _fsspec_registry


def test_non_mockfs():
    assert "mock" not in _fsspec_registry
    assert "bz2" in _fsspec_registry


def test_is_remote_filesystem(mockfs):
    is_remote = is_remote_filesystem(mockfs)
    assert is_remote is True

    fs = fsspec.filesystem("file")

    is_remote = is_remote_filesystem(fs)
    assert is_remote is False


@pytest.mark.parametrize("compression_fs_class", COMPRESSION_FILESYSTEMS)
def test_compression_filesystems(compression_fs_class, gz_file, bz2_file, lz4_file, zstd_file, xz_file, text_file):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "lz4": lz4_file}
    input_path = input_paths[compression_fs_class.protocol]
    if input_path is None:
        reason = f"for '{compression_fs_class.protocol}' compression protocol, "
        if compression_fs_class.protocol == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_fs_class.protocol == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    fs = fsspec.filesystem(compression_fs_class.protocol, fo=input_path)
    expected_filename = os.path.basename(input_path)
    expected_filename = expected_filename[: expected_filename.rindex(".")]
    assert fs.glob("*") == [expected_filename]
    with fs.open(expected_filename, "r", encoding="utf-8") as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize("protocol", ["zip", "gzip"])
def test_fs_isfile(protocol, zip_jsonl_path, jsonl_gz_path):
    compressed_file_paths = {"zip": zip_jsonl_path, "gzip": jsonl_gz_path}
    compressed_file_path = compressed_file_paths[protocol]
    member_file_path = "dataset.jsonl"
    path = f"{protocol}://{member_file_path}::{compressed_file_path}"
    fs, *_ = url_to_fs(path)
    assert fs.isfile(member_file_path)
    assert not fs.isfile("non_existing_" + member_file_path)


class SlowFS(fsspec.AbstractFileSystem):
    """In-memory backend that counts range reads and sleeps to force overlap."""

    protocol = "slow"

    def __init__(self, latency=0.02, **kw):
        super().__init__(**kw)
        self.data = {}
        self.latency = latency
        self.short = 0  # number of bytes to withhold from each range read
        self.lock = threading.Lock()
        self.requests = 0
        self.bytes_downloaded = 0

    def write(self, path, payload):
        self.data[self._strip_protocol(path)] = payload

    def info(self, path, **kwargs):
        path = self._strip_protocol(path)
        payload = self.data[path]
        return {
            "name": path,
            "size": len(payload),
            "type": "file",
            "blob_id": hashlib.sha1(payload).hexdigest(),
        }

    def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, size=None, **kwargs):
        path = self._strip_protocol(path)
        payload = self.data[path]
        outer = self

        class Handle(fsspec.spec.AbstractBufferedFile):
            def _fetch_range(self, start, end):
                with outer.lock:
                    outer.requests += 1
                    outer.bytes_downloaded += end - start
                time.sleep(outer.latency)  # make concurrent duplicate fetches observable
                return payload[start : end - outer.short]

        return Handle(self, path, mode=mode, size=size, block_size=block_size or 5 * 2**20, **kwargs)


class SharedSlowFS(SlowFS):
    """Several client instances looking at the same remote data and totals."""

    _shared: dict = {"payloads": {}, "requests": 0, "bytes": 0, "lock": threading.Lock()}

    def __init__(self, *args, **kw):
        kw.setdefault("latency", 0.005)
        super().__init__(*args, **kw)
        self.data = self._shared["payloads"]
        self.lock = self._shared["lock"]

    @property
    def requests(self) -> int:
        return self._shared["requests"]

    @requests.setter
    def requests(self, value: int) -> None:
        # __init__ sets 0 on every instance: keep the global total instead
        self._shared["requests"] = max(self._shared["requests"], value)

    @property
    def bytes_downloaded(self) -> int:
        return self._shared["bytes"]

    @bytes_downloaded.setter
    def bytes_downloaded(self, value: int) -> None:
        self._shared["bytes"] = max(self._shared["bytes"], value)


@pytest.fixture
def backend():
    # skip_instance_cache: fsspec caches filesystem instances per (class, args),
    # and each test needs a pristine backend
    fs = SlowFS(latency=0.02, skip_instance_cache=True)
    rng = random.Random(0)
    fs.write("/file.bin", bytes(rng.randrange(256) for _ in range(4 * 1024 * 1024)))
    fs.write("/small.json", b'{"hello": "world"}')
    return fs


def make_cache(backend, **kw):
    kw.setdefault("block_size", 64 * 1024)
    kw.setdefault("max_memory", 512 * 1024)
    # a fresh store per test: by default stores are shared process-wide between
    # identically configured filesystems, which would leak between tests
    store = SharedBlockCache(kw["block_size"], kw["max_memory"])
    return SharedBlockCacheFileSystem(fs=backend, store=store, **kw)


class ListingSlowFS(SharedSlowFS):
    """Shared backend that also behaves like a flat directory, for ls/glob tests."""

    def info(self, path, **kwargs):
        path = self._strip_protocol(path)
        if path in ("", "/"):
            return {"name": path, "size": 0, "type": "directory"}
        return super().info(path, **kwargs)

    def ls(self, path, detail=True, **kwargs):
        path = self._strip_protocol(path)
        if path not in ("", "/"):
            return [super().info(path)]
        entries = [{"name": p, "size": len(d), "type": "file"} for p, d in sorted(self.data.items())]
        return entries if detail else [e["name"] for e in entries]


@pytest.fixture
def remote():
    """The backend behind the registered ``slow`` protocol, shared by every client."""
    fsspec.register_implementation("slow", ListingSlowFS, clobber=True)
    fs = ListingSlowFS(skip_instance_cache=True)
    rng = random.Random(11)
    fs.write("/movie.mp4", bytes(rng.randrange(256) for _ in range(2 * 1024 * 1024)))
    fs.write("/clip.mp4", bytes(rng.randrange(256) for _ in range(64 * 1024)))
    return fs


def test_read_matches_backend(backend):
    cfs = make_cache(backend)
    reference = backend.data["/file.bin"]
    rng = random.Random(1)
    with cfs.open("/file.bin") as f:
        for _ in range(30):
            start = rng.randrange(0, len(reference) - 1)
            length = rng.randrange(1, 300_000)
            f.seek(start)
            assert f.read(length) == reference[start : start + length]
        f.seek(-100, 2)
        assert f.read(100) == reference[-100:]
        f.seek(0)
        assert f.read() == reference  # read all


def test_readinto_and_read1(backend):
    cfs = make_cache(backend)
    reference = backend.data["/file.bin"]
    buf = bytearray(1000)
    with cfs.open("/file.bin") as f:
        assert f.readinto(buf) == 1000
        assert bytes(buf) == reference[:1000]
        assert f.read1(10) == reference[1000:1010]
        assert f.tell() == 1010
        assert f.readable() and f.seekable() and not f.writable()


def test_blocks_are_aligned_and_reused(backend):
    cfs = make_cache(backend, block_size=64 * 1024)
    with cfs.open("/file.bin") as f:
        f.seek(1000)
        f.read(100)
    assert backend.requests == 1  # one aligned block for a 100 byte read
    assert backend.bytes_downloaded == 64 * 1024
    with cfs.open("/file.bin") as f:  # a NEW handle hits the shared store
        f.seek(1000)
        assert f.read(100) == backend.data["/file.bin"][1000:1100]
    assert backend.requests == 1
    assert cfs.stats()["hits"] >= 1


def test_cache_survives_close_and_is_shared_between_handles(backend):
    cfs = make_cache(backend)
    for _ in range(5):
        with cfs.open("/file.bin") as f:
            f.seek(0)
            assert f.read(1000)
    assert backend.requests == 1  # 5 opens, one download


def test_no_cache_mode_passthrough(backend):
    cfs = make_cache(backend, max_memory=0)
    for _ in range(3):
        with cfs.open("/file.bin") as f:
            f.seek(0)
            f.read(1000)
    assert backend.requests == 3
    assert cfs.stats()["cached_bytes"] == 0


def test_memory_budget_is_respected(backend):
    cfs = make_cache(backend, block_size=64 * 1024, max_memory=256 * 1024)
    rng = random.Random(7)
    reference = backend.data["/file.bin"]
    for _ in range(200):
        start = rng.randrange(0, len(reference) - 4096)
        with cfs.open("/file.bin") as f:
            f.seek(start)
            assert f.read(4096) == reference[start : start + 4096]
    assert cfs.stats()["cached_bytes"] <= 256 * 1024
    assert cfs.stats()["evictions"] > 0


def test_concurrent_reads_are_correct_and_deduplicated(backend):
    """The whole point: 16 threads, same blocks, one download per block."""
    cfs = make_cache(backend, block_size=64 * 1024, max_memory=64 * 1024 * 1024)
    reference = backend.data["/file.bin"]
    n_threads, n_rounds = 16, 8

    def worker(seed):
        rng = random.Random(seed)
        with cfs.open("/file.bin") as f:
            for _ in range(n_rounds):
                start = rng.randrange(0, 1024 * 1024)  # every thread works in the first MB
                length = 200_000
                f.seek(start)
                assert f.read(length) == reference[start : start + length]

    with cf.ThreadPoolExecutor(max_workers=n_threads) as pool:
        list(pool.map(worker, range(n_threads)))
    stats = cfs.stats()
    # the whole first MB is 16 blocks; without single-flight this would be
    # 16 threads * 8 rounds * ~4 blocks = 512 requests
    assert stats["requests"] <= 32, stats
    assert stats["deduped_waits"] > 0, stats
    # consecutive missing blocks are coalesced, so a request may carry a run of
    # blocks - but never more than the working set we were reading
    assert stats["downloaded_bytes"] % (64 * 1024) == 0, stats
    assert stats["downloaded_bytes"] <= 20 * 64 * 1024, stats


def test_stress_random_access_threads(backend):
    """Hammer the cache from many threads, checking bytes every time."""
    cfs = make_cache(backend, block_size=16 * 1024, max_memory=128 * 1024)
    reference = backend.data["/file.bin"]
    errors = []

    def worker(seed):
        rng = random.Random(seed)
        try:
            for _ in range(40):
                start = rng.randrange(0, len(reference) - 1)
                length = rng.randrange(1, 100_000)
                with cfs.open("/file.bin") as f:
                    f.seek(start)
                    got = f.read(length)
                if got != reference[start : start + length]:
                    errors.append((seed, start, length))
        except Exception as exc:  # noqa: BLE001
            errors.append((seed, repr(exc)))

    with cf.ThreadPoolExecutor(max_workers=12) as pool:
        list(pool.map(worker, range(24)))
    assert not errors


def test_error_is_propagated_and_not_cached(backend):
    cfs = make_cache(backend)
    calls = []
    original = backend.info

    def flaky_info(path, **kw):
        calls.append(path)
        if len(calls) <= 1:
            raise OSError("boom")
        return original(path, **kw)

    backend.info = flaky_info
    with pytest.raises(OSError):
        cfs.open("/file.bin")
    with cfs.open("/file.bin") as f:  # retry works, nothing poisoned
        assert f.read(10)
    assert cfs.stats()["misses"] >= 1


def test_short_read_is_not_cached(backend):
    """A backend that returns fewer bytes than asked must not poison the cache."""
    cfs = make_cache(backend)
    payload = backend.data["/file.bin"]
    backend.short = 10
    with cfs.open("/file.bin") as f:
        with pytest.raises(OSError, match="Short read"):
            f.read(100)
    assert cfs.stats()["cached_blocks"] == 0
    backend.short = 0
    with cfs.open("/file.bin") as f:
        assert f.read(100) == payload[:100]


def test_whole_file_caching_for_small_files(backend):
    cfs = make_cache(backend)
    assert cfs.read_text("/small.json") == '{"hello": "world"}'
    assert cfs.cat_file("/small.json") == b'{"hello": "world"}'
    assert cfs.read_bytes("/small.json") == b'{"hello": "world"}'
    assert cfs.stats()["cached_blocks"] == 1
    assert cfs.info("/small.json")["size"] == 18
    assert backend.requests <= 2  # one streaming request for the whole file


def test_metadata_is_cached(backend):
    cfs = make_cache(backend, meta_ttl=None)
    infos = []
    original = backend.info

    def counting_info(path, **kw):
        infos.append(path)
        return original(path, **kw)

    backend.info = counting_info
    for _ in range(10):
        assert cfs.size("/file.bin") == 4 * 1024 * 1024
    assert len(infos) == 1
    # a short ttl refreshes it
    cfs.meta_ttl = 0.001
    time.sleep(0.01)
    cfs.size("/file.bin")
    assert len(infos) == 2


def test_stale_key_change_invalidates_cache(backend):
    # meta_ttl=None caches file metadata forever: a server side change is only
    # seen after invalidate_cache(), which is the documented behaviour for
    # content-addressed stores such as a pinned Hub revision.
    cfs = make_cache(backend)
    with cfs.open("/small.json") as f:
        assert f.read() == b'{"hello": "world"}'
    assert backend.requests == 1
    backend.write("/small.json", b'{"hello": "universe"}')
    cfs.invalidate_cache("/small.json")  # metadata refreshed -> new blob_id
    with cfs.open("/small.json") as f:
        assert f.read() == b'{"hello": "universe"}'
    assert backend.requests == 2

    # with a ttl, the change is picked up on its own
    backend.write("/small.json", b'{"hello": "cosmos"}')
    cfs.meta_ttl = 0.001
    time.sleep(0.01)
    with cfs.open("/small.json") as f:
        assert f.read() == b'{"hello": "cosmos"}'
    assert backend.requests == 3


def test_backend_request_count_is_the_point(backend):
    """Simulate the workload: N samples, each reading a few KB of the same file.

    Uncached this costs N requests; cached, one request per block.
    """
    plain = backend
    reference = plain.data["/file.bin"]
    n_samples = 200
    for i in range(n_samples):
        with plain.open("/file.bin", cache_type="none") as f:
            f.seek(i * 4096)
            f.read(1000)
    uncached = plain.requests

    plain.requests = 0
    cfs = make_cache(backend, block_size=64 * 1024, max_memory=512 * 1024 * 1024)
    for i in range(n_samples):
        with cfs.open("/file.bin") as f:
            f.seek(i * 4096)
            assert f.read(1000) == reference[i * 4096 : i * 4096 + 1000]
    assert plain.requests < uncached / 5


def test_registered_as_filesystem(backend):
    fsspec.register_implementation("slowcached", SharedBlockCacheFileSystem, clobber=True)
    fs = fsspec.filesystem("slowcached", fs=backend, block_size=64 * 1024, store=SharedBlockCache(64 * 1024, 1 << 20))
    assert isinstance(fs, SharedBlockCacheFileSystem)
    assert fs.cat_file("/small.json") == b'{"hello": "world"}'


def test_stores_are_shared_per_configuration(backend):
    """Two filesystems with the same options share one store (that is the point)."""
    options = {"block_size": 64 * 1024, "max_memory": 8 * 1024 * 1024, "meta_ttl": 1234}
    fs_a = SharedBlockCacheFileSystem(fs=backend, skip_instance_cache=True, **options)
    fs_b = SharedBlockCacheFileSystem(fs=backend, skip_instance_cache=True, **options)
    assert fs_a.store is fs_b.store
    fs_a.cat_file("/small.json")
    assert backend.requests == 1
    fs_b.cat_file("/small.json")
    assert backend.requests == 1  # served from the shared store
    # a different configuration means a different store
    fs_c = SharedBlockCacheFileSystem(fs=backend, skip_instance_cache=True, block_size=64 * 1024, max_memory=1 << 20)
    assert fs_c.store is not fs_a.store


def test_read_larger_than_the_cache_is_streamed(backend):
    """A range bigger than the whole budget must still be correct (and must not
    make the LRU thrash forever)."""
    reference = backend.data["/file.bin"]
    cfs = make_cache(backend, block_size=64 * 1024, max_memory=128 * 1024)
    with cfs.open("/file.bin") as f:
        assert f.read() == reference  # 4 MB through a 128 KB cache
        f.seek(1_000_000)
        assert f.read(300_000) == reference[1_000_000:1_300_000]
    assert cfs.stats()["cached_bytes"] <= 128 * 1024
    # nothing is stored for the streamed range, so every chunk is its own request
    assert cfs.stats()["requests"] >= 4 * 1024 * 1024 // (64 * 1024 * 8)


def test_max_memory_zero_disables_caching(backend):
    reference = backend.data["/file.bin"]
    cfs = SharedBlockCacheFileSystem(fs=backend, block_size=64 * 1024, max_memory=0)
    with cfs.open("/file.bin") as f:
        f.seek(500)
        assert f.read(1000) == reference[500:1500]
    assert cfs.stats()["cached_blocks"] == 0


def test_paths_reach_the_target_unchanged(backend):
    """``hf://`` style urls must be forwarded as they are given by the caller."""
    fsspec.register_implementation("slow", SlowFS, clobber=True)
    cfs = SharedBlockCacheFileSystem(fs=backend, block_size=64 * 1024, max_memory=1 << 20)
    assert cfs._strip_protocol("slow://bucket/file.bin") == "slow://bucket/file.bin"
    # only this filesystem's own prefix is removed, and nothing else
    assert cfs._strip_protocol("sharedblockcache::slow://bucket/file.bin") == "slow://bucket/file.bin"
    assert cfs._strip_protocol("sharedblockcache://slow://bucket/file.bin") == "slow://bucket/file.bin"
    assert cfs.info("slow:///small.json")["size"] == 18
    assert cfs.cat_file("slow:///small.json") == b'{"hello": "world"}'
    assert cfs.info("/small.json")["size"] == 18  # plain paths keep working too


def test_chained_url_is_the_public_entry_point(remote):
    """``fsspec.open("sharedblockcache::slow://...")`` is what scripts will write."""
    reference = remote.data["/movie.mp4"]
    options = {"block_size": 256 * 1024, "max_memory": 32 << 20}

    opened = fsspec.open("sharedblockcache::slow:///movie.mp4", "rb", **options)
    assert isinstance(opened.fs, SharedBlockCacheFileSystem)
    assert opened.fs.block_size == 256 * 1024 and opened.fs.store.max_memory == 32 << 20

    before = remote.requests
    with opened as f:
        assert isinstance(f, CachedBlockFile)
        f.seek(1_000_000)
        assert f.read(300_000) == reference[1_000_000:1_300_000]
    first = remote.requests - before
    assert 0 < first <= 8, f"{first} requests for 300 KB: not coalesced?"
    assert opened.fs.stats()["requests"] == first, "the cache did not count these reads"

    before = remote.requests
    with fsspec.open("sharedblockcache::slow:///movie.mp4", "rb", **options) as f:
        f.seek(1_000_000)
        assert f.read(300_000) == reference[1_000_000:1_300_000]
    assert remote.requests == before, "the second open went back to the network"
    assert opened.fs.stats()["hits"] >= 1


def test_every_spelling_of_one_file_shares_one_cache(remote):
    """The chained url, the inline url and the direct object are the same cache."""
    payload = remote.data["/clip.mp4"]
    options = {"block_size": 128 * 1024, "max_memory": 16 << 20}
    fs = SharedBlockCacheFileSystem(target_protocol="slow", **options)

    before = remote.requests
    assert fs.cat_file("slow:///clip.mp4") == payload  # qualified
    assert fs.cat_file("/clip.mp4") == payload  # in the target's own namespace
    assert remote.requests - before == 1, "the two spellings did not share the cache"

    # a filesystem reached through the registry uses the same store and instance
    reg = fsspec.filesystem("sharedblockcache", target_protocol="slow", **options)
    assert reg is fs and reg.store is fs.store
    with reg.open("sharedblockcache://slow:///clip.mp4") as f:
        assert f.read() == payload
    assert remote.requests - before == 1


def test_inline_url_without_a_target_is_rejected(remote):
    """Same behaviour as fsspec's own ``filecache://``: ``::`` says what to wrap."""
    with pytest.raises(ValueError, match="target_protocol"):
        fsspec.open("sharedblockcache://slow:///clip.mp4", "rb", block_size=128 * 1024)


def test_chained_url_metadata_and_listing(remote):
    fs = fsspec.filesystem("sharedblockcache", target_protocol="slow")
    assert fs.info("slow:///clip.mp4")["size"] == len(remote.data["/clip.mp4"])
    assert fs.info("slow:///clip.mp4")["name"] == "slow:///clip.mp4"
    assert set(fs.ls("slow://", detail=False)) == {"slow:///clip.mp4", "slow:///movie.mp4"}
    # names come back qualified, so they can be listed and globbed as usual
    assert set(fs.glob("slow:///*.mp4")) == {"slow:///clip.mp4", "slow:///movie.mp4"}
    assert fs.cat_file("slow:///clip.mp4", start=1, end=5) == remote.data["/clip.mp4"][1:5]


def test_target_options_travel_with_the_url(remote):
    fsspec.register_implementation("slowslow", ListingSlowFS, clobber=True)
    fs = fsspec.open("sharedblockcache::slowslow:///clip.mp4", "rb", slowslow={"latency": 0.123}).fs
    assert fs.target.latency == 0.123
