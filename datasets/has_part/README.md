---
YAML tags:
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-Generics-KB
task_categories:
- text-scoring
task_ids:
- text-scoring-other-Meronym-Prediction
---

# Dataset Card for [HasPart]

## Table of Contents
- [Dataset Card for [HasPart]](#dataset-card-for-haspart)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://allenai.org/data/haspartkb
- **Repository:**
- **Paper:** https://arxiv.org/abs/2006.07510
- **Leaderboard:**
- **Point of Contact:** Peter Clark <peterc@allenai.org>

### Dataset Summary

This dataset is a new knowledge-base (KB) of hasPart relationships, extracted from a large corpus of generic statements. Complementary to other resources available, it is the first which is all three of: accurate (90% precision), salient (covers relationships a person may mention), and has high coverage of common terms (approximated as within a 10 year old’s vocabulary), as well as having several times more hasPart entries than in the popular ontologies ConceptNet and WordNet. In addition, it contains information about quantifiers, argument modifiers, and links the entities to appropriate concepts in Wikipedia and WordNet.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

```json
{
  "arg1": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "arg2": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "score": {
    "feature_type": "Value",
    "dtype": "float64"
  },
  "wikipedia_primary_page": {
    "feature_type": "Sequence",
    "feature": {
      "feature_type": "Value",
      "dtype": "string"
    }
  },
  "synset": {
    "feature_type": "Sequence",
    "feature": {
      "feature_type": "Value",
      "dtype": "string"
    }
  }
}
```

### Data Splits


## Dataset Creation

Our approach to hasPart extraction has five steps:

1. Collect generic sentences from a large corpus
2. Train and apply a RoBERTa model to identify hasPart relations in those sentences
3. Normalize the entity names
4. Aggregate and filter the entries
5. Link the hasPart arguments to Wikipedia pages and WordNet senses

Rather than extract knowledge from arbitrary text, we extract hasPart relations from generic sentences, e.g., “Dogs have tails.”, in order to bias the process towards extractions that are general (apply to most members of a category) and salient (notable enough to write down). As a source of generic sentences, we use **GenericsKB**, a large repository of 3.4M standalone generics previously harvested from a Webcrawl of 1.7B sentences.

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

@misc{bhakthavatsalam2020dogs,
      title={Do Dogs have Whiskers? A New Knowledge Base of hasPart Relations}, 
      author={Sumithra Bhakthavatsalam and Kyle Richardson and Niket Tandon and Peter Clark},
      year={2020},
      eprint={2006.07510},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}