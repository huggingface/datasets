---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- da
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-Danish-Universal-Dependencies-treebank
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- part-of-speech-tagging
paperswithcode_id: dane
pretty_name: DaNE
---

# Dataset Card for DaNE

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

- **Homepage:** [DaNE homepage](https://danlp-alexandra.readthedocs.io/en/latest/docs/datasets.html#dane)
- **Repository:** [Github](https://github.com/alexandrainst/danlp)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/2020.lrec-1.565)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The Danish Dependency Treebank (DaNE) is a named entity annotation for the Danish Universal Dependencies treebank using the CoNLL-2003 annotation scheme.

The Danish UD treebank (Johannsen et al., 2015, UD-DDT) is a conversion of the Danish Dependency Treebank (Buch-Kromann et al. 2003) based on texts from Parole (Britt, 1998). UD-DDT has annotations for dependency parsing and part-of-speech (POS) tagging. The dataset was annotated with Named Entities for PER, ORG, and LOC by the Alexandra Institute in the DaNE dataset (Hvingelby et al. 2020). 

### Supported Tasks and Leaderboards

Parts-of-speech tagging, dependency parsing and named entitity recognition.

### Languages

Danish

## Dataset Structure

### Data Instances

This is an example in the "train" split:
```python
{
  'sent_id': 'train-v2-0\n', 
  'lemmas': ['på', 'fredag', 'have', 'SiD', 'invitere', 'til', 'reception', 'i', 'SID-hus', 'i', 'anledning', 'af', 'at', 'formand', 'Kjeld', 'Christensen', 'gå', 'ind', 'i', 'den', 'glad', 'tresser', '.'],
  'dep_labels': [35, 16, 28, 33, 19, 35, 16, 35, 18, 35, 18, 1, 1, 33, 22, 12, 32, 11, 35, 10, 30, 16, 34],
  'ner_tags': [0, 0, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0],
  'morph_tags': ['AdpType=Prep', 'Definite=Ind|Gender=Com|Number=Sing', 'Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Act', '_', 'Definite=Ind|Number=Sing|Tense=Past|VerbForm=Part', 'AdpType=Prep', 'Definite=Ind|Gender=Com|Number=Sing', 'AdpType=Prep', 'Definite=Def|Gender=Neut|Number=Sing', 'AdpType=Prep', 'Definite=Ind|Gender=Com|Number=Sing', 'AdpType=Prep', '_', 'Definite=Def|Gender=Com|Number=Sing', '_', '_', 'Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Act', '_', 'AdpType=Prep', 'Number=Plur|PronType=Dem', 'Degree=Pos|Number=Plur', 'Definite=Ind|Gender=Com|Number=Plur', '_'], 
  'dep_ids': [2, 5, 5, 5, 0, 7, 5, 9, 7, 11, 7, 17, 17, 17, 14, 15, 11, 17, 22, 22, 22, 18, 5], 
  'pos_tags': [11, 12, 5, 7, 3, 11, 12, 11, 12, 11, 12, 11, 16, 12, 7, 7, 3, 9, 11, 14, 6, 12, 10], 
  'text': 'På fredag har SID inviteret til reception i SID-huset i anledning af at formanden Kjeld Christensen går ind i de glade tressere.\n', 
  'tokens': ['På', 'fredag', 'har', 'SID', 'inviteret', 'til', 'reception', 'i', 'SID-huset', 'i', 'anledning', 'af', 'at', 'formanden', 'Kjeld', 'Christensen', 'går', 'ind', 'i', 'de', 'glade', 'tressere', '.'], 
  'tok_ids': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
}
```

### Data Fields

Data Fields:
  - q_id: a string question identifier for each example, corresponding to its ID in the Pushshift.io Reddit submission dumps.
  - subreddit: One of explainlikeimfive, askscience, or AskHistorians, indicating which subreddit the question came from
  - title: title of the question, with URLs extracted and replaced by URL_n tokens
  - title_urls: list of the extracted URLs, the nth element of the list was replaced by URL_n
  - sent_id: a string identifier for each example
  - text: a string, the original sentence (not tokenized)
  - tok_ids: a list of ids (int), one for each token
  - tokens: a list of strings, the tokens
  - lemmas: a list of strings, the lemmas of the tokens
  - pos_tags: a list of strings, the part-of-speech tags of the tokens
  - morph_tags: a list of strings, the morphological tags of the tokens
  - dep_ids: a list of ids (int), the id of the head of the incoming dependency for each token
  - dep_labels: a list of strings, the dependency labels
  - ner_tags: a list of strings, the named entity tags (BIO format)

### Data Splits

|             |  Tain  |   Dev  |  Test  |
|-------------|-------:|-------:|-------:|
| # sentences |   4383 |    564 |    565 |
| # tokens    | 80 378 | 10 322 | 10 023 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Citation Information

```
@inproceedings{hvingelby-etal-2020-dane,
    title = "{D}a{NE}: A Named Entity Resource for {D}anish",
    author = "Hvingelby, Rasmus  and
      Pauli, Amalie Brogaard  and
      Barrett, Maria  and
      Rosted, Christina  and
      Lidegaard, Lasse Malm  and
      S{\o}gaard, Anders",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.565",
    pages = "4597--4604",
    abstract = "We present a named entity annotation for the Danish Universal Dependencies treebank using the CoNLL-2003 annotation scheme: DaNE. It is the largest publicly available, Danish named entity gold annotation. We evaluate the quality of our annotations intrinsically by double annotating the entire treebank and extrinsically by comparing our annotations to a recently released named entity annotation of the validation and test sections of the Danish Universal Dependencies treebank. We benchmark the new resource by training and evaluating competitive architectures for supervised named entity recognition (NER), including FLAIR, monolingual (Danish) BERT and multilingual BERT. We explore cross-lingual transfer in multilingual BERT from five related languages in zero-shot and direct transfer setups, and we show that even with our modestly-sized training set, we improve Danish NER over a recent cross-lingual approach, as well as over zero-shot transfer from five related languages. Using multilingual BERT, we achieve higher performance by fine-tuning on both DaNE and a larger Bokm{\aa}l (Norwegian) training set compared to only using DaNE. However, the highest performance isachieved by using a Danish BERT fine-tuned on DaNE. Our dataset enables improvements and applicability for Danish NER beyond cross-lingual methods. We employ a thorough error analysis of the predictions of the best models for seen and unseen entities, as well as their robustness on un-capitalized text. The annotated dataset and all the trained models are made publicly available.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

### Contributions

Thanks to [@ophelielacroix](https://github.com/ophelielacroix), [@lhoestq](https://github.com/lhoestq) for adding this dataset.
