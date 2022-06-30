---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- mit
multilinguality:
- monolingual
pretty_name: OpenAI HumanEval
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text2text-generation
task_ids:
- text2text-generation-other-code-generation
---

# Dataset Card for OpenAI HumanEval

## Table of Contents
- [OpenAI HumanEval](#openai-humaneval)
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

- **Repository:** [GitHub Repository](https://github.com/openai/human-eval)
- **Paper:** [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)

### Dataset Summary

The HumanEval dataset released by OpenAI includes 164 programming problems with a function sig- nature, docstring, body, and several unit tests. They were handwritten to ensure not to be included in the training set of code generation models.

### Supported Tasks and Leaderboards

### Languages
The programming problems are written in Python and contain English natural text in comments and docstrings.

## Dataset Structure

```python
from datasets import load_dataset
load_dataset("openai_humaneval")

DatasetDict({
    test: Dataset({
        features: ['task_id', 'prompt', 'canonical_solution', 'test', 'entry_point'],
        num_rows: 164
    })
})
```

### Data Instances

An example of a dataset instance:

```
{
    "task_id": "test/0",
    "prompt": "def return1():\n",
    "canonical_solution": "    return 1",
    "test": "def check(candidate):\n    assert candidate() == 1",
    "entry_point": "return1"
}
```

### Data Fields

- `task_id`: identifier for the data sample
- `prompt`: input for the model containing function header and docstrings
- `canonical_solution`: solution for the problem in the `prompt`
- `test`: contains function to test generated code for correctness
- `entry_point`: entry point for test


### Data Splits

The dataset only consists of a test split with 164 samples.

## Dataset Creation

### Curation Rationale

Since code generation models are often trained on dumps of GitHub a dataset not included in the dump was necessary to properly evaluate the model. However, since this dataset was published on GitHub it is likely to be included in future dumps.

### Source Data

The dataset was handcrafted by engineers and researchers at OpenAI.

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

None.

## Considerations for Using the Data
Make sure you execute generated Python code in a safe environment when evauating against this dataset as generated code could be harmful.

### Social Impact of Dataset
With this dataset code generating models can be better evaluated which leads to fewer issues introduced when using such models.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators
OpenAI

### Licensing Information

MIT License

### Citation Information
```
@misc{chen2021evaluating,
      title={Evaluating Large Language Models Trained on Code},
      author={Mark Chen and Jerry Tworek and Heewoo Jun and Qiming Yuan and Henrique Ponde de Oliveira Pinto and Jared Kaplan and Harri Edwards and Yuri Burda and Nicholas Joseph and Greg Brockman and Alex Ray and Raul Puri and Gretchen Krueger and Michael Petrov and Heidy Khlaaf and Girish Sastry and Pamela Mishkin and Brooke Chan and Scott Gray and Nick Ryder and Mikhail Pavlov and Alethea Power and Lukasz Kaiser and Mohammad Bavarian and Clemens Winter and Philippe Tillet and Felipe Petroski Such and Dave Cummings and Matthias Plappert and Fotios Chantzis and Elizabeth Barnes and Ariel Herbert-Voss and William Hebgen Guss and Alex Nichol and Alex Paino and Nikolas Tezak and Jie Tang and Igor Babuschkin and Suchir Balaji and Shantanu Jain and William Saunders and Christopher Hesse and Andrew N. Carr and Jan Leike and Josh Achiam and Vedant Misra and Evan Morikawa and Alec Radford and Matthew Knight and Miles Brundage and Mira Murati and Katie Mayer and Peter Welinder and Bob McGrew and Dario Amodei and Sam McCandlish and Ilya Sutskever and Wojciech Zaremba},
      year={2021},
      eprint={2107.03374},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

### Contributions

Thanks to [@lvwerra](https://github.com/lvwerra) for adding this dataset.