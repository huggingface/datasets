---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
language:
- en
language_bcp47:
- en-US
license:
- mit
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
pretty_name: HendrycksTest
---

# Dataset Card for HendrycksTest

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

[Measuring Massive Multitask Language Understanding](https://arxiv.org/pdf/2009.03300) by [Dan Hendrycks](https://people.eecs.berkeley.edu/~hendrycks/), [Collin Burns](http://collinpburns.com), [Steven Basart](https://stevenbas.art), Andy Zou, Mantas Mazeika, [Dawn Song](https://people.eecs.berkeley.edu/~dawnsong/), and [Jacob Steinhardt](https://www.stat.berkeley.edu/~jsteinhardt/) (ICLR 2021).

- **Repository**: https://github.com/hendrycks/test
- **Paper**: https://arxiv.org/abs/2009.03300

A complete list of tasks: ['abstract_algebra', 'anatomy', 'astronomy', 'business_ethics', 'clinical_knowledge', 'college_biology', 'college_chemistry', 'college_computer_science', 'college_mathematics', 'college_medicine', 'college_physics', 'computer_security', 'conceptual_physics', 'econometrics', 'electrical_engineering', 'elementary_mathematics', 'formal_logic', 'global_facts', 'high_school_biology', 'high_school_chemistry', 'high_school_computer_science', 'high_school_european_history', 'high_school_geography', 'high_school_government_and_politics', 'high_school_macroeconomics', 'high_school_mathematics', 'high_school_microeconomics', 'high_school_physics', 'high_school_psychology', 'high_school_statistics', 'high_school_us_history', 'high_school_world_history', 'human_aging', 'human_sexuality', 'international_law', 'jurisprudence', 'logical_fallacies', 'machine_learning', 'management', 'marketing', 'medical_genetics', 'miscellaneous', 'moral_disputes', 'moral_scenarios', 'nutrition', 'philosophy', 'prehistory', 'professional_accounting', 'professional_law', 'professional_medicine', 'professional_psychology', 'public_relations', 'security_studies', 'sociology', 'us_foreign_policy', 'virology', 'world_religions']

### Dataset Summary

This is a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. This covers 57 tasks including elementary mathematics, US history, computer science, law, and more. To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability.

### Supported Tasks and Leaderboards

|                Model               | Authors |  Humanities |  Social Science  | STEM | Other | Average |
|------------------------------------|----------|:-------:|:-------:|:-------:|:-------:|:-------:|
| [UnifiedQA](https://arxiv.org/abs/2005.00700) | Khashabi et al., 2020 | 45.6 | 56.6 | 40.2 | 54.6 | 48.9
| [GPT-3](https://arxiv.org/abs/2005.14165) (few-shot) | Brown et al., 2020 | 40.8 | 50.4 | 36.7 | 48.8 | 43.9
| [GPT-2](https://arxiv.org/abs/2005.14165) | Radford et al., 2019 | 32.8 | 33.3 | 30.2 | 33.1 | 32.4
| Random Baseline           | N/A | 25.0 | 25.0 | 25.0 | 25.0 | 25.0 | 25.0

### Languages

English

## Dataset Structure

### Data Instances

An example from anatomy subtask looks as follows:
```
{
  "question": "What is the embryological origin of the hyoid bone?",
  "choices": ["The first pharyngeal arch", "The first and second pharyngeal arches", "The second pharyngeal arch", "The second and third pharyngeal arches"],
  "answer": "D"
}
```

### Data Fields

- `question`: a string feature
- `choices`: a list of 4 string features
- `answer`: a ClassLabel feature

### Data Splits

- `auxiliary_train`: auxiliary multiple-choice training questions from ARC, MC_TEST, OBQA, RACE, etc.
- `dev`: 5 examples per subtask, meant for few-shot setting
- `test`: there are at least 100 examples per subtask

|       | auxiliary_train   | dev | val | test |
| ----- | :------: | :-----: | :-----: | :-----: |
| TOTAL | 99842 | 285 | 1531 | 14042

## Dataset Creation

### Curation Rationale

Transformer models have driven this recent progress by pretraining on massive text corpora, including all of Wikipedia, thousands of books, and numerous websites. These models consequently see extensive information about specialized topics, most of which is not assessed by existing NLP benchmarks. To bridge the gap between the wide-ranging knowledge that models see during pretraining and the existing measures of success, we introduce a new benchmark for assessing models across a diverse set of subjects that humans learn.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

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

[MIT License](https://github.com/hendrycks/test/blob/master/LICENSE)

### Citation Information

If you find this useful in your research, please consider citing the test and also the [ETHICS](https://arxiv.org/abs/2008.02275) dataset it draws from:
```
    @article{hendryckstest2021,
      title={Measuring Massive Multitask Language Understanding},
      author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
      journal={Proceedings of the International Conference on Learning Representations (ICLR)},
      year={2021}
    }

    @article{hendrycks2021ethics,
      title={Aligning AI With Shared Human Values},
      author={Dan Hendrycks and Collin Burns and Steven Basart and Andrew Critch and Jerry Li and Dawn Song and Jacob Steinhardt},
      journal={Proceedings of the International Conference on Learning Representations (ICLR)},
      year={2021}
    }
```
### Contributions

Thanks to [@andyzoujm](https://github.com/andyzoujm) for adding this dataset.
