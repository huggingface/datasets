---
annotations_creators:
  auto:
  - machine-generated
  auto_acl:
  - machine-generated
  manual:
  - crowdsourced
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|other-wikipedia
task_categories:
- conditional-text-generation
task_ids:
- text-simplification
---

# Dataset Card for WikiAuto

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

- **Repository:** [WikiAuto github repository](https://github.com/chaojiang06/wiki-auto)
- **Paper:** [Neural CRF Model for Sentence Alignment in Text Simplification](https://arxiv.org/abs/2005.02324)
- **Point of Contact:** [Chao Jiang](jiang.1530@osu.edu)

### Dataset Summary

WikiAuto provides a set of aligned sentences from English Wikipedia and Simple English Wikipedia as a resource to train sentence simplification systems.

The authors first crowd-sourced a set of manual alignments between sentences in a subset of the Simple English Wikipedia and their corresponding versions in English Wikipedia (this corresponds to the `manual` config in this version of dataset), then trained a neural CRF system to predict these alignments.

The trained alignment prediction model was then applied to the other articles in Simple English Wikipedia with an English counterpart to create a larger corpus of aligned sentences (corresponding to the `auto` and `auto_acl` configs here).

### Supported Tasks and Leaderboards

The dataset was created to support a `text-simplification` task. Success in these tasks is typically measured using the [SARI](https://huggingface.co/metrics/sari) and [FKBLEU](https://huggingface.co/metrics/fkbleu) metrics described in the paper [Optimizing Statistical Machine Translation for Text Simplification](https://www.aclweb.org/anthology/Q16-1029.pdf).

### Languages

While both the input and output of the proposed task are in English (`en`), it should be noted that it is presented as a translation task where Wikipedia Simple English is treated as its own idiom. For a statement of what is intended (but not always observed) to constitute Simple English on this platform, see [Simple English in Wikipedia](https://simple.wikipedia.org/wiki/Wikipedia:About#Simple_English).

## Dataset Structure

### Data Instances

The data in all of the configurations looks a little different.

A `manual` config instance consists of a sentence from the Simple English Wikipedia article, one from the linked English Wikipedia article, IDs for each of them, and a label indicating whether they are  aligned. Sentences on either side can be repeated so that the aligned sentences are in the same instances. For example:
```
{'alignment_label': 1,
 'normal_sentence': 'The Local Government Act 1985 is an Act of Parliament in the United Kingdom.',
 'normal_sentence_id': '0_66252-1-0-0',
 'simple_sentence': 'The Local Government Act 1985 was an Act of Parliament in the United Kingdom.',
 'simple_sentence_id': '0_66252-0-0-0'}
```
Is followed by
```
{'alignment_label': 0,
 'normal_sentence': 'Its main effect was to abolish the six county councils of the metropolitan counties that had been set up in 1974, 11 years earlier, by the Local Government Act 1972, along with the Greater London Council that had been established in 1965.',
 'normal_sentence_id': '0_66252-1-0-1',
 'simple_sentence': 'The Local Government Act 1985 was an Act of Parliament in the United Kingdom.',
 'simple_sentence_id': '0_66252-0-0-0'}
```

The `auto` config shows a pair of an English and corresponding Simple English Wikipedia as an instance, with an alignment at the paragraph and sentence level:
```
{'example_id': '0',
 'normal': {'normal_article_content': {'normal_sentence': ["Lata Mondal ( ; born: 16 January 1993, Dhaka) is a Bangladeshi cricketer who plays for the Bangladesh national women's cricket team.",
    'She is a right handed batter.',
    'Mondal was born on January 16, 1993 in Dhaka, Bangladesh.',
    "Mondal made her ODI career against the Ireland women's cricket team on November 26, 2011.",
    "Mondal made her T20I career against the Ireland women's cricket team on August 28, 2012.",
    "In October 2018, she was named in Bangladesh's squad for the 2018 ICC Women's World Twenty20 tournament in the West Indies.",
    "Mondal was a member of the team that won a silver medal in cricket against the China national women's cricket team at the 2010 Asian Games in Guangzhou, China."],
   'normal_sentence_id': ['normal-41918715-0-0',
    'normal-41918715-0-1',
    'normal-41918715-1-0',
    'normal-41918715-2-0',
    'normal-41918715-3-0',
    'normal-41918715-3-1',
    'normal-41918715-4-0']},
  'normal_article_id': 41918715,
  'normal_article_title': 'Lata Mondal',
  'normal_article_url': 'https://en.wikipedia.org/wiki?curid=41918715'},
 'paragraph_alignment': {'normal_paragraph_id': ['normal-41918715-0'],
  'simple_paragraph_id': ['simple-702227-0']},
 'sentence_alignment': {'normal_sentence_id': ['normal-41918715-0-0',
   'normal-41918715-0-1'],
  'simple_sentence_id': ['simple-702227-0-0', 'simple-702227-0-1']},
 'simple': {'simple_article_content': {'simple_sentence': ["Lata Mondal (born: 16 January 1993) is a Bangladeshi cricketer who plays for the Bangladesh national women's cricket team.",
    'She is a right handed bat.'],
   'simple_sentence_id': ['simple-702227-0-0', 'simple-702227-0-1']},
  'simple_article_id': 702227,
  'simple_article_title': 'Lata Mondal',
  'simple_article_url': 'https://simple.wikipedia.org/wiki?curid=702227'}}
```

Finally, the `auto_acl` config was obtained by selecting the aligned pairs of sentences from `auto` to provide a ready-to-go aligned dataset to train a sequence-to-sequence system, so an instance is a single pair of sentences:
```
{'normal_sentence': 'In early work , Rutherford discovered the concept of radioactive half-life , the radioactive element radon , and differentiated and named alpha and beta radiation .\n',
 'simple_sentence': 'Rutherford discovered the radioactive half-life , and the three parts of radiation which he named Alpha , Beta , and Gamma .\n'}
```

### Data Fields

The data has the following field:
- `normal_sentence`: a sentence from English Wikipedia.
- `normal_sentence_id`: a unique ID for each English Wikipedia sentence. The last two dash-separated numbers correspond to the paragraph number in the article and the sentence number in the paragraph.
- `simple_sentence`: a sentence from Simple English Wikipedia.
- `simple_sentence_id`: a unique ID for each Simple English Wikipedia sentence. The last two dash-separated numbers correspond to the paragraph number in the article and the sentence number in the paragraph.
- `alignment_label`: signifies whether a pair of sentences is aligned: labels are `1:aligned` and `0:notAligned`
- `paragraph_alignment`: a first step of alignment mapping English and Simple English paragraphs from linked articles
- `sentence_alignment`: the full alignment mapping English and Simple English sentences from linked articles

### Data Splits

In `auto`, the `part_2` split corresponds to the articles used in `manual`, and `part_1` has the rest of Wikipedia.

The `manual` config is provided with a `train`/`dev`/`test` split with the following amounts of data:
|                            | Tain   | Dev   | Test   |
| -----                      | ------ | ----- | ----   |
| Total sentence pairs       | 373801 | 73249 | 118074 |
| Aligned sentence pairs     |  1889  |  346  | 677    |

## Dataset Creation

### Curation Rationale

Simple English Wikipedia provides a ready source of training data for text simplification systems, as 1. articles in different languages are linked, making it easier to find parallel data and 2. the Simple English data is written by users for users rather than by professional translators. However, even though articles are aligned, finding a good sentence-level alignment can remain challenging. This work aims to provide a solution for this problem. By manually annotating a sub-set of the articles, they manage to achieve an F1 score of over 88% on predicting alignment, which allows to create a good quality sentence level aligned corpus using all of Simple English Wikipedia.

### Source Data

#### Initial Data Collection and Normalization

The authors mention that they "extracted 138,095 article pairs from the 2019/09 Wikipedia dump [...] using an improved version of the [WikiExtractor](https://github.com/attardi/wikiextractor) library". The [SpaCy](https://spacy.io/) library is used for sentence splitting.

#### Who are the source language producers?

The dataset uses langauge from Wikipedia: some demographic information is provided [here](https://en.wikipedia.org/wiki/Wikipedia:Who_writes_Wikipedia%3F).

### Annotations

#### Annotation process

Sentence alignment labels were obtained for 500 randomly sampled document pairs (10,123 sentence pairs total). The authors pre-selected several alignment candidates from English Wikipedia for each Simple Wikipedia sentence based on various similarity metrics, then asked the crowd-workers to annotate these pairs.

#### Who are the annotators?

No demographic annotation is provided for the crowd workers.
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

The dataset was created by Chao Jiang, Mounica Maddela, Wuwei Lan, Yang Zhong, and Wei Xu working at Ohio State University.

### Licensing Information

The dataset is not licensed by itself, but the source Wikipedia data is under a `cc-by-sa-3.0` license.

### Citation Information

You can cite the paper presenting the dataset as:
```
@inproceedings{acl/JiangMLZX20,
  author    = {Chao Jiang and
               Mounica Maddela and
               Wuwei Lan and
               Yang Zhong and
               Wei Xu},
  editor    = {Dan Jurafsky and
               Joyce Chai and
               Natalie Schluter and
               Joel R. Tetreault},
  title     = {Neural {CRF} Model for Sentence Alignment in Text Simplification},
  booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2020, Online, July 5-10, 2020},
  pages     = {7943--7960},
  publisher = {Association for Computational Linguistics},
  year      = {2020},
  url       = {https://www.aclweb.org/anthology/2020.acl-main.709/}
}
```
