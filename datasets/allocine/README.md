---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- fr
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 100K < n <1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for Allociné

## Table of Contents
- [Dataset Card for Allociné](#dataset-card-for-allociné)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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
- **Repository:** [Allociné dataset repository](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/tree/master/allocine_dataset)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [Théophile Blard](mailto:theophile.blard@gmail.com)

### Dataset Summary

The Allociné dataset was developed for large-scale sentiment analysis in French. The texts are movie reviews written by members of the [Allociné.fr](https://www.allocine.fr/) community for various films. The reviews were written between 2006 and 2020. Further information on the kinds of films included in the dataset has not been documented.

### Supported Tasks and Leaderboards

[tf-allociné](https://huggingface.co/tblard/tf-allocine) achieves 97.44% accuracy on the test set. 

### Languages

The BCP-47 code for French is fr.

## Dataset Structure

### Data Instances

Each data instance contains the following features: _review_ and _label_. In the Hugging Face distribution of the dataset, the _label_ has 2 possible values, _0_ and _1_, which correspond to _negative_ and _positive_ respectively. See the [Allociné corpus viewer](https://huggingface.co/datasets/viewer/?dataset=allocine) to explore more examples.

An example from the Allociné train set looks like the following:
```
{'review': 'Premier film de la saga Kozure Okami, "Le Sabre de la vengeance" est un très bon film qui mêle drame et action, et qui, en 40 ans, n'a pas pris une ride.',
 'label': 1}

```

### Data Fields

- 'review'
- 'label'

### Data Splits

The Allociné dataset has 3 splits: _train_, _validation_, and _test_. The splits contain disjoint sets of movies. The following table contains the number of reviews in each split and the percentage of positive and negative reviews. 
Dataset Split | Number of Instances in Split | Percent Negative Reviews | Percent Positive Reviews
--------------|------------------------------|--------------------------|-------------------------
Train | 160,000 | 49.6% | 50.4%
Validation | 20,000 | 51.0% | 49.0%
Test | 20,000 | 52.0% | 48.0%

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The reviews and ratings were collected using a list of [film page urls](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/allocine_films_urls.txt) and the [allocine_scraper.py](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/allocine_scraper.py) tool. Up to 30 reviews were collected for each film. 

The reviews were originally labeled with a rating from 0.5 to 5.0 with a step of 0.5 between each rating. Ratings less than or equal to 2 are labeled as negative and ratings greater than or equal to 4 are labeled as positive. Only reviews with less than 2000 characters are included in the dataset. 

#### Who are the source language producers?

The dataset contains movie reviews collected from [Allociné.fr](https://www.allocine.fr/). The content of each review may include information and opinions about the film's actors, film crew, and plot.

### Annotations

The dataset does not contain any additional annotations. 

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

The limitations of the Allociné dataset have not yet been investigated, however [Staliūnaitė and Bonfil (2017)](https://www.aclweb.org/anthology/W17-5410.pdf) detail linguistic phenomena that are generally present in sentiment analysis but difficult for models to accurately label, such as negation, adverbial modifiers, and reviewer pragmatics. 

## Additional Information

### Dataset Curators

The Allociné dataset was collected by Théophile Blard. 

### Licensing Information

The Allociné dataset is licensed under the [MIT License](https://opensource.org/licenses/MIT).

### Citation Information

> Théophile Blard, French sentiment analysis with BERT, (2020), GitHub repository, <https://github.com/TheophileBlard/french-sentiment-analysis-with-bert>

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@TheophileBlard](https://github.com/TheophileBlard), [@lewtun](https://github.com/lewtun) for adding this dataset.
