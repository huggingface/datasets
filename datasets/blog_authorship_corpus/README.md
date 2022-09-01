---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
paperswithcode_id: blog-authorship-corpus
pretty_name: Blog Authorship Corpus
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
---

# Dataset Card for Blog Authorship Corpus

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

- **Homepage:** [https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm](https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 298.45 MB
- **Size of the generated dataset:** 617.75 MB
- **Total amount of disk used:** 916.20 MB

### Dataset Summary

The Blog Authorship Corpus consists of the collected posts of 19,320 bloggers gathered from blogger.com in August 2004. The corpus incorporates a total of 681,288 posts and over 140 million words - or approximately 35 posts and 7250 words per person.

Each blog is presented as a separate file, the name of which indicates a blogger id# and the blogger’s self-provided gender, age, industry and astrological sign. (All are labeled for gender and age but for many, industry and/or sign is marked as unknown.)

All bloggers included in the corpus fall into one of three age groups:
- 8240 "10s" blogs (ages 13-17),
- 8086 "20s" blogs (ages 23-27),
- 2994 "30s" blogs (ages 33-47).

For each age group there are an equal number of male and female bloggers.

Each blog in the corpus includes at least 200 occurrences of common English words. All formatting has been stripped with two exceptions. Individual posts within a single blogger are separated by the date of the following post and links within a post are denoted by the label urllink.

The corpus may be freely used for non-commercial research purposes.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

The language of the dataset is English (`en`).

## Dataset Structure

### Data Instances

#### blog-authorship-corpus

- **Size of downloaded dataset files:** 298.45 MB
- **Size of the generated dataset:** 617.75 MB
- **Total amount of disk used:** 916.20 MB

An example of 'validation' looks as follows.
```
{
    "age": 23,
    "date": "27,July,2003",
    "gender": "female",
    "horoscope": "Scorpion",
    "job": "Student",
    "text": "This is a second test file."
}
```

### Data Fields

The data fields are the same among all splits.

#### blog-authorship-corpus
- `text`: a `string` feature.
- `date`: a `string` feature.
- `gender`: a `string` feature.
- `age`: a `int32` feature.
- `horoscope`: a `string` feature.
- `job`: a `string` feature.

### Data Splits

|         name         |train |validation|
|----------------------|-----:|---------:|
|blog-authorship-corpus|532812|     31277|

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

The corpus may be freely used for non-commercial research purposes.

### Citation Information

```
@inproceedings{schler2006effects,
    title={Effects of age and gender on blogging.},
    author={Schler, Jonathan and Koppel, Moshe and Argamon, Shlomo and Pennebaker, James W},
    booktitle={AAAI spring symposium: Computational approaches to analyzing weblogs},
    volume={6},
    pages={199--205},
    year={2006}
}

```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.
