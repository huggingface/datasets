---
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-long-range-dependency
multilinguality:
- monolingual
languages:
- en
language_creators:
- found
annotations_creators:
- expert-generated
source_datasets:
- extended|bookcorpus
size_categories:
- 10K<n<100K
licenses:
- cc-by-4.0
---

# Dataset Card for LAMBADA

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [LAMBADA homepage](https://zenodo.org/record/2630551#.X8UP76pKiIa)
- **Paper:** [The LAMBADA dataset: Word prediction requiring a broad discourse context∗](https://www.aclweb.org/anthology/P16-1144.pdf)

### Dataset Summary

The LAMBADA evaluates the capabilities of computational models
for text understanding by means of a word prediction task.
LAMBADA is a collection of narrative passages sharing the characteristic
that human subjects are able to guess their last word if
they are exposed to the whole passage, but not if they
only see the last sentence preceding the target word.
To succeed on LAMBADA, computational models cannot
simply rely on local context, but must be able to
keep track of information in the broader discourse.

The LAMBADA dataset is extracted from BookCorpus and
consists of 10'022 passages, divided into 4'869 development
and 5'153 test passages. The training data for language
models to be tested on LAMBADA include the full text
of 2'662 novels (disjoint from those in dev+test),
comprising 203 million words.

### Supported Tasks and Leaderboards

Long range dependency evaluated as (last) word prediction

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

A data point is a text sequence (passage) including the context, the target sentence (the last one) and the target word. For each passage in the dev and the test splits, the word to be guessed is the last one.

The training data include the full text of 2'662 novels (disjoint from
those in dev+test), comprising more than 200M words. It consists of text from the same domain as the dev+test passages, but not filtered in any way.

Each training instance has a `category` field indicating which sub-category the book was extracted from. This field is not given for the dev and test splits.

An example looks like this:

```
{"category": "Mystery",
 "text": "bob could have been called in at this point , but he was n't miffed at his exclusion at all . he was relieved at not being brought into this initial discussion with central command . `` let 's go make some grub , '' said bob as he turned to danny . danny did n't keep his stoic expression , but with a look of irritation got up and left the room with bob",
}
```

### Data Fields

- `category`: the sub-category of books from which the book was extracted from. Only available for the training split.
- `text`: the text (concatenation of context, target sentence and target word). The word to be guessed is the last one.

### Data Splits

- train: 2'662 novels
- dev: 4'869 passages
- test: 5'153 passages

## Dataset Creation

### Curation Rationale

The dataset aims at evaluating the ability of language models to hold long-term contextual memories. Instances are extracted from books because they display long-term dependencies. In particular, the data are curated such that the target words are easy to guess by human subjects when they can look at the whole passage they come from, but nearly impossible if only the last sentence is considered.

### Source Data

#### Initial Data Collection and Normalization

The corpus was duplicated and potentially offensive material were filtered out with a stop word list.

#### Who are the source language producers?

The passages are extracted from novels from [Book Corpus](https://github.com/huggingface/datasets/tree/master/datasets/bookcorpus).

### Annotations

#### Annotation process

The authors required two consecutive subjects (paid crowdsourcers) to exactly match the missing word based on the whole passage (comprising the context and the target sentence), and made sure that no subject (out of ten) was able to provide it based on local context only, even when given 3 guesses.

#### Who are the annotators?

The text is self-annotated but was curated by asking (paid) crowdsourcers to guess the last word.

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

The dataset is released under the [CC BY 4.0](Creative Commons Attribution 4.0 International) license.

### Citation Information

```
@InProceedings{paperno-EtAl:2016:P16-1,
  author    = {Paperno, Denis  and  Kruszewski, Germ\'{a}n  and  Lazaridou,
Angeliki  and  Pham, Ngoc Quan  and  Bernardi, Raffaella  and  Pezzelle,
Sandro  and  Baroni, Marco  and  Boleda, Gemma  and  Fernandez, Raquel},
  title     = {The {LAMBADA} dataset: Word prediction requiring a broad
discourse context},
  booktitle = {Proceedings of the 54th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers)},
  month     = {August},
  year      = {2016},
  address   = {Berlin, Germany},
  publisher = {Association for Computational Linguistics},
  pages     = {1525--1534},
  url       = {http://www.aclweb.org/anthology/P16-1144}
}
```
