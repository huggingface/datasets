---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- yo
licenses:
- Creative Commons 3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: null
---

# Dataset Card for Yoruba GV NER Corpus

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

- **Homepage:** 
- **Repository:** [Yoruba GV NER](https://github.com/ajesujoba/YorubaTwi-Embedding/tree/master/Yoruba/Yoruba-NER)
- **Paper:** https://www.aclweb.org/anthology/2020.lrec-1.335/
- **Leaderboard:**
- **Point of Contact:** [David Adelani](mailto:didelani@lsv.uni-saarland.de)

### Dataset Summary
The Yoruba GV NER is a named entity recognition (NER) dataset for Yorùbá language based on the [Global Voices news](https://yo.globalvoices.org/) corpus. Global Voices (GV) is a multilingual news platform with articles contributed by journalists, translators, bloggers, and human rights activists from around the world with a coverage of over 50 languages. Most of the texts used in creating the Yoruba GV NER are translations from other languages to Yorùbá.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is Yorùbá.

## Dataset Structure

### Data Instances

A data point consists of sentences seperated by empty line and tab-seperated tokens and tags. 
{'id': '0',
 'ner_tags': [B-LOC, 0, 0, 0, 0],
 'tokens': ['Tanzania', 'fi', 'Ajìjàgbara', 'Ọmọ', 'Orílẹ̀-èdèe']
}

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-DATE", "I-DATE",
```
The NER tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any non-initial word. There are four types of phrases: person names (PER), organizations (ORG), locations (LOC) and dates & times (DATE). (O) is used for tokens not considered part of any named entity.

### Data Splits

Training (19,421 tokens), validation (2,695 tokens) and test split (5,235 tokens)

## Dataset Creation

### Curation Rationale

The data was created to help introduce resources to new language - Yorùbá.

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The dataset is based on the news domain and was crawled from [Global Voices Yorùbá news](https://yo.globalvoices.org/).


[More Information Needed]

#### Who are the source language producers?

The dataset contributed by journalists, translators, bloggers, and human rights activists from around the world. Most of the texts used in creating the Yoruba GV NER are translations from other languages to Yorùbá
[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

The data was annotated by Jesujoba Alabi and David Adelani for the paper: 
[Massive vs. Curated Embeddings for Low-Resourced Languages: the case of Yorùbá and Twi](https://www.aclweb.org/anthology/2020.lrec-1.335/).

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

The annotated data sets were developed by students of Saarland University, Saarbrücken, Germany .


### Licensing Information

The data is under the [Creative Commons Attribution 3.0 ](https://creativecommons.org/licenses/by/3.0/)

### Citation Information
```
@inproceedings{alabi-etal-2020-massive,
    title = "Massive vs. Curated Embeddings for Low-Resourced Languages: the Case of {Y}or{\`u}b{\'a} and {T}wi",
    author = "Alabi, Jesujoba  and
      Amponsah-Kaakyire, Kwabena  and
      Adelani, David  and
      Espa{\~n}a-Bonet, Cristina",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.335",
    pages = "2754--2762",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```
### Contributions

Thanks to [@dadelani](https://github.com/dadelani) for adding this dataset.