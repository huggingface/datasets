---
annotations_creators:
  identification:
  - expert-generated
  - machine-generated
  resolution:
  - crowdsourced
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  identification:
  - 100K<n<1M
  resolution:
  - 1K<n<10K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- structure-prediction-other-fused-head-identification
paperswithcode_id: numeric-fused-head
---

# Dataset Card for Numeric Fused Heads

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

- **Homepage:** [The Numeric Fused-Head demo](https://nlp.biu.ac.il/~lazary/fh/)
- **Repository:** [Github Repo](https://github.com/yanaiela/num_fh)
- **Paper:** [Where’s My Head? Definition, Dataset and Models for Numeric Fused-Heads Identification and Resolution](https://www.mitpressjournals.org/doi/full/10.1162/tacl_a_00280)
- **Leaderboard:** [NLP Progress](http://nlpprogress.com/english/missing_elements.html)
- **Point of Contact:** [Yanai Elazar](https://yanaiela.github.io), [Yoav Goldberg](https://www.cs.bgu.ac.il/~yoavg/uni/)

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

- Numeric Fused Head Identification
- Numeric Fused Head Resolution

### Languages

English

## Dataset Structure

### Data Instances

## Identification

```
{
    "tokens": ["It", "’s", "a", "curious", "thing", ",", "the", "death", "of", "a", "loved", "one", "."]
    "start_index": 11
    "end_index": 12
    "label": 1
}
```

## Resolution

```
{
    "tokens": ["I", "'m", "eighty", "tomorrow", ".", "Are", "you", "sure", "?"],
    "line_indices": [0, 0, 0, 0, 0, 1, 1, 1, 1],
    "head": ["AGE"],
    "speakers": ["John Doe", "John Doe", "John Doe", "John Doe", "John Doe", "Joe Bloggs", "Joe Bloggs", "Joe Bloggs", "Joe Bloggs"],
    "anchors_indices": [2]
}
```

### Data Fields

## Identification

- `tokens` - List of token strings as tokenized with [Spacy](spacy.io).
- `start_index` - Start index of the anchor.
- `end_index` - End index of the anchor.
- `label` - "pos" or "neg" depending on whether this example contains a numeric fused head.

## Resolution

- `tokens` - List of token strings as tokenized with [Spacy](spacy.io)
- `line_indices` - List of indices indicating line number (one for each token)
- `head` -  Reference to the missing head. If the head exists elsewhere in the sentence this is given as a token index.
- `speakers` - List of speaker names (one for each token)
- `anchors_indices` - Index to indicate which token is the anchor (the visible number)

### Data Splits

Train, Test, Dev

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

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

MIT License

### Citation Information
```
@article{doi:10.1162/tacl\_a\_00280,
    author = {Elazar, Yanai and Goldberg, Yoav},
    title = {Where’s My Head? Definition, Data Set, and Models for Numeric Fused-Head Identification and Resolution},
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {7},
    number = {},
    pages = {519-535},
    year = {2019},
    doi = {10.1162/tacl\_a\_00280},
}
```

### Contributions

Thanks to [@ghomasHudson](https://github.com/ghomasHudson) for adding this dataset.