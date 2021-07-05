---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- abstractive-qa
paperswithcode_id: narrativeqa
---

# Dataset Card for Narrative QA

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

- **Homepage:** [NarrativeQA Homepage](https://deepmind.com/research/open-source/narrativeqa)
- **Repository:** [NarrativeQA Repo](https://github.com/deepmind/narrativeqa)
- **Paper:** [The NarrativeQA Reading Comprehension Challenge](https://arxiv.org/pdf/1712.07040.pdf)
- **Leaderboard:**
- **Point of Contact:** [Tomáš Kočiský](mailto:tkocisky@google.com) [Jonathan Schwarz](mailto:schwarzjn@google.com) [Phil Blunsom](pblunsom@google.com) [Chris Dyer](cdyer@google.com) [Karl Moritz Hermann](mailto:kmh@google.com) [Gábor Melis](mailto:melisgl@google.com) [Edward Grefenstette](mailto:etg@google.com)

### Dataset Summary

NarrativeQA is an English-lanaguage dataset of stories and corresponding questions designed to test reading comprehension, especially on long documents.

### Supported Tasks and Leaderboards

The dataset is used to test reading comprehension. There are 2 tasks proposed in the paper: "summaries only" and "stories only", depending on whether the human-generated summary or the full story text is used to answer the question.

### Languages

English

## Dataset Structure

### Data Instances

A typical data point consists of a question and answer pair along with a summary/story which can be used to answer the question. Additional information such as the url, word count, wikipedia page, are also provided.

A typical example looks like this:
```
{
    "document": {
        "id": "23jncj2n3534563110",
        "kind": "movie",
        "url": "https://www.imsdb.com/Movie%20Scripts/Name%20of%20Movie.html",
        "file_size": 80473,
        "word_count": 41000,
        "start": "MOVIE screenplay by",
        "end": ". THE END",
        "summary": {
            "text": "Joe Bloggs begins his journey exploring...",
            "tokens": ["Joe", "Bloggs", "begins", "his", "journey", "exploring",...],
            "url": "http://en.wikipedia.org/wiki/Name_of_Movie",
            "title": "Name of Movie (film)"
        },
        "text": "MOVIE screenplay by John Doe\nSCENE 1..."
    },
    "question": {
        "text": "Where does Joe Bloggs live?",
        "tokens": ["Where", "does", "Joe", "Bloggs", "live", "?"],
    },
    "answers": [
        {"text": "At home", "tokens": ["At", "home"]},
        {"text": "His house", "tokens": ["His", "house"]}
    ]
}
```

### Data Fields

- `document.id` - Unique ID for the story.
- `document.kind` - "movie" or "gutenberg" depending on the source of the story.
- `document.url` - The URL where the story was downloaded from.
- `document.file_size` - File size (in bytes) of the story.
- `document.word_count` - Number of tokens in the story.
- `document.start` - First 3 tokens of the story. Used for verifying the story hasn't been modified.
- `document.end` - Last 3 tokens of the story. Used for verifying the story hasn't been modified.
- `document.summary.text` - Text of the wikipedia summary of the story.
- `document.summary.tokens` - Tokenized version of `document.summary.text`.
- `document.summary.url` - Wikipedia URL of the summary.
- `document.summary.title` - Wikipedia Title of the summary.
- `question` - `{"text":"...", "tokens":[...]}` for the question about the story.
- `answers` - List of `{"text":"...", "tokens":[...]}` for valid answers for the question.

### Data Splits

The data is split into training, valiudation, and test sets based on story (i.e. the same story cannot appear in more than one split):

| Train  | Valid | Test  |
| ------ | ----- | ----- |
| 32747  | 3461  | 10557 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization
Stories and movies scripts were downloaded from [Project Gutenburg](https://www.gutenberg.org) and a range of movie script repositories (mainly [imsdb](http://www.imsdb.com)).

#### Who are the source language producers?

The language producers are authors of the stories and scripts as well as Amazon Turk workers for the questions.

### Annotations

#### Annotation process

Amazon Turk Workers were provided with human written summaries of the stories (To make the annotation tractable and to lead annotators towards asking non-localized questions). Stories were matched with plot summaries from Wikipedia using titles and verified the matching with help from human annotators. The annotators were asked to determine if both the story and the summary refer to a movie or a book (as some books are made into movies), or if they are the same part in a series produced in the same year. Annotators on Amazon Mechanical Turk were instructed to write 10 question–answer pairs each based solely on a given summary. Annotators were instructed to imagine that they are writing questions to test students who have read the full stories but not the summaries. We required questions that are specific enough, given the length and complexity of the narratives, and to provide adiverse set of questions about characters, events, why this happened, and so on. Annotators were encouraged to use their own words and we prevented them from copying. We asked for answers that are grammatical, complete sentences, and explicitly allowed short answers (one word, or a few-word phrase, or ashort sentence) as we think that answering with a full sentence is frequently perceived as artificial when asking about factual information. Annotators were asked to avoid extra, unnecessary information in the question or the answer, and to avoid yes/no questions or questions about the author or the actors.

#### Who are the annotators?

Amazon Mechanical Turk workers.

### Personal and Sensitive Information

None

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

The dataset is released under a [Apache-2.0 License](https://github.com/deepmind/narrativeqa/blob/master/LICENSE).

### Citation Information

```
@article{narrativeqa,
author = {Tom\'a\v s Ko\v cisk\'y and Jonathan Schwarz and Phil Blunsom and
          Chris Dyer and Karl Moritz Hermann and G\'abor Melis and
          Edward Grefenstette},
title = {The {NarrativeQA} Reading Comprehension Challenge},
journal = {Transactions of the Association for Computational Linguistics},
url = {https://TBD},
volume = {TBD},
year = {2018},
pages = {TBD},
}
```

### Contributions

Thanks to [@ghomasHudson](https://github.com/ghomasHudson) for adding this dataset.