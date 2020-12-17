---

YAML tags:
annotations_creators:
- crowdsourced
language_creators:
- machine-generated
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
---

# Dataset Card for HateOffensive

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
- **Homepage** : https://arxiv.org/abs/1905.12516 
- **Repository** : https://github.com/t-davidson/hate-speech-and-offensive-language
- **Paper** : https://arxiv.org/abs/1905.12516 
- **Leaderboard** : 
- **Point of Contact** : trd54 at cornell dot edu

### Dataset Summary

### Supported Tasks and Leaderboards
[More Information Needed]

### Languages
English (`en`)

## Dataset Structure

### Data Instances
{
"count": "3",
 "hate_speech": "0",
 "offensive_language": "0",
 "neither": "3",
 "class": "2",
 "tweet": "!!! RT @mayasolovely: As a woman you shouldn't complain about cleaning up your house. &amp; as a man you should always take the trash out...")
}

### Data Fields
"""
count: (Integer) number of users who coded each tweet (min is 3, sometimes more users coded a tweet when judgments were determined to be unreliable,
hate_speech: (Integer) number of users who judged the tweet to be hate speech,
offensive_language: (Integer) number of users who judged the tweet to be offensive,
neither: (Integer) number of users who judged the tweet to be neither offensive nor non-offensive,
class: (Class Label) class label for majority of CF users 0 - hate speech 1 - offensive language 2 - neither,
tweet: (string)
"""
### Data Splits
This dataset is not splitted, only the train split is available.

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

[More Information Needed]

### Licensing Information
MIT License

### Citation Information
@inproceedings{hateoffensive,
  title = {Automated Hate Speech Detection and the Problem of Offensive Language},
  author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar}, 
  booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media},
  series = {ICWSM '17},
  year = {2017},
  location = {Montreal, Canada},
  pages = {512-515}
  }