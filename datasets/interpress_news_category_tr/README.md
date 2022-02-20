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
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-news-category-classification
paperswithcode_id: null
pretty_name: Interpress Turkish News Category Dataset (270K)
---

# Dataset Card for Interpress Turkish News Category Dataset (270K)

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

- **Homepage:** [Interpress](https://www.interpress.com/)
- **Point of Contact:** [Yavuz Komecoglu](mailto:yavuz.komecoglu@kodiks.com)

### Dataset Summary

Turkish News Category Dataset (270K) is a Turkish news data set consisting of 273601 news in 17 categories, compiled from printed media and news websites between 2010 and 2017 by the Interpress (https://www.interpress.com/) media monitoring company.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Turkish.

## Dataset Structure

### Data Instances

A text classification dataset with 17 different news category.

```
{'id': 301365715,
 'title': 'BİR SİHİRBAZ',
 'content': 'NİANG, TAKIM ARKADAŞI FERNANDES E ÖVGÜLER YAĞDIRDI FUTBOL OYNARKEN EĞLENİYORUM YÜZDE 701E OYNUYORUM LİDERLE ARAMIZDA SADECE 5 PUAN VAR, ŞAMPİYONLUK ŞANSIMIZ YÜKSEK 4 j  Fernandes le birlikte oynamayı seviyorum, adam adeta sihirbaz gibi J Frank Ribery, futbol hayatımda oynamaktan en çok zevk aldığım isim  ı Abartılacak bir ] sonuç almadık ı .BAHÇE derbisinde Kartal ın ilk golünü atan, üçüncü golün de asistini yapan Mamadou Niang, TRT Spor da Futbol Keyfi programında özel açıklamalar yaptı. Senegalli forvet şampiyonluk şanslarının yüksek olduğunu dile getirirken, Portekizli yıldız Fernandes için  Onunla oynamayı seviyorum, adeta bir sihirbaz gibi  ifadesini kullandı. Frank Ribery nin futbol hayatında oynamaktan en çok zevk aldığım isim olduğunu ifade eden Niang, Moussa Sow ve Burak Yılmaz ın da Süper Lig deki en iyi forvetler olduğunu, ikisinin de tarzını beğendiğini söyledi. Senegalli yıldız şampiyonluk şansları için,  Çok yüksek. Çünkü liderle aramızda 5 puan fark var ve bunu kapatacak güçteyiz  yorumunu yaptı.   NİANG şöyle devam etti: t.f  En zorlandığım stoper İbrahim Toraman dır. Neyse ki şu an onunla takım arkadaşıyım. Almeida sakatlıktan döndükten sonra nasıl bir diziliş olur bilemiyorum. Onunla beraber oynayabiliriz, Holosko ile de oynayabiliriz. Türkiye, .. O NİANG, şu anda gerçek performansının yüzde 70 i ile oynadığını söyledi. İyi bir seviyede olmadığını kabul ettiğini belirten Senegalli yıldız,  Sahada savaşan oyuncularla birlikte olmayı seviyorum. Bizim takımda Olcay ve Oğuzhan gibi bu yapıda isimler var. Tabii ki şansın da önemi var  diye konuştu. zor bir lig. Eskiden arkadaşlarıma Türkiye Ligi nin iyi olduğunu söylediğimde inanmazlardı. Şimdi Didier Drogba, VVesley Sneijder, Sovvgibi oyuncuların burada olması ilgiyi artırdı. Futbol oynarken eğleniyorum ve şu an emekli olmayı düşünmüyorum.  Açılış törenine, yönetici Metin Albayrak ile birlikte futbolcular Necip Uysal, McGregor ve Mehmet Akyüz de katıldı.  BEŞİKTAŞLI Necip Uysal, +f başkan Fikret Orman gibi F.Bahçe galibiyetinin abartılmaması gerektiğini söyledi. Pazar günü İnönü Stadı nda güzel bir zafer elde ettiklerini vurgulayan genç yıldız,  10 karşılaşmaya daha çıkacağız. Her maçımız final, ayaklarımızın yere sağlam basması gerekiyor. Maçlara tek tek bakacağız ve hepsini kazanmak için oynayacağız  yorumunu yaptı. Trabzon un her zaman zor deplasman olduğunu ifade eden Necip,  Kolay olmayacağını biliyoruz ama şampiyonluk şansımızın sürmesi için kesinlikle üç puanla dönmeye mecburuz  dedi. sflPa',
 'category': 12,
 'categorycode': 12,
 'publishdatetime': '2013-03-07T00:00:00Z'}
```

### Data Fields

- `id`
- `title`
- `content`
- `category`
- `categorycode`
- `publishdatetime`

### Data Splits

The data is split into a training and testing. The split is organized as the following 

|            |   train |   test |
|------------|--------:|-------:|
| data split | 218,880 | 54,721 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

Downloaded over 270,000 news from the printed media and news websites between 2010 and 2017 by the Interpress (https://www.interpress.com/) media monitoring company. This data collection compiled from print media and internet news is presented in its raw form. For this reason, it is appropriate to use it with careful pre-processing steps regarding various OCR errors and typos.


#### Who are the source language producers?

Turkish printed news sources and online news sites. 

### Annotations

The dataset does not contain any additional annotations.

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

https://www.interpress.com/

### Contributions

Thanks to [@basakbuluz](https://github.com/basakbuluz) for adding this dataset.
