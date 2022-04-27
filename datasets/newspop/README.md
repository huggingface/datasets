---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- cc-by-4
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-scoring
- text-classification-other-social-media-shares-prediction
paperswithcode_id: null
pretty_name: News Popularity in Multiple Social Media Platforms
---

# Dataset Card for News Popularity in Multiple Social Media Platforms

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

- **Homepage:** [UCI](https://archive.ics.uci.edu/ml/datasets/News+Popularity+in+Multiple+Social+Media+Platforms)
- **Repository:**
- **Paper:** [Arxiv](https://arxiv.org/abs/1801.07055)
- **Leaderboard:** [Kaggle](https://www.kaggle.com/nikhiljohnk/news-popularity-in-multiple-social-media-platforms/code)
- **Point of Contact:**

### Dataset Summary

Social sharing data across Facebook, Google+ and LinkedIn for 100k news items on the topics of: economy, microsoft, obama and palestine.

### Supported Tasks and Leaderboards

Popularity prediction/shares prediction

### Languages

English

## Dataset Structure

### Data Instances

```
{ "id": 35873,
  "title": "Microsoft's 'teen girl' AI turns into a Hitler-loving sex robot within 24 ...",
  "headline": "Developers at Microsoft created 'Tay', an AI modelled to speak 'like a teen girl', in order to improve the customer service on their voice",
  "source": "Telegraph.co.uk",
  "topic": "microsoft",
  "publish_date": "2016-03-24 09:53:54",
  "facebook": 22346,
  "google_plus": 973,
  "linked_in": 1009
}
```

### Data Fields

- id: the sentence id in the source dataset
- title: the title of the link as shared on social media
- headline: the headline, or sometimes the lede of the story
- source: the source news site
- topic: the topic: one of "economy", "microsoft", "obama" and "palestine"
- publish_date: the date the original article was published
- facebook: the number of Facebook shares, or -1 if this data wasn't collected
- google_plus: the number of Google+ likes, or -1 if this data wasn't collected
- linked_in: the number of LinkedIn shares, or -1 if if this data wasn't collected

### Data Splits

None

## Dataset Creation

### Curation Rationale

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

The source headlines were by journalists, while the titles were written by the
people sharing it on social media.

### Annotations

#### Annotation process

The 'annotations' are simply the number of shares, or likes in the case of
Google+ as collected from various API endpoints.

#### Who are the annotators?

Social media users.

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

License: Creative Commons Attribution 4.0 International License (CC-BY)

### Citation Information

```
@article{Moniz2018MultiSourceSF,
  title={Multi-Source Social Feedback of Online News Feeds},
  author={N. Moniz and L. Torgo},
  journal={ArXiv},
  year={2018},
  volume={abs/1801.07055}
}
```

### Contributions

Thanks to [@frankier](https://github.com/frankier) for adding this dataset.
