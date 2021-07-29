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
paperswithcode_id: refresd
---

# Dataset Card for REFreSD Dataset

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

- **Homepage:** [Github](https://github.com/Elbria/xling-SemDiv/tree/master/REFreSD)
- **Repository:** [Github](https://github.com/Elbria/xling-SemDiv/)
- **Paper:** [Detecting Fine-Grained Cross-Lingual Semantic Divergences without Supervision by Learning to Rank](https://www.aclweb.org/anthology/2020.emnlp-main.121)
- **Leaderboard:**
- **Point of Contact:** [Eleftheria Briakou](mailto:ebriakou@cs.umd.edu)
- **Additional Documentation:** [Annotation workflow, data statement, DataSheet, and IRB documentation](https://elbria.github.io/post/refresd/)

### Dataset Summary

The Rationalized English-French Semantic Divergences (REFreSD) dataset consists of 1,039 English-French sentence-pairs annotated with sentence-level divergence judgments and token-level rationales. The project under which REFreSD was collected aims to advance our fundamental understanding of computational representations and methods for comparing and contrasting text meaning across languages. 

### Supported Tasks and Leaderboards

`semantic-similarity-classification` and `semantic-similarity-scoring`: This dataset can by used to assess the ability of computational methods to detect meaning mismatches between languages. The model performance is measured in terms of accuracy by comparing the model predictions with the human judgments in REFreSD. Details about the results of a BERT-based model, Divergent mBERT, over this dataset can be found in the [paper](https://www.aclweb.org/anthology/2020.emnlp-main.121).

### Languages

The text is in English and French as found on Wikipedia. The associated BCP-47 codes are `en` and `fr`. 

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
- `rationale_en`: A list of integers from 0-3 indicating the number of annotators who highlighted the token of the text in the English sentence during annotation. Word-aligned rationale for the divergent/equivalent label, from English. 
- `rationale_fr`: A list of integers from 0-3 indicating the number of annotators who highlighted the token of the text in the French sentence during annotation. Word-aligned rationale for the divergent/equivalent label, from French.

### Data Splits

The dataset contains 1039 sentence pairs in a single `"train"` split. Of these pairs, 64% are annotated as divergent, and 40% contain fine-grained meaning divergences.

| Label                   | Number of Instances |
| ----------------------- | ------------------- |
| Unrelated               | 252                 |
| Some meaning difference | 418                 |
| No meaning different    | 369                 |

## Dataset Creation

### Curation Rationale

The curators chose the English-French section of the WikiMatrix corpus because (1) it is likely to contain diverse, interesting divergence types since it consists of mined parallel sentences of diverse topics which are not necessarily generated by (human) translations, and (2) Wikipedia and WikiMatrix are widely used resources to train semantic representations and perform cross-lingual transfer in NLP. 

### Source Data

#### Initial Data Collection and Normalization

The source for this corpus is the English and French portion of the [WikiMatrix corpus](https://arxiv.org/abs/1907.05791), which itself was extracted from Wikipedia articles. The curators excluded noisy samples by filtering out sentence pairs that a) were too short or too long, b) consisted mostly of numbers, or c) had a small token-level edit difference.

#### Who are the source language producers?

Some content of Wikipedia articles has been (human) translated from existing articles in another language while others have been written or edited independently in each language. Therefore, information on how the original text is created is not available.

### Annotations

#### Annotation process

The annotations were collected over the span of three weeks in April 2020. Annotators were presented with an English sentence and a French sentence. First, they highlighted spans and labeled them as 'added', 'changed', or 'other', where added spans contain information not contained in the other sentence, changed spans contain some information that is in the other sentence but whose meaning is not the same, and other spans have some different meaning not covered in the previous two cases, such as idioms. They then assessed the relation between the two sentences as either 'unrelated', 'some meaning differences', or 'no meaning difference'. See the [annotation guidelines](https://elbria.github.io/post/refresd/files/REFreSD_Annotation_Guidelines.pdf) for more information about the task and the annotation interface, and see the [DataSheet](https://elbria.github.io/post/refresd/files/REFreSD_Datasheet.pdf) for information about the annotator compensation.

The following table contains Inter-Annotator Agreement metrics for the dataset:

| Granularity | Method          | IAA          |
| ----------- | --------------- | ------------ |
| Sentence    | Krippendorf's α | 0.60         |
| Span        | macro F1        | 45.56 ± 7.60 |
| Token       | macro F1        | 33.94 ± 8.24 |

#### Who are the annotators?

This dataset includes annotations from 6 participants recruited from the University of Maryland, College Park (UMD) educational institution. Participants ranged in age from 20–25 years, including one man and five women. For each participant, the curators ensured they were proficient in both languages of interest: three of them self-reported as English native speakers, one as a French native speaker, and two as bilingual English-French speakers. 

### Personal and Sensitive Information

The dataset contains discussions of people as they appear in Wikipedia articles. It does not contain confidential information, nor does it contain identifying information about the source language producers or the annotators. 

## Considerations for Using the Data

### Social Impact of Dataset

Models that are successful in the supported task require sophisticated semantic representations at the sentence level beyond the combined representations of the individual tokens in isolation. Such models could be used to curate parallel corpora for tasks like machine translation, cross-lingual transfer learning, or semantic modeling. 

The statements in the dataset, however, are not necessarily representative of the world and may overrepresent one worldview if one language is primarily translated to, rather than an equal distribution of translations between the languages. 

### Discussion of Biases

The English Wikipedia is known to have significantly more [contributors](https://en.wikipedia.org/wiki/Wikipedia:Who_writes_Wikipedia%3F) who identify as male than any other gender and who reside in either North America or Europe. This leads to an overrepresentation of male perspectives from these locations in the corpus in terms of both the topics covered and the language used to talk about those topics. It's not clear to what degree this holds true for the French Wikipedia. The REFreSD dataset itself has not yet been examined for the degree to which it contains the gender and other biases seen in the larger Wikipedia datasets. 

### Other Known Limitations

It is unknown how many of the sentences in the dataset were written independently, and how many were written as [translations](https://en.wikipedia.org/wiki/Wikipedia:Translation) by either humans or machines from some other language to the languages of interest in this dataset. 

## Additional Information

### Dataset Curators

The dataset curators are Eleftheria Briakou and Marine Carpuat, who are both affiliated with the University of Maryland, College Park's Department of Computer Science. 

### Licensing Information

The project is licensed under the [MIT License](https://github.com/Elbria/xling-SemDiv/blob/master/LICENSE). 

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

Thanks to [@mpariente](https://github.com/mpariente) and [@mcmillanmajora](https://github.com/mcmillanmajora) for adding this dataset.
