---
pretty_name: Children’s Book Test (CBT)
annotations_creators:
- machine-generated
language_creators:
- found
language:
- en
license:
- gfdl
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- n<1K
source_datasets:
- original
task_categories:
- other
- question-answering
task_ids:
- multiple-choice-qa
- other-other-raw-dataset
paperswithcode_id: cbt
configs:
- CN
- NE
- P
- V
- raw
---

# Dataset Card for CBT

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

- **Homepage:**[The bAbI project](https://research.fb.com/downloads/babi/)
- **Repository:**
- **Paper:** [arXiv Paper](https://arxiv.org/pdf/1511.02301.pdf)
- **Leaderboard:**
- **Point of Contact:** [Felix Hill](mailto:felix.hill@cl.cam.ac.uk) or [Antoine Bordes](mailto:abordes@fb.com).

### Dataset Summary

The Children’s Book Test (CBT) is designed to measure directly how well language models can exploit wider linguistic context. The CBT is built from books that are freely available.

This dataset contains four different configurations:

- `V`: where the answers to the questions are verbs.
- `P`: where the answers to the questions are pronouns.
- `NE`: where the answers to the questions are named entities.
- `CN`: where the answers to the questions are common nouns.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The data is present in English language as written by authors Lucy Maud Montgomery, Charles Dickens,Andrew Lang, etc. in story books for children.

## Dataset Structure

### Data Instances

An instance from the `V` config:
```
{'answer': 'said', 'options': ['christening', 'existed', 'hear', 'knows', 'read', 'remarked', 'said', 'sitting', 'talking', 'wearing'], 'question': "`` They are very kind old ladies in their way , '' XXXXX the king ; `` and were nice to me when I was a boy . ''", 'sentences': ['This vexed the king even more than the queen , who was very clever and learned , and who had hated dolls when she was a child .', 'However , she , too in spite of all the books she read and all the pictures she painted , would have been glad enough to be the mother of a little prince .', 'The king was anxious to consult the fairies , but the queen would not hear of such a thing .', 'She did not believe in fairies : she said that they had never existed ; and that she maintained , though The History of the Royal Family was full of chapters about nothing else .', 'Well , at long and at last they had a little boy , who was generally regarded as the finest baby that had ever been seen .', 'Even her majesty herself remarked that , though she could never believe all the courtiers told her , yet he certainly was a fine child -- a very fine child .', 'Now , the time drew near for the christening party , and the king and queen were sitting at breakfast in their summer parlour talking over it .', 'It was a splendid room , hung with portraits of the royal ancestors .', 'There was Cinderella , the grandmother of the reigning monarch , with her little foot in her glass slipper thrust out before her .', 'There was the Marquis de Carabas , who , as everyone knows , was raised to the throne as prince consort after his marriage with the daughter of the king of the period .', 'On the arm of the throne was seated his celebrated cat , wearing boots .', 'There , too , was a portrait of a beautiful lady , sound asleep : this was Madame La Belle au Bois-dormant , also an ancestress of the royal family .', 'Many other pictures of celebrated persons were hanging on the walls .', "`` You have asked all the right people , my dear ? ''", 'said the king .', "`` Everyone who should be asked , '' answered the queen .", "`` People are so touchy on these occasions , '' said his majesty .", "`` You have not forgotten any of our aunts ? ''", "`` No ; the old cats ! ''", "replied the queen ; for the king 's aunts were old-fashioned , and did not approve of her , and she knew it ."]}
```


### Data Fields

For the `raw` config, the data fields are:
- `title`: a `string` feature containing the title of the book present in the dataset.
- `content`: a `string` feature containing the content of the book present in the dataset.

For all other configs, the data fields are:
- `sentences`: a `list` of `string` features containing 20 sentences from a book.
- `question`: a `string` feature containing a question with blank marked as `XXXX` which is to be filled with one of the options.
- `answer`: a `string` feature containing the answer.
- `options`: a `list` of `string` features containing the options for the question.


### Data Splits

The splits and corresponding sizes are:

|   |train  |test |validation|
|:--|------:|----:|---------:|
|raw|98     |5    |5         |
|V  |105825 |2500 |2000      |
|P  |334030 |2500 |2000      |
|CN |120769 |2500 |2000      |
|NE |108719 |2500 |2000      |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Children's Book Authors

### Annotations

#### Annotation process

From the [homepage](https://research.fb.com/downloads/babi/):

>After allocating books to either training, validation or test sets, we formed example ‘questions’ from chapters in the book by enumerating 21 consecutive sentences. In each question, the first 20 sentences form the context, and a word is removed from the 21st sentence, which becomes the query. Models must identify the answer word among a selection of 10 candidate answers appearing in the context sentences and the query. For finer-grained analyses, we evaluated four classes of question by removing distinct types of word: Named Entities, (Common) Nouns, Verbs and Prepositions.

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

```
GNU Free Documentation License v1.3
```
### Citation Information

```
@misc{hill2016goldilocks,
      title={The Goldilocks Principle: Reading Children's Books with Explicit Memory Representations}, 
      author={Felix Hill and Antoine Bordes and Sumit Chopra and Jason Weston},
      year={2016},
      eprint={1511.02301},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.
