---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- es:
  - es
- nl:
  - nl
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- parsing
---

# Dataset Card Creation Guide

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

- **Homepage:** [homepage](https://www.clips.uantwerpen.be/conll2002/ner/)
- **Repository:** [github](https://github.com/teropa/nlp/tree/master/resources/corpora/conll2002)
- **Paper:** [paper](https://www.aclweb.org/anthology/W02-2024/)
- **Point of Contact:** erikt@uia.ua.ac.be

### Dataset Summary

Named entities are phrases that contain the names of persons, organizations, locations, times and quantities. Example:

[PER Wolff] , currently a journalist in [LOC Argentina] , played with [PER Del Bosque] in the final years of the seventies in [ORG Real Madrid] .

The shared task of CoNLL-2002 concerns language-independent named entity recognition. We will concentrate on four types of named entities: persons, locations, organizations and names of miscellaneous entities that do not belong to the previous three groups. The participants of the shared task will be offered training and test data for at least two languages. They will use the data for developing a named-entity recognition system that includes a machine learning component. Information sources other than the training data may be used in this shared task. We are especially interested in methods that can use additional unannotated data for improving their performance (for example co-training).

### Supported Tasks and Leaderboards

Named Entity Recognition (NER) is a subtask of Information Extraction. Different NER systems were evaluated as a part of the Sixth Message Understanding Conference in 1995 (MUC6). The target language was English. The participating systems performed well. However, many of them used language-specific resources for performing the task and it is unknown how they would have performed on another language than English.

After 1995 NER systems have been developed for some European languages and a few Asian languages. There have been at least two studies that have applied one NER system to different languages. Palmer and Day [PD97] have used statistical methods for finding named entities in newswire articles in Chinese, English, French, Japanese, Portuguese and Spanish. They found that the difficulty of the NER task was different for the six languages but that a large part of the task could be performed with simple methods. Cucerzan and Yarowsky [CY99] used both morphological and contextual clues for identifying named entities in English, Greek, Hindi, Rumanian and Turkish. With minimal supervision, they obtained overall F measures between 40 and 70, depending on the languages used.

- `named-entity-recognition`: The performance in this task is measured with [F1](https://huggingface.co/metrics/f1) (higher is better). A named entity is correct only if it is an exact match of the corresponding entity in the data.
- `parsing`: The performance in this task is measured with [F1](https://huggingface.co/metrics/f1) (higher is better). A part-of-speech tag is correct only if it is equal to the corresponding tag in the data.

### Languages

There are two languages available : Spanish (es) and Dutch (nl).

## Dataset Structure

### Data Instances

The examples look like this :

```
{'id': '0',
 'ner_tags': [5, 6, 0, 0, 0, 0, 3, 0, 0],
 'pos_tags': [4, 28, 13, 59, 28, 21, 29, 22, 20],
 'tokens': ['La', 'Coruña', ',', '23', 'may', '(', 'EFECOM', ')', '.']
}
```

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token
- `pos_tags`: the POS tags of each token


The POS tags correspond to this list for Spanish:

```
'AO', 'AQ', 'CC', 'CS', 'DA', 'DE', 'DD', 'DI', 'DN', 'DP', 'DT', 'Faa', 'Fat', 'Fc', 'Fd', 'Fe', 'Fg', 'Fh', 'Fia', 'Fit', 'Fp', 'Fpa', 'Fpt', 'Fs', 'Ft', 'Fx', 'Fz', 'I', 'NC', 'NP', 'P0', 'PD', 'PI', 'PN', 'PP', 'PR', 'PT', 'PX', 'RG', 'RN', 'SP', 'VAI', 'VAM', 'VAN', 'VAP', 'VAS', 'VMG', 'VMI', 'VMM', 'VMN', 'VMP', 'VMS', 'VSG', 'VSI', 'VSM', 'VSN', 'VSP', 'VSS', 'Y', 'Z'
 ```

And this list for Dutch:

```
'Adj', 'Adv', 'Art', 'Conj', 'Int', 'Misc', 'N', 'Num', 'Prep', 'Pron', 'Punc', 'V'
```

The NER tags correspond to this list:
```
"O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC",
```

The NER tags have the same format as in the chunking task: a B denotes the first item of a phrase and an I any non-initial word. There are four types of phrases: person names (PER), organizations (ORG), locations (LOC) and miscellaneous names (MISC).

It is assumed that named entities are non-recursive and non-overlapping. In case a named entity is embedded in another named entity usually, only the top level entity is marked.

### Data Splits

For both configurations (Spanish and Dutch), there are three splits.

The original splits were named `train`, `testa` and `testb` and they correspond to the `train`, `validation` and `test` splits.

The splits have the following sizes :

|                            | Tain   | Valid | Test |
| -----                      | ------ | ----- | ---- |
| N. Examples (Spanish)      | 8324   | 1916  | 1518 |
| N. Examples (Dutch)        | 15807  | 2896  | 5196 |

## Dataset Creation

### Curation Rationale

The dataset was introduced to introduce new resources to two languages that were under-served for statistical machine learning at the time, Dutch and Spanish.

[More Information Needed]

### Source Data

The Spanish data is a collection of news wire articles made available by the Spanish EFE News Agency. The articles are from May 2000.

The Dutch data consist of four editions of the Belgian newspaper "De Morgen" of 2000 (June 2, July 1, August 1 and September 1).

#### Initial Data Collection and Normalization

The articles were word-tokenized, information on the exact pre-processing pipeline is unavailable.

#### Who are the source language producers?

The source language was produced by journalists and writers employed by the news agency and newspaper mentioned above.

### Annotations

#### Annotation process

For the Dutch data, the annotator has followed the MITRE and SAIC guidelines for named entity recognition (Chinchor et al., 1999) as well as possible.

#### Who are the annotators?

The Spanish data annotation was carried out by the TALP Research Center of the Technical University of Catalonia (UPC) and the Center of Language and Computation (CLiC) of the University of Barcelona (UB).

The Dutch data was annotated as a part of the Atranos project at the University of Antwerp.

### Personal and Sensitive Information

The data is sourced from newspaper source and only contains mentions of public figures or individuals

## Considerations for Using the Data

### Social Impact of Dataset

Named Entity Recognition systems can be used to efficiently index news text, allowing to easily gather all information pertaining to an organization or individual. Making such resources widely available in languages other than English can support better research and user experience for a larger part of the world's population. At the same time, better indexing and discoverability can also enable surveillance by state actors.

### Discussion of Biases

News text reproduces the biases of society, and any system trained on news data should be cognizant of these limitations and the risk for models to learn spurious correlations in this context, for example between a person's gender and their occupation.

### Other Known Limitations

Users should keep in mind that the dataset only contains news text, which might limit the applicability of the developed systems to other domains.

## Additional Information

### Dataset Curators

The annotation of the Spanish data was funded by the European Commission through the NAMIC project (IST-1999-12392).

### Licensing Information

The licensing status of the data, especially the news source text, is unknown.

### Citation Information

Provide the [BibTex](http://www.bibtex.org/)-formatted reference for the dataset. For example:
```
@inproceedings{tjong-kim-sang-2002-introduction,
    title = "Introduction to the {C}o{NLL}-2002 Shared Task: Language-Independent Named Entity Recognition",
    author = "Tjong Kim Sang, Erik F.",
    booktitle = "{COLING}-02: The 6th Conference on Natural Language Learning 2002 ({C}o{NLL}-2002)",
    year = "2002",
    url = "https://www.aclweb.org/anthology/W02-2024",
}
```
