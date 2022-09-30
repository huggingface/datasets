---
annotations_creators:
- found
language_creators:
- found
language:
- tr
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|interpress_news_category_tr
task_categories:
- text-classification
task_ids:
- text-classification-other-news-category-classification
paperswithcode_id: null
pretty_name: Interpress Turkish News Category Dataset (270K - Lite Version)
---

# Dataset Card for Interpress Turkish News Category Dataset (270K - Lite Version)

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

Turkish News Category Dataset (270K - Lite Version) is a Turkish news data set consisting of 273601 news in 10 categories ("kültürsanat", "ekonomi", "siyaset", "eğitim", "dünya", "spor", "teknoloji", "magazin", "sağlık", "gündem"), compiled from printed media and news websites between 2010 and 2017 by the Interpress (https://www.interpress.com/) media monitoring company. **It has been rearranged as easily separable and with fewer classes.**

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Turkish.

## Dataset Structure

### Data Instances

A text classification dataset with 10 different news category. 

Here is an example from the dataset:

```
{
  'category': 0, 
  'content': 'Tarihten Sınıfta Kaldık Bugün tarihe damgasını vuran Osmanlı İmparatorluğu nun kuruluş yıldönümü. Adına dizilerin çekildiği tarihimizi ne kadar biliyoruz? Gerekçeler faklı; ama sonuç aynı çıktı. Tarihten sınıfta kaldık. Sayfa 5r 1 Bugün tarihe damgasını vuran Osmanlı İmparatorluğumun kuruluş yıldönümü. Adına dizilerin çekildiği tarihimizi ne kadar biliyoruz? Gerekçeler faklı; ama sonuç aynı çıktı. Tarihten sınıfta kaldık 7 Ocak 1299... Kıtalara dağılan ücüyle, ülkeler arasında gördüğü aygıyla tarihe damgasını vuran anlı devletin kuruluş tarihi. Peki, anlı tarihimizi ne kadar biliyoruz? on zamanlarda tarihimizi anlatan izilere ilgi nasıl? Bu dizilerde anlatanlar ne kadar sağlıklı? İşte sokaın değerlendirmesi; levlüdiye Karaman (42-Ev lamım):  Bir bilgim yok. Tarihle izla ilgilenmiyorum. Eşim daha ilgilidir bu konuda. Evde anlatır, ndan duyduklarımla yetiniyorum esem yalan olmaz. Osmanlı döeminde yaşamak isterdim. Tarih izileri izlerim Muhteşem Yüzyıl izisini çok izledim; hatta hiç kaırmazdım. Ama tarihimiz bu değil. Sunuün bilincindeyim. Muhteşem  üzyıl dizisi genelde haremiyle ön landaydı. Onun için tarihi diziden ğrenmeyi de doğru bulmuyorum. )kullarda verilen tarih dersleri yeisiz. Daha çok tanıtabilirler. Görel anlatım yapılsın çocuklarımız aten okumak istemiyor. En azman eğlenceli hale getirip bu şekilde ilgilendirebilirler.  erdi Üstün  (22-Saatçi):  Bu gün Osmanlı Devleti nin kuruluş yıldönümü olduğunu bilmiyordum. O dönemde yaşamak isterdim. Tarih yazılmış neden yaşamak istemeyim ki. Tarihime yeterince hakim olduğumu düşünüyorum. Araştırmalar yapıyorum. Merak ediyorum. Okullarda verilen tarih dersleri yeterli. Tarih dizisi izlemem, televizyondan tarihimi öğrenmek bana mantıklı gelmiyor. Yeterli olabilir; ama hikayeleştiriliyor. Sonuçta olduğu gibi anlatılsa daha iyi olur.  Songül Karabacak (40-Ev Hanımı):  Kuruluş yıldönümü olduğunu bilmiyordum. Tarih bilgim çok azdır. Zaten biz yaşadığımız dönemde tarih yazıyoruz. Osmanlı Dönemi nde yaşamak istemezdim. Sebebini bilmiyorum; ama hayatımdan memnunum, dönemden de memnunum. Dizileri takip etmiyorum. Ama mutlaka dizilerde tarihimiz doğru yansıtılıyor ki insanlar sürekli takip ediyor. Benim televizyonla pek aram yoktur.  Ertuğrul Şahin (47-Çalışmıyor):  Kuruluş yıldönümü olduğunu bilmiyordum. Sizden öğrendim. O dönemde yaşamak isterdim. Tarih sonuçta merak ederim. Tarihle ilgili çok bilgim yok. Okumadım, zaten şartlar el vermedi. Okullarda verilen eğitim yeterli değil. Örnek vermek gerekirse; 20 yaşında oğlum var Atatürk ün doğum yılını soruyorum yüzüme bakıyor. Verilen eğitim belli. Konu belirliyorlar onun dışına çıkmıyorlar. Daha fazla bilgi verilebilir. Tabi gençlerimizde de suç var bize baksınlar tarihimizi bilmiyoruz. Onlar araştırma yapsınlar her gün internette geziyorlar faydasız bir şeye bakacaklarına ecdatlarını okusunlar. Tarih dizlerini izlerim. Ama doğru yansıtılıyor mu orasını bilmiyorum sadece izleyiciyim. Ama önceden Süleyman Şah ı duyardım. Büyüklerimiz anlatırdı bunu diziden teyit ettim mesela.  Ahmet Efe (22-Muhasebeci):  Kuruluş yıldönümü olduğuyla ilgili bir bilgim yok. O dönemde yaşamak isterdim. Aldığımız bilgiler sonucunda illa ki bir özenme oluyor. Tam anlamıyla tarih bilgisine sahip olduğumu düşünmüyorum. Tarihe merakım var aslında; ama çok kısıtlı araştırma yapıyorum. Okullarda verilen tarih dersi yeterli değil. Çünkü şuradan birkaç çocuğu çevirip sorsanız size yeterli bilgi vermez. Veremez onun da bilgisi yok sonuçta. Zaten kısıtlı bilgiler veriliyor. Tarih dizilerini kılıç kalkan kuşanıp izliyorum. Doğru yansıtılıyor bundan dolayı da biraz insanlar tarihini öğrenmeye başladı desek yalan olmaz. Bu ne kadar doğru derseniz de bilgiyi doğru verdikten sonra tabi diziden de tarih öğrenilebilir.  Mehmet Ak (28-Satış Danışmanı):  Kuruluşunun bugün olduğunu bilmiyordum. O dönemde yaşamak isterdim. Yeterli bilgim yok bence kim tarihi tam anlamıyla öğrenebilir ki zaten. Ama tabi tarih kitapları okuyorum, araştırıyorum. Okullarda verilen tarih derslerini yeterli bulmuyorum; ama daha fazla neler yapılabilir, tarih küçüklere nasıl anlatılır bilmiyorum tek bildiğim yeterli olmadığı. Tarih dizileri gerçeği yüzde 75 yansıtıyor. Bu konuda araştırma yaptım yüzeysel anlatılıyor; fakat yine de bilgi edinilebilecek diziler. En azından rutinleşmiş dizi konularından uzak. Aile ile rahat rahat izleyebilirsin.  Hasan Çalık (65-Emekli):  Kuruluş yıldönümü olduğunu biliyorum. Araştırma yaparım. O dönemde yaşamak istemezdim Cumhuriyet döneminde yaşamayı daha çok isterdim. Okullarda verilen dersler yeterli. Film ya da dizi okumak yerine kitap okumayı tercih ederim. Bir insan ancak kitap okuyarak aydınlanabilir. Bu şekilde kendini geliştirebilir. Bir ömre ne kadar kitap sığdırırsan o kadar aydın bir insan olursun. Konusu fark etmez ister tarih olsun, ister roman okumak her zaman kazanç sağlar. Bir diziden tarihi ne kadar yeterli öğrenebilirsin ki ya da ne kadar doğru anlatılabilir. Bence diziyi bırakıp kitaplara yönelsinler.  Nuray Çelik'
}
```

### Data Fields

- **category** : Indicates to which category the news text belongs.
(Such as "kültürsanat" (0), "ekonomi" (1), "siyaset" (2), "eğitim" (3), "dünya" (4), "spor" (5), "teknoloji" (6), "magazin" (7), "sağlık" (8), "gündem" (9))
- **content** : Contains the text of the news.

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

Thanks to [@basakbuluz](https://github.com/basakbuluz) & [@yavuzkomecoglu](https://github.com/yavuzkomecoglu) & [@serdarakyol](https://github.com/serdarakyol/) for adding this dataset.
