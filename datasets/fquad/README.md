---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
language:
- fr
license:
- cc-by-nc-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
- text-retrieval
task_ids:
- extractive-qa
- closed-domain-qa
paperswithcode_id: fquad
pretty_name: "FQuAD: French Question Answering Dataset"
---

# Dataset Card for FQuAD

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

- **Homepage:** [https://fquad.illuin.tech/](https://fquad.illuin.tech/)
- **Paper:**  [FQuAD: French Question Answering Dataset](https://arxiv.org/abs/2002.06071)
- **Point of Contact:** [https://www.illuin.tech/contact/](https://www.illuin.tech/contact/)
- **Size of downloaded dataset files:** 3.14 MB
- **Size of the generated dataset:** 6.62 MB
- **Total amount of disk used:** 9.76 MB

### Dataset Summary

FQuAD: French Question Answering Dataset
We introduce FQuAD, a native French Question Answering Dataset.

FQuAD contains 25,000+ question and answer pairs.
Finetuning CamemBERT on FQuAD yields a F1 score of 88% and an exact match of 77.9%.
Developped to provide a SQuAD equivalent in the French language. Questions are original and based on high quality Wikipedia articles.

### Supported Tasks and Leaderboards

- `closed-domain-qa`, `text-retrieval`: This dataset is intended to be used for `closed-domain-qa`, but can also be used for information retrieval tasks.

### Languages

This dataset is exclusively in French, with context data from Wikipedia and questions from French university students (`fr`).

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 3.14 MB
- **Size of the generated dataset:** 6.62 MB
- **Total amount of disk used:** 9.76 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answers_starts": [161, 46, 204],
        "texts": ["La Vierge aux rochers", "documents contemporains", "objets de spéculations"]
    },
    "context": "\"Les deux tableaux sont certes décrits par des documents contemporains à leur création mais ceux-ci ne le font qu'indirectement ...",
    "questions": ["Que concerne principalement les documents ?", "Par quoi sont décrit les deux tableaux ?", "Quels types d'objets sont les deux tableaux aux yeux des chercheurs ?"]
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `context`: a `string` feature.
- `questions`: a `list` of `string` features.
- `answers`: a dictionary feature containing:
  - `texts`: a `string` feature.
  - `answers_starts`: a `int32` feature.

### Data Splits

The FQuAD dataset has 3 splits: _train_, _validation_, and _test_. The _test_ split is however not released publicly at the moment. The splits contain disjoint sets of articles. The following table contains stats about each split.

Dataset Split | Number of Articles in Split | Number of paragraphs in split | Number of questions in split
--------------|------------------------------|--------------------------|-------------------------
Train | 117 | 4921 | 20731
Validation | 768 | 51.0% | 3188
Test | 10 | 532 | 2189

## Dataset Creation

### Curation Rationale
  The FQuAD dataset was created by Illuin technology. It was developped to provide a SQuAD equivalent in the French language. Questions are original and based on high quality Wikipedia articles.

### Source Data

The text used for the contexts are from the curated list of French High-Quality Wikipedia [articles](https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Article_de_qualit%C3%A9).
### Annotations

Annotations (spans and questions) are written by students of the CentraleSupélec school of engineering.
Wikipedia articles were scraped and Illuin used an internally-developped tool to help annotators ask questions and indicate the answer spans.
Annotators were given paragraph sized contexts and asked to generate 4/5 non-trivial questions about information in the context.

### Personal and Sensitive Information

No personal or sensitive information is included in this dataset. This has been manually verified by the dataset curators.

## Considerations for Using the Data

Users should consider this dataset is sampled from Wikipedia data which might not be representative of all QA use cases.

### Social Impact of Dataset

The social biases of this dataset have not yet been investigated.

### Discussion of Biases

The social biases of this dataset have not yet been investigated, though articles have been selected by their quality and objectivity.

### Other Known Limitations

The limitations of the FQuAD dataset have not yet been investigated.

## Additional Information

### Dataset Curators

Illuin Technology:  [https://fquad.illuin.tech/](https://fquad.illuin.tech/)

### Licensing Information

The FQuAD dataset is licensed under the [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/fr/) license.

It allows personal and academic research uses of the dataset, but not commercial uses. So concretely, the dataset cannot be used to train a model that is then put into production within a business or a company. For this type of commercial use, we invite FQuAD users to contact [the authors](https://www.illuin.tech/contact/) to discuss possible partnerships.

### Citation Information

```
@ARTICLE{2020arXiv200206071
       author = {Martin, d'Hoffschmidt and Maxime, Vidal and
         Wacim, Belblidia and Tom, Brendlé},
        title = "{FQuAD: French Question Answering Dataset}",
      journal = {arXiv e-prints},
     keywords = {Computer Science - Computation and Language},
         year = "2020",
        month = "Feb",
          eid = {arXiv:2002.06071},
        pages = {arXiv:2002.06071},
archivePrefix = {arXiv},
       eprint = {2002.06071},
 primaryClass = {cs.CL}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun), [@albertvillanova](https://github.com/albertvillanova) for adding this dataset.
Thanks to [@ManuelFay](https://github.com/manuelfay) for providing information on the dataset creation process.
