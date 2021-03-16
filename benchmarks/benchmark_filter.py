import time

from datasets import load_dataset


if __name__ == "__main__":
    bc = load_dataset("bookcorpus")
    now = time.time()
    bc.filter(lambda x: len(x["text"]) < 64)
    elapsed = time.time() - now
    print(elapsed)
