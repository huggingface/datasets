---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-MPQA-KBP Challenge-MediaRank
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for PerSenT

## Table of Contents
- [Dataset Card for [PerSenT]](#dataset-card-for-dataset-name)
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

## Dataset Description

- **Homepage:** [PerSenT](https://stonybrooknlp.github.io/PerSenT/)
- **Repository:** [https://github.com/MHDBST/PerSenT](https://github.com/MHDBST/PerSenT)
- **Paper:** [arXiv](https://arxiv.org/abs/2011.06128)
- **Leaderboard:** NA
- **Point of Contact:** [Mohaddeseh Bastan](mbastan@cs.stonybrook.edu)

### Dataset Summary

PerSenT is a crowd-sourced dataset that captures the sentiment of an author towards the main entity in a news article. This dataset contains annotation for 5.3k documents and 38k paragraphs covering 3.2k unique entities.  For each article, annotators judge what the author’s sentiment is towards the main
(target) entity of the article. The annotations also include similar judgments on paragraphs within the article.

### Supported Tasks and Leaderboards

Sentiment Classification: Each document consists of multiple paragraphs.  Each paragraph is labeled separately (Positive, Neutral, Negative) and the author’s sentiment towards the whole document is included as a document-level label.

### Languages

English

## Dataset Structure

### Data Instances

```json
  {
    "DOCUMENT_INDEX": {
      "feature_type": "Value",
      "dtype": "int64"
    },
    "TITLE": {
      "feature_type": "Value",
      "dtype": "string"
    },
    "TARGET_ENTITY": {
      "feature_type": "Value",
      "dtype": "string"
    },
    "DOCUMENT": {
      "feature_type": "Value",
      "dtype": "string"
    },
    "MASKED_DOCUMENT": {
      "feature_type": "Value",
      "dtype": "string"
    },
    "TRUE_SENTIMENT": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph0": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph1": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph2": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph3": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph4": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph5": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph6": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph7": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph8": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph9": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph10": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph11": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph12": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph13": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph14": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    },
    "Paragraph15": {
      "feature_type": "ClassLabel",
      "dtype": "int32",
      "class_names": [
        "",
        "Negative",
        "Neutral",
        "Positive"
      ]
    }
  }
```

### Data Splits

To split the dataset, entities were split into 4 mutually exclusive sets. Due to the nature of news collections, some entities tend to dominate the collection. In the collection, there were four entities which were the main entity in nearly 800 articles. To avoid these entities from dominating the train or test splits, these were moved them to a separate test collection. The remaining was split into a training, dev, and test sets at random. Thus the collection includes one standard test set consisting of articles drawn at random (Test Standard), while the other is a test set which contains multiple articles about a small number of popular entities (Test Frequent).

## Dataset Creation

### Source Data

#### Initial Data Collection and Normalization

Articles were selected from 3 sources:
1. MPQA (Deng and Wiebe, 2015; Wiebe et al., 2005): This dataset contains news articles manually annotated for opinions, beliefs, emotions, sentiments, speculations, etc. It also has target annotations which are entities and event anchored to the heads of noun or verb phrases. All decisions on this dataset are made on sentence-level and over short spans.
2. KBP Challenge (Ellis et al., 2014): This resource contains TAC 2014 KBP English sentiment slot filling challenge dataset. This is a document-level sentiment filling dataset. In this task, given an entity and a sentiment (positive/negative) from the document, the goal is to find entities toward which
the original entity holds the given sentimental view. We selected documents from this resource which have been used in the following similar work in sentiment analysis task (Choi et al., 2016).
3. Media Rank (Ye and Skiena, 2019): This dataset ranks about 50k news sources along different aspects. It is also used for classifying political ideology of news articles (Kulkarni et al., 2018).

Pre-processing steps:
- First we find all the person entities in each article, using Stanford NER (Name Entity Resolution) tagger (Finkel et al., 2005) and all mentions of them using co-reference resolution (Clark and Manning, 2016; Co, 2017). 
- We removed articles which are not likely to have a main entity of focus. We used a simple heuristic of removing articles in which the most frequent person entity is mentioned only three times or less (even when counting co-referent mentions).
- For the articles that remain we deemed the most frequent entity to be the main entity of the article. We also filtered out extremely long and extremely short articles to keep the articles which have at least 3 paragraphs and at most 16 paragraphs.

Documents are randomly separated into train, dev, and two test sets. We ensure that each entity appears in only one of the sets. Our goal here is to avoid easy to learn biases over entities. To avoid the most frequent entities from dominating the training or the test sets, we remove articles that covered the most frequent entities and use them as a separate test set (referred to as frequent test set) in addition to the randomly drawn standard test set.

### Annotations

#### Annotation process

We obtained document and paragraph level annotations with the help of Amazon Mechanical Turk workers. The workers first verified if the target entity we provide is indeed the main entity in the document. Then, they rated each paragraph in a document that contained a direct mention or a reference to the target
entity. Last, they rated the sentiment towards the entity based on the entire document. In both cases, the workers made assessments about the authors view based on what they said about the target entity. For both paragraph and document level sentiment, the workers chose from five rating categories: Negative,
Slightly Negative, Neutral, Slightly Positive, or Positive. We then combine the fine-grained annotations to obtain three coarse-grained classes Negative, Neutral, or Positive.

## Additional Information

### Licensing Information

[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
  @inproceedings{bastan2020authors,
        title={Author's Sentiment Prediction}, 
        author={Mohaddeseh Bastan and Mahnaz Koupaee and Youngseo Son and Richard Sicoli and Niranjan Balasubramanian},
        year={2020},
        eprint={2011.06128},
        archivePrefix={arXiv},
        primaryClass={cs.CL}
  }
```
