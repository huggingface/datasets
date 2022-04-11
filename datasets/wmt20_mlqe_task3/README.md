---
pretty_name: WMT20 - MultiLingual Quality Estimation (MLQE) Task3
annotations_creators:
- expert-generated
- machine-generated
language_creators:
- found
languages:
- en
- fr
licenses:
- unknown
multilinguality:
- translation
size_categories:
- 1K<n<10K
source_datasets:
- extended|amazon_us_reviews
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

*The goal of this task 3 is to predict document-level quality scores as well as fine-grained annotations.*

*Each document has a product title and its description, and is annotated for translation errors according to the MQM framework. Each error annotation has:*
- ***Word span(s).*** *Errors may consist of one or more words, not necessarily contiguous.*
- ***Severity.*** *An error can be minor (if it doesn't lead to a loss of meaning and it doesn't confuse or mislead the user), major (if it changes the meaning) or critical (if it changes the meaning and carry any type of implication, or could be seen as offensive).*
- ***Type.*** *A label specifying the error type, such as wrong word order, missing words, agreement, etc. They may provide additional information, but systems don't need to predict them.*

### Supported Tasks and Leaderboards

From the homepage:

*Submissions will be evaluated as in Task 1, in terms of Pearson's correlation between the true and predicted MQM document-level scores. Additionally, the predicted annotations will be evaluated in terms of their F1 scores with respect to the gold annotations. The [official evaluation scripts](https://github.com/sheffieldnlp/qe-eval-scripts) are available.*

### Languages

There is a single language pair in the dataset: English (`en`) - French (`fr`).

## Dataset Structure

### Data Instances

An example looks like this:
```
{
  'document_id': 'B0000568SY',
  'source_segments': ['Razor Scooter Replacement Wheels Set with Bearings', 'Scooter Wheels w/Bearings-Blue'],
  'source_tokenized': ['Razor Scooter Replacement Wheels Set with Bearings', 'Scooter Wheels w / Bearings-Blue'],
  'mt_segments': ['Roues de rechange Razor Scooter sertie de roulements', 'Roues de scooter w/roulements-bleu'],
  'mt_tokenized': ['Roues de rechange Razor Scooter sertie de roulements', 'Roues de scooter w / roulements-bleu'],
  'annotations': {
    'segment_id': [[0], [1], [1], [0, 0], [0], [1], [1]],
    'annotation_start': [[42], [19], [9], [0, 32], [9], [17], [30]],
    'annotation_length': [[10], [10], [7], [5, 6], [8], [1], [4]],
    'severity': [0, 0, 0, 0, 0, 1, 0],
    'severity_weight': [1.0, 1.0, 1.0, 1.0, 1.0, 5.0, 1.0]
    'category': [3, 3, 3, 1, 3, 36, 3],
  },
  'token_annotations': {
    'category': [3, 3, 3, 1, 3, 36, 3],
    'first_token': [[7], [5], [2], [0, 5], [2], [3], [5]],
    'last_token': [[7], [5], [2], [0, 5], [2], [3], [5]],
    'segment_id': [[0], [1], [1], [0, 0], [0], [1], [1]],
    'severity': [0, 0, 0, 0, 0, 1, 0],
    'token_after_gap': [[-1], [-1], [-1], [-1, -1], [-1], [-1], [-1]]
  },
  'token_index': [[[0, 5], [6, 2], [9, 8], [18, 5], [24, 7], [32, 6], [39, 2], [42, 10]], [[0, 5], [6, 2], [9, 7], [17, 1], [18, 1], [19, 15]]],
  'total_words': 16
}
```

### Data Fields

- `document_id`: the document id (name of the folder).
- `source_segments`: the original source text, one sentence per line (i.e. per element of the list).
- `source_tokenized`: a tokenized version of `source_segments`.
- `mt_segments`: the original machine-translated text, one sentence per line (i.e. per element of the list).
- `mt_tokenized`: a tokenized version of `mt_segments`. Default value is `[]` when this information is not available (it happens 3 times in the train set: `B0001BW0PQ`, `B0001GS19U` and `B000A6SMJ0`).
- `annotations`: error annotations for the document. Each item of the list corresponds to an error annotation, which in turn may contain one or more error spans. Error fields are encoded in a dictionary. In the case of a multi-span error, multiple starting positions and lengths are encoded in the list. Note that these positions points to `mt.segments`, not `mt_tokenized`.
  - `segment_id`: List of list of integers. Id of each error.
  - `annotation_start`: List of list of integers. Start of each error.
  - `annotation_length`: List of list of intergers. Length of each error.
  - `severity`: List of one hot. Severity category of each error.
  - `severity_weight`: List of floats. Severity weight of each error.
  - `category`: List of one hot. Category of each error. See the 45 categories in `_ANNOTATION_CATEGORIES_MAPPING`.
- `token_annotations`: tokenized version of `annotations`. Each error span that contains one or more tokens has a "first token" and "last token". Again, multi-span errors have their first and last tokens encoded in a list. When a span is over a gap between two tokens, the "first" and "last" positions are `-1` (encoded as `-` in the original data), and instead the `token_after_gap` column points to the token immediately after the gap. In case of a gap occurring at the end of the sentence, this value will be equal to the number of tokens.
  - `segment_id`: List of list of integers. Id of each error.
  - `first_token`: List of list of integers. Start of each error.
  - `last_token`: List of list of intergers. End of each error.
  - `token_after_gap`: List of list of integers. Token after gap of each error.
  - `severity`: List of one hot. Severity category of each error.
  - `category`: List of one hot. Category of each error. See the 45 categories in `_ANNOTATION_CATEGORIES_MAPPING`.
- `token_index`: a mapping of tokens to their start and ending positions in `mt_segments`. For each token, a start and end value are encoded in a list of length 2, and all tokens represent one item in the list.
- `total_words`: total number of words in the document

```
_ANNOTATION_CATEGORIES_MAPPING = {
  0: 'Addition',
  1: 'Agreement',
  2: 'Ambiguous Translation',
  3: 'Capitalization',
  4: 'Character Encoding',
  5: 'Company Terminology',
  6: 'Date/Time',
  7: 'Diacritics',
  8: 'Duplication',
  9: 'False Friend',
  10: 'Grammatical Register',
  11: 'Hyphenation',
  12: 'Inconsistency',
  13: 'Lexical Register',
  14: 'Lexical Selection',
  15: 'Named Entity',
  16: 'Number',
  17: 'Omitted Auxiliary Verb',
  18: 'Omitted Conjunction',
  19: 'Omitted Determiner',
  20: 'Omitted Preposition',
  21: 'Omitted Pronoun',
  22: 'Orthography',
  23: 'Other POS Omitted',
  24: 'Over-translation',
  25: 'Overly Literal',
  26: 'POS',
  27: 'Punctuation',
  28: "Shouldn't Have Been Translated",
  29: "Shouldn't have been translated",
  30: 'Spelling',
  31: 'Tense/Mood/Aspect',
  32: 'Under-translation',
  33: 'Unidiomatic',
  34: 'Unintelligible',
  35: 'Unit Conversion',
  36: 'Untranslated',
  37: 'Whitespace',
  38: 'Word Order',
  39: 'Wrong Auxiliary Verb',
  40: 'Wrong Conjunction',
  41: 'Wrong Determiner',
  42: 'Wrong Language Variety',
  43: 'Wrong Preposition',
  44: 'Wrong Pronoun'
}
```

### Data Splits

The dataset contains 1,448 documents for training, 200 documents for validation and 180 for (blind) test (all English-French).

## Dataset Creation

### Curation Rationale

The data is dervied from the [Amazon Product Reviews dataset](http://jmcauley.ucsd.edu/data/amazon/).

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