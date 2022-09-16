---
annotations_creators:
- crowdsourced
language_creators:
- expert-generated
language:
- en
license:
- apache-2.0
multilinguality:
- monolingual
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-headline-grouping
size_categories:
- 10K<n<100K
pretty_name: Headline Grouping (HLGD)
---

# Dataset Card for Headline Grouping (HLGD)

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

- **Homepage:** [https://github.com/tingofurro/headline_grouping](https://github.com/tingofurro/headline_grouping)
- **Repository:** [https://github.com/tingofurro/headline_grouping](https://github.com/tingofurro/headline_grouping)
- **Paper:** [https://people.eecs.berkeley.edu/~phillab/pdfs/NAACL2021_HLG.pdf](https://people.eecs.berkeley.edu/~phillab/pdfs/NAACL2021_HLG.pdf)
- **Leaderboard:** N/A
- **Point of Contact:** phillab (at) berkeley (dot) edu

### Dataset Summary

HLGD is a binary classification dataset consisting of 20,056 labeled news headlines pairs indicating whether the two headlines describe the same underlying world event or not. The dataset comes with an existing split between `train`, `validation` and `test` (60-20-20).

### Supported Tasks and Leaderboards

The paper (NAACL2021) introducing HLGD proposes three challenges making use of various amounts of data:
- Challenge 1: Headline-only. Models must make predictions using only the text of both headlines.
- Challenge 2: Headline + Time. Models must make predictions using the headline and publication date of the two headlines.
- Challenge 3: Headline + Time + Other. Models can make predictions using the headline, publication date as well as any other relevant meta-data that can be obtained through the URL attached to the headline (full article content, authors, news source, etc.)

### Languages

Dataset is in english.

## Dataset Structure

### Data Instances

A typical dataset consists of a timeline_id, two headlines (A/B), each associated with a URL, and a date. Finally, a label indicates whether the two headlines describe the same underlying event (1) or not (0). Below is an example from the training set:
```
{'timeline_id': 4,
 'headline_a': 'France fines Google nearly $57 million for first major violation of new European privacy regime',
 'headline_b': "France hits Google with record EUR50mn fine over 'forced consent' data collection",
 'date_a': '2019-01-21',
 'date_b': '2019-01-21',
 'url_a': 'https://www.chicagotribune.com/business/ct-biz-france-fines-google-privacy-20190121-story.html',
 'url_b': 'https://www.rt.com/news/449369-france-hits-google-with-record-fine/',
 'label': 1}
```

### Data Fields

- `timeline_id`: Represents the id of the timeline that the headline pair belongs to (values 0 to 9). The dev set is composed of timelines 0 and 5, and the test set timelines 7 and 8
- `headline_a`, `headline_b`: Raw text for the headline pair being compared
- `date_a`, `date_b`: Publication date of the respective headlines, in the `YYYY-MM-DD` format
- `url_a`, `url_b`: Original URL of the respective headlines. Can be used to retrieve additional meta-data on the headline.
- `label`: 1 if the two headlines are part of the the same headline group and describe the same underlying event, 0 otherwise.

### Data Splits

|                             | Train   | Dev    | Test  |
| --------------------------- | ------- | ------ | ----- |
| Number of  examples         | 15,492  |  2,069 | 2,495 |

## Dataset Creation

### Curation Rationale

The task of grouping headlines from diverse news sources discussing a same underlying event is important to enable interfaces that can present the diversity of coverage of unfolding news events. Many news aggregators (such as Google or Yahoo news) present several sources for a given event, with an objective to highlight coverage diversity.
Automatic grouping of news headlines and articles remains challenging as headlines are short, heavily-stylized texts.
The HeadLine Grouping Dataset introduces the first benchmark to evaluate NLU model's ability to group headlines according to the underlying event they describe.


### Source Data

#### Initial Data Collection and Normalization

The data was obtained by collecting 10 news timelines from the NewsLens project by selecting timelines diversified in topic each contained between 80 and 300 news articles.

#### Who are the source language producers?

The source language producers are journalists or members of the newsroom of 34 news organizations listed in the paper.

### Annotations

#### Annotation process

Each timeline was annotated for group IDs by 5 independent annotators. The 5 annotations were merged into a single annotation named the global groups.
The global group IDs are then used to generate all pairs of headlines within timelines with binary labels: 1 if two headlines are part of the same global group, and 0 otherwise. A heuristic is used to remove negative examples to obtain a final dataset that has class imbalance of 1 positive example to 5 negative examples.

#### Who are the annotators?

Annotators were authors of the papers and 8 crowd-workers on the Upwork platform. The crowd-workers were native English speakers with experience either in proof-reading or data-entry.

### Personal and Sensitive Information

Annotators identity has been anonymized. Due to the public nature of news headline, it is not expected that the headlines will contain personal sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to facilitate applications that present diverse news coverage.

By simplifying the process of developing models that can group headlines that describe a common event, we hope the community can build applications that show news readers diverse sources covering similar events.

We note however that the annotations were performed in majority by crowd-workers and that even though inter-annotator agreement was high, it was not perfect. Bias of the annotators therefore remains in the dataset.

### Discussion of Biases

There are several sources of bias in the dataset:
- Annotator bias: 10 annotators participated in the creation of the dataset. Their opinions and perspectives influenced the creation of the dataset.
- Subject matter bias: HLGD consists of headlines from 10 news timelines from diverse topics (space, tech, politics, etc.). This choice has an impact on the types of positive and negative examples that appear in the dataset.
- Source selection bias: 33 English-language news sources are represented in the dataset. This selection of news sources has an effect on the content in the timeline, and the overall dataset.
- Time-range of the timelines: the timelines selected range from 2010 to 2020, which has an influence on the language and style of news headlines.

### Other Known Limitations

For the task of Headline Grouping, inter-annotator agreement is high (0.814) but not perfect. Some decisions for headline grouping are subjective and depend on interpretation of the reader.

## Additional Information

### Dataset Curators

The dataset was initially created by Philippe Laban, Lucas Bandarkar and Marti Hearst at UC Berkeley.

### Licensing Information

The licensing status of the dataset depends on the legal status of news headlines. It is commonly held that News Headlines fall under "fair-use" ([American Bar blog post](https://www.americanbar.org/groups/gpsolo/publications/gp_solo/2011/september/fair_use_news_reviews/))
The dataset only distributes headlines, a URL and a publication date. Users of the dataset can then retrieve additional information (such as the body content, author, etc.) directly by querying the URL.

### Citation Information

```
@inproceedings{Laban2021NewsHG,
  title={News Headline Grouping as a Challenging NLU Task},
  author={Laban, Philippe and Bandarkar, Lucas and Hearst, Marti A},
  booktitle={NAACL 2021},
  publisher = {Association for Computational Linguistics},
  year={2021}
}
```

### Contributions

Thanks to [@tingofurro](https://github.com/<tingofurro>) for adding this dataset.
