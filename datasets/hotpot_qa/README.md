---
language:
- en
paperswithcode_id: hotpotqa
pretty_name: HotpotQA
---

# Dataset Card for "hotpot_qa"

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

- **Homepage:** [https://hotpotqa.github.io/](https://hotpotqa.github.io/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1213.88 MB
- **Size of the generated dataset:** 1186.81 MB
- **Total amount of disk used:** 2400.69 MB

### Dataset Summary

HotpotQA is a new dataset with 113k  Wikipedia-based question-answer  pairs with  four  key  features:  (1)  the  questions  require finding and reasoning over multiple supporting  documents  to  answer;  (2)  the  questions  are  diverse  and  not  constrained  to  any pre-existing  knowledge  bases  or  knowledge schemas;  (3)  we  provide  sentence-level  supporting facts required for reasoning, allowingQA systems to reason with strong supervisionand explain the predictions; (4) we offer a new type  of  factoid  comparison  questions  to  testQA  systems’  ability  to  extract  relevant  facts and perform necessary comparison.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### distractor

- **Size of downloaded dataset files:** 584.36 MB
- **Size of the generated dataset:** 570.93 MB
- **Total amount of disk used:** 1155.29 MB

An example of 'validation' looks as follows.
```
{
    "answer": "This is the answer",
    "context": {
        "sentences": [["Sent 1"], ["Sent 21", "Sent 22"]],
        "title": ["Title1", "Title 2"]
    },
    "id": "000001",
    "level": "medium",
    "question": "What is the answer?",
    "supporting_facts": {
        "sent_id": [0, 1, 3],
        "title": ["Title of para 1", "Title of para 2", "Title of para 3"]
    },
    "type": "comparison"
}
```

#### fullwiki

- **Size of downloaded dataset files:** 629.52 MB
- **Size of the generated dataset:** 615.88 MB
- **Total amount of disk used:** 1245.40 MB

An example of 'train' looks as follows.
```
{
    "answer": "This is the answer",
    "context": {
        "sentences": [["Sent 1"], ["Sent 2"]],
        "title": ["Title1", "Title 2"]
    },
    "id": "000001",
    "level": "hard",
    "question": "What is the answer?",
    "supporting_facts": {
        "sent_id": [0, 1, 3],
        "title": ["Title of para 1", "Title of para 2", "Title of para 3"]
    },
    "type": "bridge"
}
```

### Data Fields

The data fields are the same among all splits.

#### distractor
- `id`: a `string` feature.
- `question`: a `string` feature.
- `answer`: a `string` feature.
- `type`: a `string` feature.
- `level`: a `string` feature.
- `supporting_facts`: a dictionary feature containing:
  - `title`: a `string` feature.
  - `sent_id`: a `int32` feature.
- `context`: a dictionary feature containing:
  - `title`: a `string` feature.
  - `sentences`: a `list` of `string` features.

#### fullwiki
- `id`: a `string` feature.
- `question`: a `string` feature.
- `answer`: a `string` feature.
- `type`: a `string` feature.
- `level`: a `string` feature.
- `supporting_facts`: a dictionary feature containing:
  - `title`: a `string` feature.
  - `sent_id`: a `int32` feature.
- `context`: a dictionary feature containing:
  - `title`: a `string` feature.
  - `sentences`: a `list` of `string` features.

### Data Splits

#### distractor

|          |train|validation|
|----------|----:|---------:|
|distractor|90447|      7405|

#### fullwiki

|        |train|validation|test|
|--------|----:|---------:|---:|
|fullwiki|90447|      7405|7405|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```

@inproceedings{yang2018hotpotqa,
  title={{HotpotQA}: A Dataset for Diverse, Explainable Multi-hop Question Answering},
  author={Yang, Zhilin and Qi, Peng and Zhang, Saizheng and Bengio, Yoshua and Cohen, William W. and Salakhutdinov, Ruslan and Manning, Christopher D.},
  booktitle={Conference on Empirical Methods in Natural Language Processing ({EMNLP})},
  year={2018}
}

```


### Contributions

Thanks to [@albertvillanova](https://github.com/albertvillanova), [@ghomasHudson](https://github.com/ghomasHudson) for adding this dataset.
