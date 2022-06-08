---
annotations_creators:
- found
language_creators:
- found
languages:
- tr
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-news-category-classification
paperswithcode_id: null
pretty_name: TTC4900 - A Benchmark Data for Turkish Text Categorization
---

# Dataset Card for TTC4900: A Benchmark Data for Turkish Text Categorization

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** [TTC4900 Homepage](https://www.kaggle.com/savasy/ttc4900)
- **Repository:** [TTC4900 Repository](https://github.com/savasy/TurkishTextClassification)
- **Paper:** [A Comparison of Different Approaches to Document Representation in Turkish Language](https://dergipark.org.tr/en/pub/sdufenbed/issue/38975/456349)
- **Point of Contact:** [Savaş Yıldırım](mailto:savasy@gmail.com)

### Dataset Summary

The data set is taken from [kemik group](http://www.kemik.yildiz.edu.tr/)
The data are pre-processed for the text categorization, collocations are found, character set is corrected, and so forth.
We named TTC4900 by mimicking the name convention of TTC 3600 dataset shared by the study ["A Knowledge-poor Approach to Turkish Text Categorization with a Comparative Analysis, Proceedings of CICLING 2014, Springer LNCS, Nepal, 2014"](https://link.springer.com/chapter/10.1007/978-3-642-54903-8_36)

If you use the dataset in a paper, please refer https://www.kaggle.com/savasy/ttc4900 as footnote and cite one of the papers as follows:

- A Comparison of Different Approaches to Document Representation in Turkish Language, SDU Journal of Natural and Applied Science, Vol 22, Issue 2, 2018
- A comparative analysis of text classification for Turkish language, Pamukkale University Journal of Engineering Science Volume 25 Issue 5, 2018
- A Knowledge-poor Approach to Turkish Text Categorization with a Comparative Analysis, Proceedings of CICLING 2014, Springer LNCS, Nepal, 2014.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Turkish.

## Dataset Structure

### Data Instances

A text classification dataset with 7 different news category. 

Here is an example from the dataset:

```
{
"category": 0,  # politics/siyaset
"text": "paris teki infaz imralı ile başlayan sürece bir darbe mi elif_çakır ın sunduğu söz_bitmeden in bugünkü konuğu gazeteci melih altınok oldu programdan satıbaşları imralı ile görüşmeler hangi aşamada bundan sonra ne olacak hangi kesimler sürece engel oluyor psikolojik mayınlar neler türk solu bu dönemde evrensel sorumluluğunu yerine getirebiliyor mu elif_çakır sordu melih altınok söz_bitmeden de yanıtladı elif_çakır pkk nın silahsızlandırılmasına yönelik olarak öcalan ile görüşme sonrası 3 kadının infazı enteresan çünkü kurucu isimlerden birisi sen nasıl okudun bu infazı melih altınok herkesin ciddi anlamda şüpheleri var şu an yürüttüğümüz herşey bir delile dayanmadığı için komple teorisinden ibaret kalacak ama şöyle bir durum var imralı görüşmelerin ilk defa bir siyasi iktidar tarafından açıkça söylendiği bir dönem ardından geliyor bu sürecin gerçekleşmemesini isteyen kesimler yaptırmıştır dedi"
}
```

### Data Fields

- **category** : Indicates to which category the news text belongs.
(Such as "politics", "world", "economy", "culture", "health", "sports", "technology".)
- **text** : Contains the text of the news.

### Data Splits

It is not divided into Train set and Test set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The data are pre-processed for the text categorization, collocations are found, character set is corrected, and so forth. 

#### Who are the source language producers?

Turkish online news sites. 

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

The dataset was created by [Savaş Yıldırım](https://github.com/savasy)  

### Licensing Information

[More Information Needed]

### Citation Information

```
@article{doi:10.5505/pajes.2018.15931,
  author = {Yıldırım, Savaş and Yıldız, Tuğba},
  title = {A comparative analysis of text classification for Turkish language},
  journal = {Pamukkale Univ Muh Bilim Derg},
  volume = {24},
  number = {5},
  pages = {879-886},
  year = {2018},
  doi = {10.5505/pajes.2018.15931},
  note ={doi: 10.5505/pajes.2018.15931},

  URL = {https://dx.doi.org/10.5505/pajes.2018.15931},
  eprint = {https://dx.doi.org/10.5505/pajes.2018.15931}
}
```

### Contributions

Thanks to [@yavuzKomecoglu](https://github.com/yavuzKomecoglu) for adding this dataset.
