---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- rn
- rw
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- topic-classification
paperswithcode_id: kinnews-and-kirnews
pretty_name: KinnewsKirnews
configs:
- kinnews_cleaned
- kinnews_raw
- kirnews_cleaned
- kirnews_raw
dataset_info:
- config_name: kinnews_raw
  features:
  - name: label
    dtype:
      class_label:
        names:
          0: politics
          1: sport
          2: economy
          3: health
          4: entertainment
          5: history
          6: technology
          7: tourism
          8: culture
          9: fashion
          10: religion
          11: environment
          12: education
          13: relationship
  - name: kin_label
    dtype: string
  - name: en_label
    dtype: string
  - name: url
    dtype: string
  - name: title
    dtype: string
  - name: content
    dtype: string
  splits:
  - name: test
    num_bytes: 11971938
    num_examples: 4254
  - name: train
    num_bytes: 38316546
    num_examples: 17014
  download_size: 27377755
  dataset_size: 50288484
- config_name: kinnews_cleaned
  features:
  - name: label
    dtype:
      class_label:
        names:
          0: politics
          1: sport
          2: economy
          3: health
          4: entertainment
          5: history
          6: technology
          7: tourism
          8: culture
          9: fashion
          10: religion
          11: environment
          12: education
          13: relationship
  - name: title
    dtype: string
  - name: content
    dtype: string
  splits:
  - name: test
    num_bytes: 8217453
    num_examples: 4254
  - name: train
    num_bytes: 32780382
    num_examples: 17014
  download_size: 27377755
  dataset_size: 40997835
- config_name: kirnews_raw
  features:
  - name: label
    dtype:
      class_label:
        names:
          0: politics
          1: sport
          2: economy
          3: health
          4: entertainment
          5: history
          6: technology
          7: tourism
          8: culture
          9: fashion
          10: religion
          11: environment
          12: education
          13: relationship
  - name: kir_label
    dtype: string
  - name: en_label
    dtype: string
  - name: url
    dtype: string
  - name: title
    dtype: string
  - name: content
    dtype: string
  splits:
  - name: test
    num_bytes: 2499189
    num_examples: 923
  - name: train
    num_bytes: 7343223
    num_examples: 3689
  download_size: 5186111
  dataset_size: 9842412
- config_name: kirnews_cleaned
  features:
  - name: label
    dtype:
      class_label:
        names:
          0: politics
          1: sport
          2: economy
          3: health
          4: entertainment
          5: history
          6: technology
          7: tourism
          8: culture
          9: fashion
          10: religion
          11: environment
          12: education
          13: relationship
  - name: title
    dtype: string
  - name: content
    dtype: string
  splits:
  - name: test
    num_bytes: 1570745
    num_examples: 923
  - name: train
    num_bytes: 6629767
    num_examples: 3689
  download_size: 5186111
  dataset_size: 8200512
---
# Dataset Card for kinnews_kirnews

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

- **Homepage:** [More Information Needed]
- **Repository:** https://github.com/Andrews2017/KINNEWS-and-KIRNEWS-Corpus
- **Paper:** [KINNEWS and KIRNEWS: Benchmarking Cross-Lingual Text Classification for Kinyarwanda and Kirundi](https://arxiv.org/abs/2010.12174)
- **Leaderboard:** NA
- **Point of Contact:** [Rubungo Andre Niyongabo1](mailto:niyongabor.andre@std.uestc.edu.cn)

### Dataset Summary

Kinyarwanda and Kirundi news classification datasets (KINNEWS and KIRNEWS,respectively), which were both collected from Rwanda and Burundi news websites and newspapers, for low-resource monolingual and cross-lingual multiclass classification tasks.

### Supported Tasks and Leaderboards
This dataset can be used for text classification of news articles in Kinyarwadi and Kirundi languages. Each news article can be classified into one of the 14 possible classes. The classes are:

- politics
- sport
- economy
- health
- entertainment
- history
- technology
- culture
- religion
- environment
- education
- relationship


### Languages

Kinyarwanda and Kirundi

## Dataset Structure

### Data Instances

Here is an example from the dataset:

| Field | Value |
| ----- | ----------- |
| label | 1 |
| kin_label/kir_label | 'inkino' |
| url | 'https://nawe.bi/Primus-Ligue-Imirwi-igiye-guhura-gute-ku-ndwi-ya-6-y-ihiganwa.html' |
| title | 'Primus Ligue\xa0: Imirwi igiye guhura gute ku ndwi ya 6 y’ihiganwa\xa0?'|
| content | ' Inkino zitegekanijwe kuruno wa gatandatu igenekerezo rya 14 Nyakanga umwaka wa 2019...'|
| en_label| 'sport'|




### Data Fields

The raw version of the data for Kinyarwanda language consists of these fields
- label: The category of the news article
- kin_label/kir_label: The associated label in Kinyarwanda/Kirundi language
- en_label: The associated label in English
- url: The URL of the news article
- title: The title of the news article
- content: The content of the news article

The cleaned version contains only the `label`, `title` and the `content` fields
 

### Data Splits

Lang| Train | Test |
|---| ----- | ---- |
|Kinyarwandai Raw|17014|4254|
|Kinyarwandai Clean|17014|4254|
|Kirundi Raw|3689|923|
|Kirundi Clean|3689|923|

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

```
@article{niyongabo2020kinnews,
  title={KINNEWS and KIRNEWS: Benchmarking Cross-Lingual Text Classification for Kinyarwanda and Kirundi},
  author={Niyongabo, Rubungo Andre and Qu, Hong and Kreutzer, Julia and Huang, Li},
  journal={arXiv preprint arXiv:2010.12174},
  year={2020}
}
```

### Contributions

Thanks to [@saradhix](https://github.com/saradhix) for adding this dataset.