---
annotations_creators:
- expert-generated
  language_creators:
- expert-generated
  languages:
- en
  licenses:
- cc-by-nc-4.0
  multilinguality:
- monolingual
  size_categories:
- n<1K
  source_datasets:
- original
  task_categories:
- question-answering
  task_ids:
- open-domain-qa
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Dataset Card for [Dataset Name]](#dataset-card-for-dataset-name)
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

- **Homepage:** https://github.com/aviaefrat/cryptonite
- **Repository:** https://github.com/aviaefrat/cryptonite
- **Paper:** https://arxiv.org/pdf/2103.01242.pdf
- **Leaderboard:**
- **Point of Contact:** https://twitter.com/AviaEfrat

### Dataset Summary

Current NLP datasets targeting ambiguity can be solved by a native speaker with relative ease. We present Cryptonite, a large-scale dataset based on cryptic crosswords, which is both linguistically complex and naturally sourced. Each example in Cryptonite is a cryptic clue, a short phrase or sentence with a misleading surface reading, whose solving requires disambiguating semantic, syntactic, and phonetic wordplays, as well as world knowledge. Cryptic clues pose a challenge even for experienced solvers, though top-tier experts can solve them with almost 100% accuracy. Cryptonite is a challenging task for current models; fine-tuning T5-Large on 470k cryptic clues achieves only 7.6% accuracy, on par with the accuracy of a rule-based clue solver (8.6%).

### Languages

English

## Dataset Structure

### Data Instances

This is one example from the train set.

```json
{
  "url": "https://puzzles.telegraph.co.uk/puzzle?puzzle_id=6419",
  "publisher": "Telegraph",
  "crossword_id": 6419,
  "date": 1229126400000,
  "title": "CROSSWORD NO: 25,799",
  "author": null,
  "setter": null,
  "number": 3,
  "orientation": "down",
  "clue": "ski-slope in poor condition (3,4)",
  "answer": "run down",
  "demarcation": null,
  "enumeration": "(3,4)",
  "length": null,
  "quick": false,
  "sub_publisher": null
}
```

### Data Fields

```python
{
    "clue": datasets.Value("string"),
    "answer": datasets.Value("string"),
    "enumeration": datasets.Value("string"),
    "publisher": datasets.Value("string"),
    "date": datasets.Value("int64"),
    "quick": datasets.Value("bool"),
    "id": datasets.Value("string")
}
```


### Data Splits

Train, val, test.

## Dataset Creation

### Curation Rationale

Crosswords from the Times and the Telegraph.

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

Avia Efrat, Uri Shaham, Dan Kilman, Omer Levy

### Licensing Information

`cc-by-nc-4.0`

### Citation Information

```
@misc{efrat2021cryptonite,
      title={Cryptonite: A Cryptic Crossword Benchmark for Extreme Ambiguity in Language}, 
      author={Avia Efrat and Uri Shaham and Dan Kilman and Omer Levy},
      year={2021},
      eprint={2103.01242},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


### Contributions

Thanks to [@theo-m](https://github.com/theo-m) for adding this dataset.
