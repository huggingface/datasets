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
- fr
- gu
- kk
- lt
- ru
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
- extended|un_multi
task_categories:
- translation
task_ids: []
pretty_name: WMT19
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
  - name: train
    num_bytes: 1314871994
    num_examples: 7270695
  - name: validation
    num_bytes: 696229
    num_examples: 2983
  download_size: 2018537046
  dataset_size: 1315568223
- config_name: de-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - en
  splits:
  - name: train
    num_bytes: 8420967590
    num_examples: 38690334
  - name: validation
    num_bytes: 757649
    num_examples: 2998
  download_size: 10422475109
  dataset_size: 8421725239
- config_name: fi-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fi
        - en
  splits:
  - name: train
    num_bytes: 1422922267
    num_examples: 6587448
  - name: validation
    num_bytes: 691841
    num_examples: 3000
  download_size: 1006124909
  dataset_size: 1423614108
- config_name: gu-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - en
  splits:
  - name: train
    num_bytes: 590763
    num_examples: 11670
  - name: validation
    num_bytes: 774621
    num_examples: 1998
  download_size: 38891457
  dataset_size: 1365384
- config_name: kk-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - kk
        - en
  splits:
  - name: train
    num_bytes: 9157438
    num_examples: 126583
  - name: validation
    num_bytes: 846857
    num_examples: 2066
  download_size: 41558315
  dataset_size: 10004295
- config_name: lt-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - lt
        - en
  splits:
  - name: train
    num_bytes: 513084361
    num_examples: 2344893
  - name: validation
    num_bytes: 541953
    num_examples: 2000
  download_size: 411309952
  dataset_size: 513626314
- config_name: ru-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - en
  splits:
  - name: train
    num_bytes: 13721377178
    num_examples: 37492126
  - name: validation
    num_bytes: 1085596
    num_examples: 3000
  download_size: 4134147853
  dataset_size: 13722462774
- config_name: zh-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - zh
        - en
  splits:
  - name: train
    num_bytes: 5584359748
    num_examples: 25984574
  - name: validation
    num_bytes: 1107522
    num_examples: 3981
  download_size: 2195879129
  dataset_size: 5585467270
- config_name: fr-de
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - de
  splits:
  - name: train
    num_bytes: 2358413485
    num_examples: 9824476
  - name: validation
    num_bytes: 441426
    num_examples: 1512
  download_size: 757345846
  dataset_size: 2358854911
---

# Dataset Card for "wmt19"

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

- **Homepage:** [http://www.statmt.org/wmt19/translation-task.html](http://www.statmt.org/wmt19/translation-task.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1924.57 MB
- **Size of the generated dataset:** 1254.62 MB
- **Total amount of disk used:** 3179.19 MB

### Dataset Summary

Translation dataset based on the data from statmt.org.

Versions exist for different years using a combination of data
sources. The base `wmt` allows you to create a custom dataset by choosing
your own data/language pair. This can be done as follows:

```python
from datasets import inspect_dataset, load_dataset_builder

inspect_dataset("wmt19", "path/to/scripts")
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

- **Size of downloaded dataset files:** 1924.57 MB
- **Size of the generated dataset:** 1254.62 MB
- **Total amount of disk used:** 3179.19 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### cs-en
- `translation`: a multilingual `string` variable, with possible languages including `cs`, `en`.

### Data Splits

|name | train |validation|
|-----|------:|---------:|
|cs-en|7270695|      2983|

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

@ONLINE {wmt19translate,
    author = "Wikimedia Foundation",
    title  = "ACL 2019 Fourth Conference on Machine Translation (WMT19), Shared Task: Machine Translation of News",
    url    = "http://www.statmt.org/wmt19/translation-task.html"
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf) for adding this dataset.