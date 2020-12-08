---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|wikipedia
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
---

# Dataset Card Creation Guide

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [ROPES dataset](https://allenai.org/data/ropes)
- **Paper:** [Reasoning Over Paragraph Effects in Situations](https://arxiv.org/abs/1908.05852)
- **Leaderboard:** [ROPES leaderboard](https://leaderboard.allenai.org/ropes)

### Dataset Summary

ROPES (Reasoning Over Paragraph Effects in Situations) is a QA dataset which tests a system's ability to apply knowledge from a passage of text to a new situation. A system is presented a background passage containing a causal or qualitative relation(s) (e.g., "animal pollinators increase efficiency of fertilization in flowers"), a novel situation that uses this background, and questions that require reasoning about effects of the relationships in the background passage in the context of the situation.

### Supported Tasks and Leaderboards

The reading comprehension task is framed as an extractive question answering problem.

Models are evaluated by computing word-level F1 and exact match (EM) metrics, following common practice for recent reading comprehension datasets (e.g., SQuAD).

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

Data closely follow the SQuAD v1.1 format. An example looks like this:

```
{
  "id": "2058517998",
  "background": "Cancer is a disease that causes cells to divide out of control. Normally, the body has systems that prevent cells from dividing out of control. But in the case of cancer, these systems fail. Cancer is usually caused by mutations. Mutations are random errors in genes. Mutations that lead to cancer usually happen to genes that control the cell cycle. Because of the mutations, abnormal cells divide uncontrollably. This often leads to the development of a tumor. A tumor is a mass of abnormal tissue. As a tumor grows, it may harm normal tissues around it. Anything that can cause cancer is called a carcinogen . Carcinogens may be pathogens, chemicals, or radiation.",
  "situation": "Jason recently learned that he has cancer. After hearing this news, he convinced his wife, Charlotte, to get checked out. After running several tests, the doctors determined Charlotte has no cancer, but she does have high blood pressure. Relieved at this news, Jason was now focused on battling his cancer and fighting as hard as he could to survive.",
  "question": "Whose cells are dividing more rapidly?",
  "answers": {
    "text": ["Jason"]
  },
}
```

### Data Fields

- `id`: identification
- `background`: background passage
- `situation`: the grounding situation
- `question`: the question to answer
- `answers`: the answer text which is a span from either the situation or the question. The text list always contain a single element.

Note that the answers for the test set are hidden (and thus represented as an empty list). Predictions for the test set should be submitted to the leaderboard.

### Data Splits

The dataset contains 14k QA pairs over 1.7K paragraphs, split between train (10k QAs), development (1.6k QAs) and a hidden test partition (1.7k QAs).

## Dataset Creation

### Curation Rationale

From the original paper:

*ROPES challenges reading comprehension models to handle more difficult phenomena: understanding the implications of a passage of text. ROPES is also particularly related to datasets focusing on "multi-hop reasoning", as by construction answering questions in ROPES requires connecting information from multiple parts of a given passage.*

*We constructed ROPES by first collecting background passages from science textbooks and Wikipedia articles that describe causal relationships. We showed the collected paragraphs to crowd workers and asked them to write situations that involve the relationships found in the background passage, and questions that connect the situation and the background using the causal relationships. The answers are spans from either the situation or the question. The dataset consists of 14,322 questions from various domains, mostly in science and economics.*

### Source Data

From the original paper:

*We automatically scraped passages from science textbooks and Wikipedia that contained causal connectives eg. ”causes,” ”leads to,” and keywords that signal qualitative relations, e.g. ”increases,” ”decreases.”. We then manually filtered out the passages that do not have at least one relation. The passages can be categorized into physical science (49%), life science (45%), economics (5%) and other (1%). In total, we collected over 1,000 background passages.*

#### Initial Data Collection and Normalization

From the original paper:

*We used Amazon Mechanical Turk (AMT) to generate the situations, questions, and answers. The AMT workers were given background passages and asked to write situations that involved the relation(s) in the background passage. The AMT workers then authored questions about the situation that required both the background and the situation to answer. In each human intelligence task (HIT), AMT workers are given 5 background passages to select from and are asked to create a total of 10 questions. To mitigate the potential for easy lexical shortcuts in the dataset, the workers were encouraged via instructions to write questions in minimal pairs, where a very small change in the question results in a different answer.*

*Most questions are designed to have two sensible answer choices (eg. “more” vs. “less”).*

To reduce annotator bias, training and evaluation sets are writter by different annotators.

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The data is distributed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

### Citation Information

```
@inproceedings{Lin2019ReasoningOP,
  title={Reasoning Over Paragraph Effects in Situations},
  author={Kevin Lin and Oyvind Tafjord and Peter Clark and Matt Gardner},
  booktitle={MRQA@EMNLP},
  year={2019}
}
```
