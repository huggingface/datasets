---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- tl
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-twitter-data-philippine-election
task_categories:
- text-classification
task_ids:
- sentiment-analysis
paperswithcode_id: null
---

# Dataset Card for Hate Speech in Filipino

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

- **Homepage: [Hate Speech Dataset in Filipino homepage](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Repository: [Hate Speech Dataset in Filipino homepage](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Paper: [PCJ paper](https://pcj.csp.org.ph/index.php/pcj/issue/download/29/PCJ%20V14%20N1%20pp1-14%202019)**
- **Leaderboard:**
- **Point of Contact: [Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph)**

### Dataset Summary
Contains 10k tweets (training set) that are labeled as hate speech or non-hate speech. Released with 4,232 validation and 4,232 testing samples. Collected during the 2016 Philippine Presidential Elections.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is primarily in Filipino, with the addition of some English words commonly used in Filipino vernacular

## Dataset Structure

### Data Instances

Sample data:
```
{
  "text": "Taas ni Mar Roxas ah. KULTONG DILAW NGA NAMAN",
  "label": 1
}
```

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

This study seeks to contribute to the filling of this gap through the development of a model that can automate hate speech detection and classification in Philippine election-related tweets. The role of the microblogging site Twitter as a platform for the expression of support and hate during the 2016 Philippine presidential election has been supported in news reports and systematic studies. Thus, the particular question addressed in this paper is: Can existing techniques in language processing and machine learning be applied to detect hate speech in the Philippine election context?

### Source Data

#### Initial Data Collection and Normalization

The dataset used in this study was a subset of the corpus 1,696,613 tweets crawled by Andrade et al. and posted from November 2015 to May 2016 during the campaign period for the Philippine presidential election. They were culled based on the presence of candidate names (e.g., Binay, Duterte, Poe, Roxas, and Santiago) and election-related hashtags (e.g., #Halalan2016, #Eleksyon2016, and #PiliPinas2016).

Data preprocessing was performed to prepare the tweets for feature extraction and classification. It consisted of the following steps: data de-identification, uniform resource locator (URL) removal, special character processing, normalization, hashtag processing, and tokenization.

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

[Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph)

### Licensing Information

[More Information Needed]

### Citation Information

@article{Cabasag-2019-hate-speech,
  title={Hate speech in Philippine election-related tweets: Automatic detection and classification using natural language processing.},
  author={Neil Vicente Cabasag, Vicente Raphael Chan, Sean Christian Lim, Mark Edward Gonzales, and Charibeth Cheng},
  journal={Philippine Computing Journal},
  volume={XIV},
  number={1},
  month={August},
  year={2019}
}

### Contributions

Thanks to [@anaerobeth](https://github.com/anaerobeth) for adding this dataset.