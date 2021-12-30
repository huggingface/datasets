---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- pt
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
- text-scoring
task_ids:
- natural-language-inference
- semantic-similarity-scoring
paperswithcode_id: assin2
---

# Dataset Card for ASSIN 2

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

- **Homepage:** [ASSIN 2 homepage](https://sites.google.com/view/assin2)
- **Repository:** [ASSIN 2 repository](https://sites.google.com/view/assin2)
- **Paper:** [The ASSIN 2 shared task: a quick overview](https://drive.google.com/file/d/1ft1VU6xiVm-N58dfAp6FHWjQ4IvcXgqp/view)
- **Point of Contact:** [Livy Real](mailto:livyreal@gmail.com)

### Dataset Summary

The ASSIN 2 corpus is composed of rather simple sentences. Following the procedures of SemEval 2014 Task 1.
The training and validation data are composed, respectively, of 6,500 and 500 sentence pairs in Brazilian Portuguese, 
annotated for entailment and semantic similarity. Semantic similarity values range from 1 to 5, and text entailment 
classes are either entailment or none. The test data are composed of approximately 3,000 sentence pairs with the same 
annotation. All data were manually annotated.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is Portuguese.

## Dataset Structure

### Data Instances

An example from the ASSIN 2 dataset looks as follows:

```
{
  "entailment_judgment": 1,
  "hypothesis": "Uma criança está segurando uma pistola de água",
  "premise": "Uma criança risonha está segurando uma pistola de água e sendo espirrada com água",
  "relatedness_score": 4.5,
  "sentence_pair_id": 1
}
```

### Data Fields

- `sentence_pair_id`: a `int64` feature.
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `relatedness_score`: a `float32` feature.
- `entailment_judgment`: a classification label, with possible values including `NONE`, `ENTAILMENT`.

### Data Splits

The data is split into train, validation and test set. The split sizes are as follow:

| Train  | Val   | Test |
| ------ | ----- | ---- |
| 6500   | 500   | 2448 |

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

[More Information Needed]

### Citation Information

```
@inproceedings{real2020assin,
  title={The assin 2 shared task: a quick overview},
  author={Real, Livy and Fonseca, Erick and Oliveira, Hugo Goncalo},
  booktitle={International Conference on Computational Processing of the Portuguese Language},
  pages={406--412},
  year={2020},
  organization={Springer}
}
```

### Contributions

Thanks to [@jonatasgrosman](https://github.com/jonatasgrosman) for adding this dataset.