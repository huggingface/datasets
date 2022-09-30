---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- ru
license:
- apache-2.0
multilinguality:
- monolingual
pretty_name: The Corpus for Emotions Detecting in Russian-language text sentences (CEDR)
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
- multi-label-classification
- text-classification-other-emotion-classification
---

# Dataset Card for [cedr]

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** [GitHub](https://github.com/sag111/CEDR)
- **Repository:** [GitHub](https://github.com/sag111/CEDR)
- **Paper:** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1877050921013247)
- **Leaderboard:**
- **Point of Contact:** [@sag111](mailto:sag111@mail.ru)

### Dataset Summary

The Corpus for Emotions Detecting in Russian-language text sentences of different social sources (CEDR) contains 9410  comments labeled for 5 emotion categories (joy, sadness, surprise, fear, and anger). 

Here are 2 dataset configurations:
- "main" - contains "text", "labels", and "source" features;
- "enriched" - includes all "main" features and "sentences".

Dataset with predefined train/test splits.

### Supported Tasks and Leaderboards

This dataset is intended for multi-label emotion classification.

### Languages

The data is in Russian.

## Dataset Structure

### Data Instances

Each instance is a text sentence in Russian from several sources with one or more emotion annotations (or no emotion at all).

An example for an instance from the dataset is shown below:
```
{
  'text': 'Забавно как люди в возрасте удивляются входящим звонкам на мобильник)',
  'labels': [0],
  'source': 'twitter',
  'sentences': [
    [
      {'forma': 'Забавно', 'lemma': 'Забавно'},
      {'forma': 'как', 'lemma': 'как'},
      {'forma': 'люди', 'lemma': 'человек'},
      {'forma': 'в', 'lemma': 'в'},
      {'forma': 'возрасте', 'lemma': 'возраст'},
      {'forma': 'удивляются', 'lemma': 'удивляться'},
      {'forma': 'входящим', 'lemma': 'входить'},
      {'forma': 'звонкам', 'lemma': 'звонок'},
      {'forma': 'на', 'lemma': 'на'},
      {'forma': 'мобильник', 'lemma': 'мобильник'},
      {'forma': ')', 'lemma': ')'}
    ]
  ]
}
```

Emotion label codes: {0: "joy", 1: "sadness", 2: "surprise", 3: "fear", 4: "anger"}

### Data Fields

The main configuration includes:
- text: the text of the sentence;
- labels: the emotion annotations;
- source: the tag name of the corresponding source

In addition to the above, the raw data includes:
- sentences: text tokenized and lemmatized with [udpipe](https://ufal.mff.cuni.cz/udpipe)
  - 'forma': the original word form;
  - 'lemma': the lemma of this word

### Data Splits

The dataset includes a set of train/test splits. 
with 7528, and 1882 examples respectively.

## Dataset Creation

### Curation Rationale

The formed dataset of examples consists of sentences in Russian from several sources (blogs, microblogs, news), which allows creating methods to analyse various types of texts. The created methodology for building the dataset based on applying a crowdsourcing service can be used to expand the number of examples to improve the accuracy of supervised classifiers.

### Source Data

#### Initial Data Collection and Normalization

Data was collected from several sources: posts of the Live Journal social network, texts of the online news agency Lenta.ru, and Twitter microblog posts.

Only those sentences were selected that contained marker words from the dictionary of [the emotive vocabulary of the Russian language](http://lexrus.ru/default.aspx?p=2876). The authors manually formed a list of marker words for each emotion by choosing words from different categories of the dictionary.

In total, 3069 sentences were selected from LiveJournal posts, 2851 sentences from Lenta.Ru, and 3490 sentencesfrom Twitter. After selection, sentences were offered to annotators for labeling.

#### Who are the source language producers?

Russian-speaking LiveJournal and Tweeter users, and authors of news articles on the site lenta.ru.

### Annotations

#### Annotation process

Annotating sentences with labels of their emotions was performed with the help of [a crowdsourcing platform](https://yandex.ru/support/toloka/index.html?lang=en).

The annotators’ task was: “What emotions did the author express in the sentence?”. The annotators were allowed to put an arbitrary number of the following emotion labels: "joy", "sadness", "anger", "fear", and "surprise".

If the accuracy of an annotator on the control sentences (including the trial run) became less than 70%, or if the accuracy was less than 66% over the last six control samples, the annotator was dismissed. 

Sentences were split into tasks and assigned to annotators so that each sentence was annotated at least three times. A label of a specific emotion was assigned to a sentence if put by more than half of the annotators.

#### Who are the annotators?

Only those of the 30% of the best-performing active users (by the platform’s internal rating) who spoke Russian and were over 18 years old were allowed into the annotation process. Moreover, before a platform user could be employed as an annotator, they underwent a training task, after which they were to mark 25 trial samples with more than 80% agreement compared to the annotation that the authors had performed themselves.

### Personal and Sensitive Information

The text of the sentences may contain profanity.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Researchers at AI technology lab at NRC "Kurchatov Institute". See the author [list](https://www.sciencedirect.com/science/article/pii/S1877050921013247).

### Licensing Information

The GitHub repository which houses this dataset has an Apache License 2.0.

### Citation Information
If you have found our results helpful in your work, feel free to cite our publication. This is an updated version of the dataset, the collection and preparation of which is described here:
```
@article{sboev2021data,
  title={Data-Driven Model for Emotion Detection in Russian Texts},
  author={Sboev, Alexander and Naumov, Aleksandr and Rybka, Roman},
  journal={Procedia Computer Science},
  volume={190},
  pages={637--642},
  year={2021},
  publisher={Elsevier}
}
```

### Contributions

Thanks to [@naumov-al](https://github.com/naumov-al) for adding this dataset.
