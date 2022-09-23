---
annotations_creators:
- machine-generated
language:
- en
language_creators:
- found
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: WikiSplit
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text2text-generation
task_ids:
- text2text-generation-other-split-and-rephrase
paperswithcode_id: wikisplit
dataset_info:
  features:
  - name: complex_sentence
    dtype: string
  - name: simple_sentence_1
    dtype: string
  - name: simple_sentence_2
    dtype: string
  splits:
  - name: test
    num_bytes: 1949294
    num_examples: 5000
  - name: train
    num_bytes: 384513073
    num_examples: 989944
  - name: validation
    num_bytes: 1935459
    num_examples: 5000
  download_size: 100279164
  dataset_size: 388397826
---

# Dataset Card for "wiki_split"

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

- **Homepage:** [https://dataset-homepage/](https://dataset-homepage/)
- **Repository:** https://github.com/google-research-datasets/wiki-split
- **Paper:** [Learning To Split and Rephrase From Wikipedia Edit History](https://arxiv.org/abs/1808.09468)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 95.63 MB
- **Size of the generated dataset:** 370.41 MB
- **Total amount of disk used:** 466.04 MB

### Dataset Summary

One million English sentences, each split into two sentences that together preserve the original meaning, extracted from Wikipedia
Google's WikiSplit dataset was constructed automatically from the publicly available Wikipedia revision history. Although
the dataset contains some inherent noise, it can serve as valuable training data for models that split or merge sentences.

### Supported Tasks and Leaderboards

- Split and Rephrase

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 95.63 MB
- **Size of the generated dataset:** 370.41 MB
- **Total amount of disk used:** 466.04 MB

An example of 'train' looks as follows.
```
{
    "complex_sentence": " '' As she translates from one language to another , she tries to find the appropriate wording and context in English that would correspond to the work in Spanish her poems and stories started to have differing meanings in their respective languages .",
    "simple_sentence_1": "' '' As she translates from one language to another , she tries to find the appropriate wording and context in English that would correspond to the work in Spanish . ",
    "simple_sentence_2": " Ergo , her poems and stories started to have differing meanings in their respective languages ."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `complex_sentence`: a `string` feature.
- `simple_sentence_1`: a `string` feature.
- `simple_sentence_2`: a `string` feature.

### Data Splits

| name  |train |validation|test|
|-------|-----:|---------:|---:|
|default|989944|      5000|5000|

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

The WikiSplit dataset is a verbatim copy of certain content from the publicly available Wikipedia revision history. 
The dataset is therefore licensed under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/). 
Any third party content or data is provided "As Is" without any warranty, express or implied.

### Citation Information

```
@inproceedings{botha-etal-2018-learning,
    title = "Learning To Split and Rephrase From {W}ikipedia Edit History",
    author = "Botha, Jan A.  and
      Faruqui, Manaal  and
      Alex, John  and
      Baldridge, Jason  and
      Das, Dipanjan",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D18-1080",
    doi = "10.18653/v1/D18-1080",
    pages = "732--737",
}
```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@albertvillanova](https://github.com/albertvillanova), [@lewtun](https://github.com/lewtun) for adding this dataset.