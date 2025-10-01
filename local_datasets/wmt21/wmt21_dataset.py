# local_datasets/wmt21/wmt21_dataset.py
import os
from datasets import Dataset, DatasetDict


class WMT21Dataset:
    def __init__(self, data_dir: str):
        """
        Args:
            data_dir (str): Path to the directory containing train.tsv, validation.tsv, test.tsv
        """
        self.data_dir = data_dir

    def load(self) -> DatasetDict:
        """
        Load the dataset into a Hugging Face DatasetDict with 'train', 'validation', 'test' splits.
        Handles empty lines and malformed lines gracefully.
        """
        splits = ["train", "validation", "test"]
        data_dict = {}

        for split in splits:
            file_path = os.path.join(self.data_dir, f"{split}.tsv")
            if os.path.exists(file_path):
                with open(file_path, encoding="utf-8") as f:
                    data = []
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue  # skip empty lines
                        parts = line.split("\t")
                        if len(parts) < 2:
                            continue  # skip malformed lines
                        # Take only first two columns
                        source, target = parts[0], parts[1]
                        data.append({"source": source, "target": target})
                data_dict[split] = Dataset.from_list(data)
            else:
                # If split file does not exist, create empty Dataset
                data_dict[split] = Dataset.from_list([])

        return DatasetDict(data_dict)
