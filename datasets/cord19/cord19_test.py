import csv

from datasets import load_dataset


def main():
    print("Loading cord19 metadata...")
    dataset = load_dataset("../cord19", "metadata")
    print("Loading cord19 metadata + fulltext...")
    dataset = load_dataset("../cord19", "fulltext")
    print("Loading cord19 metadata + embeddings...")
    dataset = load_dataset("../cord19", "embeddings")

    sample = dataset["train"][0]
    print(sample)


if __name__ == "__main__":
    # execute only if run as a script
    main()
