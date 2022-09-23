---
annotations_creators:
- machine-generated
language_creators:
- expert-generated
language:
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
license:
- cc-by-4.0
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
paperswithcode_id: parapat
pretty_name: Parallel Corpus of Patents Abstracts
dataset_info:
- config_name: el-en
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - en
  splits:
  - name: train
    num_bytes: 24818840
    num_examples: 10855
  download_size: 24894705
  dataset_size: 24818840
- config_name: cs-en
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - en
  splits:
  - name: train
    num_bytes: 117555722
    num_examples: 78977
  download_size: 118010340
  dataset_size: 117555722
- config_name: en-hu
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hu
  splits:
  - name: train
    num_bytes: 80637157
    num_examples: 42629
  download_size: 80893995
  dataset_size: 80637157
- config_name: en-ro
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ro
  splits:
  - name: train
    num_bytes: 80290819
    num_examples: 48789
  download_size: 80562562
  dataset_size: 80290819
- config_name: en-sk
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sk
  splits:
  - name: train
    num_bytes: 31510348
    num_examples: 23410
  download_size: 31707728
  dataset_size: 31510348
- config_name: en-uk
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - uk
  splits:
  - name: train
    num_bytes: 136808871
    num_examples: 89226
  download_size: 137391928
  dataset_size: 136808871
- config_name: es-fr
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - fr
  splits:
  - name: train
    num_bytes: 53767035
    num_examples: 32553
  download_size: 53989438
  dataset_size: 53767035
- config_name: fr-ru
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ru
  splits:
  - name: train
    num_bytes: 33915203
    num_examples: 10889
  download_size: 33994490
  dataset_size: 33915203
- config_name: de-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - fr
  splits:
  - name: train
    num_bytes: 655742822
    num_examples: 1167988
  download_size: 204094654
  dataset_size: 655742822
- config_name: en-ja
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ja
  splits:
  - name: train
    num_bytes: 3100002828
    num_examples: 6170339
  download_size: 1093334863
  dataset_size: 3100002828
- config_name: en-es
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - es
  splits:
  - name: train
    num_bytes: 337690858
    num_examples: 649396
  download_size: 105202237
  dataset_size: 337690858
- config_name: en-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fr
  splits:
  - name: train
    num_bytes: 6103179552
    num_examples: 12223525
  download_size: 1846098331
  dataset_size: 6103179552
- config_name: de-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - en
  splits:
  - name: train
    num_bytes: 1059631418
    num_examples: 2165054
  download_size: 339299130
  dataset_size: 1059631418
- config_name: en-ko
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ko
  splits:
  - name: train
    num_bytes: 1466703472
    num_examples: 2324357
  download_size: 475152089
  dataset_size: 1466703472
- config_name: fr-ja
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ja
  splits:
  - name: train
    num_bytes: 211127021
    num_examples: 313422
  download_size: 69038401
  dataset_size: 211127021
- config_name: en-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zh
  splits:
  - name: train
    num_bytes: 2297993338
    num_examples: 4897841
  download_size: 899568201
  dataset_size: 2297993338
- config_name: en-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ru
  splits:
  - name: train
    num_bytes: 1974874480
    num_examples: 4296399
  download_size: 567240359
  dataset_size: 1974874480
- config_name: fr-ko
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ko
  splits:
  - name: train
    num_bytes: 222006786
    num_examples: 120607
  download_size: 64621605
  dataset_size: 222006786
- config_name: ru-uk
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - uk
  splits:
  - name: train
    num_bytes: 163442529
    num_examples: 85963
  download_size: 38709524
  dataset_size: 163442529
- config_name: en-pt
  features:
  - name: index
    dtype: int32
  - name: family_id
    dtype: int32
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pt
  splits:
  - name: train
    num_bytes: 37372555
    num_examples: 23121
  download_size: 12781082
  dataset_size: 37372555
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