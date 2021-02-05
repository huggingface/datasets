---
---

# Dataset Card for "asnq"

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

- **Homepage:** [https://github.com/alexa/wqa_tanda#answer-sentence-natural-questions-asnq](https://github.com/alexa/wqa_tanda#answer-sentence-natural-questions-asnq)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3398.76 MB
- **Size of the generated dataset:** 3647.70 MB
- **Total amount of disk used:** 7046.46 MB

### [Dataset Summary](#dataset-summary)

ASNQ is a dataset for answer sentence selection derived from
Google's Natural Questions (NQ) dataset (Kwiatkowski et al. 2019).

Each example contains a question, candidate sentence, label indicating whether or not
the sentence answers the question, and two additional features --
sentence_in_long_answer and short_answer_in_sentence indicating whether ot not the
candidate sentence is contained in the long_answer and if the short_answer is in the candidate sentence.

For more details please see
https://arxiv.org/pdf/1911.04118.pdf

and

https://research.google/pubs/pub47761/

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 3398.76 MB
- **Size of the generated dataset:** 3647.70 MB
- **Total amount of disk used:** 7046.46 MB

An example of 'validation' looks as follows.
```
{
    "label": 0,
    "question": "when did somewhere over the rainbow come out",
    "sentence": "In films and TV shows ( edit ) In the film Third Finger , Left Hand ( 1940 ) with Myrna Loy , Melvyn Douglas , and Raymond Walburn , the tune played throughout the film in short sequences .",
    "sentence_in_long_answer": false,
    "short_answer_in_sentence": false
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `question`: a `string` feature.
- `sentence`: a `string` feature.
- `label`: a classification label, with possible values including `neg` (0), `pos` (1).
- `sentence_in_long_answer`: a `bool` feature.
- `short_answer_in_sentence`: a `bool` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  | train  |validation|
|-------|-------:|---------:|
|default|20377568|    930062|

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
@article{garg2019tanda,
    title={TANDA: Transfer and Adapt Pre-Trained Transformer Models for Answer Sentence Selection},
    author={Siddhant Garg and Thuy Vu and Alessandro Moschitti},
    year={2019},
    eprint={1911.04118},
}

```


### Contributions

Thanks to [@mkserge](https://github.com/mkserge) for adding this dataset.