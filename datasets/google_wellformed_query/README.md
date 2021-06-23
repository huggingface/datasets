---
task_categories:
- text-scoring
multilinguality:
- monolingual
task_ids:
- other
languages:
- en
annotations_creators:
- crowdsourced
source_datasets:
- extended
size_categories:
- 10K<n<100K
licenses:
- CC-BY-SA-4.0
paperswithcode_id: null
---

# Dataset Card Creation Guide

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

- **Homepage:** [GitHub](https://github.com/google-research-datasets/query-wellformedness)
- **Repository:** [GitHub](https://github.com/google-research-datasets/query-wellformedness)
- **Paper:** [ARXIV](https://arxiv.org/abs/1808.09419)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Google's query wellformedness dataset was created by crowdsourcing well-formedness annotations for 25,100 queries from the Paralex corpus. Every query was annotated by five raters each with 1/0 rating of whether or not the query is well-formed.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- `rating`: a `float` between 0-1
- `sentence`: query which you want to rate

### Data Splits

|                            | Train   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Input Sentences            |   17500     |   3750    |  3850    |

## Dataset Creation

### Curation Rationale

Understanding search queries is a hard problem as it involves dealing with “word salad” text ubiquitously issued by users. However, if a query resembles a well-formed question, a natural language processing pipeline is able to perform more accurate interpretation, thus reducing downstream compounding errors. Hence, identifying whether or not a query is well formed can enhance query understanding. This dataset introduce a new task of identifying a well-formed natural language question. 

### Source Data

Used the Paralex corpus (Fader et al., 2013) that contains pairs of noisy paraphrase questions. These questions were issued by users in WikiAnswers (a Question-Answer forum) and consist of both web-search query like constructs (“5 parts of chloroplast?”) and well-formed questions (“What is the punishment for grand theft?”).

#### Initial Data Collection and Normalization

Selected 25,100 queries from the unique list of queries extracted from the corpus such that no two queries in the selected set are paraphrases.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The queries are annotated into well-formed or non-wellformed questions if it satisfies the following:

1. Query is grammatical.
2. Query is an explicit question.
3. Query does not contain spelling errors.

#### Who are the annotators?

Every query was labeled by five different crowdworkers with a binary label indicating whether a query is well-formed or not. And average of the ratings of the five annotators was reported, to get the probability of a query being well-formed.

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

Query-wellformedness dataset is licensed under CC BY-SA 4.0. Any third party content or data is provided “As Is” without any warranty, express or implied.

### Citation Information

```
@InProceedings{FaruquiDas2018,
   title = {{Identifying Well-formed Natural Language Questions}},
   author = {Faruqui, Manaal and Das, Dipanjan},
   booktitle = {Proc. of EMNLP},
   year = {2018}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.