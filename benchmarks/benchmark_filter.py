import logging
import sys
import time
import tracemalloc

from datasets import load_dataset, set_caching_enabled


if __name__ == "__main__":
    set_caching_enabled(False)
    logging.basicConfig(level=logging.DEBUG)

    tracemalloc.start()
    bc = load_dataset("bookcorpus")

    now = time.time()
    try:
        snapshot1 = tracemalloc.take_snapshot()
        bc["train"].filter(lambda x: len(x["text"]) < 64, num_proc=int(sys.argv[1]))
    except Exception as e:
        print(f"cancelled: {e}")
        exit(1)
    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()
    elapsed = time.time() - now

    print(elapsed)
    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)
