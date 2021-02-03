---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- id
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for Indonesian Newspapers 2018

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

- **Homepage:** [Indonesian Newspapers](https://github.com/feryandi/Dataset-Artikel)
- **Repository:** [Indonesian Newspapers](https://github.com/feryandi/Dataset-Artikel)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [feryandi.n@gmail.com](mailto:feryandi.n@gmail.com),
[cahya.wirawan@gmail.com](mailto:cahya.wirawan@gmail.com)

### Dataset Summary

The dataset contains around 500K articles (136M of words) from 7 Indonesian newspapers: Detik, Kompas, Tempo,
CNN Indonesia, Sindo, Republika and Poskota. The articles are dated between 1st January 2018 and 20th August 2018
(with few exceptions dated earlier). The size of uncompressed 500K json files (newspapers-json.tgz) is around 2.2GB,
and the cleaned uncompressed in a big text file (newspapers.txt.gz) is about 1GB. The original source in Google Drive
contains also a dataset in html format which include raw data (pictures, css, javascript, ...)
from the online news website. A copy of the original dataset is available at
https://cloud.uncool.ai/index.php/s/mfYEAgKQoY3ebbM

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
Indonesian

## Dataset Structure
```
{
  'id': 'string',
  'url': 'string',
  'date': 'string',
  'title': 'string',
  'content': 'string'
}
```
### Data Instances

[More Information Needed]

### Data Fields
- `id`: id of the sample
- `url`: the url to the original article
- `date`: the publishing date of the article
- `title`: the title of the article
- `content`: the content of the article

### Data Splits

The dataset contains train set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

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

[More Information Needed]

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) for adding this dataset.