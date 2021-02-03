---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
- found
languages:
- ro
licenses:
- mit
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
---

# Dataset Card for RONEC

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://github.com/dumitrescustefan/ronec
- **Repository:** https://github.com/dumitrescustefan/ronec
- **Paper:** https://arxiv.org/abs/1909.01247
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** dumitrescu.stefan@gmail.com, avram.andreimarius@gmail.com

### Dataset Summary

We present RONEC - the Named Entity Corpus for the Romanian language. The corpus contains over 26000 entities in 5000 annotatedsentences, belonging to 16 distinct classes. The sentenceshave been extracted from a copy-right free newspaper, covering severalstyles. This corpus represents the first initiative in the Romanian language space specifically targeted for named entity recognition.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text dataset is in Romanian (`ro`)

## Dataset Structure

### Data Instances

An example looks like this:

```
{'id': '1',
 'ner_tags': [13, 29, 29, 0, 4, 0, 13, 29, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
 'tokens': ['Secretarul', 'de', 'stat', 'al', 'S.U.A.', ',', 'Colin', 'Powell', ',', 'începe', 'un', 'turneu', 'în', 'țările', 'asiatice', 'afectate', 'de', 'valurile', 'seismice', 'uriașe', '.']
}
```

### Data Fields

- `id`: a `string` feature describing the index of the sentence in the dataset
- `tokens`: a `list` of `string` features.
- `ner_tags`: a `list` of classification labels, with possible values including `O`, `B-DATETIME`, `B-EVENT`, `B-FACILITY`, `B-GPE`, `B-LANGUAGE`, `B-LOC`, `B-MONEY`, `B-NAT_REL_POL`, `B-NUMERIC_VALUE`, `B-ORDINAL`, `B-ORGANIZATION`, `B-PERIOD`, `B-PERSON`, `B-PRODUCT`, `B-QUANTITY`, `B-WORK_OF_ART`, `I-DATETIME`, `I-EVENT`, `I-FACILITY`, `I-GPE`, `I-LANGUAGE`, `I-LOC`, `I-MONEY`, `I-NAT_REL_POL`, `I-NUMERIC_VALUE`, `I-ORDINAL`, `I-ORGANIZATION`, `I-PERIOD`, `I-PERSON`, `I-PRODUCT`, `I-QUANTITY`, `I-WORK_OF_ART`.

### Data Splits

The dataset was also split in train (80%), dev (10%) and test (10%) 

## Dataset Creation

### Curation Rationale

From the original paper:

*The corpus, at its current version 1.0 is composed of5127 sentences, annotated with16 classes, for a totalof26377 annotated entities. The 16 classes are: PER-SON, NATRELPOL, ORG, GPE, LOC, FACILITY,PRODUCT,  EVENT,  LANGUAGE,  WORKOFART,DATETIME,  PERIOD,  MONEY,  QUANTITY,  NU-MERICVALUE and ORDINAL. It is based on copyright-free text extracted from SoutheastEuropean Times (SETimes) (Tyers and Alperen, 2010).The news portal has published10“news and views fromSoutheast Europe” in ten languages, including Romanian.SETimes has been used in the past for several annotatedcorpora, including parallel corpora for machine translation.For RONEC we have used a hand-picked11selection of sen-tences belonging to several categories* 

### Source Data

#### Initial Data Collection and Normalization

*The corpus creation process involved a small number ofpeople that have voluntarily joined the initiative, with theauthors of this paper directing the work.  Initially, wesearched for NER resources in Romanian, and found none.Then we looked at English resources and read the in-depthACE guide, out of which a 16-class draft evolved. We thenidentified a copy-right free text from which we hand-pickedsentences to maximize the amount of entities while main-taining style balance. The annotation process was a trial-and-error, with cycles composed of annotation, discussingconfusing entities, updating the annotation guide schematicand going through the corpus section again to correct enti-ties following guide changes.*

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

*The corpus creation process involved a small number ofpeople that have voluntarily joined the initiative, with theauthors of this paper directing the work.  Initially, wesearched for NER resources in Romanian, and found none.Then we looked at English resources and read the in-depthACE guide, out of which a 16-class draft evolved. We thenidentified a copy-right free text from which we hand-pickedsentences to maximize the amount of entities while main-taining style balance. The annotation process was a trial-and-error, with cycles composed of annotation, discussingconfusing entities, updating the annotation guide schematicand going through the corpus section again to correct enti-ties following guide changes.*

#### Who are the annotators?

Stefan Dumitrescu, Marius Avram

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

MIT License

### Citation Information

@article{dumitrescu2019introducing,
  title={Introducing RONEC--the Romanian Named Entity Corpus},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius},
  journal={arXiv preprint arXiv:1909.01247},
  year={2019}
}

### Contributions

Thanks to [@iliemihai](https://github.com/iliemihai) for adding this dataset.