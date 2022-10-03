---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: 'DISFL-QA: A Benchmark Dataset for Understanding Disfluencies in Question
  Answering'
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
- open-domain-qa
---

# Dataset Card for DISFL-QA: A Benchmark Dataset for Understanding Disfluencies in Question Answering

## Table of Contents
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

- **Homepage:** [Disfl-QA](https://github.com/google-research-datasets/disfl-qa)
- **Paper:** [Disfl-QA: A Benchmark Dataset for Understanding Disfluencies in Question Answering](https://arxiv.org/pdf/2106.04016.pdf)
- **Point of Contact:** [disfl-qa team](disfl-qa@google.com)

### Dataset Summary

Disfl-QA is a targeted dataset for contextual disfluencies in an information seeking  setting, namely question answering over Wikipedia passages.  Disfl-QA builds upon the SQuAD-v2 ([Rajpurkar et al., 2018](https://www.aclweb.org/anthology/P18-2124/)) dataset, where each question in the dev set is annotated to add a contextual disfluency using the paragraph as a source of distractors.

The final dataset consists of ~12k (disfluent question, answer) pairs. Over 90\% of the disfluencies are corrections or restarts, making it a much harder test set for disfluency correction. Disfl-QA aims to fill a major gap between speech and NLP research community. The authors hope the dataset can serve as a benchmark dataset for testing robustness of models against disfluent inputs.

The expriments reveal that the state-of-the-art models are brittle when subjected to disfluent inputs from Disfl-QA. Detailed experiments and analyses can be found in the [paper](https://arxiv.org/pdf/2106.04016.pdf).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in English only.

## Dataset Structure

### Data Instances

This example was too long and was cropped:
```
{
    "answers": {
        "answer_start": [94, 87, 94, 94],
        "text": ["10th and 11th centuries", "in the 10th and 11th centuries", "10th and 11th centuries", "10th and 11th centuries"]
    },
    "context": "\"The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave thei...",
    "id": "56ddde6b9a695914005b9629",
    "original question": "When were the Normans in Normandy?",
    "disfluent question": "From which countries no tell me when were the Normans in Normandy?"
    "title": "Normans"
}
```
### Data Fields

- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `original question`: Original question from SQuAD-v2 (a `string` feature)
- `disfluent question`: Disfluent question from Disfl-QA (a `string` feature)
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### Data Splits

Disfl-QA consists of ~12k disfluent questions with the following train/dev/test splits:
| File      | Questions   |
|-----|-----|
|train.json  | 7182  |
|dev.json  | 1000   |
|test.json  | 3643  |

## Dataset Creation

### Curation Rationale

The research in NLP and speech community has been impeded by the lack of curated datasets containing such disfluencies. The datasets available today are mostly conversational in nature, and span a limited number of very specific domains (e.g., telephone conversations, court proceedings). Furthermore, only a small fraction of the utterances in these datasets contain disfluencies, with a limited and skewed distribution of disfluencies types. In the most popular dataset in the literature, the SWITCHBOARD corpus (Godfrey et al., 1992), only 5.9% of the words are disfluencies (Charniak and Johnson, 2001), of which > 50% are repetitions (Shriberg, 1996), which has been shown to be the relatively simpler form of disfluencies (Zayats et al., 2014; Jamshid Lou et al., 2018; Zayats et al., 2019). To fill this gap, the authors presented DISFL-QA, the first dataset containing contextual disfluencies in an information seeking setting, namely question answering over Wikipedia passages.

### Source Data

#### Initial Data Collection and Normalization

DISFL-QA is constructed by asking human raters to insert disfluencies in questions from SQUAD-v2, a popular question answering dataset, using the passage and remaining questions as context. These contextual disfluencies lend naturalness to DISFL-QA, and challenge models relying on shallow matching between question and context to predict an answer.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Each question associated with the paragraph is sent for a human annotation task to add a contextual disfluency using the paragraph as a source of distractors. Finally, to ensure the quality of the dataset, a subsequent round of human evaluation with an option to re-annotate is conducted.

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

[More Information Needed]

### Licensing Information

Disfl-QA dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

```
@inproceedings{gupta-etal-2021-disflqa,
    title = "{Disfl-QA: A Benchmark Dataset for Understanding Disfluencies in Question Answering}",
    author = "Gupta, Aditya and Xu, Jiacheng and Upadhyay, Shyam and Yang, Diyi and Faruqui, Manaal",
    booktitle = "Findings of ACL",
    year = "2021"
}
```

### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.
