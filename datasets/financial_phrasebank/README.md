---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- cc-by-nc-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- sentiment-classification
paperswithcode_id: null
pretty_name: FinancialPhrasebank
---

# Dataset Card for financial_phrasebank

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

- **Homepage:** [Kaggle](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news) [ResearchGate](https://www.researchgate.net/publication/251231364_FinancialPhraseBank-v10)
- **Repository:**
- **Paper:** [Arxiv](https://arxiv.org/abs/1307.5336)
- **Leaderboard:** [Kaggle](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news/code) [PapersWithCode](https://paperswithcode.com/sota/sentiment-analysis-on-financial-phrasebank) =
- **Point of Contact:** [Pekka Malo](mailto:pekka.malo@aalto.fi) [Ankur Sinha](mailto:ankur.sinha@aalto.fi)

### Dataset Summary

Polar sentiment dataset of sentences from financial news. The dataset consists of 4840 sentences from English language financial news categorised by sentiment. The dataset is divided by agreement rate of 5-8 annotators.

### Supported Tasks and Leaderboards

Sentiment Classification

### Languages

English

## Dataset Structure

### Data Instances

```
{ "sentence": "Pharmaceuticals group Orion Corp reported a fall in its third-quarter earnings that were hit by larger expenditures on R&D and marketing .",
  "label": "negative"
}
```

### Data Fields

- sentence: a tokenized line from the dataset
- label: a label corresponding to the class as a string: 'positive', 'negative' or 'neutral'

### Data Splits
There's no train/validation/test split.

However the dataset is available in four possible configurations depending on the percentage of agreement of annotators:

`sentences_50agree`; Number of instances with >=50% annotator agreement: 4846 
`sentences_66agree`: Number of instances with >=66% annotator agreement: 4217
`sentences_75agree`: Number of instances with >=75% annotator agreement: 3453
`sentences_allagree`: Number of instances with 100% annotator agreement: 2264

## Dataset Creation

### Curation Rationale

The key arguments for the low utilization of statistical techniques in
financial sentiment analysis have been the difficulty of implementation for
practical applications and the lack of high quality training data for building
such models. Especially in the case of finance and economic texts, annotated
collections are a scarce resource and many are reserved for proprietary use
only. To resolve the missing training data problem, we present a collection of
∼ 5000 sentences to establish human-annotated standards for benchmarking
alternative modeling techniques. 

The objective of the phrase level annotation task was to classify each example
sentence into a positive, negative or neutral category by considering only the
information explicitly available in the given sentence. Since the study is
focused only on financial and economic domains, the annotators were asked to
consider the sentences from the view point of an investor only; i.e. whether
the news may have positive, negative or neutral influence on the stock price.
As a result, sentences which have a sentiment that is not relevant from an
economic or financial perspective are considered neutral.

### Source Data

#### Initial Data Collection and Normalization

The corpus used in this paper is made out of English news on all listed
companies in OMX Helsinki. The news has been downloaded from the LexisNexis
database using an automated web scraper. Out of this news database, a random
subset of 10,000 articles was selected to obtain good coverage across small and
large companies, companies in different industries, as well as different news
sources. Following the approach taken by Maks and Vossen (2010), we excluded
all sentences which did not contain any of the lexicon entities. This reduced
the overall sample to 53,400 sentences, where each has at least one or more
recognized lexicon entity. The sentences were then classified according to the
types of entity sequences detected. Finally, a random sample of ∼5000 sentences
was chosen to represent the overall news database.

#### Who are the source language producers?

The source data was written by various financial journalists.

### Annotations

#### Annotation process

This release of the financial phrase bank covers a collection of 4840
sentences. The selected collection of phrases was annotated by 16 people with
adequate background knowledge on financial markets.

Given the large number of overlapping annotations (5 to 8 annotations per
sentence), there are several ways to define a majority vote based gold
standard. To provide an objective comparison, we have formed 4 alternative
reference datasets based on the strength of majority agreement: 

#### Who are the annotators?

Three of the annotators were researchers and the remaining 13 annotators were
master's students at Aalto University School of Business with majors primarily
in finance, accounting, and economics.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

All annotators were from the same institution and so interannotator agreement
should be understood with this taken into account.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/.

If you are interested in commercial use of the data, please contact the following authors for an appropriate license:
- [Pekka Malo](mailto:pekka.malo@aalto.fi)
- [Ankur Sinha](mailto:ankur.sinha@aalto.fi)

### Citation Information

```
@article{Malo2014GoodDO,
  title={Good debt or bad debt: Detecting semantic orientations in economic texts},
  author={P. Malo and A. Sinha and P. Korhonen and J. Wallenius and P. Takala},
  journal={Journal of the Association for Information Science and Technology},
  year={2014},
  volume={65}
}
```

### Contributions

Thanks to [@frankier](https://github.com/frankier) for adding this dataset.
