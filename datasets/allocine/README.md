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
---

# Dataset Card for Allociné

## Table of Contents
- [Tasks Supported](#tasks-supported)
- [Purpose](#purpose)
- [Languages](#languages)
- [People Involved](#who-iswas-involved-in-the-dataset-use-and-creation)
- [Data Characteristics](#data-characteristics)
- [Dataset Structure](#dataset-structure)
- [Known Limitations](#known-limitations)
- [Licensing information](#licensing-information)

## Tasks supported:
### Task categorization / tags

Text to binary text classification

## Purpose

The Allociné dataset was developed for large-scale sentiment analysis in French. 

## Languages 
### Per language:

The BCP-47 code for French is fr. Dialect information is unknown (see Speaker section for further details).

## Who is/was involved in the dataset use and creation?
### Who are the dataset curators?

The Allociné dataset was collected by Théophile Blard. 

### Who are the language producers (who wrote the text / created the base content)?

The dataset contains movie reviews collected from [Allociné.fr](https://www.allocine.fr/). The content of each review may include information and opinions about the film's actors, film crew, and plot.

### Who are the annotators?

No annotations were included in this dataset. 

## Data characteristics

The texts are movie reviews written by members of the [Allociné.fr](https://www.allocine.fr/) community for various films. The reviews were written between 2006 and 2020. Further information on the kinds of films included in the dataset has not been documented.

### How was the data collected?

The reviews and ratings were collected using a list of [film page urls](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/allocine_films_urls.txt) and the [allocine_scraper.py](https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/blob/master/allocine_dataset/allocine_scraper.py) tool. Up to 30 reviews were collected for each film. 

### Normalization information

The reviews were originally labeled with a rating from 0.5 to 5.0 with a step of 0.5 between each rating. Ratings less than or equal to 2 are labeled as negative and ratings greater than or equal to 4 are labeled as positive. Only reviews with less than 2000 characters are included in the dataset. 

### Annotation process

No annotations were included in this dataset. 

## Dataset Structure
### Splits, features, and labels

The Allociné dataset has 3 splits: _train_, _validation_, and _test_. The splits contain disjoint sets of movies. The following table contains the number of reviews in each split and the percentage of positive and negative reviews. 
Dataset Split | Number of Instances in Split | Percent Negative Reviews | Percent Positive Reviews
--------------|------------------------------|--------------------------|-------------------------
Train | 160,000 | 49.6% | 50.4%
Validation | 20,000 | 51.0% | 49.0%
Test | 20,000 | 52.0% | 48.0%

Each data instance contains the following features: _review_ and _label_. In the Hugging Face distribution of the dataset, the _label_ has 2 possible values, _0_ and _1_, which correspond to _negative_ and _positive_ respectively. 

### Span indices

No span indices are included in this dataset.

### Example ID

The ID is an integer starting from 0. It has no inherent meaning. 

### Free text description for context (e.g. describe difference between title / selftext / body in Reddit data) and example

For each ID, there is a string for the review and an integer for the label. See the [Allociné corpus viewer](https://huggingface.co/nlp/viewer/?dataset=allocine) to explore more examples.

ID | Review | Label
---|--------|-------
4	| Premier film de la saga Kozure Okami, "Le Sabre de la vengeance" est un très bon film qui mêle drame et action, et qui, en 40 ans, n'a pas pris une ride.	| 1
5	| L'amnésie est un thème en or pour susciter le mystère. Encore faut-il être capable de construire un scénario qui se tienne. Celui-ci est boursouflé et accumule incohérences et invraisemblances. Notons aussi la stupidité du titre français, sans lien avec l'histoire.	| 0


### Suggested metrics / models:

[tf-allociné](https://huggingface.co/tblard/tf-allocine) achieves 97.44% accuracy on the test set. 

## Known Limitations
### Known social biases

The social biases of this dataset have not yet been investigated.

### Other known limitations

The limitations of the Allociné dataset have not yet been investigated, however [Staliūnaitė and Bonfil (2017)](https://www.aclweb.org/anthology/W17-5410.pdf) detail linguistic phenomena that are generally present in sentiment analysis but difficult for models to accurately label, such as negation, adverbial modifiers, and reviewer pragmatics. 

## Licensing information

The Allociné dataset is licensed under the [MIT License](https://opensource.org/licenses/MIT).

