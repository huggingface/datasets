---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- tw
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for Twi Text C3

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

- **Homepage:** https://www.aclweb.org/anthology/2020.lrec-1.335
- **Repository:** https://github.com/ajesujoba/YorubaTwi-Embedding/
- **Paper:** https://www.aclweb.org/anthology/2020.lrec-1.335
- **Leaderboard:**
- **Point of Contact:** [Kwabena Amponsah-Kaakyire](mailto:s8kwampo@stud.uni-saarland.de)

### Dataset Summary

Twi Text C3 was collected from various sources from the web (Bible, JW300, wikipedia, etc)
to compare pre-trained word embeddings (Fasttext) and embeddings and embeddings trained on curated Twi Texts. 
The dataset consists of clean texts (i.e the Bible) and noisy texts (with incorrect orthography and mixed dialects)
from other online sources like Wikipedia and JW300


### Supported Tasks and Leaderboards

For training word embeddings and language models on Twi texts.

### Languages

The language supported is Twi.

## Dataset Structure

### Data Instances

A data point is a sentence in each line.
{
 'text': 'mfitiaseɛ no onyankopɔn bɔɔ ɔsoro ne asaase'
}
### Data Fields

- `text`: a `string` feature.
a sentence text per line

### Data Splits

Contains only the training split.

## Dataset Creation

### Curation Rationale

The data was created to help introduce resources to new language - Twi.

### Source Data

#### Initial Data Collection and Normalization

The dataset comes from various sources of the web: Bible, JW300, and wikipedia. 
See Table 1 in the [paper](https://www.aclweb.org/anthology/2020.lrec-1.335/) for the summary of the dataset and statistics

#### Who are the source language producers?

[Jehovah Witness](https://www.jw.org/) (JW300)
[Twi Bible](http://www.bible.com/)
[Yorùbá Wikipedia](dumps.wikimedia.org/twwiki)
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

The dataset is biased to the religion domain (Christianity) because of the inclusion of JW300 and the Bible.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The data sets were curated by Kwabena Amponsah-Kaakyire, Jesujoba Alabi, and David Adelani, students of Saarland University, Saarbrücken, Germany .

### Licensing Information


The data is under the [Creative Commons Attribution-NonCommercial 4.0 ](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

### Citation Information
```
@inproceedings{alabi-etal-2020-massive,
    title = "Massive vs. Curated Embeddings for Low-Resourced Languages: the Case of {Y}or{\`u}b{\'a} and {T}wi",
    author = "Alabi, Jesujoba  and
      Amponsah-Kaakyire, Kwabena  and
      Adelani, David  and
      Espa{\~n}a-Bonet, Cristina",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.335",
    pages = "2754--2762",
    abstract = "The success of several architectures to learn semantic representations from unannotated text and the availability of these kind of texts in online multilingual resources such as Wikipedia has facilitated the massive and automatic creation of resources for multiple languages. The evaluation of such resources is usually done for the high-resourced languages, where one has a smorgasbord of tasks and test sets to evaluate on. For low-resourced languages, the evaluation is more difficult and normally ignored, with the hope that the impressive capability of deep learning architectures to learn (multilingual) representations in the high-resourced setting holds in the low-resourced setting too. In this paper we focus on two African languages, Yor{\`u}b{\'a} and Twi, and compare the word embeddings obtained in this way, with word embeddings obtained from curated corpora and a language-dependent processing. We analyse the noise in the publicly available corpora, collect high quality and noisy data for the two languages and quantify the improvements that depend not only on the amount of data but on the quality too. We also use different architectures that learn word representations both from surface forms and characters to further exploit all the available information which showed to be important for these languages. For the evaluation, we manually translate the wordsim-353 word pairs dataset from English into Yor{\`u}b{\'a} and Twi. We extend the analysis to contextual word embeddings and evaluate multilingual BERT on a named entity recognition task. For this, we annotate with named entities the Global Voices corpus for Yor{\`u}b{\'a}. As output of the work, we provide corpora, embeddings and the test suits for both languages.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```
### Contributions

Thanks to [@dadelani](https://github.com/dadelani) for adding this dataset.