---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- "ab"
- "ar"
- "as"
- "br"
- "ca"
- "cnh"
- "cs"
- "cv"
- "cy"
- "de"
- "dv"
- "el"
- "en"
- "eo"
- "es"
- "et"
- "eu"
- "fa"
- "fi"
- "fr"
- "fy-NL"
- "ga-IE"
- "hi"
- "hsb"
- "hu"
- "ia"
- "id"
- "it"
- "ja"
- "ka"
- "kab"
- "ky"
- "lg"
- "lt"
- "lv"
- "mn"
- "mt"
- "nl"
- "or"
- "pa-IN"
- "pl"
- "pt"
- "rm-sursilv"
- "rm-vallader"
- "ro"
- "ru"
- "rw"
- "sah"
- "sl"
- "sv-SE"
- "ta"
- "th"
- "tr"
- "tt"
- "uk"
- "vi"
- "vot"
- "zh-CN"
- "zh-HK"
- "zh-TW"
licenses:
- cc-by-nc-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|other-common-voice
task_categories:
- other
task_ids:
- other-other-speech-translation
---

# Dataset Card for common_voice

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

- **Homepage:** https://commonvoice.mozilla.org/en/datasets
- **Repository:** https://github.com/common-voice/common-voice
- **Paper:** https://commonvoice.mozilla.org/en/datasets
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The Common Voice dataset consists of a unique MP3 and corresponding text file. Many of the 9,283 recorded hours in the dataset also include demographic metadata like age, sex, and accent that can help train the accuracy of speech recognition engines.

The dataset currently consists of 7,335 validated hours in 60 languages, but were always adding more voices and languages. Take a look at our Languages page to request a language or start contributing.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, called path and its sentence. Additional fields include accent, age, client_id, up_votes down_votes, gender, locale and segment.

`
{'accent': 'netherlands', 'age': 'fourties', 'client_id': 'bbbcb732e0f422150c30ff3654bbab572e2a617da107bca22ff8b89ab2e4f124d03b6a92c48322862f60bd0179ae07baf0f9b4f9c4e11d581e0cec70f703ba54', 'down_votes': 0, 'gender': 'male', 'locale': 'nl', 'path': 'nl/clips/common_voice_nl_23522441.mp3', 'segment': "''", 'sentence': 'Ik vind dat een dubieuze procedure.', 'up_votes': 2}
`

### Data Fields

client_id: An id for which client (voice) made the recording

path: The path to the audio file

sentence: The sentence the user was prompted to speak

up_votes: How many upvotes the audio file has received from reviewers

down_votes: How many downvotes the audio file has received from reviewers

age: The age of the speaker.

gender: The gender of the speaker

accent: Accent of the speaker

locale: The locale of the speaker

segment: Usually empty field

### Data Splits

The speech material has been subdivided into portions for dev, train, test, validated, invalidated, reported and other.

The validated data is data that has been validated with reviewers and recieved upvotes that the data is of high quality.

The invalidated data is data has been invalidated by reviewers
and recieved downvotes that the data is of low quality.

The reported data is data that has been reported, for different reasons.

The other data is data that has not yet been reviewed.

The dev, test, train are all data that has been reviewed, deemed of high quality and split into dev, test and train.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

## Considerations for Using the Data

### Social Impact of Dataset

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

### Discussion of Biases

[More Information Needed] 

### Other Known Limitations

[More Information Needed] 

## Additional Information

### Dataset Curators

[More Information Needed] 

### Licensing Information

[More Information Needed] 

### Citation Information

```
@inproceedings{commonvoice:2020,
  author = {Ardila, R. and Branson, M. and Davis, K. and Henretty, M. and Kohler, M. and Meyer, J. and Morais, R. and Saunders, L. and Tyers, F. M. and Weber, G.},
  title = {Common Voice: A Massively-Multilingual Speech Corpus},
  booktitle = {Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020)},
  pages = {4211--4215},
  year = 2020
}
```
