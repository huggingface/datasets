---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- sequence-modeling
- structure-prediction
task_ids:
- coreference-resolution
- dialogue-modeling
---

# Dataset Card for IRC Disentanglement

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://jkk.name/irc-disentanglement/
- **Repository:** https://github.com/jkkummerfeld/irc-disentanglement/tree/master/data
- **Paper:** https://aclweb.org/anthology/papers/P/P19/P19-1374/
- **Leaderboard:** NA
- **Point of Contact:** jkummerf@umich.edu

### Dataset Summary

Disentangling conversations mixed together in a single stream of messages is a difficult task, made harder by the lack of large manually annotated datasets. This new dataset of 77,563 messages manually annotated with reply-structure graphs that both disentangle conversations and define internal conversation structure. The dataset is 16 times larger than all previously released datasets combined, the first to include adjudication of annotation disagreements, and the first to include context.

### Supported Tasks and Leaderboards

Conversational Disentanglement, Coreference Resolution, Dialogue Modeling

### Languages

English (en)

## Dataset Structure

### Data Instances

For Ubuntu:

data["train"][1050]

```
{

  'ascii': "[03:57] <Xophe> (also, I'm guessing that this isn't a good place to report minor but annoying bugs... what is?)", 

  'connections': [1048, 1054, 1055, 1072, 1073], 

  'date': '2004-12-25', 

  'id': 1050,

  'raw': "[03:57] <Xophe> (also, I'm guessing that this isn't a good place to report minor but annoying bugs... what is?)", 

  'tokenized': "<s> ( also , i 'm guessing that this is n't a good place to report minor but annoying bugs ... what is ?) </s>"

}
```

For Channel_two:

data["train"][50]

```
{

  'ascii': "[01:04] <Felicia> Chanel: i don't know off hand sorry", 

  'connections': [49, 53], 

  'id': 50,

  'raw': "[01:04] <Felicia> Chanel: i don't know off hand sorry", 

  'tokenized': "<s> <user> : i do n't know off hand sorry </s>"

}
```

### Data Fields

'id' : The id of the message, this is the value that would be in the 'connections' of associated messages.

'raw' : The original message from the IRC log, as downloaded.

'ascii' : The raw message converted to ascii (unconvertable characters are replaced with a special word).

'tokenized' : The same message with automatic tokenisation and replacement of rare words with placeholder symbols.

'connections' : The indices of linked messages.

(only ubuntu) 'date' : The date the messages are from. The labelling for each date only start after the first 1000 messages of that date.

### Data Splits

ubuntu: This data split is a new dataset introduced by the authors which labels connected messages in an online chatroom about ubuntu.

channel_two: This data split is a re-analysis of prior work on IRC-Disentanglement where issues about the previous data are resolved. The previous dataset is outlined in https://www.aclweb.org/anthology/P08-1095.pdf.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

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

Jonathan K. Kummerfeld, Sai R. Gouravajhala, Joseph Peper, Vignesh Athreya, Chulaka Gunasekara, Jatin Ganhotra, Siva Sankalp Patel, Lazaros Polymenakos, and Walter S. Lasecki

### Licensing Information

Creative Commons Attribution 4.0

### Citation Information

@InProceedings{acl19disentangle,
  author    = {Jonathan K. Kummerfeld and Sai R. Gouravajhala and Joseph Peper and Vignesh Athreya and Chulaka Gunasekara and Jatin Ganhotra and Siva Sankalp Patel and Lazaros Polymenakos and Walter S. Lasecki},
  title     = {A Large-Scale Corpus for Conversation Disentanglement},
  booktitle = {Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
  location  = {Florence, Italy},
  month     = {July},
  year      = {2019},
  doi       = {10.18653/v1/P19-1374},
  pages     = {3846--3856},
  url       = {https://aclweb.org/anthology/papers/P/P19/P19-1374/},
  arxiv     = {https://arxiv.org/abs/1810.11118},
  software  = {https://jkk.name/irc-disentanglement},
  data      = {https://jkk.name/irc-disentanglement},
}

### Contributions

Thanks to [@dhruvjoshi1998](https://github.com/dhruvjoshi1998) for adding this dataset.