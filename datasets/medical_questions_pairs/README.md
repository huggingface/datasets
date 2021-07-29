---
annotations_creators:
- expert-generated
language_creators:
- other
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- semantic-similarity-classification
paperswithcode_id: null
---

# Dataset Card for [medical_questions_pairs]

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
- **Repository:** [Medical questions pairs repository](https://github.com/curai/medical-question-pair-dataset)
- **Paper:** [Effective Transfer Learning for Identifying Similar Questions:Matching User Questions to COVID-19 FAQs](https://arxiv.org/abs/2008.13546)

### Dataset Summary

This dataset consists of 3048 similar and dissimilar medical question pairs hand-generated and labeled by Curai's doctors. Doctors with a list of 1524 patient-asked questions randomly sampled from the publicly available crawl of [HealthTap](https://github.com/durakkerem/Medical-Question-Answer-Datasets). Each question results in one similar and one different pair through the following instructions provided to the labelers:

- Rewrite the original question in a different way while maintaining the same intent. Restructure the syntax as much as possible and change medical details that would not impact your response. e.g. "I'm a 22-y-o female" could become "My 26 year old daughter"
- Come up with a related but dissimilar question for which the answer to the original question would be WRONG OR IRRELEVANT. Use similar key words.

The first instruction generates a positive question pair (similar) and the second generates a negative question pair (different). With the above instructions,  the task was intentionally framed such that positive question pairs can look very different by superficial metrics, and negative question pairs can conversely look very similar. This ensures that the task is not trivial.


### Supported Tasks and Leaderboards

- `text-classification` : The dataset can be used to train a model to identify similar and non similar medical question pairs.

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

The dataset contains dr_id, question_1, question_2, label. 11 different doctors were used for this task so dr_id ranges from 1 to 11. The label is 1 if the question pair is similar and 0 otherwise.


### Data Fields

- `dr_id`: 11 different doctors were used for this task so dr_id ranges from 1 to 11
- `question_1`: Original Question
- `question_2`: Rewritten Question maintaining the same intent like Original Question
- `label`: The label is 1 if the question pair is similar and 0 otherwise.

### Data Splits

The dataset as of now consists of only one split(train) but can be split seperately based on the requirement

|                             | Tain   | 
| -----                       | ------ | 
| Non similar Question Pairs  | 1524   |
| Similar Question Pairs      | 1524   |

## Dataset Creation
Doctors with a list of 1524 patient-asked questions randomly sampled from the publicly available crawl of [HealthTap](https://github.com/durakkerem/Medical-Question-Answer-Datasets). Each question results in one similar and one different pair through the following instructions provided to the labelers:

- Rewrite the original question in a different way while maintaining the same intent. Restructure the syntax as much as possible and change medical details that would not impact your response. e.g. "I'm a 22-y-o female" could become "My 26 year old daughter"
- Come up with a related but dissimilar question for which the answer to the original question would be WRONG OR IRRELEVANT. Use similar key words.

The first instruction generates a positive question pair (similar) and the second generates a negative question pair (different). With the above instructions,  the task was intentionally framed such that positive question pairs can look very different by superficial metrics, and negative question pairs can conversely look very similar. This ensures that the task is not trivial.

### Curation Rationale
[More Information Needed]

### Source Data
1524 patient-asked questions randomly sampled from the publicly available crawl of [HealthTap](https://github.com/durakkerem/Medical-Question-Answer-Datasets)

#### Initial Data Collection and Normalization
[More Information Needed]

#### Who are the source language producers?
[More Information Needed]

### Annotations
[More Information Needed]

#### Annotation process

Doctors with a list of 1524 patient-asked questions randomly sampled from the publicly available crawl of [HealthTap](https://github.com/durakkerem/Medical-Question-Answer-Datasets). Each question results in one similar and one different pair through the following instructions provided to the labelers:

- Rewrite the original question in a different way while maintaining the same intent. Restructure the syntax as much as possible and change medical details that would not impact your response. e.g. "I'm a 22-y-o female" could become "My 26 year old daughter"
- Come up with a related but dissimilar question for which the answer to the original question would be WRONG OR IRRELEVANT. Use similar key words.

The first instruction generates a positive question pair (similar) and the second generates a negative question pair (different). With the above instructions,  the task was intentionally framed such that positive question pairs can look very different by superficial metrics, and negative question pairs can conversely look very similar. This ensures that the task is not trivial.

#### Who are the annotators?
**Curai's doctors** 

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
[More Information Needed]

### Dataset Curators
[More Information Needed]

### Licensing Information
[More Information Needed]

### Citation Information
```
@misc{mccreery2020effective,
      title={Effective Transfer Learning for Identifying Similar Questions: Matching User Questions to COVID-19 FAQs}, 
      author={Clara H. McCreery and Namit Katariya and Anitha Kannan and Manish Chablani and Xavier Amatriain},
      year={2020},
      eprint={2008.13546},
      archivePrefix={arXiv},
      primaryClass={cs.IR}
}
```

### Contributions

Thanks to [@tuner007](https://github.com/tuner007) for adding this dataset.