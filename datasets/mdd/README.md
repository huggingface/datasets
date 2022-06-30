---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- en
license:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- dialogue-modeling
paperswithcode_id: mdd
pretty_name: Movie Dialog dataset (MDD)
configs:
- task1_qa
- task2_recs
- task3_qarecs
- task4_reddit
---

# Dataset Card for MDD

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

- **Homepage:**[The bAbI project](https://research.fb.com/downloads/babi/)
- **Repository:**
- **Paper:** [arXiv Paper](https://arxiv.org/pdf/1511.06931.pdf)
- **Leaderboard:**
- **Point of Contact:** 
### Dataset Summary

The Movie Dialog dataset (MDD) is designed to measure how well models can perform at goal and non-goal orientated dialog centered around the topic of movies (question answering, recommendation and discussion), from various movie reviews sources such as MovieLens and OMDb.
### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The data is present in English language as written by users on OMDb and MovieLens websites.

## Dataset Structure

### Data Instances
An instance from the `task3_qarecs` config's `train` split:
```
{'dialogue_turns': {'speaker': [0, 1, 0, 1, 0, 1], 'utterance': ["I really like Jaws, Bottle Rocket, Saving Private Ryan, Tommy Boy, The Muppet Movie, Face/Off, and Cool Hand Luke. I'm looking for a Documentary movie.", 'Beyond the Mat', 'Who is that directed by?', 'Barry W. Blaustein', 'I like Jon Fauer movies more. Do you know anything else?', 'Cinematographer Style']}}
```
An instance from the `task4_reddit` config's `cand-valid` split:
```
{'dialogue_turns': {'speaker': [0], 'utterance': ['MORTAL KOMBAT !']}}
```
### Data Fields

For all configurations:
- `dialogue_turns`: a dictionary feature containing:
  - `speaker`: an integer with possible values including `0`, `1`, indicating which speaker wrote the utterance.
  - `utterance`: a `string` feature containing the text utterance.

### Data Splits

The splits and corresponding sizes are:

|config  |train  |test |validation|cand_valid|cand_test|
|:--|------:|----:|---------:|----:|----:|
|task1_qa|96185|9952|9968|-|-|
|task2_recs|1000000|10000|10000|-|-|
|task3_qarecs|952125|4915|5052|-|-|
|task4_reddit|945198|10000|10000|10000|10000|

The `cand_valid` and `cand_test` are negative candidates for the `task4_reddit` configuration which is used in ranking true positive against these candidates and hits@k (or another ranking metric) is reported. (See paper)


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The construction of the tasks depended on some existing datasets:

1) MovieLens. The data was downloaded from: http://grouplens.org/datasets/movielens/20m/ on May 27th, 2015.

2) OMDB. The data was downloaded from: http://beforethecode.com/projects/omdb/download.aspx on May 28th, 2015.

3) For `task4_reddit`, the data is a processed subset (movie subreddit only) of the data available at:
https://www.reddit.com/r/datasets/comments/3bxlg7

#### Who are the source language producers?

Users on MovieLens, OMDB website and reddit websites, among others.

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

Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston (at Facebook Research).

### Licensing Information

```
Creative Commons Attribution 3.0 License
```

### Citation Information

```
@misc{dodge2016evaluating,
      title={Evaluating Prerequisite Qualities for Learning End-to-End Dialog Systems}, 
      author={Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston},
      year={2016},
      eprint={1511.06931},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.
