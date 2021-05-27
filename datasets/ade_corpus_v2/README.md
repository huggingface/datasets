---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
  Ade_corpus_v2_classification:
  - 10K<n<100K
  Ade_corpus_v2_drug_ade_relation:
  - 1K<n<10K
  Ade_corpus_v2_drug_dosage_relation:
  - n<1K
source_datasets:
- original
task_categories:
  Ade_corpus_v2_classification:
  - text-classification
  Ade_corpus_v2_drug_ade_relation:
  - structure-prediction
  Ade_corpus_v2_drug_dosage_relation:
  - structure-prediction
task_ids:
  Ade_corpus_v2_classification:
  - fact-checking
  Ade_corpus_v2_drug_ade_relation:
  - coreference-resolution
  Ade_corpus_v2_drug_dosage_relation:
  - coreference-resolution
paperswithcode_id: null
---

# Dataset Card for Adverse Drug Reaction Data v2

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

- **Homepage:** https://www.sciencedirect.com/science/article/pii/S1532046412000615
- **Repository:** [Needs More Information]
- **Paper:** https://www.sciencedirect.com/science/article/pii/S1532046412000615
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

ADE-Corpus-V2  Dataset: Adverse Drug Reaction Data.
 This is a dataset for Classification if a sentence is ADE-related (True) or not (False) and Relation Extraction between Adverse Drug Event and Drug.
 DRUG-AE.rel provides relations between drugs and adverse effects.
 DRUG-DOSE.rel provides relations between drugs and dosages.
 ADE-NEG.txt provides all sentences in the ADE corpus that DO NOT contain any drug-related adverse effects.

### Supported Tasks and Leaderboards

Sentiment classification, Relation Extraction

### Languages

English

## Dataset Structure

### Data Instances

#### Config - `Ade_corpus_v2_classification`
```
{
      'label': 1, 
      'text': 'Intravenous azithromycin-induced ototoxicity.'
}

```

#### Config - `Ade_corpus_v2_drug_ade_relation`

```
{ 
    'drug': 'azithromycin', 
    'effect': 'ototoxicity', 
    'indexes': {
                  'drug': {
                            'end_char': [24], 
                            'start_char': [12]
                          }, 
                  'effect': {
                            'end_char': [44], 
                            'start_char': [33]
                            }
                }, 
    'text': 'Intravenous azithromycin-induced ototoxicity.'
    
}

```

#### Config - `Ade_corpus_v2_drug_dosage_relation`

```
{
    'dosage': '4 times per day', 
    'drug': 'insulin', 
    'indexes': {
                'dosage': {
                            'end_char': [56], 
                            'start_char': [41]
                        }, 
                'drug': {
                          'end_char': [40], 
                          'start_char': [33]}
                        }, 
    'text': 'She continued to receive regular insulin 4 times per day over the following 3 years with only occasional hives.'
}

```


### Data Fields

#### Config - `Ade_corpus_v2_classification`

- `text` - Input text.
- `label` - Whether the adverse drug effect(ADE) related (1) or not (0).
- 
#### Config - `Ade_corpus_v2_drug_ade_relation`

- `text` - Input text.
- `drug` - Name of drug.
- `effect` - Effect caused by the drug.
- `indexes.drug.start_char` - Start index of `drug` string in text.
- `indexes.drug.end_char` - End index of `drug` string in text.
- `indexes.effect.start_char` - Start index of `effect` string in text.
- `indexes.effect.end_char` - End index of `effect` string in text.

#### Config - `Ade_corpus_v2_drug_dosage_relation`

- `text` - Input text.
- `drug` - Name of drug.
- `dosage` - Dosage of the drug.
- `indexes.drug.start_char` - Start index of `drug` string in text.
- `indexes.drug.end_char` - End index of `drug` string in text.
- `indexes.dosage.start_char` - Start index of `dosage` string in text.
- `indexes.dosage.end_char` - End index of `dosage` string in text.


### Data Splits

| Train  |
| ------ | 
| 23516  |

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

[Needs More Information]

### Citation Information

```
@article{GURULINGAPPA2012885,
title = "Development of a benchmark corpus to support the automatic extraction of drug-related adverse effects from medical case reports",
journal = "Journal of Biomedical Informatics",
volume = "45",
number = "5",
pages = "885 - 892",
year = "2012",
note = "Text Mining and Natural Language Processing in Pharmacogenomics",
issn = "1532-0464",
doi = "https://doi.org/10.1016/j.jbi.2012.04.008",
url = "http://www.sciencedirect.com/science/article/pii/S1532046412000615",
author = "Harsha Gurulingappa and Abdul Mateen Rajput and Angus Roberts and Juliane Fluck and Martin Hofmann-Apitius and Luca Toldo",
keywords = "Adverse drug effect, Benchmark corpus, Annotation, Harmonization, Sentence classification",
abstract = "A significant amount of information about drug-related safety issues such as adverse effects are published in medical case reports that can only be explored by human readers due to their unstructured nature. The work presented here aims at generating a systematically annotated corpus that can support the development and validation of methods for the automatic extraction of drug-related adverse effects from medical case reports. The documents are systematically double annotated in various rounds to ensure consistent annotations. The annotated documents are finally harmonized to generate representative consensus annotations. In order to demonstrate an example use case scenario, the corpus was employed to train and validate models for the classification of informative against the non-informative sentences. A Maximum Entropy classifier trained with simple features and evaluated by 10-fold cross-validation resulted in the F1 score of 0.70 indicating a potential useful application of the corpus."
}
```

### Contributions

Thanks to [@Nilanshrajput](https://github.com/Nilanshrajput), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
