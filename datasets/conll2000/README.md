---
---

# Dataset Card for "conll2000"

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

- **Homepage:** [https://www.clips.uantwerpen.be/conll2000/chunking/](https://www.clips.uantwerpen.be/conll2000/chunking/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3.32 MB
- **Size of the generated dataset:** 6.25 MB
- **Total amount of disk used:** 9.57 MB

### [Dataset Summary](#dataset-summary)

 Text chunking consists of dividing a text in syntactically correlated parts of words. For example, the sentence
 He reckons the current account deficit will narrow to only # 1.8 billion in September . can be divided as follows:
[NP He ] [VP reckons ] [NP the current account deficit ] [VP will narrow ] [PP to ] [NP only # 1.8 billion ]
[PP in ] [NP September ] .

Text chunking is an intermediate step towards full parsing. It was the shared task for CoNLL-2000. Training and test
data for this task is available. This data consists of the same partitions of the Wall Street Journal corpus (WSJ)
as the widely used data for noun phrase chunking: sections 15-18 as training data (211727 tokens) and section 20 as
test data (47377 tokens). The annotation of the data has been derived from the WSJ corpus by a program written by
Sabine Buchholz from Tilburg University, The Netherlands.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### conll2000

- **Size of downloaded dataset files:** 3.32 MB
- **Size of the generated dataset:** 6.25 MB
- **Total amount of disk used:** 9.57 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "chunk_tags": [11, 13, 11, 12, 21, 22, 22, 22, 22, 11, 12, 12, 17, 11, 12, 13, 11, 0, 1, 13, 11, 11, 0, 21, 22, 22, 11, 12, 12, 13, 11, 12, 12, 11, 12, 12, 0],
    "id": "0",
    "pos_tags": [19, 14, 11, 19, 39, 27, 37, 32, 34, 11, 15, 19, 14, 19, 22, 14, 20, 5, 15, 14, 19, 19, 5, 34, 32, 34, 11, 15, 19, 14, 20, 9, 20, 24, 15, 22, 6],
    "tokens": "[\"Confidence\", \"in\", \"the\", \"pound\", \"is\", \"widely\", \"expected\", \"to\", \"take\", \"another\", \"sharp\", \"dive\", \"if\", \"trade\", \"figur..."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### conll2000
- `id`: a `string` feature.
- `tokens`: a `list` of `string` features.
- `pos_tags`: a `list` of classification labels, with possible values including `''` (0), `#` (1), `$` (2), `(` (3), `)` (4).
- `chunk_tags`: a `list` of classification labels, with possible values including `O` (0), `B-ADJP` (1), `I-ADJP` (2), `B-ADVP` (3), `I-ADVP` (4).

### [Data Splits Sample Size](#data-splits-sample-size)

|  name   |train|test|
|---------|----:|---:|
|conll2000| 8937|2013|

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
@inproceedings{tksbuchholz2000conll,
   author     = "Tjong Kim Sang, Erik F. and Sabine Buchholz",
   title      = "Introduction to the CoNLL-2000 Shared Task: Chunking",
   editor     = "Claire Cardie and Walter Daelemans and Claire
                 Nedellec and Tjong Kim Sang, Erik",
   booktitle  = "Proceedings of CoNLL-2000 and LLL-2000",
   publisher  = "Lisbon, Portugal",
   pages      = "127--132",
   year       = "2000"
}

```


### Contributions

Thanks to [@vblagoje](https://github.com/vblagoje), [@jplu](https://github.com/jplu) for adding this dataset.