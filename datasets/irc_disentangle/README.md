---
annotations_creators:
- expert-generated
language_creators:
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
- original
task_categories:
- token-classification
task_ids:
- token-classification-other-conversation-disentanglement
paperswithcode_id: irc-disentanglement
pretty_name: IRC Disentanglement
---


# Dataset Card for IRC Disentanglement

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
  - [Acknowledgments](#acknowledgments)

## Dataset Description

- **Homepage:** https://jkk.name/irc-disentanglement/
- **Repository:** https://github.com/jkkummerfeld/irc-disentanglement/tree/master/data
- **Paper:** https://aclanthology.org/P19-1374/
- **Leaderboard:** NA
- **Point of Contact:** jkummerf@umich.edu

### Dataset Summary

Disentangling conversations mixed together in a single stream of messages is a difficult task, made harder by the lack of large manually annotated datasets. This new dataset of 77,563 messages manually annotated with reply-structure graphs that both disentangle conversations and define internal conversation structure. The dataset is 16 times larger than all previously released datasets combined, the first to include adjudication of annotation disagreements, and the first to include context.

Note, the Github repository for the dataset also contains several useful tools for:

- Conversion (e.g. extracting conversations from graphs)
- Evaluation
- Preprocessing
- Word embeddings trained on the full Ubuntu logs in 2018

### Supported Tasks and Leaderboards

Conversational Disentanglement

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


The dataset has 4 parts:

| Part          | Number of Annotated Messages                |
| ------------- | ------------------------------------------- |
| Train         | 67,463                                      |
| Dev           |  2,500                                      |
| Test          |  5,000                                      |
| Channel 2     |  2,600                                      |


## Dataset Creation

### Curation Rationale

IRC is a synchronous chat setting with a long history of use.
Several channels log all messages and make them publicly available.
The Ubuntu channel is particularly heavily used and has been the subject of several academic studies.

Data was selected from the channel in order to capture the diversity of situations in the channel (e.g. when there are many users or very few users).
For full details, see the [annotation information page](https://github.com/jkkummerfeld/irc-disentanglement/blob/master/data/READ.history.md).

### Source Data

#### Initial Data Collection and Normalization

Data was collected from the Ubuntu IRC channel logs, which are publicly available at [https://irclogs.ubuntu.com/](https://irclogs.ubuntu.com/).
The raw files are included, as well as two other versions:

- ASCII, converted using the script [make_txt.py](https://github.com/jkkummerfeld/irc-disentanglement/blob/master/tools/preprocessing/make-txt.py)
- Tok, tokenised text with rare words replaced by UNK using the script [dstc8-tokenise.py](https://github.com/jkkummerfeld/irc-disentanglement/blob/master/tools/preprocessing/dstc8-tokenise.py)

The raw channel two data is from prior work [(Elsner and Charniak, 2008)](https://www.aclweb.org/anthology/P08-1095.pdf)].

#### Who are the source language producers?

The text is from a large group of internet users asking questions and providing answers related to Ubuntu.

### Annotations

#### Annotation process

The data is expert annotated with:

- Training, one annotation per line in general, a small portion is double-annotated and adjudicated
- Dev, Channel 2, double annotated and adjudicated
- Test, triple annotated and adjudicated

| Part          | Annotators      | Adjudication?                         |
| ------------- | --------------- | ------------------------------------- |
| Train         | 1 or 2 per file | For files with 2 annotators (only 10) |
| Dev           | 2               | Yes                                   |
| Test          | 3               | Yes                                   |
| Channel 2     | 2               | Yes                                   |

#### Who are the annotators?

Students and a postdoc at the University of Michigan.
Everyone involved went through a training process with feedback to learn the annotation guidelines.

### Personal and Sensitive Information

No content is removed or obfuscated.
There is probably personal information in the dataset from users.

## Considerations for Using the Data

### Social Impact of Dataset

The raw data is already available online and the annotations do not significantly provide additional information that could have a direct social impact.

### Discussion of Biases

The data is mainly from a single technical domain (Ubuntu tech support) that probably has a demographic skew of some sort.
Given that users are only identified by their self-selected usernames, it is difficult to know more about the authors.

### Other Known Limitations

Being focused on a single language and a single channel means that the data is likely capturing a particular set of conventions in communication.
Those conventions may not apply to other channels, or beyond IRC.

## Additional Information

### Dataset Curators

Jonathan K. Kummerfeld

### Licensing Information

Creative Commons Attribution 4.0

### Citation Information

```
@inproceedings{kummerfeld-etal-2019-large,
    title = "A Large-Scale Corpus for Conversation Disentanglement",
    author = "Kummerfeld, Jonathan K.  and
      Gouravajhala, Sai R.  and
      Peper, Joseph J.  and
      Athreya, Vignesh  and
      Gunasekara, Chulaka  and
      Ganhotra, Jatin  and
      Patel, Siva Sankalp  and
      Polymenakos, Lazaros C  and
      Lasecki, Walter",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P19-1374",
    doi = "10.18653/v1/P19-1374",
    pages = "3846--3856",
    arxiv = "https://arxiv.org/abs/1810.11118",
    software = "https://jkk.name/irc-disentanglement",
    data = "https://jkk.name/irc-disentanglement",
    abstract = "Disentangling conversations mixed together in a single stream of messages is a difficult task, made harder by the lack of large manually annotated datasets. We created a new dataset of 77,563 messages manually annotated with reply-structure graphs that both disentangle conversations and define internal conversation structure. Our data is 16 times larger than all previously released datasets combined, the first to include adjudication of annotation disagreements, and the first to include context. We use our data to re-examine prior work, in particular, finding that 89{\%} of conversations in a widely used dialogue corpus are either missing messages or contain extra messages. Our manually-annotated data presents an opportunity to develop robust data-driven methods for conversation disentanglement, which will help advance dialogue research.",
}
```

### Contributions

Thanks to [@dhruvjoshi1998](https://github.com/dhruvjoshi1998) for adding this dataset.

Thanks to [@jkkummerfeld](https://github.com/jkkummerfeld) for improvements to the documentation.


### Acknowledgments

This material is based in part upon work supported by IBM under contract 4915012629. Any opinions, findings, conclusions or recommendations expressed are those of the authors and do not necessarily reflect the views of IBM.
