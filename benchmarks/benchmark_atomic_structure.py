"""Benchmark supplied public structure files; no downloads or mutations of source files.

Example:
    python benchmarks/benchmark_atomic_structure.py --files /data/*.cif.gz --output result.json

Each single-file case runs in a fresh interpreter. Worker-pool measurements use
spawn (including cold imports), one and two workers, and repeat the supplied files.
Peak RSS is a process high-water mark, not incremental memory or simultaneous total.
"""

import argparse
import hashlib
import json
import multiprocessing
import os
import platform
import resource
import statistics
import subprocess
import sys
import time
from pathlib import Path


def rss_mib():
    scale = 1024**2 if sys.platform == "darwin" else 1024
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / scale


def timed(function, repeats):
    values = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = function()
        values.append(time.perf_counter() - start)
    return result, {"median_seconds": statistics.median(values), "runs_seconds": values}


def case(path, repeats):
    start = time.perf_counter()
    from datasets import AtomicStructure
    from datasets.features.atomic_structure import _preparation_runtime

    feature = AtomicStructure()
    record = {"path": path, "bytes": None}
    atoms = feature.decode_example(record)
    first_seconds = time.perf_counter() - start
    n_atoms = atoms.array_length() if hasattr(atoms, "array_length") else [a.array_length() for a in atoms]
    del atoms
    _, minimal = timed(lambda: feature.decode_example(record), repeats)
    del _
    prepare = AtomicStructure(parse_config={"remove_waters": True, "altloc": "first"})
    result = {
        "path": path,
        "source_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "source_bytes": Path(path).stat().st_size,
        "feature_source_sha256": hashlib.sha256(
            Path(sys.modules[AtomicStructure.__module__].__file__).read_bytes()
        ).hexdigest(),
        "atoms": n_atoms,
        "first_decode_including_import_seconds": first_seconds,
        "minimal_decode": minimal,
        "runtime": _preparation_runtime(),
    }
    try:
        prepared, preparation = timed(lambda: prepare.decode_example(record), repeats)
        encoded, materialization = timed(lambda: feature.materialize(prepared), 1)
        del prepared
        _, materialized_read = timed(lambda: feature.decode_example(encoded), repeats)
        del _
        saving = preparation["median_seconds"] - materialized_read["median_seconds"]
        result.update(
            preparation=preparation,
            materialization=materialization,
            materialized_bytes=len(encoded["bytes"]),
            materialized_decode=materialized_read,
            approximate_reads_to_amortize=(
                (preparation["median_seconds"] + materialization["median_seconds"]) / saving if saving > 0 else None
            ),
        )
    except Exception as error:
        result["preparation_or_materialization_error"] = f"{type(error).__name__}: {error}"
    result["peak_rss_mib"] = rss_mib()
    return result


def decode_task(path):
    start = time.perf_counter()
    from datasets import AtomicStructure

    atoms = AtomicStructure().decode_example({"path": path, "bytes": None})
    count = atoms.array_length() if hasattr(atoms, "array_length") else sum(a.array_length() for a in atoms)
    return {"pid": os.getpid(), "atoms": count, "seconds": time.perf_counter() - start, "peak_rss_mib": rss_mib()}


def pool_case(paths, workers, repeats):
    start = time.perf_counter()
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        iterator = pool.imap_unordered(decode_task, paths * repeats)
        first = next(iterator)
        first_seconds = time.perf_counter() - start
        results = [first, *iterator]
    peaks = {}
    for row in results:
        peaks[str(row["pid"])] = max(peaks.get(str(row["pid"]), 0), row["peak_rss_mib"])
    return {
        "workers": workers,
        "rows": len(results),
        "wall_seconds": time.perf_counter() - start,
        "first_result_seconds": first_seconds,
        "worker_peak_rss_mib": peaks,
        "tasks": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--single", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    paths = [str(Path(p).resolve()) for p in args.files]
    if args.single:
        print(json.dumps(case(paths[0], args.repeats)))
        return
    report = {
        "platform": platform.platform(),
        "python": sys.version,
        "cases": [],
        "pools": [],
        "policy": {"remove_waters": True, "altloc": "first"},
    }
    for path in paths:
        print(f"Benchmarking {Path(path).name}", file=sys.stderr, flush=True)
        result = subprocess.run(
            [sys.executable, __file__, "--single", "--files", path, "--repeats", str(args.repeats)],
            capture_output=True,
            text=True,
            timeout=300,
            check=True,
        )
        report["cases"].append(json.loads(result.stdout))
        if args.output:
            args.output.write_text(json.dumps(report, indent=2) + "\n")
    for workers in (1, 2):
        print(f"Benchmarking {workers} spawn workers", file=sys.stderr, flush=True)
        report["pools"].append(pool_case(paths, workers, args.repeats))
        if args.output:
            args.output.write_text(json.dumps(report, indent=2) + "\n")
    if not args.output:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
