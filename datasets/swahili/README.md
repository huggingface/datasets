---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- sw
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7339006/**
- **Repository: NA**
- **Paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7339006/**
- **Leaderboard: [More Information Needed]**
- **Point of Contact: [More Information Needed]**

### Dataset Summary

The Swahili dataset developed specifically for language modeling task.
The dataset contains 28,000 unique words with 6.84M, 970k, and 2M words for the train,
valid and test partitions respectively which represent the ratio 80:10:10.
The entire dataset is lowercased, has no punctuation marks and,
the start and end of sentence markers have been incorporated to facilitate easy tokenization during language modeling.

### Supported Tasks and Leaderboards

Language Modeling

### Languages

Swahili (sw)

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- text : A line of text in Swahili

### Data Splits

train = 80%, valid = 10%, test = 10%

## Dataset Creation

### Curation Rationale

Enhancing African low-resource languages

### Source Data

#### Initial Data Collection and Normalization

The dataset contains 28,000 unique words with 6.84 M, 970k, and 2 M words for the train, valid and test partitions respectively which represent the ratio 80:10:10. 
The entire dataset is lowercased, has no punctuation marks and, the start and end of sentence markers have been incorporated to facilitate easy tokenization during language modelling.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Unannotated data

#### Who are the annotators?

NA

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

Enhancing African low-resource languages

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

Creative Commons Attribution 4.0 International

### Citation Information

"""\
@InProceedings{huggingface:dataset,
title = Language modeling data for Swahili (Version 1),
authors={Shivachi Casper Shikali, & Mokhosi Refuoe.
},
year={2019},
link = http://doi.org/10.5281/zenodo.3553423
}
"""

### Contributions

Thanks to [@akshayb7](https://github.com/akshayb7) for adding this dataset.