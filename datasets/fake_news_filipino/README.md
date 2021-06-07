---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- tl
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- fact-checking
paperswithcode_id: fake-news-filipino-dataset
---

# Dataset Card for Fake News Filipino

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

- **Homepage: [Fake News Filipino homepage](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Repository: [Fake News Filipino repository](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Paper: [LREC 2020 paper](http://www.lrec-conf.org/proceedings/lrec2020/index.html)**
- **Leaderboard:**
- **Point of Contact:[Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph)**

### Dataset Summary

Low-Resource Fake News Detection Corpora in Filipino. The first of its kind. Contains 3,206 expertly-labeled news samples, half of which are real and half of which are fake.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is primarily in Filipino, with the addition of some English words commonly used in Filipino vernacular.

## Dataset Structure

### Data Instances

Sample data:
```
{
  "label": "0",
  "article": "Sa 8-pahinang desisyon, pinaboran ng Sandiganbayan First Division ang petition for Writ of Preliminary Attachment/Garnishment na inihain ng prosekusyon laban sa mambabatas."
}
```


### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

Fake news articles were sourced from online sites that were tagged as fake news sites by the non-profit independent media fact-checking organization Verafiles and the National Union of Journalists in the Philippines (NUJP). Real news articles were sourced from mainstream news websites in the Philippines, including Pilipino Star Ngayon, Abante, and Bandera.

### Curation Rationale

We remedy the lack of a proper, curated benchmark dataset for fake news detection in Filipino by constructing and producing what we call “Fake News Filipino.” 


### Source Data

#### Initial Data Collection and Normalization

We construct the dataset by scraping our source websites, encoding all characters into UTF-8. Preprocessing was light to keep information intact: we retain capitalization and punctuation, and do not correct any misspelled words.

#### Who are the source language producers?

Jan Christian Blaise Cruz, Julianne Agatha Tan, and Charibeth Cheng

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

[Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph), Julianne Agatha Tan, and Charibeth Cheng

### Licensing Information

[More Information Needed]

### Citation Information

    @inproceedings{cruz2020localization,
      title={Localization of Fake News Detection via Multitask Transfer Learning},
      author={Cruz, Jan Christian Blaise and Tan, Julianne Agatha and Cheng, Charibeth},
      booktitle={Proceedings of The 12th Language Resources and Evaluation Conference},
      pages={2596--2604},
      year={2020}
    }

### Contributions

Thanks to [@anaerobeth](https://github.com/anaerobeth) for adding this dataset.