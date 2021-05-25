---
task_categories:
- text-classification
multilinguality:
- multilingual
task_ids:
- text-classification-other-language-identification
languages:
- hi
- awa
- bho
- mag
- bra
annotations_creators:
- unknown
source_datasets:
- original
size_categories:
- 10K<n<100K
licenses:
- unknown
paperswithcode_id: null
---

# Dataset Card Creation Guide

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

- **Homepage:** [GitHub](https://github.com/kmi-linguistics/vardial2018)
- **Repository:** [GitHub](https://github.com/kmi-linguistics/vardial2018)
- **Paper:** [Link](https://www.aclweb.org/anthology/W18-3900/)
- **Leaderboard:**
- **Point of Contact:** linguistics.kmi@gmail.com

### Dataset Summary

This datasets is introduced in a task which aimed at identifying 5 closely-related languages of Indo-Aryan language family – Hindi (also known as Khari Boli), Braj Bhasha, Awadhi, Bhojpuri and Magahi. These languages form part of a continuum starting from Western Uttar Pradesh (Hindi and Braj Bhasha) to Eastern Uttar Pradesh (Awadhi and Bhojpuri) and the neighbouring Eastern state of Bihar (Bhojpuri and Magahi). For this task, participants were provided with a dataset of approximately 15,000 sentences in each language, mainly from the domain of literature, published over the web as well as in print.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

 Hindi, Braj Bhasha, Awadhi, Bhojpuri and Magahi

## Dataset Structure

### Data Instances

```
{
    "language_id": 4,
    "text": 'तभी बारिश हुई थी जिसका गीलापन इन मूर्तियों को इन तस्वीरों में एक अलग रूप देता है .'
}
```

### Data Fields

- `text`: text which you want to classify
- `language_id`: label for the text as an integer from 0 to 4
The language ids correspond to the following languages: "AWA", "BRA", "MAG", "BHO", "HIN".

### Data Splits

|                      | train | valid | test  |
|----------------------|-------|-------|-------|
| # of input sentences | 70351 | 9692  | 10329 |

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

```
@proceedings{ws-2018-nlp-similar,
    title = "Proceedings of the Fifth Workshop on {NLP} for Similar Languages, Varieties and Dialects ({V}ar{D}ial 2018)",
    editor = {Zampieri, Marcos  and
      Nakov, Preslav  and
      Ljube{\v{s}}i{\'c}, Nikola  and
      Tiedemann, J{\"o}rg  and
      Malmasi, Shervin  and
      Ali, Ahmed},
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-3900",
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.