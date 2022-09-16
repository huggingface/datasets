---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
paperswithcode_id: null
pretty_name: Reddit Webis-TLDR-17
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- summarization
task_ids:
- summarization-other-reddit-posts-summarization
train-eval-index:
- config: default
  task: summarization
  task_id: summarization
  splits:
    train_split: train
  col_mapping:
    content: text
    summary: target
  metrics:
    - type: rouge
      name: Rouge
---

# Dataset Card for Reddit Webis-TLDR-17

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

- **Homepage:** [https://webis.de/data/webis-tldr-17.html](https://webis.de/data/webis-tldr-17.html)
- **Repository:** [https://github.com/webis-de/webis-tldr-17-corpus](https://github.com/webis-de/webis-tldr-17-corpus)
- **Paper:** [https://aclanthology.org/W17-4508]
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2996.31 MB
- **Size of the generated dataset:** 18063.11 MB
- **Total amount of disk used:** 21059.41 MB

### Dataset Summary

This corpus contains preprocessed posts from the Reddit dataset (Webis-TLDR-17).
The dataset consists of 3,848,330 posts with an average length of 270 words for content,
and 28 words for the summary.

Features includes strings: author, body, normalizedBody, content, summary, subreddit, subreddit_id.
Content is used as document and summary is used as summary.

### Supported Tasks and Leaderboards

Summarization (abstractive)

Known ROUGE scores achieved for the Webis-TLDR-17:

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Paper/Source |
|-------|-------|-------|-------|------:|
| Transformer + Copy (Gehrmann et al., 2019) | 22 | 6 | 17 | Generating Summaries with Finetuned Language Models | 	
| Unified VAE + PGN (Choi et al., 2019) |	19 | 4 | 15 | VAE-PGN based Abstractive Model in Multi-stage Architecture for Text Summarization | 	

(Source: https://github.com/sebastianruder/NLP-progress/blob/master/english/summarization.md)

### Languages

English

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 2996.31 MB
- **Size of the generated dataset:** 18063.11 MB
- **Total amount of disk used:** 21059.41 MB

An example of 'train' looks as follows.
```
{
    "author": "me",
    "body": "<>",
    "content": "input document.",
    "id": "1",
    "normalizedBody": "",
    "subreddit": "machinelearning",
    "subreddit_id": "2",
    "summary": "output summary."
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `author`: a `string` feature.
- `body`: a `string` feature.
- `normalizedBody`: a `string` feature.
- `subreddit`: a `string` feature.
- `subreddit_id`: a `string` feature.
- `id`: a `string` feature.
- `content`: a `string` feature.
- `summary`: a `string` feature.

### Data Splits

| name  | train |
|-------|------:|
|default|3848330|

This corpus does not contain a separate test set. Thus it is up to the users to divide the corpus into appropriate training, validation and test sets.

## Dataset Creation

### Curation Rationale

In the scope of the task of absractive summarization the creators of the Webis-TLDR-17 propose mining social media for author-provided summaries and taking advantage of the common practice of appending a "TL;DR" to long posts. A large Reddit crawl was used to yield the Webis-TLDR-17 corpus. This dataset intends to complement the existing summarization corpora primarily from the news genre.

### Source Data

Reddit subreddits posts (submissions & comments) containing "TL;DR" from 2006 to 2016. Multiple subreddits are included.

#### Initial Data Collection and Normalization

Initial data: a set of 286 million submissions and 1.6 billion comments posted to Reddit between 2006 and 2016.
Then a five-step pipeline of consecutive filtering steps was applied.

#### Who are the source language producers?

The contents of the dataset are produced by human authors, bot-generated content was eliminated by filtering out all bot accounts with the help of an extensive list provided by the Reddit community, as well as manual inspection of cases where the user name contained the substring "bot."

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

This dataset has been created to serve as a source of large-scale summarization training data. It is primarily geared towards the automatic abstractive summarization task, that can be considered one of the most challenging variants of automatic summarization. It also aims to tackle the lack of genre diversity in the summarization datasets (most are news-related).

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

Reddit users write TL;DRs with various intentions, such as providing a “true” summary, asking questions or for help, or forming judgments and conclusions. As noted in the paper introducing the dataset, although the first kind of TL;DR posts are most important for training summarization models, yet, the latter allow for various alternative summarization-related tasks.

Although filtering was performed abusive language maybe still be present.

## Additional Information

### Dataset Curators

Michael Völske, Martin Potthast, Shahbaz Syed, Benno Stein

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```

@inproceedings{volske-etal-2017-tl,
    title = "{TL};{DR}: Mining {R}eddit to Learn Automatic Summarization",
    author = {V{"o}lske, Michael  and
      Potthast, Martin  and
      Syed, Shahbaz  and
      Stein, Benno},
    booktitle = "Proceedings of the Workshop on New Frontiers in Summarization",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-4508",
    doi = "10.18653/v1/W17-4508",
    pages = "59--63",
    abstract = "Recent advances in automatic text summarization have used deep neural networks to generate high-quality abstractive summaries, but the performance of these models strongly depends on large amounts of suitable training data. We propose a new method for mining social media for author-provided summaries, taking advantage of the common practice of appending a {``}TL;DR{''} to long posts. A case study using a large Reddit crawl yields the Webis-TLDR-17 dataset, complementing existing corpora primarily from the news genre. Our technique is likely applicable to other social media sites and general web crawls.",
}

```


### Contributions

Thanks to [@mariamabarham](https://github.com/mariamabarham), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
