---
annotations_creators:
- crowdsourced
- machine-generated
language_creators:
- crowdsourced
- machine-generated
languages:
- en
- fr
licenses:
- mit
multilinguality:
- translation
size_categories:
- 1K<n<10K
source_datasets: []
task_categories:
- text-classification
- text-scoring
task_ids:
- semantic-similarity-classification
- semantic-similarity-scoring
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [Github](https://github.com/Elbria/xling-SemDiv/tree/master/REFreSD)
- **Repository:** [Github](https://github.com/Elbria/xling-SemDiv/)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/2020.emnlp-main.121)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The Rationalized English-French Semantic Divergences (REFreSD) dataset consists of 1,039
 English-French sentence-pairs annotated with sentence-level divergence judgments and token-level
 rationales. For any questions, write to ebriakou@cs.umd.edu.

### Supported Tasks and Leaderboards

Similarity classification and scoring (3 classes).

### Languages

English and French

## Dataset Structure
### Data Instances
Each data point looks like this:

```python
{
  'sentence_pair': {'en': 'The invention of farming some 10,000 years ago led to the development of agrarian societies , whether nomadic or peasant , the latter in particular almost always dominated by a strong sense of traditionalism .', 
                    'fr': "En quelques décennies , l' activité économique de la vallée est passée d' une mono-activité agricole essentiellement vivrière , à une quasi mono-activité touristique , si l' on excepte un artisanat du bâtiment traditionnel important , en partie saisonnier ."}
  'label': 0, 
  'all_labels': 0, 
  'rationale_en': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
  'rationale_fr': [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3], 
}
```

### Data Fields

- `sentence_pair`: Dictionary of sentences containing the following field.
  - `en`: The English sentence.
  - `fr`: The corresponding (or not) French sentence.
  
- `label`: Binary. Whether both sentences correspond. `{0:divergent, 1:equivalent}`
- `all_labels`: 3-class label `{0: "unrelated", 1: "some_meaning_difference", 2:"no_meaning_difference"}`. The first two are sub-classes of the `divergent` label. 
- `rationale_en`: Word-aligned rationale for the classification, from English. 
- `rationale_fr`: Word-aligned rationale for the classification, from French.

### Data Splits
1039 sentence pairs in a single `"train"` split.

## Dataset Creation

### Curation Rationale

See [paper](https://arxiv.org/abs/2010.03662v1).

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

See [paper](https://arxiv.org/abs/2010.03662v1).

#### Who are the annotators?

See [paper](https://arxiv.org/abs/2010.03662v1).

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

Eleftheria Briakou and Marine Carpuat

### Licensing Information

[MIT License](https://github.com/Elbria/xling-SemDiv/blob/master/LICENSE)

### Citation Information

```BibTeX
@inproceedings{briakou-carpuat-2020-detecting,
    title = "Detecting Fine-Grained Cross-Lingual Semantic Divergences without Supervision by Learning to Rank",
    author = "Briakou, Eleftheria and Carpuat, Marine",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.121",
    pages = "1563--1580",
}
```

### Contributions

Thanks to [@mpariente](https://github.com/mpariente) for adding this dataset.