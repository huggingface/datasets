"""Compare indexed batch reads against the original row-slice implementation.

Run with: python benchmarks/benchmark_fast_gather.py --output /tmp/fast-gather.json
The fixtures are generated locally; no dataset downloads are needed.
"""

import argparse
import json
import platform
import statistics
import tempfile
import timeit
from pathlib import Path

import numpy as np
import pyarrow as pa

from datasets import Dataset
from datasets.table import InMemoryTable, MemoryMappedTable


def original_fast_gather(self, indices):
    """Row-slice implementation from datasets main at 9e7496a4."""
    if not len(indices):
        raise ValueError("Indices must be non-empty")
    batch_indices = np.searchsorted(self._offsets, indices, side="right") - 1
    return pa.Table.from_batches(
        [self._batches[batch].slice(i - self._offsets[batch], 1) for batch, i in zip(batch_indices, indices)],
        schema=self._schema,
    )


def measure_pair(before, after, repeats, iterations):
    """Alternate the measurement order and report median time per call."""
    timings = {"before": [], "after": []}
    before()
    after()
    for repeat in range(repeats):
        cases = [("before", before), ("after", after)]
        if repeat % 2:
            cases.reverse()
        for name, function in cases:
            timings[name].append(timeit.timeit(function, number=iterations) / iterations)
    return {name: statistics.median(values) * 1000 for name, values in timings.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rng = np.random.default_rng(0)
    raw = pa.table(
        {
            "id": np.arange(args.rows),
            "text": ["training example " * 12] * args.rows,
            "tokens": [[1, 2, 3, 4]] * args.rows,
        }
    )
    results = []
    with tempfile.TemporaryDirectory() as temporary:
        for chunks in (1, 100, 1000):
            chunked = pa.Table.from_batches(raw.to_batches(max_chunksize=max(args.rows // chunks, 1)))
            filename = Path(temporary) / "data.arrow"
            with pa.OSFile(str(filename), "wb") as stream, pa.ipc.new_stream(stream, chunked.schema) as writer:
                writer.write_table(chunked)
            tables = {"in_memory": InMemoryTable(chunked), "memory_mapped": MemoryMappedTable.from_file(str(filename))}
            for storage, table in tables.items():
                for batch_size in (32, 1000, 10_000):
                    indices = rng.integers(0, args.rows, size=batch_size)
                    original = original_fast_gather(table, indices)
                    optimized = table.fast_gather(indices)
                    assert optimized.equals(original)
                    for formatting in ("arrow", "python"):

                        def read_before():
                            result = original_fast_gather(table, indices)
                            return result.to_pydict() if formatting == "python" else result

                        def read_after():
                            result = table.fast_gather(indices)
                            return result.to_pydict() if formatting == "python" else result

                        times = measure_pair(read_before, read_after, args.repeats, args.iterations)
                        results.append(
                            {
                                "storage": storage,
                                "chunks": chunks,
                                "batch_size": batch_size,
                                "format": formatting,
                                **times,
                                "speedup": times["before"] / times["after"],
                            }
                        )

        dataset = Dataset.from_dict(raw.to_pydict()).shuffle(seed=0)
        original_dataset = Dataset(InMemoryTable(dataset.data.table), indices_table=dataset._indices)
        original_dataset.data.fast_gather = lambda indices: original_fast_gather(original_dataset.data, indices)
        assert original_dataset[:1000] == dataset[:1000]
        times = measure_pair(lambda: original_dataset[:1000], lambda: dataset[:1000], args.repeats, args.iterations)
        results.append(
            {"storage": "public_dataset_api", "batch_size": 1000, **times, "speedup": times["before"] / times["after"]}
        )

        large_rows = min(args.rows, 4096)
        large = InMemoryTable(pa.table({"id": np.arange(large_rows), "payload": [b"x" * 65_536] * large_rows}))
        indices = rng.integers(0, large_rows, size=1000)
        assert large.fast_gather(indices).equals(original_fast_gather(large, indices))
        for formatting in ("arrow", "python"):

            def read_large_before():
                result = original_fast_gather(large, indices)
                return result.to_pydict() if formatting == "python" else result

            def read_large_after():
                result = large.fast_gather(indices)
                return result.to_pydict() if formatting == "python" else result

            times = measure_pair(read_large_before, read_large_after, args.repeats, args.iterations)
            results.append(
                {
                    "storage": "large_payload",
                    "payload_bytes": 65_536,
                    "batch_size": 1000,
                    "format": formatting,
                    **times,
                    "speedup": times["before"] / times["after"],
                }
            )

    report = {
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "pyarrow": pa.__version__,
            "numpy": np.__version__,
        },
        "parameters": {
            "rows": args.rows,
            "repeats": args.repeats,
            "iterations": args.iterations,
            "cyclic_gc_during_timing": False,
        },
        "results": results,
    }
    serialized = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    else:
        print(serialized)


if __name__ == "__main__":
    main()
