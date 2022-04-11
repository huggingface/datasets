---
pretty_name: WMT20 - MultiLingual Quality Estimation (MLQE) Task2
annotations_creators:
- expert-generated
- machine-generated
language_creators:
- found
languages:
  en-de:
  - en
  - de
  en-zh:
  - en
  - zh
licenses:
- unknown
multilinguality:
- translation
size_categories:
- 1K<n<10K
source_datasets:
- extended|wikipedia
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
---

# Dataset Card Creation Guide

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

- **Homepage:** [WMT20 Quality Estimation Shared Task](http://www.statmt.org/wmt20/quality-estimation-task.html)
- **Repository**: [Github repository](https://github.com/deep-spin/deep-spin.github.io/tree/master/docs/data/wmt2020_qe)
- **Paper:** *Not available*

### Dataset Summary

From the homepage:
*This shared task (part of WMT20) will build on its previous editions to further examine automatic methods for estimating the quality of neural machine translation output at run-time, without relying on reference translations. As in previous years, we cover estimation at various levels. Important elements introduced this year include: a new task where sentences are annotated with Direct Assessment (DA) scores instead of labels based on post-editing; a new multilingual sentence-level dataset mainly from Wikipedia articles, where the source articles can be retrieved for document-wide context; the availability of NMT models to explore system-internal information for the task.*

*Task 1 evaluates the application of QE for post-editing purposes. It consists of predicting:*
- ***Word-level tags.*** *This is done both on source side (to detect which words caused errors) and target side (to detect mistranslated or missing words).*
  - ***Target.*** *Each token is tagged as either `OK` or `BAD`. Additionally, each gap between two words is tagged as `BAD` if one or more missing words should have been there, and `OK` otherwise. Note that number of tags for each target sentence is 2*N+1, where N is the number of tokens in the sentence.*
  - ***Source.*** *Tokens are tagged as `OK` if they were correctly translated, and `BAD` otherwise. Gaps are not tagged.*
- ***Sentence-level HTER scores.*** *HTER (Human Translation Error Rate) is the ratio between the number of edits (insertions/deletions/replacements) needed and the reference translation length.*

### Supported Tasks and Leaderboards

From the homepage:

*For sentence-level QE, submissions are evaluated in terms of the Pearson's correlation metric for the sentence-level HTER prediction. For word-level QE, they will be evaluated in terms of MCC ([Matthews correlation coefficient](https://en.wikipedia.org/wiki/Matthews_correlation_coefficient)). These are the [official evaluation scripts](https://github.com/sheffieldnlp/qe-eval-scripts).*

### Languages

There are two language pairs in this dataset:
- English - German (`en` - `de`)
- German - Chinese (`en` - `zh`)

## Dataset Structure

### Data Instances

An example looks like this:
```
{
  'translation': {
    'en': 'favorite fish include cod , salmon , winter flounder , haddock , striped bass , pollock , hake , bluefish , and , in southern New England , Tautog .',
    'de': 'zu den Lieblingsfischen gehören Kabeljau , Lachs , Winterflounder , Schellfisch , gestreifter Bass , Pollock , Seehecht , Rotbarsch und in Südengland Tautog .',
  }
  'src_tags': [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
  'mt_tags': [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
  'pe': 'zu den Lieblingsfischen zählen Kabeljau , Lachs , Winterflunder , Schellfisch , Wolfsbarsch , Pollock , Seehecht , Bluefish und im Süden Neuenglands Tautog .',
  'hter': 0.3199999928474426,
  'alignments': [[2, 0], [2, 1], [2, 3], [3, 2], [3, 4], [4, 5], [5, 6], [6, 5], [7, 6], [8, 6], [9, 7], [10, 8], [10, 10], [11, 9], [12, 12], [13, 13], [14, 11], [15, 12], [15, 15], [16, 14], [17, 17], [19, 16], [20, 16], [21, 20], [22, 18], [23, 19], [23, 21], [24, 22], [25, 21], [26, 22], [27, 22], [28, 23], [29, 24]],
}
```

### Data Fields

- `translation`: Dictionary with pairs (source,target).
  - src_lg: sequence of text in source language.
  - tgt_lg: sequence of text in target language.
- `src_tags`: source word-level tags. `0`=`BAD`, `1`=`OK`. `[]` if N/A (only for test).
- `mt_tags`: target word-level tags. `0`=`BAD`, `1`=`OK`. `[]` if N/A (only for test).
- `pe`: post-edited version of NMT output. `""` if N/A (only for test).
- `hter`: human translation error rate. `-10_000` if N/A (only for test).
- `alignments`: Word aligments. List of pairs of integers.

### Data Splits

There are 2 configurations in this dataset (one for each available language pair). Each configuration is composed of 7K examples for training, 1K for validation and 1K for (blind) test.

## Dataset Creation

### Curation Rationale

The original text is extracted from Wikipedia.

From the homepage:

*Word-level labels have been obtained by using the alignments provided by the [TER](http://www.cs.umd.edu/~snover/tercom/) tool (settings: tokenised, case insensitive, exact matching only, disabling shifts by using the `-d 0` option) between machine translations and their post-edited versions. Shifts (word order errors) were not annotated as such (but rather as deletions + insertions) to avoid introducing noise in the annotation.*

*HTER values are obtained deterministically from word-level tags. However, when computing HTER, we allow shifts in TER.*

*The baseline system is a neural predictor-estimator approach implemented in [OpenKiwi](https://github.com/Unbabel/OpenKiwi) ([Kepler at al., 2019](https://arxiv.org/abs/1902.08646)), where the predictor model will be trained on the parallel data used to train the NMT model.*

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

Unknown

### Citation Information

```
Not available.
```

### Contributions

Thanks to [@VictorSanh](https://github.com/VictorSanh) for adding this dataset.