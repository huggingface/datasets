from datasets import load_dataset

def load_your_dataset(data_dir, split):
    return load_dataset(data_dir, split=split)
