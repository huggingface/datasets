---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- sv
licenses:
- cc-by-4.0
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

# Swedish NER Corpus

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

- **Homepage:** [https://github.com/klintan/swedish-ner-corpus]()
- **Repository:** [https://github.com/klintan/swedish-ner-corpus]()
- **Point of contact:** Andreas Klintberg (ankl@kth.se)

### Dataset Summary

Webbnyheter 2012 from Spraakbanken, semi-manually annotated and adapted for CoreNLP Swedish NER. Semi-manually defined in this case as: Bootstrapped from Swedish Gazetters then manually correcte/reviewed by two independent native speaking swedish annotators. No annotator agreement calculated.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Swedish

## Dataset Structure

### Data Instances

A sample dataset instance is provided below:

```json
{'id': '3',
 'ner_tags': [4, 4, 0, 0, 0, 0, 0, 0, 3, 3, 0],
 'tokens': ['Margaretha',
  'Fahlgren',
  ',',
  'professor',
  'i',
  'litteraturvetenskap',
  ',',
  'vice-rektor',
  'Uppsala',
  'universitet',
  '.']}
```



### Data Fields

- `id`: id of the sentence
- `token`: current token
- `ner_tag`: ner tag of the token

Full fields:

```json
{
  "id":{
    "feature_type":"Value"
      "dtype":"string"
      }
      "tokens":{
        "feature_type":"Sequence"
        "feature":{
        "feature_type":"Value"
        "dtype":"string"
        }
      }
    "ner_tags":{
      "feature_type":"Sequence"
        "dtype":"int32"
        "feature":{
        "feature_type":"ClassLabel"
          "dtype":"int32"
          "class_names":[
              0:"0"
              1:"LOC"
              2:"MISC"
              3:"ORG"
              4:"PER"
              ]
      }
  }
}
```

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

The original dataset was provided by Språkbanken which consists of news from Swedish newspapers' websites.

### Licensing Information

https://github.com/klintan/swedish-ner-corpus/blob/master/LICENSE

### Citation Information

[More Information Needed]
