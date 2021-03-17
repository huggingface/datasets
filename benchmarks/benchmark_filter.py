import logging
import sys
import time

from datasets import load_dataset, set_caching_enabled


if __name__ == "__main__":
    set_caching_enabled(False)
    logging.basicConfig(level=logging.DEBUG)

    bc = load_dataset("bookcorpus")

    now = time.time()
    try:
        bc["train"].filter(lambda x: len(x["text"]) < 64, num_proc=int(sys.argv[1]))
    except Exception as e:
        print(f"cancelled: {e}")
    elapsed = time.time() - now

    print(elapsed)
