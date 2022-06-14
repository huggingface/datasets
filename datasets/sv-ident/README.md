---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
- de
licenses:
- mit
multilinguality:
- multilingual
pretty_name: sv-ident
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
- semantic-similarity-classification
pretty_name: SV-Ident
---

# Dataset Card for SV-Ident

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

- **Homepage:** https://vadis-project.github.io/sv-ident-sdp2022/
- **Repository:** https://github.com/vadis-project/sv-ident
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** svident2022@googlegroups.com

### Dataset Summary

SV-Ident comprises 4,248 sentences from social science publications in English and German. The data is the official data for the Shared Task: “Survey Variable Identification in Social Science Publications” (SV-Ident) 2022. Visit the homepage to find out more details about the shared task.

### Supported Tasks and Leaderboards

The dataset supports:

- **Variable Detection**: identifying whether a sentence contains a variable mention or not.

- **Variable Disambiguation**: identifying which variable from a given vocabulary is mentioned in a sentence.

### Languages

The text in the dataset is in English and German, as written by researchers. The domain of the texts is scientific publications in the social sciences.

## Dataset Structure

### Data Instances

```
{
  "sentence": "Our point, however, is that so long as downward (favorable comparisons overwhelm the potential for unfavorable comparisons, system justification should be a likely outcome amongst the disadvantaged.",
  "is_variable": 1,
  "variable": ["exploredata-ZA5400_VarV66", "exploredata-ZA5400_VarV53"],
  "research_data": ["ZA5400"],
  "doc_id": "73106",
  "uuid": "b9fbb80f-3492-4b42-b9d5-0254cc33ac10",
  "lang": "en",
}
```

### Data Fields

The following data fields are provided for documents:

`sentence`:       Textual instance, which may contain a variable mention.<br />
`is_variable`:    Label, whether the textual instance contains a variable mention (1) or not (0). This column can be used for Task 1 (Variable Detection).<br />
`variable`:       Variables (separated by a comma ";") that are mentioned in the textual instance. This column can be used for Task 2 (Variable Disambiguation).<br />
`research_data`:  Research data IDs (separated by a ";") that are relevant for each instance (and in general for each "doc_id").<br />
`doc_id`:         ID of the source document. Each document is written in one language (either English or German).<br />
`uuid`:           Unique ID of the instance in uuid4 format.<br />
`lang`:           Language of the sentence.

### Data Splits

| Split               | No of sentences                       |
| ------------------- | ------------------------------------  |
| Train               | 4,248                                 |

## Dataset Creation

### Curation Rationale

The dataset was curated by the VADIS project (https://vadis-project.github.io/).
The documents were annotated by two expert annotators.

### Source Data

#### Initial Data Collection and Normalization

The original data are available at GESIS (https://www.gesis.org/home) in an unprocessed format.

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

The documents were annotated by two expert annotators.

### Personal and Sensitive Information

The dataset does not include personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

VADIS project (https://vadis-project.github.io/)

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]