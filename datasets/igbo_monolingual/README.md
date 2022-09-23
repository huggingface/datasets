---
annotations_creators:
- found
language_creators:
- found
language:
- ig
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
paperswithcode_id: null
pretty_name: Igbo Monolingual Dataset
configs:
- bbc-igbo
- eze_goes_to_school
- igbo-radio
- jw-books
- jw-nt-igbo
- jw-ot-igbo
- jw-teta
- jw-ulo_nche
- jw-ulo_nche_naamu
dataset_info:
- config_name: eze_goes_to_school
  features:
  - name: format
    dtype: string
  - name: title
    dtype: string
  - name: chapters
    sequence:
    - name: title
      dtype: string
    - name: content
      dtype: string
  splits:
  - name: train
    num_bytes: 128309
    num_examples: 1
  download_size: 8260947
  dataset_size: 128309
- config_name: bbc-igbo
  features:
  - name: source
    dtype: string
  - name: title
    dtype: string
  - name: description
    dtype: string
  - name: date
    dtype: string
  - name: headline
    dtype: string
  - name: content
    dtype: string
  - name: tags
    sequence: string
  splits:
  - name: train
    num_bytes: 3488908
    num_examples: 1297
  download_size: 8260947
  dataset_size: 3488908
- config_name: igbo-radio
  features:
  - name: source
    dtype: string
  - name: headline
    dtype: string
  - name: author
    dtype: string
  - name: date
    dtype: string
  - name: description
    dtype: string
  - name: content
    dtype: string
  splits:
  - name: train
    num_bytes: 1129644
    num_examples: 440
  download_size: 8260947
  dataset_size: 1129644
- config_name: jw-ot-igbo
  features:
  - name: format
    dtype: string
  - name: title
    dtype: string
  - name: chapters
    sequence:
    - name: title
      dtype: string
    - name: content
      dtype: string
  splits:
  - name: train
    num_bytes: 3489314
    num_examples: 39
  download_size: 8260947
  dataset_size: 3489314
- config_name: jw-nt-igbo
  features:
  - name: format
    dtype: string
  - name: title
    dtype: string
  - name: chapters
    sequence:
    - name: title
      dtype: string
    - name: content
      dtype: string
  splits:
  - name: train
    num_bytes: 1228779
    num_examples: 27
  download_size: 8260947
  dataset_size: 1228779
- config_name: jw-books
  features:
  - name: title
    dtype: string
  - name: content
    dtype: string
  - name: format
    dtype: string
  - name: date
    dtype: string
  splits:
  - name: train
    num_bytes: 9456342
    num_examples: 48
  download_size: 8260947
  dataset_size: 9456342
- config_name: jw-teta
  features:
  - name: title
    dtype: string
  - name: content
    dtype: string
  - name: format
    dtype: string
  - name: date
    dtype: string
  splits:
  - name: train
    num_bytes: 991111
    num_examples: 37
  download_size: 8260947
  dataset_size: 991111
- config_name: jw-ulo_nche
  features:
  - name: title
    dtype: string
  - name: content
    dtype: string
  - name: format
    dtype: string
  - name: date
    dtype: string
  splits:
  - name: train
    num_bytes: 1952360
    num_examples: 55
  download_size: 8260947
  dataset_size: 1952360
- config_name: jw-ulo_nche_naamu
  features:
  - name: title
    dtype: string
  - name: content
    dtype: string
  - name: format
    dtype: string
  - name: date
    dtype: string
  splits:
  - name: train
    num_bytes: 7248017
    num_examples: 88
  download_size: 8260947
  dataset_size: 7248017
---

# Dataset Card for Igbo Monolingual Dataset

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

- **Homepage:** https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_monoling
- **Repository:** https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_monoling
- **Paper:** https://arxiv.org/abs/2004.00648

### Dataset Summary

A dataset is a collection of Monolingual Igbo sentences.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Igbo (ig)

## Dataset Structure

### Data Instances

Here is an example from the bb-igbo config:
```
{'content': 'Ike Ekweremmadụ\n\nIke ịda jụụ otụ nkeji banyere oke ogbugbu na-eme n\'ala Naijiria agwụla Ekweremmadụ\n\nOsote onye-isi ndị ome-iwu Naịjirịa bụ Ike Ekweremadu ekwuola na ike agwụla ndị Sịnatị iji otu nkeji darajụụ akwanyere ndị egburu n\'ime oke ọgbaghara dị na Naịjirịa oge ọ bula.\n\nEkweremadu  katọrọ mwakpọ na ogbugbu ndị Naịjirịa aka ha dị ọcha nke ndị Fulani na-achị ehi mere, kwuo na ike agwụla ndị ome- iwu ịkwanyere ha ugwu n\'otu nkeji\'\n\nCheta n\'otu ịzụka gara-aga ka emere akwam ozu mmadụ ruru iri asaa egburu na Local Gọọmenti Logo na Guma nke Benue Steeti, e be ihe kariri mmadụ iri ise ka akụkọ kwuru n\'egburu na Taraba Steeti.\n\nEkweremadu gosiri iwe gbasara ogbugbu ndị mmadụ na nzukọ ndị ome-iwu n\'ụbọchị taa, kwuo na Naịjirịa ga-ebu ụzọ nwe udo na nchekwa, tupu e kwuowa okwu iwulite obodo.\n\nỌ sịrị:  "Ndị ome-iwu abụghị sọ ọsọ ndị ihe a metụtara, kama ndị Naịjirịa niile.\n\n\'Ike agwụla anyị iji otu nkeji dị jụụ maka nkwanye ugwu. Ihe anyị chọrọ bụ udo na nchekwa tupu echewa echịchị nwuli obodo."',
 'date': '2018-01-19T17:07:38Z',
 'description': "N'ihi oke ogbugbu ndị mmadụ na Naịjirịa gbagburu gburu, osota onyeisi ndị ome-iwu Naịjirịa bụ Ike Ekweremadu ekwuola na ihe Naịjiria chọrọ bụ nchekwa tara ọchịchị, tupu ekwuwa okwu ihe ọzọ.",
 'headline': 'Ekweremadu: Ike agwụla ndị ụlọ ome iwu',
 'source': 'https://www.bbc.com/igbo/42712250',
 'tags': [],
 'title': 'Ekweremadu: Ike agwụla ndị ụlọ ome iwu'}
```

### Data Fields

For config 'eze_goes_to_school':
  - format, title, chapters

For config 'bbc-igbo' :
  - source, title, description, date (Missing date values replaced with empty strings), headline, content, tags (Missing tags replaced with empty list)

For config 'igbo-radio':
  - source, headline, author, date, description, content

For config 'jw-ot-igbo':
  - format, title, chapters

For config 'jw-nt-igbo':
  - format, title, chapters

For config 'jw-books': 
  - title, content, format, date (Missing date values replaced with empty strings)

For config 'jw-teta': 
  -  title, content, format, date (Missing date values replaced with empty strings)

For config 'jw-ulo_nche': 
  - title, content, format, date (Missing date values replaced with empty strings)

For config 'jw-ulo_nche_naamu':
  - title, content, format, date (Missing date values replaced with empty strings)


### Data Splits
| bbc-igbo  | eze_goes_to_school |igbo-radio| jw-books|jw-nt-igbo| jw-ot-igbo | jw-teta |jw-ulo_nche |jw-ulo_nche_naamu
| ------------- |:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
|  1297     | 1     | 440   | 48     | 27     | 39 | 37 | 55 | 88

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

@misc{ezeani2020igboenglish,  
title={Igbo-English Machine Translation: An Evaluation Benchmark},  
author={Ignatius Ezeani and Paul Rayson and Ikechukwu Onyenwe and Chinedu Uchechukwu and Mark Hepple},  
year={2020},  
eprint={2004.00648},  
archivePrefix={arXiv},  
primaryClass={cs.CL}  
}

### Contributions

Thanks to [@purvimisal](https://github.com/purvimisal) for adding this dataset.