---
pretty_name: WMT16
paperswithcode_id: wmt-2016
multilinguality:
- translation
task_categories:
- translation
task_ids: []
---

# Dataset Card for "wmt16"

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

- **Homepage:** [http://www.statmt.org/wmt16/translation-task.html](http://www.statmt.org/wmt16/translation-task.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1611.50 MB
- **Size of the generated dataset:** 283.51 MB
- **Total amount of disk used:** 1895.01 MB

### Dataset Summary

Translate dataset based on the data from statmt.org.

Versions exists for the different years using a combination of multiple data
sources. The base `wmt_translate` allows you to create your own config to choose
your own data/language pair by creating a custom `datasets.translate.wmt.WmtConfig`.

```
config = datasets.wmt.WmtConfig(
    version="0.0.1",
    language_pair=("fr", "de"),
    subsets={
        datasets.Split.TRAIN: ["commoncrawl_frde"],
        datasets.Split.VALIDATION: ["euelections_dev2019"],
    },
)
builder = datasets.builder("wmt_translate", config=config)
```

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### cs-en

- **Size of downloaded dataset files:** 1611.50 MB
- **Size of the generated dataset:** 283.51 MB
- **Total amount of disk used:** 1895.01 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### cs-en
- `translation`: a multilingual `string` variable, with possible languages including `cs`, `en`.

### Data Splits

|name |train |validation|test|
|-----|-----:|---------:|---:|
|cs-en|997240|      2656|2999|

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

@InProceedings{bojar-EtAl:2016:WMT1,
  author    = {Bojar, Ond{r}ej  and  Chatterjee, Rajen  and  Federmann, Christian  and  Graham, Yvette  and  Haddow, Barry  and  Huck, Matthias  and  Jimeno Yepes, Antonio  and  Koehn, Philipp  and  Logacheva, Varvara  and  Monz, Christof  and  Negri, Matteo  and  Neveol, Aurelie  and  Neves, Mariana  and  Popel, Martin  and  Post, Matt  and  Rubino, Raphael  and  Scarton, Carolina  and  Specia, Lucia  and  Turchi, Marco  and  Verspoor, Karin  and  Zampieri, Marcos},
  title     = {Findings of the 2016 Conference on Machine Translation},
  booktitle = {Proceedings of the First Conference on Machine Translation},
  month     = {August},
  year      = {2016},
  address   = {Berlin, Germany},
  publisher = {Association for Computational Linguistics},
  pages     = {131--198},
  url       = {http://www.aclweb.org/anthology/W/W16/W16-2301}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.