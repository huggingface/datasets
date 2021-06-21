---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: hate-speech
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

- **Homepage:** https://github.com/Vicomtech/hate-speech-dataset
- **Repository:** https://github.com/Vicomtech/hate-speech-dataset
- **Paper:** https://www.aclweb.org/anthology/W18-51.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

These files contain text extracted from Stormfront, a white supremacist forum. A random set of forums posts have been sampled from 
several subforums and split into sentences. Those sentences have been manually labelled as containing hate speech or not, according 
to certain annotation guidelines.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- text: the provided sentence
- user_id: information to make it possible to re-build the conversations these sentences belong to
- subforum_id: information to make it possible to re-build the conversations these sentences belong to
- num_contexts: number of previous posts the annotator had to read before making a decision over the category of the sentence
- label: hate, noHate, relation (sentence in the post doesn't contain hate speech on their own, but combination of serveral sentences does) 
         or idk/skip (sentences that are not written in English or that don't contain information as to be classified into hate or noHate)

### Data Splits

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

[More Information Needed]

### Citation Information

```
@inproceedings{gibert2018hate,
    title = "{Hate Speech Dataset from a White Supremacy Forum}",
    author = "de Gibert, Ona  and
      Perez, Naiara  and
      Garc{\'\i}a-Pablos, Aitor  and
      Cuadros, Montse",
    booktitle = "Proceedings of the 2nd Workshop on Abusive Language Online ({ALW}2)",
    month = oct,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-5102",
    doi = "10.18653/v1/W18-5102",
    pages = "11--20",
}
```

### Contributions

Thanks to [@czabo](https://github.com/czabo) for adding this dataset.