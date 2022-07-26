---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- other
multilinguality:
- monolingual
pretty_name: CORNELL NEWSROOM
size_categories:
- unknown
source_datasets:
- original
task_categories:
- summarization
task_ids:
- news-articles-summarization
paperswithcode_id: newsroom
---

# Dataset Card for "newsroom"

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

- **Homepage:** [https://summari.es](https://summari.es)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 5057.49 MB
- **Total amount of disk used:** 5057.49 MB

### Dataset Summary

NEWSROOM is a large dataset for training and evaluating summarization systems.
It contains 1.3 million articles and summaries written by authors and
editors in the newsrooms of 38 major publications.

Dataset features includes:
  - text: Input news text.
  - summary: Summary for the news.
And additional features:
  - title: news title.
  - url: url of the news.
  - date: date of the article.
  - density: extractive density.
  - coverage: extractive coverage.
  - compression: compression ratio.
  - density_bin: low, medium, high.
  - coverage_bin: extractive, abstractive.
  - compression_bin: low, medium, high.

This dataset can be downloaded upon requests. Unzip all the contents
"train.jsonl, dev.josnl, test.jsonl" to the `tfds` folder.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

English (`en`).

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 0.00 MB
- **Size of the generated dataset:** 5057.49 MB
- **Total amount of disk used:** 5057.49 MB

An example of 'train' looks as follows.
```
{
    "compression": 33.880001068115234,
    "compression_bin": "medium",
    "coverage": 1.0,
    "coverage_bin": "high",
    "date": "200600000",
    "density": 11.720000267028809,
    "density_bin": "extractive",
    "summary": "some summary 1",
    "text": "some text 1",
    "title": "news title 1",
    "url": "url.html"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `text`: a `string` feature.
- `summary`: a `string` feature.
- `title`: a `string` feature.
- `url`: a `string` feature.
- `date`: a `string` feature.
- `density_bin`: a `string` feature.
- `coverage_bin`: a `string` feature.
- `compression_bin`: a `string` feature.
- `density`: a `float32` feature.
- `coverage`: a `float32` feature.
- `compression`: a `float32` feature.

### Data Splits

| name  |train |validation| test |
|-------|-----:|---------:|-----:|
|default|995041|    108837|108862|

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

https://cornell.qualtrics.com/jfe/form/SV_6YA3HQ2p75XH4IR

This Dataset Usage Agreement ("Agreement") is a legal agreement with the Cornell Newsroom Summaries Team ("Newsroom") for the Dataset made available to the individual or entity ("Researcher") exercising rights under this Agreement. "Dataset" includes all text, data, information, source code, and any related materials, documentation, files, media, updates or revisions.

The Dataset is intended for non-commercial research and educational purposes only, and is made available free of charge without extending any license or other intellectual property rights. By downloading or using the Dataset, the Researcher acknowledges that they agree to the terms in this Agreement, and represent and warrant that they have authority to do so on behalf of any entity exercising rights under this Agreement. The Researcher accepts and agrees to be bound by the terms and conditions of this Agreement. If the Researcher does not agree to this Agreement, they may not download or use the Dataset.

By sharing content with Newsroom, such as by submitting content to this site or by corresponding with Newsroom contributors, the Researcher grants Newsroom the right to use, reproduce, display, perform, adapt, modify, distribute, have distributed, and promote the content in any form, anywhere and for any purpose, such as for evaluating and comparing summarization systems. Nothing in this Agreement shall obligate Newsroom to provide any support for the Dataset. Any feedback, suggestions, ideas, comments, improvements given by the Researcher related to the Dataset is voluntarily given, and may be used by Newsroom without obligation or restriction of any kind.

The Researcher accepts full responsibility for their use of the Dataset and shall defend indemnify, and hold harmless Newsroom, including their employees, trustees, officers, and agents, against any and all claims arising from the Researcher's use of the Dataset. The Researcher agrees to comply with all laws and regulations as they relate to access to and use of the Dataset and Service including U.S. export jurisdiction and other U.S. and international regulations.

THE DATASET IS PROVIDED "AS IS." NEWSROOM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WITHOUT LIMITATION OF THE ABOVE, NEWSROOM DISCLAIMS ANY WARRANTY THAT DATASET IS BUG OR ERROR-FREE, AND GRANTS NO WARRANTY REGARDING ITS USE OR THE RESULTS THEREFROM INCLUDING, WITHOUT LIMITATION, ITS CORRECTNESS, ACCURACY, OR RELIABILITY. THE DATASET IS NOT WARRANTIED TO FULFILL ANY PARTICULAR PURPOSES OR NEEDS.

TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT SHALL NEWSROOM BE LIABLE FOR ANY LOSS, DAMAGE OR INJURY, DIRECT AND INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER FOR BREACH OF CONTRACT, TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, ARISING OUT OF THIS AGREEMENT, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THESE LIMITATIONS SHALL APPLY NOTWITHSTANDING ANY FAILURE OF ESSENTIAL PURPOSE OF ANY LIMITED REMEDY.

This Agreement is effective until terminated. Newsroom reserves the right to terminate the Researcher's access to the Dataset at any time. If the Researcher breaches this Agreement, the Researcher's rights to use the Dataset shall terminate automatically. The Researcher will immediately cease all use and distribution of the Dataset and destroy any copies or portions of the Dataset in their possession.

This Agreement is governed by the laws of the State of New York, without regard to conflict of law principles. All terms and provisions of this Agreement shall, if possible, be construed in a manner which makes them valid, but in the event any term or provision of this Agreement is found by a court of competent jurisdiction to be illegal or unenforceable, the validity or enforceability of the remainder of this Agreement shall not be affected.

This Agreement is the complete and exclusive agreement between the parties with respect to its subject matter and supersedes all prior or contemporaneous oral or written agreements or understandings relating to the subject matter.


### Citation Information

```

@inproceedings{N18-1065,
  author    = {Grusky, Max and Naaman, Mor and Artzi, Yoav},
  title     = {NEWSROOM: A Dataset of 1.3 Million Summaries
               with Diverse Extractive Strategies},
  booktitle = {Proceedings of the 2018 Conference of the
               North American Chapter of the Association for
               Computational Linguistics: Human Language Technologies},
  year      = {2018},
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@yoavartzi](https://github.com/yoavartzi), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
