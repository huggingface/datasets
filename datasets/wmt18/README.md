---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- cs
- de
- en
- et
- fi
- kk
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
- extended|opus_paracrawl
- extended|setimes
- extended|un_multi
task_categories:
- translation
task_ids: []
pretty_name: WMT18
paperswithcode_id: wmt-2018
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
    num_bytes: 696229
    num_examples: 2983
  - name: train
    num_bytes: 1461016186
    num_examples: 11046024
  - name: validation
    num_bytes: 674430
    num_examples: 3005
  download_size: 2030359086
  dataset_size: 1462386845
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
    num_bytes: 757649
    num_examples: 2998
  - name: train
    num_bytes: 8187552108
    num_examples: 42271874
  - name: validation
    num_bytes: 729519
    num_examples: 3004
  download_size: 3808612335
  dataset_size: 8189039276
- config_name: et-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - et
        - en
  splits:
  - name: test
    num_bytes: 489394
    num_examples: 2000
  - name: train
    num_bytes: 647992667
    num_examples: 2175873
  - name: validation
    num_bytes: 459398
    num_examples: 2000
  download_size: 524534404
  dataset_size: 648941459
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
    num_bytes: 691841
    num_examples: 3000
  - name: train
    num_bytes: 857171881
    num_examples: 3280600
  - name: validation
    num_bytes: 1388828
    num_examples: 6004
  download_size: 491874780
  dataset_size: 859252550
- config_name: kk-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - kk
        - en
  splits:
  - name: test
  - name: train
  - name: validation
  download_size: 0
  dataset_size: 0
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
    num_bytes: 1085596
    num_examples: 3000
  - name: train
    num_bytes: 13665367647
    num_examples: 36858512
  - name: validation
    num_bytes: 1040195
    num_examples: 3001
  download_size: 4195144356
  dataset_size: 13667493438
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
    num_bytes: 770313
    num_examples: 3000
  - name: train
    num_bytes: 60416617
    num_examples: 205756
  - name: validation
    num_bytes: 752773
    num_examples: 3007
  download_size: 62263061
  dataset_size: 61939703
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
    num_bytes: 1107522
    num_examples: 3981
  - name: train
    num_bytes: 5536169801
    num_examples: 25160346
  - name: validation
    num_bytes: 540347
    num_examples: 2001
  download_size: 2259428767
  dataset_size: 5537817670
---

# Dataset Card for "wmt18"

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

- **Homepage:** [http://www.statmt.org/wmt18/translation-task.html](http://www.statmt.org/wmt18/translation-task.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1935.34 MB
- **Size of the generated dataset:** 1394.65 MB
- **Total amount of disk used:** 3329.99 MB

### Dataset Summary

Translation dataset based on the data from statmt.org.

Versions exist for different years using a combination of data
sources. The base `wmt` allows you to create a custom dataset by choosing
your own data/language pair. This can be done as follows:

```python
from datasets import inspect_dataset, load_dataset_builder

inspect_dataset("wmt18", "path/to/scripts")
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

- **Size of downloaded dataset files:** 1935.34 MB
- **Size of the generated dataset:** 1394.65 MB
- **Total amount of disk used:** 3329.99 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### cs-en
- `translation`: a multilingual `string` variable, with possible languages including `cs`, `en`.

### Data Splits

|name | train  |validation|test|
|-----|-------:|---------:|---:|
|cs-en|11046024|      3005|2983|

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
@InProceedings{bojar-EtAl:2018:WMT1,
  author    = {Bojar, Ond{r}ej  and  Federmann, Christian  and  Fishel, Mark
    and Graham, Yvette  and  Haddow, Barry  and  Huck, Matthias  and
    Koehn, Philipp  and  Monz, Christof},
  title     = {Findings of the 2018 Conference on Machine Translation (WMT18)},
  booktitle = {Proceedings of the Third Conference on Machine Translation,
    Volume 2: Shared Task Papers},
  month     = {October},
  year      = {2018},
  address   = {Belgium, Brussels},
  publisher = {Association for Computational Linguistics},
  pages     = {272--307},
  url       = {http://www.aclweb.org/anthology/W18-6401}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.