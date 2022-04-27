---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- other-for-non-commercial-research-and-educational-purposes-only
multilinguality:
- monolingual
pretty_name: Multi-News
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- summarization
task_ids:
- news-articles-summarization
paperswithcode_id: multi-news
---

# Dataset Card for Multi-News

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

- **Homepage:** [https://github.com/Alex-Fabbri/Multi-News](https://github.com/Alex-Fabbri/Multi-News)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 245.06 MB
- **Size of the generated dataset:** 667.74 MB
- **Total amount of disk used:** 912.80 MB

### Dataset Summary

Multi-News, consists of news articles and human-written summaries
of these articles from the site newser.com.
Each summary is professionally written by editors and
includes links to the original articles cited.

There are two features:
  - document: text of news articles seperated by special token "|||||".
  - summary: news summary.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### default

- **Size of downloaded dataset files:** 245.06 MB
- **Size of the generated dataset:** 667.74 MB
- **Total amount of disk used:** 912.80 MB

An example of 'validation' looks as follows.
```
{
    "document": "some line val \n another line",
    "summary": "target val line"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `document`: a `string` feature.
- `summary`: a `string` feature.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|44972|      5622|5622|

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

```
This Dataset Usage Agreement ("Agreement") is a legal agreement with LILY LAB for the Dataset made available to the individual or entity ("Researcher") exercising rights under this Agreement. "Dataset" includes all text, data, information, source code, and any related materials, documentation, files, media, updates or revisions.

The Dataset is intended for non-commercial research and educational purposes only, and is made available free of charge without extending any license or other intellectual property rights. By downloading or using the Dataset, the Researcher acknowledges that they agree to the terms in this Agreement, and represent and warrant that they have authority to do so on behalf of any entity exercising rights under this Agreement. The Researcher accepts and agrees to be bound by the terms and conditions of this Agreement. If the Researcher does not agree to this Agreement, they may not download or use the Dataset.

By sharing content with m, such as by submitting content to this site or by corresponding with LILY LAB contributors, the Researcher grants LILY LAB the right to use, reproduce, display, perform, adapt, modify, distribute, have distributed, and promote the content in any form, anywhere and for any purpose, such as for evaluating and comparing summarization systems. Nothing in this Agreement shall obligate LILY LAB to provide any support for the Dataset. Any feedback, suggestions, ideas, comments, improvements given by the Researcher related to the Dataset is voluntarily given, and may be used by LILY LAB without obligation or restriction of any kind.

The Researcher accepts full responsibility for their use of the Dataset and shall defend indemnify, and hold harmless m, including their employees, trustees, officers, and agents, against any and all claims arising from the Researcher's use of the Dataset. The Researcher agrees to comply with all laws and regulations as they relate to access to and use of the Dataset and Service including U.S. export jurisdiction and other U.S. and international regulations.

THE DATASET IS PROVIDED "AS IS." LILY LAB DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WITHOUT LIMITATION OF THE ABOVE, LILY LAB DISCLAIMS ANY WARRANTY THAT DATASET IS BUG OR ERROR-FREE, AND GRANTS NO WARRANTY REGARDING ITS USE OR THE RESULTS THEREFROM INCLUDING, WITHOUT LIMITATION, ITS CORRECTNESS, ACCURACY, OR RELIABILITY. THE DATASET IS NOT WARRANTIED TO FULFILL ANY PARTICULAR PURPOSES OR NEEDS.

TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT SHALL LILY LAB BE LIABLE FOR ANY LOSS, DAMAGE OR INJURY, DIRECT AND INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER FOR BREACH OF CONTRACT, TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, ARISING OUT OF THIS AGREEMENT, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THESE LIMITATIONS SHALL APPLY NOTWITHSTANDING ANY FAILURE OF ESSENTIAL PURPOSE OF ANY LIMITED REMEDY.

This Agreement is effective until terminated. LILY LAB reserves the right to terminate the Researcher's access to the Dataset at any time. If the Researcher breaches this Agreement, the Researcher's rights to use the Dataset shall terminate automatically. The Researcher will immediately cease all use and distribution of the Dataset and destroy any copies or portions of the Dataset in their possession.

This Agreement is governed by the laws of the SOME_PLACE, without regard to conflict of law principles. All terms and provisions of this Agreement shall, if possible, be construed in a manner which makes them valid, but in the event any term or provision of this Agreement is found by a court of competent jurisdiction to be illegal or unenforceable, the validity or enforceability of the remainder of this Agreement shall not be affected.

This Agreement is the complete and exclusive agreement between the parties with respect to its subject matter and supersedes all prior or contemporaneous oral or written agreements or understandings relating to the subject matter.
```

### Citation Information

```

@misc{alex2019multinews,
    title={Multi-News: a Large-Scale Multi-Document Summarization Dataset and Abstractive Hierarchical Model},
    author={Alexander R. Fabbri and Irene Li and Tianwei She and Suyi Li and Dragomir R. Radev},
    year={2019},
    eprint={1906.01749},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
