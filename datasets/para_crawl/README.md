---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- bg
- cs
- da
- de
- el
- en
- es
- et
- fi
- fr
- ga
- hr
- hu
- it
- lt
- lv
- mt
- nl
- pl
- pt
- ro
- sk
- sl
- sv
licenses:
- cc0-1.0
multilinguality:
- translation
pretty_name: ParaCrawl
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: paracrawl
---

# Dataset Card for "para_crawl"

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

- **Homepage:** [https://paracrawl.eu/releases.html](https://paracrawl.eu/releases.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 9879.92 MB
- **Size of the generated dataset:** 31378.09 MB
- **Total amount of disk used:** 41258.01 MB

### Dataset Summary

Web-Scale Parallel Corpora for Official European Languages.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### enbg

- **Size of downloaded dataset files:** 98.94 MB
- **Size of the generated dataset:** 340.02 MB
- **Total amount of disk used:** 438.95 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"bg\": \". “A felirat faragott karnis a bejárat fölött, templom épült 14 Július 1643, A földesúr és felesége Jeremiás Murguleţ, C..."
}
```

#### encs

- **Size of downloaded dataset files:** 187.31 MB
- **Size of the generated dataset:** 608.51 MB
- **Total amount of disk used:** 795.82 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"cs\": \". “A felirat faragott karnis a bejárat fölött, templom épült 14 Július 1643, A földesúr és felesége Jeremiás Murguleţ, C..."
}
```

#### enda

- **Size of downloaded dataset files:** 174.34 MB
- **Size of the generated dataset:** 570.89 MB
- **Total amount of disk used:** 745.23 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"da\": \". “A felirat faragott karnis a bejárat fölött, templom épült 14 Július 1643, A földesúr és felesége Jeremiás Murguleţ, C..."
}
```

#### ende

- **Size of downloaded dataset files:** 1247.17 MB
- **Size of the generated dataset:** 3812.02 MB
- **Total amount of disk used:** 5059.19 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"de\": \". “A felirat faragott karnis a bejárat fölött, templom épült 14 Július 1643, A földesúr és felesége Jeremiás Murguleţ, C..."
}
```

#### enel

- **Size of downloaded dataset files:** 184.59 MB
- **Size of the generated dataset:** 656.19 MB
- **Total amount of disk used:** 840.78 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"el\": \". “A felirat faragott karnis a bejárat fölött, templom épült 14 Július 1643, A földesúr és felesége Jeremiás Murguleţ, C..."
}
```

### Data Fields

The data fields are the same among all splits.

#### enbg
- `translation`: a multilingual `string` variable, with possible languages including `en`, `bg`.

#### encs
- `translation`: a multilingual `string` variable, with possible languages including `en`, `cs`.

#### enda
- `translation`: a multilingual `string` variable, with possible languages including `en`, `da`.

#### ende
- `translation`: a multilingual `string` variable, with possible languages including `en`, `de`.

#### enel
- `translation`: a multilingual `string` variable, with possible languages including `en`, `el`.

### Data Splits

| name |    train |
|------|---------:|
| enbg |  1039885 |
| encs |  2981949 |
| enda |  2414895 |
| ende | 16264448 |
| enel |  1985233 |

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

[Creative Commons CC0 license ("no rights reserved")](https://creativecommons.org/share-your-work/public-domain/cc0/).

### Citation Information

```
@inproceedings{banon-etal-2020-paracrawl,
    title = "{P}ara{C}rawl: Web-Scale Acquisition of Parallel Corpora",
    author = "Ba{\~n}{\'o}n, Marta  and
      Chen, Pinzhen  and
      Haddow, Barry  and
      Heafield, Kenneth  and
      Hoang, Hieu  and
      Espl{\`a}-Gomis, Miquel  and
      Forcada, Mikel L.  and
      Kamran, Amir  and
      Kirefu, Faheem  and
      Koehn, Philipp  and
      Ortiz Rojas, Sergio  and
      Pla Sempere, Leopoldo  and
      Ram{\'\i}rez-S{\'a}nchez, Gema  and
      Sarr{\'\i}as, Elsa  and
      Strelec, Marek  and
      Thompson, Brian  and
      Waites, William  and
      Wiggins, Dion  and
      Zaragoza, Jaume",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.417",
    doi = "10.18653/v1/2020.acl-main.417",
    pages = "4555--4567",
    abstract = "We report on methods to create the largest publicly available parallel corpora by crawling the web, using open source software. We empirically compare alternative methods and publish benchmark data sets for sentence alignment and sentence pair filtering. We also describe the parallel corpora released and evaluate their quality and their usefulness to create machine translation systems.",
}
```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.
