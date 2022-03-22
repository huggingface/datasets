---
annotations_creators: []
language_creators: []
languages: ['en']
licenses: []
multilinguality: []
pretty_name: Adversarial GLUE
paperswithcode_id: advglue
size_categories:
- unknown
source_datasets: []
task_categories: []
task_ids: []
---

# Dataset Card for Adversarial GLUE

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

- **Homepage:**  https://adversarialglue.github.io/
- **Repository:**
- **Paper:** [arXiv](https://arxiv.org/pdf/2111.02840.pdf)
- **Leaderboard:**
- **Point of Contact:**
Adversarial GLUE Benchmark (AdvGLUE) is a comprehensive robustness evaluation benchmark that focuses on the adversarial robustness evaluation of language models. It covers five natural language understanding tasks from the famous GLUE tasks and is an adversarial version of GLUE benchmark.

AdvGLUE considers textual adversarial attacks from different perspectives and hierarchies, including word-level transformations, sentence-level manipulations, and human-written adversarial examples, which provide comprehensive coverage of various adversarial linguistic phenomena.

### Supported Tasks and Leaderboards

Leaderboard available on the homepage: [https://adversarialglue.github.io/](https://adversarialglue.github.io/).

### Languages

AdvGLUE deviates from the GLUE dataset, which has a base language of English.
## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### default

- **Size of downloaded dataset files:** 198 KB
- **Example**:
```python
>>> datasets.load_dataset('adv_glue', 'adv_sst2')['validation'][0]
{'sentence': "it 's an uneven treat that bores fun at the democratic exercise while also examining its significance for those who take part .", 'label': 1, 'idx': 0}
```

### Data Fields

The data fields are the same as in the GLUE dataset, which differ by task.

### Data Splits

Adversarial GLUE provides only a 'dev' split.
## Dataset Creation
### Curation Rationale
[More Information Needed]

### Source Data
[More Information Needed]
### Annotations
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
### Citation Information

```
@article{Wang2021AdversarialGA,
  title={Adversarial GLUE: A Multi-Task Benchmark for Robustness Evaluation of Language Models},
  author={Boxin Wang and Chejian Xu and Shuohang Wang and Zhe Gan and Yu Cheng and Jianfeng Gao and Ahmed Hassan Awadallah and B. Li},
  journal={ArXiv},
  year={2021},
  volume={abs/2111.02840}
}
```


### Contributions

Thanks to [@jxmorris12](https://github.com/jxmorris12) for adding this dataset.