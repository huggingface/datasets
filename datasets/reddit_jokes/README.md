---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
- question-answering
- text-scoring
task_ids:
- explanation-generation
- machine-translation
- open-domain-qa
- other-stuctured-to-text
- sentiment-scoring
---

# Dataset Card for [Needs More Information]

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

- **Homepage:** https://github.com/taivop/joke-dataset
- **Repository:** https://github.com/taivop/joke-dataset
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [Taivo Pungas](taivo@pungas.ee)

### Dataset Summary

A jokes dataset contains 195k english plaintext jokes scraped from Reddit /r/jokes. Contains all submissions to the subreddit as of 13.02.2017. This dataset is a subset of "A dataset of English plaintext jokes." The main dataset contains 200k English plain text jokes but here only the reddit jokes has been taken.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in plain English.

## Dataset Structure

### Data Instances

```
{
        "body":  "Pizza doesn't scream when you put it in the oven .\n\nI'm so sorry.",
        "id":  "5tz4dd",
        "score":  0,
        "title":  "What's the difference between a Jew in Nazi Germany and pizza ?"
 }
```

### Data Fields

- `id`: submission ID in the subreddit.
- `score`: post score displayed on Reddit.
- `title`: title of the submission.
- `body`: reply on the submission.

### Data Splits

This dataset has no splits.

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

This dataset contains no annotation.

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

The dataset was created by Taivo Pungas

### Licensing Information

This dataset contains no license.

### Citation Information

```
@misc{pungas,
        title={A dataset of English plaintext jokes.},
        url={https://github.com/taivop/joke-dataset},
        author={Pungas, Taivo},
        year={2017},
        publisher = {GitHub},
        journal = {GitHub repository}
}
```