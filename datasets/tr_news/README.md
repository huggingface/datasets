---
annotations_creators:
- other
language_creators:
- other
languages:
- TR
licenses:
- apache-2.0
multilinguality:
- monolingual
pretty_name: TR-News
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- summarization
task_ids:
- news-articles-summarization
- news-articles-headline-generation
---

# Dataset Card for [TR-News]

## Table of Contents
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

- **Homepage:**
- **Repository:** https://github.com/batubayk/news_datasets
- **Paper:** https://link.springer.com/article/10.1007%2Fs10579-021-09568-y
- **Leaderboard:**
- **Point of Contact:** batuhan.baykara@boun.edu.tr

### Dataset Summary
TR-News is mainly a text summarization dataset for Turkish, however it can be used utilized for 
other tasks such as text classification and language modelling. It is constructed 
from three different news sources: NTV, Cumhuriyet, and Habertürk websites. It contains 
a total of 307,562 articles with the article count from each source being, respectively,
222,301, 44,990, and 40,271. The articles’ date varies in the range of 2009-2020. 
The dataset contains articles from a total of 121 various different domains 
(e.g. Domestic, World, Sports, Economy, Health, Life, Art, Technology, Education, Politics)
where some being sub-categories of others.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Turkish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

Training, validation and test

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data
Three new websites: NTV, HaberTürk and Cumhuriyet.

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

Batuhan Baykara and Tunga Güngör

### Licensing Information

[More Information Needed]

### Citation Information

@article{10.1007/s10579-021-09568-y, 
    year = {2022}, 
    title = {{Abstractive text summarization and new large-scale datasets for agglutinative languages Turkish and Hungarian}}, 
    author = {Baykara, Batuhan and Güngör, Tunga}, 
    journal = {Language Resources and Evaluation}, 
    issn = {1574-020X}, 
    doi = {10.1007/s10579-021-09568-y},
    pages = {1--35}
}

### Contributions
