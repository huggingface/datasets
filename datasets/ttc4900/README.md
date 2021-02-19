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
- 100k<n<1M
source_datasets:
- original
task_categories:
- text_classification
task_ids:
- text_classification-other-news-category-classification
---

# Dataset Card for TTC4900: A Benchmark Data for Turkish Text Categorization

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
  - [Discussion of Social Impact and Biases](#discussion-of-social-impact-and-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [https://www.kaggle.com/savasy/ttc4900](https://www.kaggle.com/savasy/ttc4900)
- **Point of Contact:** [ Avatar
Savaş Yıldırım](mailto:savasy@gmail.com)

### Dataset Summary

The data set is taken from [kemik group](http://www.kemik.yildiz.edu.tr/)

The data are pre-processed (noun phrase chunking etc.) for the text categorization problem by the study ["A Knowledge-poor Approach to Turkish Text Categorization with a Comparative Analysis, Proceedings of CICLING 2014, Springer LNCS, Nepal, 2014"](https://link.springer.com/chapter/10.1007/978-3-642-54903-8_36)

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

[More Information Needed]

#### Initial Data Collection and Normalization

The data are pre-processed for the text categorization, collocations are found, character set is corrected, and so forth. 


#### Who are the source language producers?

Turkish online news sites. 

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Discussion of Social Impact and Biases

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

### Contributions

Thanks to [@yavuzKomecoglu](https://github.com/yavuzKomecoglu) for adding this dataset.