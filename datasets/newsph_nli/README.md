---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- tl
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- natural-language-inference
paperswithcode_id: newsph-nli
---

# Dataset Card for NewsPH NLI

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

- **Homepage: [NewsPH NLI homepage](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Repository: [NewsPH NLI repository](https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks)**
- **Paper: [Arxiv paper](https://arxiv.org/pdf/2010.11574.pdf)**
- **Leaderboard:**
- **Point of Contact: [Jan Christian Cruz](mailto:jan_christian_cruz@dlsu.edu.ph)**

### Dataset Summary

First benchmark dataset for sentence entailment in the low-resource Filipino language. Constructed through exploting the structure of news articles. Contains 600,000 premise-hypothesis pairs, in 70-15-15 split for training, validation, and testing.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset contains news articles in Filipino (Tagalog) scraped rom all major Philippine news sites online.

## Dataset Structure

### Data Instances
Sample data:
  {
    "premise": "Alam ba ninyo ang ginawa ni Erap na noon ay lasing na lasing na rin?",
    "hypothesis": "Ininom niya ang alak na pinagpulbusan!",
    "label": "0"
  }


### Data Fields

[More Information Needed]

### Data Splits
Contains 600,000 premise-hypothesis pairs, in 70-15-15 split for training, validation, and testing.


## Dataset Creation

### Curation Rationale

We propose the use of news articles for automatically creating benchmark datasets for NLI because of two reasons. First, news articles commonly use single-sentence paragraphing, meaning every paragraph in a news article is limited to a single sentence. Second, straight news articles follow the “inverted pyramid” structure, where every succeeding paragraph builds upon the premise of those that came before it, with the most important information on top and the least important towards the end.

### Source Data

#### Initial Data Collection and Normalization

To create the dataset, we scrape news articles from all major Philippine news sites online. We collect a total of 229,571 straight news articles, which we then lightly preprocess to remove extraneous unicode characters and correct minimal misspellings. No further preprocessing is done to preserve information in the data.

#### Who are the source language producers?

The dataset was created by Jan Christian, Blaise Cruz, Jose Kristian Resabal, James Lin, Dan John Velasco, and Charibeth Cheng from De La Salle University and the University of the Philippines

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

Jan Christian Blaise Cruz, Jose Kristian Resabal, James Lin, Dan John Velasco and Charibeth Cheng

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

[Jan Christian Blaise Cruz] (mailto:jan_christian_cruz@dlsu.edu.ph)

### Licensing Information

[More Information Needed]

### Citation Information

@article{cruz2020investigating,
  title={Investigating the True Performance of Transformers in Low-Resource Languages: A Case Study in Automatic Corpus Creation},
  author={Jan Christian Blaise Cruz and Jose Kristian Resabal and James Lin and Dan John Velasco and Charibeth Cheng},
  journal={arXiv preprint arXiv:2010.11574},
  year={2020}
}

### Contributions

Thanks to [@anaerobeth](https://github.com/anaerobeth) for adding this dataset.