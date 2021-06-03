---
annotations_creators:
- machine-generated
language_creators:
- expert-generated
languages:
- cs
- de
- el
- en
- es
- fr
- hu
- ja
- ko
- pt
- ro
- ru
- sk
- uk
- zh
- hu
licenses:
- cc-by-4.0
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: parapat
---

# Dataset Card for ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts

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

- **Homepage:** [ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts](https://figshare.com/articles/ParaPat_The_Multi-Million_Sentences_Parallel_Corpus_of_Patents_Abstracts/12627632)
- **Repository:** [ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts](https://github.com/soares-f/parapat)
- **Paper:** [ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts](https://www.aclweb.org/anthology/2020.lrec-1.465/)
- **Point of Contact:** [Felipe Soares](fs@felipesoares.net)

### Dataset Summary

ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts

This dataset contains the developed parallel corpus from the open access Google Patents dataset in 74 language pairs, comprising more than 68 million sentences and 800 million tokens. Sentences were automatically aligned using the Hunalign algorithm for the largest 22 language pairs, while the others were abstract (i.e. paragraph) aligned.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset contains samples in cs, de, el, en, es, fr, hu, ja, ko, pt, ro, ru, sk, uk, zh, hu

## Dataset Structure

### Data Instances

They are of 2 types depending on the dataset:

First type
{
   "translation":{
      "en":"A method for converting a series of m-bit information words to a modulated signal is described.",
      "es":"Se describe un método para convertir una serie de palabras de informacion de bits m a una señal modulada."
   }
}

Second type
{
   "family_id":10944407,
   "index":844,
   "translation":{
      "el":"αφές ο οποίος παρασκευάζεται με χαρμάνι ελληνικού καφέ είτε σε συσκευή καφέ εσπρέσο είτε σε συσκευή γαλλικού καφέ (φίλτρου) είτε κατά τον παραδοσιακό τρόπο του ελληνικού καφέ και διυλίζεται, κτυπιέται στη συνέχεια με πάγο σε χειροκίνητο ή ηλεκτρικόμίξερ ώστε να παγώσει ομοιόμορφα και να αποκτήσει πλούσιο αφρό και σερβίρεται σε ποτήρι. ΰ",
      "en":"offee prepared using the mix for Greek coffee either in an espresso - type coffee making machine, or in a filter coffee making machine or in the traditional way for preparing Greek coffee and is then filtered , shaken with ice manually or with an electric mixer so that it freezes homogeneously, obtains a rich froth and is served in a glass."
   }
}

### Data Fields

**index:** position in the corpus
**family id:** for each abstract, such that researchers can use that information for other text mining purposes.
**translation:** distionary containing source and target sentence for that example

### Data Splits

No official train/val/test splits given.

Parallel corpora aligned into sentence level

|Language Pair|# Sentences|# Unique Tokens|
|--------|-----|------|
|EN/ZH|4.9M|155.8M|
|EN/JA|6.1M|189.6M|
|EN/FR|12.2M|455M|
|EN/KO|2.3M|91.4M|
|EN/DE|2.2M|81.7M|
|EN/RU|4.3M|107.3M|
|DE/FR|1.2M|38.8M|
|FR/JA|0.3M|9.9M|
|EN/ES|0.6M|24.6M|

Parallel corpora aligned into abstract level

|Language Pair|# Abstracts|
|--------|-----|
|FR/KO|120,607|
|EN/UK|89,227|
|RU/UK|85,963|
|CS/EN|78,978|
|EN/RO|48,789|
|EN/HU|42,629|
|ES/FR|32,553|
|EN/SK|23,410|
|EN/PT|23,122|
|BG/EN|16,177|
|FR/RU|10,889|


## Dataset Creation

### Curation Rationale

The availability of parallel corpora is required by current Statistical and Neural Machine Translation systems (SMT and NMT). Acquiring a high-quality parallel corpus that is large enough to train MT systems, particularly NMT ones, is not a trivial task due to the need for correct alignment and, in many cases, human curation. In this context, the automated creation of parallel corpora from freely available resources is extremely important in Natural Language Pro- cessing (NLP).

### Source Data

#### Initial Data Collection and Normalization

Google makes patents data available under the Google Cloud Public Datasets. BigQuery is a Google service that supports the efficient storage and querying of massive datasets which are usually a challenging task for usual SQL databases. For instance, filtering the September 2019 release of the dataset, which contains more than 119 million rows, can take less than 1 minute for text fields. The on-demand billing for BigQuery is based on the amount of data processed by each query run, thus for a single query that performs a full-scan, the cost can be over USD 15.00, since the cost per TB is currently USD 5.00.

#### Who are the source language producers?

BigQuery is a Google service that supports the efficient storage and querying of massive datasets which are usually a challenging task for usual SQL databases.

### Annotations

#### Annotation process

The following steps describe the process of producing patent aligned abstracts:

1. Load the nth individual file
2. Remove rows where the number of abstracts with more than one language is less than 2 for a given family id. The family id attribute is used to group patents that refers to the same invention. By removing these rows, we remove abstracts that are available only in one language.
3. From the resulting set, create all possible parallel abstracts from the available languages. For instance, an abstract may be available in English, French and German, thus, the possible language pairs are English/French, English/German, and French/German.
4. Store the parallel patents into an SQL database for easier future handling and sampling.

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

Funded by Google Tensorflow Research Cloud.

### Licensing Information

CC BY 4.0

### Citation Information

```
@inproceedings{soares-etal-2020-parapat,
    title = "{P}ara{P}at: The Multi-Million Sentences Parallel Corpus of Patents Abstracts",
    author = "Soares, Felipe  and
      Stevenson, Mark  and
      Bartolome, Diego  and
      Zaretskaya, Anna",
    booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.465",
    pages = "3769--3774",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

[DOI](https://doi.org/10.6084/m9.figshare.12627632)
### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.