---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- de
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-from-One-Million-Posts-Corpus
task_categories:
- text-classification
task_ids:
- topic-classification
paperswithcode_id: null
---

# Dataset Card for 10k German News Articles Datasets

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

- **Homepage: [10k German News Article Dataset](https://tblock.github.io/10kGNAD/)**
- **Repository: [10k German News Article Dataset](https://github.com/tblock/10kGNAD)()**
- **Point of Contact: [Steven Liu](stevhliu@gmail.com)**

### Dataset Summary

The 10k German News Article Dataset consists of 10273 German language news articles from the online Austrian 
newspaper website DER Standard. Each news article has been classified into one of 9 categories by professional
forum moderators employed by the newspaper. This dataset is extended from the original
[One Million Posts Corpus](https://ofai.github.io/million-post-corpus/). The dataset was created to support
topic classification in German because a classifier effective on a English dataset may not be as effective on
a German dataset due to higher inflections and longer compound words. Additionally, this dataset can be used
as a benchmark dataset for German topic classification.

### Supported Tasks and Leaderboards

This dataset can be used to train a model, like [BERT](https://huggingface.co/bert-base-uncased) for `topic classification` on German news articles. There are 9 possible categories.

### Languages

The text is in German and it comes from an online Austrian newspaper website. The BCP-47 code for German is
`de-DE`.

## Dataset Structure

### Data Instances

An example data instance contains a German news article (title and article are concatenated) and it's corresponding topic category.

```
{'text': ''Die Gewerkschaft GPA-djp lanciert den "All-in-Rechner" und findet, dass die Vertragsform auf die Führungsebene beschränkt gehört. Wien – Die Gewerkschaft GPA-djp sieht Handlungsbedarf bei sogenannten All-in-Verträgen.'
'label': 'Wirtschaft'
}
```

### Data Fields

* `text`: contains the title and content of the article
* `label`: can be one of 9 possible topic categories (`Web`, `Panorama`, `International`, `Wirtschaft`, `Sport`, `Inland`, `Etat`, `Wissenschaft`, `Kultur`)

### Data Splits

The data is split into a training set consisting of 9245 articles and a test set consisting of 1028 articles.

## Dataset Creation

### Curation Rationale

The dataset was created to support topic classification in the German language. English text classification datasets are common ([AG News](https://huggingface.co/datasets/ag_news) and [20 Newsgroup](https://huggingface.co/datasets/newsgroup)), but German datasets are less common. A classifier trained on an English dataset may not work as well on a set of German text due to grammatical differences. Thus there is a need for a German dataset for effectively assessing model performance.

### Source Data

#### Initial Data Collection and Normalization

The 10k German News Article Dataset is extended from the One Million Posts Corpus. 10273 German news articles were collected from this larger corpus. In the One Million Posts Corpus, each article has a topic path like
`Newsroom/Wirtschaft/Wirtschaftpolitik/Finanzmaerkte/Griechenlandkrise`. The 10kGNAD uses the second part of the topic path as the topic label. Article title and texts are concatenated into one text and author names are removed to avoid keyword classification on authors who write frequently on a particular topic.

#### Who are the source language producers?

The language producers are the authors of the Austrian newspaper website DER Standard.

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

This dataset was curated by Timo Block.

### Licensing Information

This dataset is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license.

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@stevhliu](https://github.com/stevhliu) for adding this dataset.