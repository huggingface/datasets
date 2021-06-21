---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- expert-generated
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
paperswithcode_id: aqua-rat
---

# Dataset Card for AQUA-RAT

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

- **Homepage:** [https://github.com/deepmind/AQuA](https://github.com/deepmind/AQuA)
- **Repository:** [https://github.com/deepmind/AQuA](https://github.com/deepmind/AQuA)
- **Paper:** [https://arxiv.org/pdf/1705.04146.pdf](https://arxiv.org/pdf/1705.04146.pdf)

### Dataset Summary

A large-scale dataset consisting of approximately 100,000 algebraic word problems.
The solution to each question is explained step-by-step using natural language.
This data is used to train a program generation model that learns to generate the explanation,
while generating the program that solves the question.

### Supported Tasks and Leaderboards

### Languages

en

## Dataset Structure

### Data Instances
```
{
"question": "A grocery sells a bag of ice for $1.25, and makes 20% profit. If it sells 500 bags of ice, how much total profit does it make?",
"options": ["A)125", "B)150", "C)225", "D)250", "E)275"],
"rationale": "Profit per bag = 1.25 * 0.20 = 0.25\nTotal profit = 500 * 0.25 = 125\nAnswer is A.",
"correct": "A"
}
```

### Data Fields

- `question` : (str) A natural language definition of the problem to solve
- `options` : (list(str)) 5 possible options (A, B, C, D and E), among which one is correct
- `rationale` : (str) A natural language description of the solution to the problem
- `correct` : (str) The correct option

### Data Splits
|                            | Train  | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Examples                   | 97467  |   254 | 254  |

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information


### Dataset Curators

[Needs More Information]

### Licensing Information
Copyright 2017 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

### Citation Information
```
@article{ling2017program,
  title={Program induction by rationale generation: Learning to solve and explain algebraic word problems},
  author={Ling, Wang and Yogatama, Dani and Dyer, Chris and Blunsom, Phil},
  journal={ACL},
  year={2017}
}
```

### Contributions

Thanks to [@arkhalid](https://github.com/arkhalid) for adding this dataset.
