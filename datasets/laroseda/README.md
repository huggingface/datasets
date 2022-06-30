---
annotations_creators:
- found
language_creators:
- found
language:
- ro
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
pretty_name: LaRoSeDa
---

# Dataset Card for LaRoSeDa

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

- **Homepage:** [Github](https://github.com/ancatache/LaRoSeDa)
- **Repository:** [Github](https://github.com/ancatache/LaRoSeDa)
- **Paper:** [Arxiv](https://arxiv.org/pdf/2101.04197.pdf)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** raducu.ionescu@gmail.com

### Dataset Summary

LaRoSeDa - A **La**rge and **Ro**manian **Se**ntiment **Da**ta Set. LaRoSeDa contains 15,000 reviews written in Romanian, of which 7,500 are positive and 7,500 negative. 
The samples have one of four star ratings: 1 or 2 - for reviews that can be considered of negative polarity, and 4 or 5 for the positive ones.
The 15,000 samples featured in the corpus and labelled with the star rating, are splitted in a train and test subsets, with 12,000 and 3,000 samples in each subset.

### Supported Tasks and Leaderboards

[LiRo Benchmark and Leaderboard](https://eemlcommunity.github.io/ro_benchmark_leaderboard/site/)

### Languages

The text dataset is in Romanian (`ro`).

## Dataset Structure

### Data Instances

Below we have an example of sample from LaRoSeDa:

```
{
    "index": "9675",
    "title": "Nu recomand",
    "content": "probleme cu localizarea, mari...",
    "starRating": 1,
}
```

where "9675" is the sample index, followed by the title of the review, review content and then the star rating given by the user.


### Data Fields

- `index`: string, the unique indentifier of a sample.
- `title`: string, the review title.
- `content`: string, the content of the review.
- `starRating`: integer, with values in the following set {1, 2, 4, 5}.

### Data Splits

The train/test split contains 12,000/3,000 samples tagged with the star rating assigned to each sample in the dataset.

## Dataset Creation

### Curation Rationale

The samples are preprocessed in order to eliminate named entities. This is required to prevent classifiers from taking the decision based on features that are not related to the topics. 
For example, named entities that refer to politicians or football players names can provide clues about the topic. For more details, please read the [paper](https://arxiv.org/abs/1901.06543).

### Source Data


#### Data Collection and Normalization

For the data collection, one of the largest Romanian e-commerce platform was targetted. Along with the textual content of each review, the associated star ratings was also collected in order to automatically assign labels to
the collected text samples. 


#### Who are the source language producers?

The original text comes from one of the largest e-commerce platforms in Romania.

### Annotations

#### Annotation process

As mentioned above, LaRoSeDa is composed of product reviews from one of the largest e-commerce websites in Romania. The resulting samples are automatically tagged with the star rating assigned by the users.

#### Who are the annotators?

N/A

### Personal and Sensitive Information

The textual data collected for LaRoSeDa consists in product reviews freely available on the Internet. 
To the best of authors' knowledge, there is no personal or sensitive information that needed to be considered in the said textual inputs collected.

## Considerations for Using the Data

### Social Impact of Dataset

This dataset is part of an effort to encourage text classification research in languages other than English. Such work increases the accessibility of natural language technology to more regions and cultures. 
In the past three years there was a growing interest for studying Romanian from a Computational Linguistics perspective. However, we are far from having enough datasets and resources in this particular language.

### Discussion of Biases

*We note that most of the negative reviews (5,561) are rated with one star. Similarly, most of the positive reviews (6,238) are rated with five stars. Hence, the corpus is highly polarized.*

### Other Known Limitations

*The star rating might not always reflect the polarity of the text. We thus acknowledge that the automatic labeling process is not optimal, i.e. some labels might be noisy.*

## Additional Information

### Dataset Curators

Published and managed by Anca Tache, Mihaela Gaman and Radu Tudor Ionescu.

### Licensing Information

CC BY-SA 4.0 License

### Citation Information

```
@article{
    tache2101clustering,
    title={Clustering Word Embeddings with Self-Organizing Maps. Application on LaRoSeDa -- A Large Romanian Sentiment Data Set},
    author={Anca Maria Tache and Mihaela Gaman and Radu Tudor Ionescu},
    journal={ArXiv},
    year = {2021}
}
```

### Contributions

Thanks to [@MihaelaGaman](https://github.com/MihaelaGaman) for adding this dataset.

