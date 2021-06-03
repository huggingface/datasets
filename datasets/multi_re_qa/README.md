---
annotations_creators:
- expert-generated
- found
language_creators:
- expert-generated
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
  BioASQ:
  - 10K<n<100K
  DuoRC:
  - 1K<n<10K
  HotpotQA:
  - 100K<n<1M
  NaturalQuestions:
  - 100K<n<1M
  RelationExtraction:
  - 1K<n<10K
  SQuAD:
  - 100K<n<1M
  SearchQA:
  - 1M<n<10M
  TextbookQA:
  - 10K<n<100K
  TriviaQA:
  - 1M<n<10M
source_datasets:
  BioASQ:
  - extended|other-BioASQ
  DuoRC:
  - extended|other-DuoRC
  HotpotQA:
  - extended|other-HotpotQA
  NaturalQuestions:
  - extended|other-Natural-Questions
  RelationExtraction:
  - extended|other-Relation-Extraction
  SQuAD:
  - extended|other-SQuAD
  SearchQA:
  - extended|other-SearchQA
  TextbookQA:
  - extended|other-TextbookQA
  TriviaQA:
  - extended|other-TriviaQA
task_categories:
- question-answering
task_ids:
- extractive-qa
- open-domain-qa
paperswithcode_id: multireqa
---
# Dataset Card for MultiReQA

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

- **Homepage:** https://github.com/google-research-datasets/MultiReQA
- **Repository:** https://github.com/google-research-datasets/MultiReQA
- **Paper:** https://arxiv.org/pdf/2005.02507.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary
MultiReQA contains the sentence boundary annotation from eight publicly available QA datasets including SearchQA, TriviaQA, HotpotQA, NaturalQuestions, SQuAD, BioASQ, RelationExtraction, and TextbookQA. Five of these datasets, including SearchQA, TriviaQA, HotpotQA, NaturalQuestions, SQuAD, contain both training and test data, and three, in cluding BioASQ, RelationExtraction, TextbookQA, contain only the test data (also includes DuoRC but not specified in the official documentation)
### Supported Tasks and Leaderboards

- Question answering (QA)
- Retrieval question answering (ReQA)
### Languages

Sentence boundary annotation for SearchQA, TriviaQA, HotpotQA, NaturalQuestions, SQuAD, BioASQ, RelationExtraction, TextbookQA and DuoRC

## Dataset Structure

### Data Instances

The general format is:
`
{
  "candidate_id": <candidate_id>,
  "response_start": <response_start>,
  "response_end": <response_end>
}
...
`

An example from SearchQA:
`{'candidate_id': 'SearchQA_000077f3912049dfb4511db271697bad/_0_1',
 'response_end': 306,
 'response_start': 243} `

### Data Fields

`
{
  "candidate_id": <STRING>,
  "response_start": <INT>,
  "response_end": <INT>
}
...
`
-  **candidate_id:**  The candidate id of the candidate sentence. It consists of the original qid from the MRQA shared task.
-   **response_start:**  The start index of the sentence with respect to its original context.
-   **response_end:**  The end index of the sentence with respect to its original context

### Data Splits

Train and Dev splits are available only for the following datasets,
 - SearchQA
 - TriviaQA
 - HotpotQA
 - SQuAD 
 - NaturalQuestions

Test splits are available only for the following datasets,
 - BioASQ
 - RelationExtraction
 - TextbookQA

The number of candidate sentences for each dataset in the table below.

|                    | MultiReQA |         |
|--------------------|-----------|---------|
|                    | train     | test    |
| SearchQA           | 629,160   | 454,836 |
| TriviaQA           | 335,659   | 238,339 |
| HotpotQA           | 104,973   | 52,191  |
| SQuAD              | 87,133    | 10,642  |
| NaturalQuestions   | 106,521   | 22,118  |
| BioASQ             | -         | 14,158  |
| RelationExtraction | -         | 3,301   |
| TextbookQA         | -         | 3,701   |

## Dataset Creation

### Curation Rationale

MultiReQA is a new multi-domain ReQA evaluation suite composed of eight retrieval QA tasks drawn from publicly available QA datasets from the [MRQA shared task](https://mrqa.github.io/). The dataset was curated by converting existing QA datasets from [MRQA shared task](https://mrqa.github.io/) to the format of MultiReQA benchmark.
### Source Data

#### Initial Data Collection and Normalization

The Initial data collection was performed by  converting existing QA datasets from MRQA shared task to the format of MultiReQA benchmark.
#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

The annotators/curators of the dataset are [mandyguo-xyguo](https://github.com/mandyguo-xyguo) and [mwurts4google](https://github.com/mwurts4google), the contributors of the official MultiReQA github repository 
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

The annotators/curators of the dataset are [mandyguo-xyguo](https://github.com/mandyguo-xyguo) and [mwurts4google](https://github.com/mwurts4google), the contributors of the official MultiReQA github repository 

### Licensing Information

[More Information Needed]

### Citation Information

```
@misc{m2020multireqa,
    title={MultiReQA: A Cross-Domain Evaluation for Retrieval Question Answering Models},
    author={Mandy Guo and Yinfei Yang and Daniel Cer and Qinlan Shen and Noah Constant},
    year={2020},
    eprint={2005.02507},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@Karthik-Bhaskar](https://github.com/Karthik-Bhaskar) for adding this dataset.