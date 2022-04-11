---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- en
licenses:
- cc0-1.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-retrieval
task_ids:
- document-retrieval
- explanation-generation
- fact-checking-retrieval
- other-structured-to-text
- text-simplification
paperswithcode_id: null
pretty_name: Times of India News Headlines
---

# Dataset Card for Times of India News Headlines

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

- **Homepage:** https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/J7BYRX
- **Repository:** [More Information Needed]
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

This news dataset is a persistent historical archive of noteable events in the Indian subcontinent from start-2001 to mid-2020, recorded in realtime by the journalists of India. It contains approximately 3.3 million events published by Times of India. Times Group as a news agency, reaches out a very wide audience across Asia and drawfs every other agency in the quantity of english articles published per day. Due to the heavy daily volume over multiple years, this data offers a deep insight into Indian society, its priorities, events, issues and talking points and how they have unfolded over time. It is possible to chop this dataset into a smaller piece for a more focused analysis, based on one or more facets.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

```
 {
    'publish_date':  '20010530',
    'headline_category': city.kolkata,
    'headline_text': "Malda fake notes"
 }
```

### Data Fields

- `publish_date`: Date of publishing in yyyyMMdd format
- `headline_category`: Category of event in ascii, dot-delimited values
- `headline_text`: Headline of article en la Engrezi (2020-07-10)

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

The dataset was created by Rohit Kulkarni.  

### Licensing Information

The data is under the [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)

### Citation Information

```
@data{DVN/DPQMQH_2020,
author = {Kulkarni, Rohit},
publisher = {Harvard Dataverse},
title = {{Times of India News Headlines}},
year = {2020},
version = {V1},
doi = {10.7910/DVN/DPQMQH},
url = {https://doi.org/10.7910/DVN/DPQMQH}
}
```
### Contributions

Thanks to [@tanmoyio](https://github.com/tanmoyio) for adding this dataset.