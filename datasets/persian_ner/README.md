---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- fa
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
---

# Dataset Card for [Persian NER]

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

- **Homepage:** 
- **Repository:** https://github.com/HaniehP/PersianNER
- **Paper:** https://www.aclweb.org/anthology/C16-1319.pdf
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

The dataset includes 7,682 Persian sentences, split into 250,015 tokens and their NER labels. It is available in 3 folds to be used in turn as training and test sets. The NER tags are in IOB format.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

 ```
{'ner_labels': [1,
  12,
  6,
  1,
  8],
 'tokens': ['دکتر',
  'اکبر',
  'میرعرب',
  'در',
  'همایش']}
 ```

### Data Fields

- `id`: id of the sample
 - `tokens`: the tokens of the example text
 - `ner_labels`: the NER tags of each token

The NER tags correspond to this list:
 ```
"","I-pers","B-fac","I-pro", "I-org", "O", "I-event", "B-pers",
"I-fac","B-org", "B-pro", "B-loc","B-event","I-loc",
 ```

### Data Splits

Training and test splits

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Hanieh Poostchi, Ehsan Zare Borzeshi, Mohammad Abdous, Massimo Piccardi

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

Hanieh Poostchi, Ehsan Zare Borzeshi, Mohammad Abdous, Massimo Piccardi

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

Dataset is published for academic use only

### Dataset Curators

[More Information Needed]

### Licensing Information

Creative Commons Attribution 4.0 International License.

### Citation Information

@inproceedings{poostchi-etal-2016-personer,
    title = "{P}erso{NER}: {P}ersian Named-Entity Recognition",
    author = "Poostchi, Hanieh  and
      Zare Borzeshi, Ehsan  and
      Abdous, Mohammad  and
      Piccardi, Massimo",
    booktitle = "Proceedings of {COLING} 2016, the 26th International Conference on Computational Linguistics: Technical Papers",
    month = dec,
    year = "2016",
    address = "Osaka, Japan",
    publisher = "The COLING 2016 Organizing Committee",
    url = "https://www.aclweb.org/anthology/C16-1319",
    pages = "3381--3389",
    abstract = "Named-Entity Recognition (NER) is still a challenging task for languages with low digital resources. The main difficulties arise from the scarcity of annotated corpora and the consequent problematic training of an effective NER pipeline. To abridge this gap, in this paper we target the Persian language that is spoken by a population of over a hundred million people world-wide. We first present and provide ArmanPerosNERCorpus, the first manually-annotated Persian NER corpus. Then, we introduce PersoNER, an NER pipeline for Persian that leverages a word embedding and a sequential max-margin classifier. The experimental results show that the proposed approach is capable of achieving interesting MUC7 and CoNNL scores while outperforming two alternatives based on a CRF and a recurrent neural network.",
}