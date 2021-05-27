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
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: allocine
---

# Dataset Card for Allociné

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

- **Homepage:** 
- **Repository:** [Allociné dataset repository](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/tree/master/allocine_dataset)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [Théophile Blard](mailto:theophile.blard@gmail.com)

### Dataset Summary

The Allociné dataset is a French-language dataset for sentiment analysis. The texts are movie reviews written between 2006 and 2020 by members of the [Allociné.fr](https://www.allocine.fr/) community for various films. It contains 100k positive and 100k negative reviews divided into train (160k), validation (20k), and test (20k). 

### Supported Tasks and Leaderboards

- `text-classification`, `sentiment-classification`: The dataset can be used to train a model for sentiment classification. The model performance is evaluated based on the accuracy of the predicted labels as compared to the given labels in the dataset. A BERT-based model, [tf-allociné](https://huggingface.co/tblard/tf-allocine), achieves 97.44% accuracy on the test set. 

### Languages

The text is in French, as spoken by users of the [Allociné.fr](https://www.allocine.fr/) website. The BCP-47 code for French is fr.

## Dataset Structure

### Data Instances

Each data instance contains the following features: _review_ and _label_. In the Hugging Face distribution of the dataset, the _label_ has 2 possible values, _0_ and _1_, which correspond to _negative_ and _positive_ respectively. See the [Allociné corpus viewer](https://huggingface.co/datasets/viewer/?dataset=allocine) to explore more examples.

An example from the Allociné train set looks like the following:
```
{'review': 'Premier film de la saga Kozure Okami, "Le Sabre de la vengeance" est un très bon film qui mêle drame et action, et qui, en 40 ans, n'a pas pris une ride.',
 'label': 1}

```

### Data Fields

- 'review': a string containing the review text
- 'label': an integer, either _0_ or _1_, indicating a _negative_ or _positive_ review, respectively

### Data Splits

The Allociné dataset has 3 splits: _train_, _validation_, and _test_. The splits contain disjoint sets of movies. The following table contains the number of reviews in each split and the percentage of positive and negative reviews. 

| Dataset Split | Number of Instances in Split | Percent Negative Reviews | Percent Positive Reviews |
| ------------- | ---------------------------- | ------------------------ | ------------------------ |
| Train         | 160,000                      | 49.6%                    | 50.4%                    |
| Validation    | 20,000                       | 51.0%                    | 49.0%                    |
| Test          | 20,000                       | 52.0%                    | 48.0%                    |

## Dataset Creation

### Curation Rationale

The Allociné dataset was developed to support large-scale sentiment analysis in French. It was released alongside the [tf-allociné](https://huggingface.co/tblard/tf-allocine) model and used to compare the performance of several language models on this task. 

### Source Data

#### Initial Data Collection and Normalization

The reviews and ratings were collected using a list of [film page urls](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/allocine_films_urls.txt) and the [allocine_scraper.py](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/allocine_scraper.py) tool. Up to 30 reviews were collected for each film. 

The reviews were originally labeled with a rating from 0.5 to 5.0 with a step of 0.5 between each rating. Ratings less than or equal to 2 are labeled as negative and ratings greater than or equal to 4 are labeled as positive. Only reviews with less than 2000 characters are included in the dataset. 

#### Who are the source language producers?

The dataset contains movie reviews produced by the online community of the [Allociné.fr](https://www.allocine.fr/) website. 

### Annotations

The dataset does not contain any additional annotations. 

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

Reviewer usernames or personal information were not collected with the reviews, but could potentially be recovered. The content of each review may include information and opinions about the film's actors, film crew, and plot.

## Considerations for Using the Data

### Social Impact of Dataset

Sentiment classification is a complex task which requires sophisticated language understanding skills. Successful models can support decision-making based on the outcome of the sentiment analysis, though such models currently require a high degree of domain specificity. 

It should be noted that the community represented in the dataset may not represent any downstream application's potential users, and the observed behavior of a model trained on this dataset may vary based on the domain and use case. 

### Discussion of Biases

The Allociné website lists a number of topics which violate their [terms of service](https://www.allocine.fr/service/conditions.html#charte). Further analysis is needed to determine the extent to which moderators have successfully removed such content. 

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

Thanks to [@thomwolf](https://github.com/thomwolf), [@TheophileBlard](https://github.com/TheophileBlard), [@lewtun](https://github.com/lewtun) and [@mcmillanmajora](https://github.com/mcmillanmajora) for adding this dataset.
