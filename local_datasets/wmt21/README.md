# WMT21 Local Dataset

This is a local copy of WMT21 for testing / development.

## Structure

- train.tsv
- validation.tsv
- test.tsv

Each line is tab-separated: `<source>\t<target>`

## Usage

```python
from local_datasets.wmt21.wmt21 import WMT21Dataset

wmt21 = WMT21Dataset("local_datasets/wmt21/dummy_data")
ds = wmt21.load()
print(ds["train"][0])
