"""Benchmark JSON export with and without an indices mapping, using local data."""

import argparse
import hashlib
import io
import json
import statistics
import time

import numpy as np
import pyarrow as pa

from datasets import Dataset, disable_progress_bars


def benchmark_json(num_rows=50_000, repeats=5):
    disable_progress_bars()
    table = pa.table(
        {
            "id": [f"example-{i}" for i in range(num_rows)],
            "text": [f"context {i} " + "text with unicode 中 " * 8 for i in range(num_rows)],
            "nullable": [None if i % 7 == 0 else 2**54 + i for i in range(num_rows)],
            "answers": [{"text": [str(i)], "answer_start": [i % 100]} for i in range(num_rows)],
        }
    )
    for chunk_size in [num_rows, 1_000]:
        dataset = Dataset(pa.Table.from_batches(table.to_batches(max_chunksize=chunk_size)))
        for name, indices in [
            ("unselected", None),
            ("reversed", range(num_rows - 1, -1, -1)),
            ("shuffled", np.random.default_rng(42).permutation(num_rows)),
            ("duplicates", [i % num_rows for i in range(num_rows * 2 - 1, -1, -2)]),
        ]:
            selected = dataset if indices is None else dataset.select(indices)
            times = []
            for _ in range(repeats):
                with io.BytesIO() as output:
                    start = time.perf_counter()
                    selected.to_json(output, batch_size=10_000, force_ascii=False)
                    times.append(time.perf_counter() - start)
                    digest = hashlib.sha256(output.getbuffer()).hexdigest()
            print(
                json.dumps(
                    {
                        "chunk_size": chunk_size,
                        "selection": name,
                        "rows": num_rows,
                        "repeats": repeats,
                        "seconds_median": statistics.median(times),
                        "sha256": digest,
                    }
                ),
                flush=True,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--num-rows", type=int, default=50_000)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    benchmark_json(args.num_rows, args.repeats)
