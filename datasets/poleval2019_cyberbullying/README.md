---
annotations_creators:
- found
language_creators:
- found
languages:
- pl
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: null
---

# Dataset Card for Poleval 2019 cyberbullying

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

- **Homepage:** http://2019.poleval.pl/index.php/tasks/task6
- **Repository:** 
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Task 6-1: Harmful vs non-harmful

In this task, the participants are to distinguish between normal/non-harmful tweets (class: 0) and tweets that contain any kind of harmful
information (class: 1). This includes cyberbullying, hate speech and related phenomena. The data for the task is available now and can be
downloaded from the link provided below.

Task 6-2: Type of harmfulness

In this task, the participants shall distinguish between three classes of tweets: 0 (non-harmful), 1 (cyberbullying), 2 (hate-speech). There
are various definitions of both cyberbullying and hate-speech, some of them even putting those two phenomena in the same group. The specific
conditions on which we based our annotations for both cyberbullying and hate-speech, which have been worked out during ten years of research
will be summarized in an introductory paper for the task, however, the main and definitive condition to distinguish the two is whether the
harmful action is addressed towards a private person(s) (cyberbullying), or a public person/entity/large group (hate-speech).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Polish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

- text: the provided tweet
- label: for task 6-1 the label can be 0 (non-harmful) or 1 (harmful)
         for task 6-2 the label can be 0 (non-harmful), 1 (cyberbullying) or 2 (hate-speech)

### Data Splits

Train and Test

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

[More Information Needed]

### Citation Information

```
@proceedings{ogr:kob:19:poleval,
  editor    = {Maciej Ogrodniczuk and Łukasz Kobyliński},
  title     = {{Proceedings of the PolEval 2019 Workshop}},
  year      = {2019},
  address   = {Warsaw, Poland},
  publisher = {Institute of Computer Science, Polish Academy of Sciences},
  url       = {http://2019.poleval.pl/files/poleval2019.pdf},
  isbn      = "978-83-63159-28-3"}
}
```

### Contributions

Thanks to [@czabo](https://github.com/czabo) for adding this dataset.