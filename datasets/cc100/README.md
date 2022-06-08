---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- af
- am
- ar
- as
- az
- be
- bg
- bn
- bn-Latn
- br
- bs
- ca
- cs
- cy
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- ff
- fi
- fr
- fy
- ga
- gd
- gl
- gn
- gu
- ha
- he
- hi
- hi-Latn
- hr
- ht
- hu
- hy
- id
- ig
- is
- it
- ja
- jv
- ka
- kk
- km
- kn
- ko
- ku
- ky
- la
- lg
- li
- ln
- lo
- lt
- lv
- mg
- mk
- ml
- mn
- mr
- ms
- my
- my-x-zawgyi
- ne
- nl
- 'no'
- ns
- om
- or
- pa
- pl
- ps
- pt
- qu
- rm
- ro
- ru
- sa
- si
- sc
- sd
- sk
- sl
- so
- sq
- sr
- ss
- su
- sv
- sw
- ta
- ta-Latn
- te
- te-Latn
- th
- tl
- tn
- tr
- ug
- uk
- ur
- ur-Latn
- uz
- vi
- wo
- xh
- yi
- yo
- zh-Hans
- zh-Hant
- zu
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- 10M<n<100M
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
paperswithcode_id: cc100
pretty_name: CC100
configs:
- am
- sr
---

# Dataset Card for CC100

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

- **Homepage:** https://data.statmt.org/cc-100/
- **Repository:** None
- **Paper:** https://www.aclweb.org/anthology/2020.acl-main.747.pdf, https://www.aclweb.org/anthology/2020.lrec-1.494.pdf
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

This corpus is an attempt to recreate the dataset used for training XLM-R. This corpus comprises of monolingual data for 100+ languages and also includes data for romanized languages (indicated by *_rom). This was constructed using the urls and paragraph indices provided by the CC-Net repository by processing January-December 2018 Commoncrawl snapshots.

### Supported Tasks and Leaderboards

CC-100 is mainly inteded to pretrain language models and word represantations.

### Languages

To load a language which isn't part of the config, all you need to do is specify the language code in the config.
You can find the valid languages in Homepage section of Dataset Description: https://data.statmt.org/cc-100/
E.g.

`dataset = load_dataset("cc100", lang="en")`

## Dataset Structure

### Data Instances

An example from the `am` configuration:

```
{'id': '0', 'text': 'ተለዋዋጭ የግድግዳ አንግል ሙቅ አንቀሳቅሷል ቲ-አሞሌ አጥቅሼ ...\n'}
```

Each data point is a paragraph of text. The paragraphs are presented in the original (unshuffled) order. Documents are separated by a data point consisting of a single newline character.

### Data Fields

The data fields are:

- id: id of the example
- text: content as a string

### Data Splits

Sizes of some configurations:

|   name   |train|
|----------|----:|
|am|3124561|
|sr|35747957|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The data comes from multiple web pages in a large variety of languages.

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

Being constructed from Common Crawl, personal and sensitive information might be present. This **must** be considered before training deep learning models with CC-100, specially in the case of text-generation models.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset was prepared by [Statistical Machine Translation at the University of Edinburgh](https://www.statmt.org/ued/) using the [CC-Net](https://github.com/facebookresearch/cc_net) toolkit by Facebook Research.

### Licensing Information

Statistical Machine Translation at the University of Edinburgh makes no claims of intellectual property on the work of preparation of the corpus. By using this, you are also bound by the [Common Crawl terms of use](https://commoncrawl.org/terms-of-use/) in respect of the content contained in the dataset.

### Citation Information

```bibtex
@inproceedings{conneau-etal-2020-unsupervised,
    title = "Unsupervised Cross-lingual Representation Learning at Scale",
    author = "Conneau, Alexis  and
      Khandelwal, Kartikay  and
      Goyal, Naman  and
      Chaudhary, Vishrav  and
      Wenzek, Guillaume  and
      Guzm{\'a}n, Francisco  and
      Grave, Edouard  and
      Ott, Myle  and
      Zettlemoyer, Luke  and
      Stoyanov, Veselin",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.747",
    doi = "10.18653/v1/2020.acl-main.747",
    pages = "8440--8451",
    abstract = "This paper shows that pretraining multilingual language models at scale leads to significant performance gains for a wide range of cross-lingual transfer tasks. We train a Transformer-based masked language model on one hundred languages, using more than two terabytes of filtered CommonCrawl data. Our model, dubbed XLM-R, significantly outperforms multilingual BERT (mBERT) on a variety of cross-lingual benchmarks, including +14.6{\%} average accuracy on XNLI, +13{\%} average F1 score on MLQA, and +2.4{\%} F1 score on NER. XLM-R performs particularly well on low-resource languages, improving 15.7{\%} in XNLI accuracy for Swahili and 11.4{\%} for Urdu over previous XLM models. We also present a detailed empirical analysis of the key factors that are required to achieve these gains, including the trade-offs between (1) positive transfer and capacity dilution and (2) the performance of high and low resource languages at scale. Finally, we show, for the first time, the possibility of multilingual modeling without sacrificing per-language performance; XLM-R is very competitive with strong monolingual models on the GLUE and XNLI benchmarks. We will make our code and models publicly available.",
}
```

```bibtex
@inproceedings{wenzek-etal-2020-ccnet,
    title = "{CCN}et: Extracting High Quality Monolingual Datasets from Web Crawl Data",
    author = "Wenzek, Guillaume  and
      Lachaux, Marie-Anne  and
      Conneau, Alexis  and
      Chaudhary, Vishrav  and
      Guzm{\'a}n, Francisco  and
      Joulin, Armand  and
      Grave, Edouard",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.494",
    pages = "4003--4012",
    abstract = "Pre-training text representations have led to significant improvements in many areas of natural language processing. The quality of these models benefits greatly from the size of the pretraining corpora as long as its quality is preserved. In this paper, we describe an automatic pipeline to extract massive high-quality monolingual datasets from Common Crawl for a variety of languages. Our pipeline follows the data processing introduced in fastText (Mikolov et al., 2017; Grave et al., 2018), that deduplicates documents and identifies their language. We augment this pipeline with a filtering step to select documents that are close to high quality corpora like Wikipedia.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.
