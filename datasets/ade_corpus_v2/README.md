[Needs More Information]

# Dataset Card for [Needs More Information]

## Table of Contents
- [Dataset Card for [Needs More Information]](#dataset-card-for-needs-more-information)
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

[Needs More Information]

### Data Fields

{
  "text": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "label": {
    "feature_type": "ClassLabel",
    "dtype": "int32",
    "class_names": [
      "Not-Related",
      "Related"
    ]
  }
}

{
  "text": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "drug": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "effect": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "indexes": {
    "drug": {
      "feature_type": "Sequence",
      "start_char": {
        "feature_type": "Value",
        "dtype": "int32"
      },
      "end_char": {
        "feature_type": "Value",
        "dtype": "int32"
      }
    },
    "effect": {
      "feature_type": "Sequence",
      "start_char": {
        "feature_type": "Value",
        "dtype": "int32"
      },
      "end_char": {
        "feature_type": "Value",
        "dtype": "int32"
      }
    }
  }
}

{
  "text": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "drug": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "dosage": {
    "feature_type": "Value",
    "dtype": "string"
  },
  "indexes": {
    "drug": {
      "feature_type": "Sequence",
      "start_char": {
        "feature_type": "Value",
        "dtype": "int32"
      },
      "end_char": {
        "feature_type": "Value",
        "dtype": "int32"
      }
    },
    "dosage": {
      "feature_type": "Sequence",
      "start_char": {
        "feature_type": "Value",
        "dtype": "int32"
      },
      "end_char": {
        "feature_type": "Value",
        "dtype": "int32"
      }
    }
  }
}

### Data Splits

Train

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

[Needs More Information]