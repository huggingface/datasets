---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
- expert-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Mostly Basic Python Problems
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text2text-generation
task_ids:
- text2text-generation-other-code-generation
---

# Dataset Card for Mostly Basic Python Problems (mbpp)

## Table of Contents
- [Dataset Card for Mostly Basic Python Problems (mbpp)](#dataset-card-for-mostly-basic-python-problems-(mbpp))
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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
- **Repository: https://github.com/google-research/google-research/tree/master/mbpp**
- **Paper: [Program Synthesis with Large Language Models](https://arxiv.org/abs/2108.07732)**

### Dataset Summary
The benchmark consists of around 1,000 crowd-sourced Python programming problems, designed to be solvable by entry level programmers, covering programming fundamentals, standard library functionality, and so on. Each problem consists of a task description, code solution and 3 automated test cases. As described in the paper, a subset of the data has been hand-verified by us. 

Released [here](https://github.com/google-research/google-research/tree/master/mbpp) as part of [Program Synthesis with Large Language Models, Austin et. al., 2021](https://arxiv.org/abs/2108.07732).

### Supported Tasks and Leaderboards
This dataset is used to evaluate code generations.

### Languages
English - Python code

## Dataset Structure

```python
dataset_full = load_dataset("mbpp")
DatasetDict({
    test: Dataset({
        features: ['task_id', 'text', 'code', 'test_list', 'test_setup_code', 'challenge_test_list'],
        num_rows: 974
    })
})

dataset_sanitized = load_dataset("mbpp", "sanitized")
DatasetDict({
    test: Dataset({
        features: ['source_file', 'task_id', 'prompt', 'code', 'test_imports', 'test_list'],
        num_rows: 427
    })
})
```

### Data Instances

#### mbpp - full
```
{
    'task_id': 1,
    'text': 'Write a function to find the minimum cost path to reach (m, n) from (0, 0) for the given cost matrix cost[][] and a position (m, n) in cost[][].',
    'code': 'R = 3\r\nC = 3\r\ndef min_cost(cost, m, n): \r\n\ttc = [[0 for x in range(C)] for x in range(R)] \r\n\ttc[0][0] = cost[0][0] \r\n\tfor i in range(1, m+1): \r\n\t\ttc[i][0] = tc[i-1][0] + cost[i][0] \r\n\tfor j in range(1, n+1): \r\n\t\ttc[0][j] = tc[0][j-1] + cost[0][j] \r\n\tfor i in range(1, m+1): \r\n\t\tfor j in range(1, n+1): \r\n\t\t\ttc[i][j] = min(tc[i-1][j-1], tc[i-1][j], tc[i][j-1]) + cost[i][j] \r\n\treturn tc[m][n]',
    'test_list': [
        'assert min_cost([[1, 2, 3], [4, 8, 2], [1, 5, 3]], 2, 2) == 8',
        'assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12',
        'assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16'],
    'test_setup_code': '',
    'challenge_test_list': []
}
```
#### mbpp - sanitized
```
{
    'source_file': 'Benchmark Questions Verification V2.ipynb',
    'task_id': 2,
    'prompt': 'Write a function to find the shared elements from the given two lists.',
    'code': 'def similar_elements(test_tup1, test_tup2):\n  res = tuple(set(test_tup1) & set(test_tup2))\n  return (res) ',
    'test_imports': [],
    'test_list': [
        'assert set(similar_elements((3, 4, 5, 6),(5, 7, 4, 10))) == set((4, 5))',
        'assert set(similar_elements((1, 2, 3, 4),(5, 4, 3, 7))) == set((3, 4))',
        'assert set(similar_elements((11, 12, 14, 13),(17, 15, 14, 13))) == set((13, 14))'
        ]
}
```
### Data Fields

- `source_file`: unknown
- `text`/`prompt`: description of programming task
- `code`: solution for programming task
- `test_setup_code`/`test_imports`: necessary code imports to execute tests
- `test_list`: list of tests to verify solution
- `challenge_test_list`: list of more challenging test to further probe solution

### Data Splits
There are two version of the dataset (full and sanitized) which only one split each (test).
## Dataset Creation
See section 2.1 of original [paper](https://arxiv.org/abs/2108.07732).

### Curation Rationale
In order to evaluate code generation functions a set of simple programming tasks as well as solutions is necessary which this dataset provides.

### Source Data

#### Initial Data Collection and Normalization
The dataset was manually created from scratch.

#### Who are the source language producers?
The dataset was created with an internal crowdsourcing effort at Google.

### Annotations

#### Annotation process
The full dataset was created first and a subset then underwent a second round to improve the task descriptions.

#### Who are the annotators?
The dataset was created with an internal crowdsourcing effort at Google.

### Personal and Sensitive Information
None.

## Considerations for Using the Data
Make sure you execute generated Python code in a safe environment when evauating against this dataset as generated code could be harmful.

### Social Impact of Dataset
With this dataset code generating models can be better evaluated which leads to fewer issues introduced when using such models.

### Discussion of Biases

### Other Known Limitations
Since the task descriptions might not be expressive enough to solve the task. The `sanitized` split aims at addressing this issue by having a second round of annotators improve the dataset.

## Additional Information

### Dataset Curators
Google Research

### Licensing Information
CC-BY-4.0

### Citation Information
```
@article{austin2021program,
  title={Program Synthesis with Large Language Models},
  author={Austin, Jacob and Odena, Augustus and Nye, Maxwell and Bosma, Maarten and Michalewski, Henryk and Dohan, David and Jiang, Ellen and Cai, Carrie and Terry, Michael and Le, Quoc and others},
  journal={arXiv preprint arXiv:2108.07732},
  year={2021}
```
### Contributions
Thanks to [@lvwerra](https://github.com/lvwerra) for adding this dataset.

