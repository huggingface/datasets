---
annotations_creators:
- expert-generated
- found
language_creators:
- expert-generated
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
source_datasets:
- extended|other-BioASQ
- extended|other-DuoRC
- extended|other-HotpotQA
- extended|other-Natural-Questions
- extended|other-Relation-Extraction
- extended|other-SQuAD
- extended|other-SearchQA
- extended|other-TextbookQA
- extended|other-TriviaQA
task_categories:
- question-answering
task_ids:
- extractive-qa
- open-domain-qa
paperswithcode_id: multireqa
pretty_name: MultiReQA
configs:
- BioASQ
- DuoRC
- HotpotQA
- NaturalQuestions
- RelationExtraction
- SQuAD
- SearchQA
- TextbookQA
- TriviaQA
dataset_info:
- config_name: SearchQA
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: train
    num_bytes: 183902877
    num_examples: 3163801
  - name: validation
    num_bytes: 26439174
    num_examples: 454836
  download_size: 36991959
  dataset_size: 210342051
- config_name: TriviaQA
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: train
    num_bytes: 107326326
    num_examples: 1893674
  - name: validation
    num_bytes: 13508062
    num_examples: 238339
  download_size: 21750402
  dataset_size: 120834388
- config_name: HotpotQA
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: train
    num_bytes: 29516866
    num_examples: 508879
  - name: validation
    num_bytes: 3027229
    num_examples: 52191
  download_size: 6343389
  dataset_size: 32544095
- config_name: SQuAD
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: train
    num_bytes: 16828974
    num_examples: 95659
  - name: validation
    num_bytes: 2012997
    num_examples: 10642
  download_size: 3003646
  dataset_size: 18841971
- config_name: NaturalQuestions
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: train
    num_bytes: 28732767
    num_examples: 448355
  - name: validation
    num_bytes: 1418124
    num_examples: 22118
  download_size: 6124487
  dataset_size: 30150891
- config_name: BioASQ
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: test
    num_bytes: 766190
    num_examples: 14158
  download_size: 156649
  dataset_size: 766190
- config_name: RelationExtraction
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: test
    num_bytes: 217870
    num_examples: 3301
  download_size: 73019
  dataset_size: 217870
- config_name: TextbookQA
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: test
    num_bytes: 4182675
    num_examples: 71147
  download_size: 704602
  dataset_size: 4182675
- config_name: DuoRC
  features:
  - name: candidate_id
    dtype: string
  - name: response_start
    dtype: int32
  - name: response_end
    dtype: int32
  splits:
  - name: test
    num_bytes: 1483518
    num_examples: 5525
  download_size: 97625
  dataset_size: 1483518
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