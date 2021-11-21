annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
- found
languages:
- en-US
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
paperswithcode_id: squad
pretty_name: onestop_qa
size_categories:
- 10K<n<100K
source_datasets:
- original
- extended|onestop_english
task_categories:
- question-answering
task_ids:
- multiple-choice-qa

# Dataset Card for onestop_qa

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

- **Homepage:** [OneStopQA repository](https://github.com/berzak/onestop-qa)
- **Repository:** [OneStopQA repository](https://github.com/berzak/onestop-qa)
- **Paper:** [STARC: Structured Annotations for Reading Comprehension](https://arxiv.org/abs/2004.14797)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

OneStopQA is a multiple choice reading comprehension dataset annotated according to the STARC (Structured Annotations for Reading Comprehension) scheme. The reading materials are Guardian articles taken from the [OneStopEnglish corpus](https://github.com/nishkalavallabhi/OneStopEnglishCorpus). Each article comes in three difficulty levels, Elementary, Intermediate and Advanced. Each paragraph is annotated with three multiple choice reading comprehension questions. The reading comprehension questions can be answered based on any of the three paragraph levels.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English

## Dataset Structure

### Data Instances

{'text':'Leading water scientists have issued one of the sternest warnings yet about global food supplies, saying that the worlds population may have to switch almost completely to a vegetarian diet by 2050 to avoid catastrophic shortages. <D>Humans derive about 20% of their protein from animal-based products now, but this may need to drop to just 5% to feed the extra two billion people expected to be alive by 2050,</D> according to research by some of the worlds leading water scientists. <A>There will not be enough water available on current croplands to produce food for the expected nine-billion population in 2050 if we follow current trends and changes towards diets common in western nations, the report by Malik Falkenmark and colleagues at the Stockholm International Water Institute (SIWI) said.</A>'

'question':'According to Malik Falkenmarks report, what will happen if the world adopts the current diet trends of western nations?'

'answers':{'a':'There will not be sufficient water to grow enough food for everyone',
'b': 'By 2050, nine billion people will not have enough drinking wate'r,
'c': 'By 2050, animal-based protein consumption will reduce from 20% to 5%',
'd': 'Obesity rates around the world will rise',}
}

### Data Fields

-text: text data
-question: the question
-answers: the possible answers



### Data Splits

[Needs More Information]

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