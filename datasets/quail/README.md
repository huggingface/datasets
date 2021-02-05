---
---

# Dataset Card for "quail"

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

- **Homepage:** [https://text-machine-lab.github.io/blog/2020/quail/](https://text-machine-lab.github.io/blog/2020/quail/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 6.11 MB
- **Size of the generated dataset:** 28.25 MB
- **Total amount of disk used:** 34.36 MB

### [Dataset Summary](#dataset-summary)

QuAIL is a  reading comprehension dataset. QuAIL contains 15K multi-choice questions in texts 300-350 tokens long 4 domains (news, user stories, fiction, blogs).QuAIL is balanced and annotated for question types.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### quail

- **Size of downloaded dataset files:** 6.11 MB
- **Size of the generated dataset:** 28.25 MB
- **Total amount of disk used:** 34.36 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answers": ["the cousin is not friendly", "the cousin could have been pretier", "not enough information", "the cousin was too nice"],
    "context": "\"That fall came and I went back to Michigan and the school year went by and summer came and I never really thought about it. I'm...",
    "context_id": "f001",
    "correct_answer_id": 0,
    "domain": "fiction",
    "id": "f001_19",
    "metadata": {
        "author": "Joseph Devon",
        "title": "Black Eyed Susan",
        "url": "http://manybooks.net/pages/devonjother08black_eyed_susan/0.html"
    },
    "question": "After the events in the text what does the author think about the cousin?",
    "question_id": "19",
    "question_type": "Subsequent_state"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### quail
- `id`: a `string` feature.
- `context_id`: a `string` feature.
- `question_id`: a `string` feature.
- `domain`: a `string` feature.
- `author`: a `string` feature.
- `title`: a `string` feature.
- `url`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `question_type`: a `string` feature.
- `answers`: a `list` of `string` features.
- `correct_answer_id`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|name |train|challenge|validation|
|-----|----:|--------:|---------:|
|quail|10246|      556|      2164|

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
@inproceedings{DBLP:conf/aaai/RogersKDR20,
  author    = {Anna Rogers and
               Olga Kovaleva and
               Matthew Downey and
               Anna Rumshisky},
  title     = {Getting Closer to {AI} Complete Question Answering: {A} Set of Prerequisite
               Real Tasks},
  booktitle = {The Thirty-Fourth {AAAI} Conference on Artificial Intelligence, {AAAI}
               2020, The Thirty-Second Innovative Applications of Artificial Intelligence
               Conference, {IAAI} 2020, The Tenth {AAAI} Symposium on Educational
               Advances in Artificial Intelligence, {EAAI} 2020, New York, NY, USA,
               February 7-12, 2020},
  pages     = {8722--8731},
  publisher = {{AAAI} Press},
  year      = {2020},
  url       = {https://aaai.org/ojs/index.php/AAAI/article/view/6398},
  timestamp = {Thu, 04 Jun 2020 13:18:48 +0200},
  biburl    = {https://dblp.org/rec/conf/aaai/RogersKDR20.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

```


### Contributions

Thanks to [@sai-prasanna](https://github.com/sai-prasanna), [@ngdodd](https://github.com/ngdodd) for adding this dataset.