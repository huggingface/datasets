---
pretty_name: C4
annotations_creators:
- no-annotation
language_creators:
- found
language:
- en
license:
- odc-by
multilinguality:
- multilingual
size_categories:
- 100M<n<1B
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
paperswithcode_id: c4
---

# Dataset Card for C4

## Table of Contents

- [Dataset Card for C4](#dataset-card-for-c4)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://huggingface.co/datasets/allenai/c4
- **Paper:** https://arxiv.org/abs/1910.10683

### Dataset Summary

A colossal, cleaned version of Common Crawl's web crawl corpus. Based on Common Crawl dataset: "https://commoncrawl.org".

This is the version prepared by AllenAI, hosted at this address: https://huggingface.co/datasets/allenai/c4

It comes in four variants:

- `en`: 305GB in JSON format
- `en.noblocklist`: 380GB in JSON format
- `en.noclean`: 2.3TB in JSON format
- `realnewslike`: 15GB in JSON format

The `en.noblocklist` variant is exactly the same as the `en` variant, except we turned off the so-called "badwords filter", which removes all documents that contain words from the lists at https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words.

### Supported Tasks and Leaderboards

C4 is mainly intended to pretrain language models and word representations.

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

An example form the `en` config is:

```
{
  'url': 'https://klyq.com/beginners-bbq-class-taking-place-in-missoula/',
  'text': 'Beginners BBQ Class Taking Place in Missoula!\nDo you want to get better at making delicious BBQ? You will have the opportunity, put this on your calendar now. Thursday, September 22nd join World Class BBQ Champion, Tony Balay from Lonestar Smoke Rangers. He will be teaching a beginner level class for everyone who wants to get better with their culinary skills.\nHe will teach you everything you need to know to compete in a KCBS BBQ competition, including techniques, recipes, timelines, meat selection and trimming, plus smoker and fire information.\nThe cost to be in the class is $35 per person, and for spectators it is free. Included in the cost will be either a t-shirt or apron and you will be tasting samples of each meat that is prepared.',
  'timestamp': '2019-04-25T12:57:54Z'
}
```

### Data Fields

The data have several fields:

- `url`: url of the source as a string
- `text`: text content as a string
- `timestamp`: timestamp as a string

### Data Splits

|      name      |  train  |validation|
|----------------|--------:|---------:|
| en             |364868892|    364608|
| en.noblocklist |393391519|    393226|
| en.noclean     |        ?|         ?|
| realnewslike   | 13799838|     13863|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

C4 dataset is a collection of about 750GB of English-language text sourced from the public Common Crawl web scrape. It includes heuristics to extract only natural language (as opposed to boilerplate and other gibberish) in addition to extensive deduplication. You can find the code that has been used to build this dataset in [c4.py](https://github.com/tensorflow/datasets/blob/5952d3d60d60e1727786fa7a9a23d24bb463d4d6/tensorflow_datasets/text/c4.py) by Tensorflow Datasets.

The dataset was explicitly designed to be English only: any page that was not given a probability of at least 99% of being English by [langdetect](https://github.com/Mimino666/langdetect) was discarded.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

AllenAI are releasing this dataset under the terms of ODC-BY. By using this, you are also bound by the Common Crawl terms of use in respect of the content contained in the dataset.

### Citation Information

```
@article{2019t5,
    author = {Colin Raffel and Noam Shazeer and Adam Roberts and Katherine Lee and Sharan Narang and Michael Matena and Yanqi Zhou and Wei Li and Peter J. Liu},
    title = {Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer},
    journal = {arXiv e-prints},
    year = {2019},
    archivePrefix = {arXiv},
    eprint = {1910.10683},
}
```

### Contributions

Thanks to [@dirkgr](https://github.com/dirkgr) and [@lhoestq](https://github.com/lhoestq) for adding this dataset.
