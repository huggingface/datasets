---
YAML tags:
- copy-paste the tags obtained with the tagging app: https://github.com/huggingface/datasets-tagging
---

# Dataset Card for LogiQA

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
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

## Dataset Description

- **Homepage:**
- **Repository: https://github.com/lgw863/LogiQA-dataset**
- **Paper: https://arxiv.org/pdf/2007.08124.pdf**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

LogiQA, which contains 8,678 paragraph-question pairs, each with four candidate answers. The dataset is sourced from publically available logical examination papers for reading comprehension, which are designed by domain experts for evaluating the logical reasoning ability and test participants.

### Supported Tasks and Leaderboards

Question-Answering

### Languages

English

## Dataset Structure

### Data Instances

The each example consists of 8 lines from the text files of a given split.
These lines consists of strings and constitute a single question-answer pair with a following context and set of 4 multiple choice answers.
Here is an example:
```buildoutcfg
c
Some Cantonese don't like chili, so some southerners don't like chili.
Which of the following can guarantee the above argument?
A.Some Cantonese love chili
B.Some people who like peppers are southerners
C.All Cantonese are southerners
D.Some Cantonese like neither peppers nor sweets

```

### Data Fields
- The first line is the correct answer (choice A, B, C, or D).
- The second line is the context.
- The third line is the question.
- The fourth line is choice A.
- The fourth line is choice B.
- The fourth line is choice C.
- The fourth line is choice D.


### Data Splits

File Name | n examples|
| -----               | ----      |
| Train.txt           | 7376      |
| Eval.txt            | 651       |
| Test.txt            | 651       | 


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

Domain experts.

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

[More Information Needed]

### Citation Information
@misc{liu2020logiqa,
      title={LogiQA: A Challenge Dataset for Machine Reading Comprehension with Logical Reasoning}, 
      author={Jian Liu and Leyang Cui and Hanmeng Liu and Dandan Huang and Yile Wang and Yue Zhang},
      year={2020},
      eprint={2007.08124},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

