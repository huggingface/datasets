---
paperswithcode_id: wikihow
pretty_name: WikiHow
dataset_info:
- config_name: all
  features:
  - name: text
    dtype: string
  - name: headline
    dtype: string
  - name: title
    dtype: string
  splits:
  - name: test
    num_bytes: 18276023
    num_examples: 5577
  - name: train
    num_bytes: 513238309
    num_examples: 157252
  - name: validation
    num_bytes: 18246897
    num_examples: 5599
  download_size: 5460385
  dataset_size: 549761229
- config_name: sep
  features:
  - name: text
    dtype: string
  - name: headline
    dtype: string
  - name: title
    dtype: string
  - name: overview
    dtype: string
  - name: sectionLabel
    dtype: string
  splits:
  - name: test
    num_bytes: 35271826
    num_examples: 37800
  - name: train
    num_bytes: 990499776
    num_examples: 1060732
  - name: validation
    num_bytes: 35173966
    num_examples: 37932
  download_size: 5460385
  dataset_size: 1060945568
---

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.