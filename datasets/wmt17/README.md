---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- cs
- de
- en
- fi
- lv
- ru
- tr
- zh
license:
- unknown
multilinguality:
- translation
size_categories:
- 10M<n<100M
source_datasets:
- extended|europarl_bilingual
- extended|news_commentary
- extended|setimes
- extended|un_multi
task_categories:
- translation
task_ids: []
pretty_name: WMT17
paperswithcode_id: null
dataset_info:
- config_name: cs-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - en
  splits:
  - name: test
    num_bytes: 674430
    num_examples: 3005
  - name: train
    num_bytes: 300698431
    num_examples: 1018291
  - name: validation
    num_bytes: 707870
    num_examples: 2999
  download_size: 1784240523
  dataset_size: 302080731
- config_name: de-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - en
  splits:
  - name: test
    num_bytes: 729519
    num_examples: 3004
  - name: train
    num_bytes: 1715537443
    num_examples: 5906184
  - name: validation
    num_bytes: 735516
    num_examples: 2999
  download_size: 1945382236
  dataset_size: 1717002478
- config_name: fi-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fi
        - en
  splits:
  - name: test
    num_bytes: 1388828
    num_examples: 6004
  - name: train
    num_bytes: 743856525
    num_examples: 2656542
  - name: validation
    num_bytes: 1410515
    num_examples: 6000
  download_size: 434531933
  dataset_size: 746655868
- config_name: lv-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - lv
        - en
  splits:
  - name: test
    num_bytes: 530474
    num_examples: 2001
  - name: train
    num_bytes: 517419100
    num_examples: 3567528
  - name: validation
    num_bytes: 544604
    num_examples: 2003
  download_size: 169634544
  dataset_size: 518494178
- config_name: ru-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - en
  splits:
  - name: test
    num_bytes: 1040195
    num_examples: 3001
  - name: train
    num_bytes: 11000075522
    num_examples: 24782720
  - name: validation
    num_bytes: 1050677
    num_examples: 2998
  download_size: 3582640660
  dataset_size: 11002166394
- config_name: tr-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - tr
        - en
  splits:
  - name: test
    num_bytes: 752773
    num_examples: 3007
  - name: train
    num_bytes: 60416617
    num_examples: 205756
  - name: validation
    num_bytes: 732436
    num_examples: 3000
  download_size: 62263061
  dataset_size: 61901826
- config_name: zh-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - zh
        - en
  splits:
  - name: test
    num_bytes: 540347
    num_examples: 2001
  - name: train
    num_bytes: 5529286149
    num_examples: 25134743
  - name: validation
    num_bytes: 589591
    num_examples: 2002
  download_size: 2314906945
  dataset_size: 5530416087
---

# Dataset Card for "wmt17"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [http://www.statmt.org/wmt17/translation-task.html](http://www.statmt.org/wmt17/translation-task.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1700.58 MB
- **Size of the generated dataset:** 288.10 MB
- **Total amount of disk used:** 1988.68 MB

### Dataset Summary

Translation dataset based on the data from statmt.org.

Versions exist for different years using a combination of data
sources. The base `wmt` allows you to create a custom dataset by choosing
your own data/language pair. This can be done as follows:

```python
from datasets import inspect_dataset, load_dataset_builder

inspect_dataset("wmt17", "path/to/scripts")
builder = load_dataset_builder(
    "path/to/scripts/wmt_utils.py",
    language_pair=("fr", "de"),
    subsets={
        datasets.Split.TRAIN: ["commoncrawl_frde"],
        datasets.Split.VALIDATION: ["euelections_dev2019"],
    },
)

# Standard version
builder.download_and_prepare()
ds = builder.as_dataset()

# Streamable version
ds = builder.as_streaming_dataset()
```

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### cs-en

- **Size of downloaded dataset files:** 1700.58 MB
- **Size of the generated dataset:** 288.10 MB
- **Total amount of disk used:** 1988.68 MB

An example of 'train' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### cs-en
- `translation`: a multilingual `string` variable, with possible languages including `cs`, `en`.

### Data Splits

|name | train |validation|test|
|-----|------:|---------:|---:|
|cs-en|1018291|      2999|3005|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```

@InProceedings{bojar-EtAl:2017:WMT1,
  author    = {Bojar, Ond{r}ej  and  Chatterjee, Rajen  and  Federmann, Christian  and  Graham, Yvette  and  Haddow, Barry  and  Huang, Shujian  and  Huck, Matthias  and  Koehn, Philipp  and  Liu, Qun  and  Logacheva, Varvara  and  Monz, Christof  and  Negri, Matteo  and  Post, Matt  and  Rubino, Raphael  and  Specia, Lucia  and  Turchi, Marco},
  title     = {Findings of the 2017 Conference on Machine Translation (WMT17)},
  booktitle = {Proceedings of the Second Conference on Machine Translation, Volume 2: Shared Task Papers},
  month     = {September},
  year      = {2017},
  address   = {Copenhagen, Denmark},
  publisher = {Association for Computational Linguistics},
  pages     = {169--214},
  url       = {http://www.aclweb.org/anthology/W17-4717}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.