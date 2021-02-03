---
---

# Dataset Card for "bookcorpusopen"

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

- **Homepage:** [https://github.com/soskek/bookcorpus/issues/27](https://github.com/soskek/bookcorpus/issues/27)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2292.89 MB
- **Size of the generated dataset:** 6336.36 MB
- **Total amount of disk used:** 8629.25 MB

### [Dataset Summary](#dataset-summary)

Books are a rich source of both fine-grained information, how a character, an object or a scene looks like, as well as high-level semantics, what someone is thinking, feeling and how these states evolve through a story.
This version of bookcorpus has 17868 dataset items (books). Each item contains two fields: title and text. The title is the name of the book (just the file name) while text contains unprocessed book text. The bookcorpus has been prepared by Shawn Presser and is generously hosted by The-Eye. The-Eye is a non-profit, community driven platform dedicated to the archiving and long-term preservation of any and all data including but by no means limited to... websites, books, games, software, video, audio, other digital-obscura and ideas.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### plain_text

- **Size of downloaded dataset files:** 2292.89 MB
- **Size of the generated dataset:** 6336.36 MB
- **Total amount of disk used:** 8629.25 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "text": "\"\\n\\nzONE\\n\\n## The end and the beginning\\n\\nby\\n\\nPhilip F. Blood\\n\\nSMASHWORDS EDITION\\n\\nVersion 3.55\\n\\nPUBLISHED BY:\\n\\nPhi...",
    "title": "zone-the-end-and-the-beginning.epub.txt"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### plain_text
- `title`: a `string` feature.
- `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|   name   |train|
|----------|----:|
|plain_text|17868|

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
@InProceedings{Zhu_2015_ICCV,
    title = {Aligning Books and Movies: Towards Story-Like Visual Explanations by Watching Movies and Reading Books},
    author = {Zhu, Yukun and Kiros, Ryan and Zemel, Rich and Salakhutdinov, Ruslan and Urtasun, Raquel and Torralba, Antonio and Fidler, Sanja},
    booktitle = {The IEEE International Conference on Computer Vision (ICCV)},
    month = {December},
    year = {2015}
}

```


### Contributions

Thanks to [@vblagoje](https://github.com/vblagoje) for adding this dataset.