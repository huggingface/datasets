---
annotations_creators:
- found
language_creators:
- found
languages:
- sv
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
---

# Dataset Card for Swedish Reviews

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

- **Homepage:** [swedish_reviews homepage](https://github.com/timpal0l/swedish-sentiment)
- **Repository:** [swedish_reviews repository](https://github.com/timpal0l/swedish-sentiment)
- **Point of Contact:** [Tim Isbister](mailto:timisbisters@gmail.com)

### Dataset Summary

The dataset is scraped from various Swedish websites where reviews are present. The dataset consists of 103 482 samples split between `train`, `valid` and `test`. It is a sample of the full dataset, where this sample is balanced to the minority class (negative). The original data dump was heavly skewved to positive samples with a 95/5 ratio.  

### Supported Tasks and Leaderboards

This dataset can be used to evaluate sentiment classification on Swedish.

### Languages

The text in the dataset is in Swedish.

## Dataset Structure

### Data Instances

What a sample looks like:
```
{
 'text': 'Jag tycker huggingface är ett grymt project!',
 'label': 1,
}
```

### Data Fields

- `text`:  A text where the sentiment expression is present.
- `label`: a int representing the label `0`for negative and `1`for positive.

### Data Splits

The data is split into a training, validation and test set. The final split sizes are as follow:

| Train   | Valid  | Test  |
| ------  | -----  | ----  |
| 62089   |  20696 | 20697 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

Various Swedish websites with product reviews.

#### Initial Data Collection and Normalization

#### Who are the source language producers?

Swedish

### Annotations

[More Information Needed]

#### Annotation process

Automatically annotated based on user reviews on a scale 1-5, where 1-2 is considered `negative` and 4-5 is `positive`, 3 is skipped as it tends to be more neutral. 

#### Who are the annotators?

The users who have been using the products.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

[More Information Needed]

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

[More Information Needed]

### Dataset Curators

The corpus was scraped by @timpal0l

### Licensing Information

Research only.

### Citation Information

No paper exists currently.

### Contributions

Thanks to [@timpal0l](https://github.com/timpal0l) for adding this dataset.