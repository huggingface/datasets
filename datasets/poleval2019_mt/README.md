---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
- found
languages:
- en
- pl
- ru
licenses:
- unknown
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
---

# Dataset Card for poleval2019_mt

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

- **Homepage:** PolEval-2019 competition. http://2019.poleval.pl/
- **Repository:** Links available [in this page](http://2019.poleval.pl/index.php/tasks/task4)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

PolEval is a SemEval-inspired evaluation campaign for natural language processing tools for Polish.
Submitted solutions compete against one another within certain tasks selected by organizers, using available data and are evaluated according to
pre-established procedures. One of the tasks in PolEval-2019 was Machine Translation (Task-4).

The task is to train as good as possible machine translation system, using any technology,with limited textual resources.
The competition will be done for 2 language pairs, more popular English-Polish (into Polish direction) and pair that can be called low resourced
Russian-Polish (in both directions).

Here, Polish-English is also made available to allow for training in both directions. However, the test data is ONLY available for English-Polish

### Supported Tasks and Leaderboards
Supports Machine Translation between Russian to Polish and English to Polish (and vice versa). 

### Languages
- Polish (pl)
- Russian (ru)
- English (en) 

## Dataset Structure

### Data Instances
As the training data set, a set of bi-lingual corpora aligned at the sentence level has been prepared. The corpora are saved in UTF-8 encoding as plain text, one language per file.

### Data Fields
One example of the translation is as below:
```
{
  'translation': {'ru': 'не содержала в себе моделей. Модели это сравнительно новое явление. ', 
                  'pl': 'nie miała w sobie modeli. Modele to względnie nowa dziedzina. Tak więc, jeśli '}
}
```

### Data Splits

The dataset is divided into two splits. All the headlines are scraped from news websites on the internet.
|       | Tain   | Valid | Test  |
| ----- | ------ | ----- | ----- |
| ru-pl |  20001 | 3001  | 2969  |
| pl-ru |  20001 | 3001  | 2969  |
| en-pl | 129255 | 1000  | 9845  |

## Dataset Creation

### Curation Rationale

This data was curated as a task for the PolEval-2019. The task is to train as good as possible machine translation system, using any technology, with limited textual resources. The competition will be done for 2 language pairs, more popular English-Polish (into Polish direction) and pair that can be called low resourced Russian-Polish (in both directions).

PolEval is a SemEval-inspired evaluation campaign for natural language processing tools for Polish. Submitted tools compete against one another within certain tasks selected by organizers, using available data and are evaluated according to pre-established procedures.

PolEval 2019-related papers were presented at AI & NLP Workshop Day (Warsaw, May 31, 2019).
The links for the top performing models on various tasks (including the Task-4: Machine Translation) is present in [this](http://2019.poleval.pl/index.php/publication) link

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The organization details of PolEval is present in this [link](http://2019.poleval.pl/index.php/organizers)

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

[More Information Needed]

### Contributions

Thanks to [@vrindaprabhu](https://github.com/vrindaprabhu) for adding this dataset.