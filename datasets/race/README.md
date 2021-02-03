---
---

# Dataset Card for "race"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [http://www.cs.cmu.edu/~glai1/data/race/](http://www.cs.cmu.edu/~glai1/data/race/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 72.79 MB
- **Size of the generated dataset:** 333.27 MB
- **Total amount of disk used:** 406.07 MB

### [Dataset Summary](#dataset-summary)

Race is a large-scale reading comprehension dataset with more than 28,000 passages and nearly 100,000 questions. The
 dataset is collected from English examinations in China, which are designed for middle school and high school students.
The dataset can be served as the training and test sets for machine comprehension.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### all

- **Size of downloaded dataset files:** 24.26 MB
- **Size of the generated dataset:** 166.64 MB
- **Total amount of disk used:** 190.90 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answer": "A",
    "article": "\"Schoolgirls have been wearing such short skirts at Paget High School in Branston that they've been ordered to wear trousers ins...",
    "example_id": "high132.txt",
    "options": ["short skirts give people the impression of sexualisation", "short skirts are too expensive for parents to afford", "the headmaster doesn't like girls wearing short skirts", "the girls wearing short skirts will be at the risk of being laughed at"],
    "question": "The girls at Paget High School are not allowed to wear skirts in that    _  ."
}
```

#### high

- **Size of downloaded dataset files:** 24.26 MB
- **Size of the generated dataset:** 133.63 MB
- **Total amount of disk used:** 157.89 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answer": "A",
    "article": "\"Schoolgirls have been wearing such short skirts at Paget High School in Branston that they've been ordered to wear trousers ins...",
    "example_id": "high132.txt",
    "options": ["short skirts give people the impression of sexualisation", "short skirts are too expensive for parents to afford", "the headmaster doesn't like girls wearing short skirts", "the girls wearing short skirts will be at the risk of being laughed at"],
    "question": "The girls at Paget High School are not allowed to wear skirts in that    _  ."
}
```

#### middle

- **Size of downloaded dataset files:** 24.26 MB
- **Size of the generated dataset:** 33.01 MB
- **Total amount of disk used:** 57.27 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answer": "B",
    "article": "\"There is not enough oil in the world now. As time goes by, it becomes less and less, so what are we going to do when it runs ou...",
    "example_id": "middle3.txt",
    "options": ["There is more petroleum than we can use now.", "Trees are needed for some other things besides making gas.", "We got electricity from ocean tides in the old days.", "Gas wasn't used to run cars in the Second World War."],
    "question": "According to the passage, which of the following statements is TRUE?"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### all
- `example_id`: a `string` feature.
- `article`: a `string` feature.
- `answer`: a `string` feature.
- `question`: a `string` feature.
- `options`: a `list` of `string` features.

#### high
- `example_id`: a `string` feature.
- `article`: a `string` feature.
- `answer`: a `string` feature.
- `question`: a `string` feature.
- `options`: a `list` of `string` features.

#### middle
- `example_id`: a `string` feature.
- `article`: a `string` feature.
- `answer`: a `string` feature.
- `question`: a `string` feature.
- `options`: a `list` of `string` features.

### [Data Splits Sample Size](#data-splits-sample-size)

| name |train|validation|test|
|------|----:|---------:|---:|
|all   |87866|      4887|4934|
|high  |62445|      3451|3498|
|middle|25421|      1436|1436|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```
@article{lai2017large,
    title={RACE: Large-scale ReAding Comprehension Dataset From Examinations},
    author={Lai, Guokun and Xie, Qizhe and Liu, Hanxiao and Yang, Yiming and Hovy, Eduard},
    journal={arXiv preprint arXiv:1704.04683},
    year={2017}
}

```


### Contributions

Thanks to [@abarbosa94](https://github.com/abarbosa94), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.