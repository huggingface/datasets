---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
---

# Dataset Card for subjqa

## Table of Contents
- [Dataset Card for subjqa](#dataset-card-for-subjqa)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
      - [Data collection](#data-collection)
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

## Dataset Description

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/lewtun/SubjQA
- **Paper:** https://arxiv.org/abs/2004.14283
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Lewis Tunstall](mailto:lewis.c.tunstall@gmail.com)

### Dataset Summary

SubjQA is a question answering dataset that focuses on subjective (as opposed to factual) questions and answers. The dataset consists of roughly **10,000** questions over reviews from 6 different domains: books, movies, grocery, electronics, TripAdvisor (i.e. hotels), and restaurants. Each question is paired with a review and a span is highlighted as the answer to the question (with some questions having no answer). Moreover, both questions and answer spans are assigned a _subjectivity_ label by annotators. Questions such as _"How much does this product weigh?"_ is a factual question (i.e., low subjectivity), while "Is this easy to use?" is a subjective question (i.e., high subjectivity).

In short, SubjQA provides a setting to study how well extractive QA systems perform on finding answer that are less factual and to what extent modeling subjectivity can imporve thte performance of QA systems.

To load a domain with `datasets` you can run the following:

```python
from datasets import load_dataset

# other options include: electronics, grocery, movies, restaurants, tripadvisor
dataset = load_dataset("subjqa", "books")
```

#### Data collection
The SubjQA dataset is constructed based on publicly available review datasets. Specifically, the _movies_, _books_, _electronics_, and _grocery_ categories are constructed using reviews from the [Amazon Review dataset](http://jmcauley.ucsd.edu/data/amazon/links.html). The _TripAdvisor_ category, as the name suggests, is constructed using reviews from TripAdvisor which can be found [here](http://times.cs.uiuc.edu/~wang296/Data/). Finally, the _restaurants_ category is constructed using the [Yelp Dataset](https://www.yelp.com/dataset) which is also publicly available.

The process of constructing SubjQA is discussed in detail in our [paper](https://arxiv.org/abs/2004.14283). In a nutshell, the dataset construction consists of the following steps:

1. First, all _opinions_ expressed in reviews are extracted. In the pipeline, each opinion is modeled as a (_modifier_, _aspect_) pair which is a pair of spans where the former describes the latter. (good, hotel), and (terrible, acting) are a few examples of extracted opinions.
2. Using Matrix Factorization techninques, implication relationships between different expressed opinions are mined. For instance, the system mines that "responsive keys" implies "good keyboard". In our pipeline, we refer to the conclusion of an implication (i.e., "good keyboard" in this examples) as the _query_ opinion, and we refer to the premise (i.e., "responsive keys") as its _neighboring_ opinion.
3. Annotators are then asked to write a question based on _query_ opinions. For instance given "good keyboard" as the query opinion, they might write "Is this keyboard any good?"
4. Each question written based on a _query_ opinion is then paired with a review that mentions its _neighboring_ opinion. In our example, that would be a review that mentions "responsive keys".
5. The question and review pairs are presented to annotators to select the correct answer span, and rate the subjectivity level of the question as well as the subjectivity level of the highlighted answer span.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text in the dataset is in English and the associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

An example from Books domain is shown below:

```json
{'ans_subj_score': 1.0,
 'answer_subj_level': 5,
 'domain': 'books',
 'human_ans_indices': '(1568, 1585)',
 'human_ans_spans': 'excellent writing',
 'is_ans_subjective': True,
 'is_ques_subjective': True,
 'item_id': '014104179X',
 'nn_asp': 'write',
 'nn_mod': 'outstanding',
 'q_review_id': '5680d7a8e25e322c08c0247547b397e8',
 'q_reviews_id': 'fccf9075ab3d3ee56ba71d04d900b786',
 'query_asp': 'write',
 'query_mod': 'intelligent',
 'ques_subj_score': 0.0,
 'question': 'How is the write?',
 'question_subj_level': 5,
 'review': 'This was a really tough book to get through. I only did because I thought the writing was outstanding. Tolz is a literary virtuoso. There are great positives in this book, from the overall originality of the novel; to the very moving and powerful climax; to an extraordinarily original and intricate plot; through Tolz\'s writing. But there are also aspects that irritate and almost made me give up halfway. These are:- the characters are impossible to like. This applies to Martin and Jasper Dean, both of whom are just too wierd and eccentric and self-important to care about. The review on the cover page comparing this novel to " A Confederacy of Dunces" does "Confederacy..." a disservice: Ignatius O Reilly is also wierd and eccentric and self important but he was comic and pathetic in a way that the Deans never manage to be.  By the way, its not easy to like much any of the secondary characters either...- some plot twists are hard to handle, eg. Anouk\'s transformation from hippy into "one of the richest women in Australia";- while the book had a hugely entertaining first 100 or so pages and equally excellent final 100 pages, the middle was boring at times, irratating at others (where it seems Tolz wants to show he\'s read every book on philosophy ever written). The one exception here is the part involving bullying and suicides at Jasper\'s school, which is really really emotionally devastating - enough so to make one persist through the book in search of more of the same power (which does finally happen).3 stars therefore for exceptional power and excellent writing, versus some (rather lengthy) deeply irritating sections and unsympathetic characters. But I\'m very curious to see what Tolz will come up with next ANSWERNOTFOUND',
 'review_id': '8d63e311f8f6ab0ae17a6a883fdae5d7'}
```

### Data Fields

Each domain and split consists of the following columns:

* ```domain```: The category/domain of the review (e.g., hotels, books, ...).
* ```question```: The question (written based on a query opinion).
* ```review```: The review (that mentions the neighboring opinion).
* ```human_ans_spans```: The span labeled by annotators as the answer.
* ```human_ans_indices```: The (character-level) start and end indices of the answer span highlighted by annotators.
* ```question_subj_level```: The subjectiviy level of the question (on a 1 to 5 scale with 1 being the most subjective).
* ```ques_subj_score```: The subjectivity score of the question computed using the [TextBlob](https://textblob.readthedocs.io/en/dev/) package.
* ```is_ques_subjective```: A boolean subjectivity label derived from ```question_subj_level``` (i.e., scores below 4 are considered as subjective)
* ```answer_subj_level```: The subjectiviy level of the answer span (on a 1 to 5 scale with 5 being the most subjective).
* ```ans_subj_score```: The subjectivity score of the answer span computed usign the [TextBlob](https://textblob.readthedocs.io/en/dev/) package.
* ```is_ans_subjective```: A boolean subjectivity label derived from ```answer_subj_level``` (i.e., scores below 4 are considered as subjective)
* ```nn_mod```: The modifier of the neighboring opinion (which appears in the review).
* ```nn_asp```: The aspect of the neighboring opinion (which appears in the review).
* ```query_mod```: The modifier of the query opinion (around which a question is manually written).
* ```query_asp```: The aspect of the query opinion (around which a question is manually written).
* ```item_id```: The id of the item/business discussed in the review.
* ```review_id```: A unique id associated with the review.
* ```q_review_id```: A unique id assigned to the question-review pair.
* ```q_reviews_id```: A unique id assigned to all question-review pairs with a shared question.

### Data Splits

Each domain consists of three splits: train, dev, and test.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

The SubjQA dataset is provided "as-is", and its creators make no
represenntation as to its accuracy. Furthermore, the creators
have on obligation to maintain the dataset.

The SubjQA dataset is constructed based on the following datasets and thus contains subsets of their data:
* [Amazon Review Dataset](http://jmcauley.ucsd.edu/data/amazon/links.html) from UCSD
    * Used for _books_, _movies_, _grocery_, and _electronics_ domains
* [The TripAdvisor Dataset](http://times.cs.uiuc.edu/~wang296/Data/) from UIUC's Database and Information Systems Laboratory
    * Used for the _TripAdvisor_ domain
* [The Yelp Dataset](https://www.yelp.com/dataset)
    * Used for the _restaurants_ domain

Consequently, the data within each domain of the SubjQA dataset should be considered under the same license as the dataset it was built upon.

### Citation Information

If you are using the dataset, please cite the following in your work:
```
@inproceedings{bjerva20subjqa,
    title = "SubjQA: A Dataset for Subjectivity and Review Comprehension",
    author = "Bjerva, Johannes  and
      Bhutani, Nikita  and
      Golahn, Behzad  and
      Tan, Wang-Chiew  and
      Augenstein, Isabelle",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing",
    month = November,
    year = "2020",
    publisher = "Association for Computational Linguistics",
}
```