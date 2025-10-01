import os
from datasets import Dataset, DatasetDict

class WMT22Dataset:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def load(self):
        splits = ["train", "validation", "test"]
        data_dict = {}
        for split in splits:
            file_path = os.path.join(self.data_dir, f"{split}.tsv")
            if os.path.exists(file_path):
                data = []
                with open(file_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue  # skip empty lines
                        parts = line.split("\t")
                        if len(parts) != 2:
                            continue  # skip malformed lines
                        s, t = parts
                        data.append({"source": s, "target": t})
                data_dict[split] = Dataset.from_list(data)
        return DatasetDict(data_dict)
