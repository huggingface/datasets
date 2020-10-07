# Let's import the library. We typically only need at most four methods:
from datasets import list_datasets, list_metrics, load_dataset, load_metric, Dataset, concatenate_datasets

from pprint import pprint

datasets = [Dataset.from_dict({"foo": [i for i in range(100)]}) for _ in range(2)] 
ds2 = concatenate_datasets(datasets)
ds3 = ds2.train_test_split(0.1)
