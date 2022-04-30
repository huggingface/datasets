---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id:
- mr
size_categories:
- 1K<n<10K
source_datasets:
- original
pretty_name: MR Movie Reviews
---

# Dataset Card for mr_polarity

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://www.cs.cornell.edu/people/pabo/movie-review-data/
- **Repository:** [Needs More Information]
- **Paper:** https://arxiv.org/abs/cs/0506075
- **Leaderboard:** https://paperswithcode.com/sota/sentiment-analysis-on-mr
- **Point of Contact:** [Needs More Information]

### Dataset Summary

MR Movie Reviews is a dataset for use in sentiment-analysis experiments. Note that this dataset contains the labeled sentences, not the labeled reviews. 

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English

## Dataset Structure

### Data Instances

{
    'label': 1,
    'text': "director robert zemekis must be given an equal amount of praise for overseeing the entire production, which included hundreds of animators. "
}

### Data Fields

- `text`: A sentence from a movie review.
- `label`: Sentiment; 0 = negative, 1 = positive

### Data Splits

The original dataset was not divided into splits, therefore we are only providing a 'train' split which contains 5331 positive and 5331 negative examples.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```
@inproceedings{Pang+Lee:05a,
   author = {Bo Pang and Lillian Lee},
   title = {Seeing stars: Exploiting class relationships for sentiment categorization with respect to rating scales},
   year = {2005},
   pages = {115--124},
   booktitle = {Proceedings of ACL}
}
```

### Contributions

Thanks to [@mo6zes](https://github.com/mo6zes/) for this dataset.


