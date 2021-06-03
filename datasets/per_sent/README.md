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
paperswithcode_id: persent
---

# Dataset Card for PerSenT

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

- **Homepage:** [PerSenT](https://stonybrooknlp.github.io/PerSenT/)
- **Repository:** [https://github.com/MHDBST/PerSenT](https://github.com/MHDBST/PerSenT)
- **Paper:** [arXiv](https://arxiv.org/abs/2011.06128)
- **Leaderboard:** NA
- **Point of Contact:** [Mohaddeseh Bastan](mbastan@cs.stonybrook.edu)

### Dataset Summary

PerSenT is a crowd-sourced dataset that captures the sentiment of an author towards the main entity in a news article. This dataset contains annotations for 5.3k documents and 38k paragraphs covering 3.2k unique entities.  For each article, annotators judge what the author’s sentiment is towards the main
(target) entity of the article. The annotations also include similar judgments on paragraphs within the article.

### Supported Tasks and Leaderboards

Sentiment Classification: Each document consists of multiple paragraphs.  Each paragraph is labeled separately (Positive, Neutral, Negative) and the author’s sentiment towards the whole document is included as a document-level label.

### Languages

English

## Dataset Structure

### Data Instances

```json
{'DOCUMENT': "Germany's Landesbank Baden Wuertemberg won EU approval Tuesday for a state bailout after it promised to shrink its balance sheet by 40 percent and refocus on lending to companies.\n The bank was several state-owned German institutions to run into trouble last year after it ran up more huge losses from investing in high-risk proprietary trading and capital market activities -- a business the EU has now told it to shun.\n Seven current and former managers of the bank are also being investigated by German authorities for risking or damaging the bank's capital by carrying out or failing to block investments in high-risk deals worth hundreds of millions from 2006.\n The European Commission said its Tuesday approval for the state rescue of the bank and its new restructuring plan would allow it become a viable business again -- and that the cutbacks would help limit the unfair advantage over rivals that the bank would get from the state aid.\n Stuttgart-based LBBW earlier this year received a capital injection of (EURO)5 billion from the bank's shareholders  all of them public authorities or state-owned  including the state of Baden-Wuerttemberg  the region's savings bank association and the city of Stuttgart.",
 'DOCUMENT_INDEX': 1,
 'MASKED_DOCUMENT': "[TGT] won EU approval Tuesday for a state bailout after it promised to shrink its balance sheet by 40 percent and refocus on lending to companies.\n [TGT] was several state-owned German institutions to run into trouble last year after [TGT] ran up more huge losses from investing in high-risk proprietary trading and capital market activities -- a business the EU has now told it to shun.\n Seven current and former managers of [TGT] are also being investigated by German authorities for risking or damaging [TGT]'s capital by carrying out or failing to block investments in high-risk deals worth hundreds of millions from 2006.\n The European Commission said its Tuesday approval for the state rescue of [TGT] and its new restructuring plan would allow it become a viable business again -- and that the cutbacks would help limit the unfair advantage over rivals that [TGT] would get from the state aid.\n Stuttgart-based LBBW earlier this year received a capital injection of (EURO)5 billion from [TGT]'s shareholders  all of them public authorities or state-owned  including the state of Baden-Wuerttemberg  the region's savings bank association and the city of Stuttgart.",
 'Paragraph0': 2,
 'Paragraph1': 0,
 'Paragraph10': -1,
 'Paragraph11': -1,
 'Paragraph12': -1,
 'Paragraph13': -1,
 'Paragraph14': -1,
 'Paragraph15': -1,
 'Paragraph2': 0,
 'Paragraph3': 1,
 'Paragraph4': 1,
 'Paragraph5': -1,
 'Paragraph6': -1,
 'Paragraph7': -1,
 'Paragraph8': -1,
 'Paragraph9': -1,
 'TARGET_ENTITY': 'Landesbank Baden Wuertemberg',
 'TITLE': 'German bank LBBW wins EU bailout approval',
 'TRUE_SENTIMENT': 0}
```

### Data Fields

- DOCUMENT_INDEX: ID of the document per original dataset
- TITLE: Title of the article
- DOCUMENT: Text of the article
- MASKED_DOCUMENT: Text of the article with the target entity masked with `[TGT]` token
- TARGET_ENTITY: The entity that the author is expressing opinion about
- TRUE_SENTIMENT: Label for entire article
- Paragraph{0..15}: Label for each paragraph in the article

**Note**: Labels are one of `[Negative, Neutral, Positive]`.  Missing labels were replaced with `-1`.

### Data Splits

To split the dataset, entities were split into 4 mutually exclusive sets. Due to the nature of news collections, some entities tend to dominate the collection. In the collection, there were four entities which were the main entity in nearly 800 articles. To avoid these entities from dominating the train or test splits, these were moved them to a separate test collection. The remaining was split into a training, dev, and test sets at random. Thus the collection includes one standard test set consisting of articles drawn at random (Test Standard), while the other is a test set which contains multiple articles about a small number of popular entities (Test Frequent).

## Dataset Creation

### Curation Rationale

[More Information Needed]

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

#### Who are the annotators?

[More Information Needed]

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

### Dataset Curators

[More Information Needed]

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

### Contributions

Thanks to [@jeromeku](https://github.com/jeromeku) for adding this dataset.