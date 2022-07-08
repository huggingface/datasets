---
annotations_creators:
- expert-generated
language_creators:
- machine-generated
language:
- en
license:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: gooaq
pretty_name: 'GooAQ: Open Question Answering with Diverse Answer Types'
---

# Dataset Card for GooAQ

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

- **Homepage:** [GooAQ 🥑: Google Answers to Google Questions!](https://github.com/allenai/gooaq)
- **Repository:** [GooAQ 🥑: Google Answers to Google Questions!](https://github.com/allenai/gooaq)
- **Paper:** [GOOAQ: Open Question Answering with Diverse Answer Types](https://arxiv.org/abs/2104.08727)
- **Point of Contact:** [Daniel Khashabi](danielk@allenai.org)

### Dataset Summary

GooAQ is a large-scale dataset with a variety of answer types. This dataset contains over
5 million questions and 3 million answers collected from Google. GooAQ questions are collected
semi-automatically from the Google search engine using its autocomplete feature. This results in
naturalistic questions of practical interest that are nonetheless short and expressed using simple
language. GooAQ answers are mined from Google's responses to our collected questions, specifically from
the answer boxes in the search results. This yields a rich space of answer types, containing both
textual answers (short and long) as well as more structured ones such as collections.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset contains samples in English only.

## Dataset Structure

### Data Instances

Each row of the data file should look like this:
```
{
  "id": 3339543,
  "question": "what is the difference between collagen and whey protein?",
  "short_answer": None,
  "answer": "The main differences between the amino acid profiles of whey and collagen are that whey contains all 9 essential amino acids, while collagen only has 8. ... Collagen is a fibrous protein found in the skin, cartilage, and bones of animals whereas whey comes from milk.",
  "answer_type": "feat_snip"
}
```
where the questions `question` are collected via Google auto-complete.
The answers responses (`short_answer` and `answer`) were collected from Google's answer boxes.
The answer types (`answer_type`) are inferred based on the html content of Google's response.
Here is the dominant types in the current dataset:
 - `feat_snip`: explanatory responses; the majoriy the question/responses are of this type.
 - `collection`: list responses (e.g., steps to accomplish something).
 - `knowledge`: typically short responses for knowledge seeking questions.
 - `unit_conv`: questions about converting units.
 - `time_conv`: questions about converting times.
 - `curr_conv`: questions about converting currencies.

 Dataset instances which are not part of dominant types are marked with -1 label.

### Data Fields

- `id`: an `int` feature.
- `question`: a `string` feature.
- `short_answer`: a `string` feature (could be None as well in some cases).
- `answer`: a `string` feature (could be None as well in some cases).
- `answer_type`: a `string` feature.

### Data Splits

Number of samples in train/validation/test set are given below:

| Split      | Number of samples |
|------------|-------------------|
| Train      | 3112679           |
| Validation | 2500              |
| Test       | 2500              |


## Dataset Creation

### Curation Rationale

While day-to-day questions come with a variety of answer types, the current question-answering (QA)
literature has failed to adequately address the answer diversity of questions. Many of the everyday questions
that humans deal with and pose to search engines have a more diverse set of responses. Their answer can be a multi-sentence description (a snippet) (e.g., ‘what is’ or ‘can you’ questions), a collection of items such as ingredients (‘what are’, ‘things to’) or of steps towards a goal such as unlocking a phone (‘how to’), etc. Even when the answer is short, it can have richer types, e.g., unit conversion, time zone conversion, or various kinds of knowledge look-up (‘how much’, ‘when is’, etc.).
Such answer type diversity is not represented in any existing dataset.

### Source Data

#### Initial Data Collection and Normalization

Construction this dataset involved two main steps, extracting questions from search auto-complete and extracting answers from answer boxes.

1) Query Extraction: To extract a rich yet natural set of questions they used Google auto-completion. They start with a seed set of question terms (e.g., “who”, “where”, etc.). They bootstrap based on this set, by repeatedly querying prefixes of previously extracted questions, in order to discover longer and richer sets of questions. Such questions extracted from the autocomplete algorithm are highly reflective of popular questions posed by users of Google. They filter out any questions shorter than 5 tokens as they are often in-complete questions. This process yields over ∼5M questions, which were collected over a span of 6 months. The average length of the questions is about 8 tokens.

2) Answer Extraction:  They rely on the Google answer boxes shown on top of the search results when the questions are issued to Google. There are a variety of answer boxes. The most common kind involves highlighted sentences (extracted from various websites) that contain the answer to a given question. These form the snippet and collection answers in GOOAQ. In some cases, the answer box shows the answer directly, possibly in addition to the textual snippet. These form theshort answers in GOOAQ.

They first scrape the search results for all questions. This is the main extraction bottleneck, which was done over a span of 2 months. Subsequently, they extract answer strings from the HTML content of the search results. Answer types are also inferred at this stage, based on the HTML tags around the answer.

#### Who are the source language producers?

Answered above.

### Annotations

#### Annotation process

Answered in above section.

#### Who are the annotators?

Since their task is focused on English, they required workers to be based in a country with a population predominantly of native English speakers (e.g., USA, Canada, UK, and Australia) and have completed at least 5000 HITs with ≥ 99% assignment approval rate. Additionally, they have a qualification test with half-a-dozen questions all of which need to be answered correctly by the annotators.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

To prevent biased judgements, they also ask the annotators to avoid using Google search (which is what they used when mined GOOAQ) when annotating the quality of shown instances.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

List the people involved in collecting the dataset and their affiliation(s). If funding information is known, include it here.

### Licensing Information

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

### Citation Information

```
@article{gooaq2021,
  title={GooAQ: Open Question Answering with Diverse Answer Types},
  author={Khashabi, Daniel and Ng, Amos and Khot, Tushar and Sabharwal, Ashish and Hajishirzi, Hannaneh and Callison-Burch, Chris},
  journal={arXiv preprint},
  year={2021}
}
```

### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.
