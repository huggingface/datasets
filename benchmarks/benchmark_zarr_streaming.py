"""
Benchmark Zarr loading via 🤗 Datasets.

This benchmark creates a small local Zarr store and compares:
- streaming=True  (iterates directly from the Zarr store)
- streaming=False (builds an Arrow dataset first, then iterates)

Note: This is a best-effort benchmark intended for development/profiling.
"""

from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path

import numpy as np

from datasets import load_dataset


def make_zarr_store(root: Path, n_rows: int, n_cols: int) -> Path:
    import zarr

    store_dir = root / "bench.zarr"
    g = zarr.open_group(store=str(store_dir), mode="w")
    g.create_array("x", data=np.arange(n_rows, dtype=np.int32), chunks=(min(8192, n_rows),))
    g.create_array("y", data=np.random.randn(n_rows, n_cols).astype(np.float32), chunks=(min(1024, n_rows), n_cols))
    return store_dir / "zarr.json"


def bench(streaming: bool, zarr_json: str, n_take: int) -> float:
    ds = load_dataset("zarr", data_files=[zarr_json], split="train", streaming=streaming)
    t0 = time.perf_counter()
    it = iter(ds)
    for _ in range(n_take):
        next(it)
    t1 = time.perf_counter()
    return t1 - t0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=200_000)
    parser.add_argument("--cols", type=int, default=64)
    parser.add_argument("--take", type=int, default=10_000)
    args = parser.parse_args()

    try:
        import zarr  # noqa: F401
    except Exception as e:
        raise SystemExit("This benchmark requires `zarr` (pip install zarr).") from e

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        zarr_json = make_zarr_store(tmp, n_rows=args.rows, n_cols=args.cols)

        t_stream = bench(streaming=True, zarr_json=str(zarr_json), n_take=args.take)
        t_nonstream = bench(streaming=False, zarr_json=str(zarr_json), n_take=args.take)

        print(f"rows={args.rows} cols={args.cols} take={args.take}")
        print(f\"streaming=True   : {t_stream:.3f}s  ({args.take / max(t_stream, 1e-9):.1f} ex/s)\")
        print(f\"streaming=False  : {t_nonstream:.3f}s ({args.take / max(t_nonstream, 1e-9):.1f} ex/s)\")


if __name__ == "__main__":
    main()

"""
Benchmark Zarr loading via 🤗 Datasets.

This benchmark creates a small local Zarr store and compares:
- streaming=True  (iterates directly from the Zarr store)
- streaming=False (builds an Arrow dataset first, then iterates)

Note: This is a best-effort benchmark intended for development/profiling.
"""

from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path

import numpy as np

from datasets import load_dataset


def make_zarr_store(root: Path, n_rows: int, n_cols: int) -> Path:
    import zarr

    store_dir = root / "bench.zarr"
    g = zarr.open_group(store=str(store_dir), mode="w")
    g.create_array("x", data=np.arange(n_rows, dtype=np.int32), chunks=(min(8192, n_rows),))
    g.create_array("y", data=np.random.randn(n_rows, n_cols).astype(np.float32), chunks=(min(1024, n_rows), n_cols))
    return store_dir / "zarr.json"


def bench(streaming: bool, zarr_json: str, n_take: int) -> float:
    ds = load_dataset("zarr", data_files=[zarr_json], split="train", streaming=streaming)
    t0 = time.perf_counter()
    it = iter(ds)
    for _ in range(n_take):
        next(it)
    t1 = time.perf_counter()
    return t1 - t0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=200_000)
    parser.add_argument("--cols", type=int, default=64)
    parser.add_argument("--take", type=int, default=10_000)
    args = parser.parse_args()

    try:
        import zarr  # noqa: F401
    except Exception as e:
        raise SystemExit("This benchmark requires `zarr` (pip install zarr).") from e

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        zarr_json = make_zarr_store(tmp, n_rows=args.rows, n_cols=args.cols)

        t_stream = bench(streaming=True, zarr_json=str(zarr_json), n_take=args.take)
        t_nonstream = bench(streaming=False, zarr_json=str(zarr_json), n_take=args.take)

        print(f"rows={args.rows} cols={args.cols} take={args.take}")
        print(f"streaming=True   : {t_stream:.3f}s  ({args.take / max(t_stream, 1e-9):.1f} ex/s)")
        print(f"streaming=False  : {t_nonstream:.3f}s ({args.take / max(t_nonstream, 1e-9):.1f} ex/s)")


if __name__ == "__main__":
    main()

"""
Benchmark Zarr loading via 🤗 Datasets.

This benchmark creates a small local Zarr store and compares:
- streaming=True  (iterates directly from the Zarr store)
- streaming=False (builds an Arrow dataset first, then iterates)

Note: This is a best-effort benchmark intended for development/profiling.
"""

from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path

import numpy as np

from datasets import load_dataset


def make_zarr_store(root: Path, n_rows: int, n_cols: int) -> Path:
    import zarr

    store_dir = root / "bench.zarr"
    g = zarr.open_group(store=str(store_dir), mode="w")
    g.create_array("x", data=np.arange(n_rows, dtype=np.int32), chunks=(min(8192, n_rows),))
    g.create_array("y", data=np.random.randn(n_rows, n_cols).astype(np.float32), chunks=(min(1024, n_rows), n_cols))
    return store_dir / "zarr.json"


def bench(streaming: bool, zarr_json: str, n_take: int) -> float:
    ds = load_dataset("zarr", data_files=[zarr_json], split="train", streaming=streaming)
    t0 = time.perf_counter()
    it = iter(ds)
    for _ in range(n_take):
        next(it)
    t1 = time.perf_counter()
    return t1 - t0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=200_000)
    parser.add_argument("--cols", type=int, default=64)
    parser.add_argument("--take", type=int, default=10_000)
    args = parser.parse_args()

    try:
        import zarr  # noqa: F401
    except Exception as e:
        raise SystemExit("This benchmark requires `zarr` (pip install zarr).") from e

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        zarr_json = make_zarr_store(tmp, n_rows=args.rows, n_cols=args.cols)

        t_stream = bench(streaming=True, zarr_json=str(zarr_json), n_take=args.take)
        t_nonstream = bench(streaming=False, zarr_json=str(zarr_json), n_take=args.take)

        print(f"rows={args.rows} cols={args.cols} take={args.take}")
        print(f"streaming=True   : {t_stream:.3f}s  ({args.take / max(t_stream, 1e-9):.1f} ex/s)")
        print(f"streaming=False  : {t_nonstream:.3f}s ({args.take / max(t_nonstream, 1e-9):.1f} ex/s)")


if __name__ == "__main__":
    main()

