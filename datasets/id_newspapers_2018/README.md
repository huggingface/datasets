---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- id
licenses:
- cc-by-4.0
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
pretty_name: Indonesian Newspapers 2018
---

# Dataset Card for Indonesian Newspapers 2018

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

- **Homepage:** [Indonesian Newspapers](https://github.com/feryandi/Dataset-Artikel)
- **Repository:** [Indonesian Newspapers](https://github.com/feryandi/Dataset-Artikel)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [feryandi.n@gmail.com](mailto:feryandi.n@gmail.com),
[cahya.wirawan@gmail.com](mailto:cahya.wirawan@gmail.com)

### Dataset Summary

The dataset contains around 500K articles (136M of words) from 7 Indonesian newspapers: Detik, Kompas, Tempo,
CNN Indonesia, Sindo, Republika and Poskota. The articles are dated between 1st January 2018 and 20th August 2018
(with few exceptions dated earlier). The size of uncompressed 500K json files (newspapers-json.tgz) is around 2.2GB,
and the cleaned uncompressed in a big text file (newspapers.txt.gz) is about 1GB. The original source in Google Drive
contains also a dataset in html format which include raw data (pictures, css, javascript, ...)
from the online news website. A copy of the original dataset is available at
https://cloud.uncool.ai/index.php/s/mfYEAgKQoY3ebbM

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
Indonesian

## Dataset Structure
```
{
  'id': 'string',
  'url': 'string',
  'date': 'string',
  'title': 'string',
  'content': 'string'
}
```
### Data Instances

An instance from the dataset is

```
{'id': '0',
 'url': 'https://www.cnnindonesia.com/olahraga/20161221234219-156-181385/lorenzo-ingin-samai-rekor-rossi-dan-stoner',
 'date': '2016-12-22 07:00:00',
 'title': 'Lorenzo Ingin Samai Rekor Rossi dan Stoner',
 'content': 'Jakarta, CNN Indonesia -- Setelah bergabung dengan Ducati, Jorge Lorenzo berharap bisa masuk dalam jajaran pebalap yang mampu jadi juara dunia kelas utama dengan dua pabrikan berbeda. Pujian Max Biaggi untuk Valentino Rossi Jorge Lorenzo Hadir dalam Ucapan Selamat Natal Yamaha Iannone: Saya Sering Jatuh Karena Ingin yang Terbaik Sepanjang sejarah, hanya ada lima pebalap yang mampu jadi juara kelas utama (500cc/MotoGP) dengan dua pabrikan berbeda, yaitu Geoff Duke, Giacomo Agostini, Eddie Lawson, Valentino Rossi, dan Casey Stoner. Lorenzo ingin bergabung dalam jajaran legenda tersebut. “Fakta ini sangat penting bagi saya karena hanya ada lima pebalap yang mampu menang dengan dua pabrikan berbeda dalam sejarah balap motor.” “Kedatangan saya ke Ducati juga menghadirkan tantangan yang sangat menarik karena hampir tak ada yang bisa menang dengan Ducati sebelumnya, kecuali Casey Stoner. Hal itu jadi motivasi yang sangat bagus bagi saya,” tutur Lorenzo seperti dikutip dari Crash Lorenzo saat ini diliputi rasa penasaran yang besar untuk menunggang sepeda motor Desmosedici yang dipakai tim Ducati karena ia baru sekali menjajal motor tersebut pada sesi tes di Valencia, usai MotoGP musim 2016 berakhir. “Saya sangat tertarik dengan Ducati arena saya hanya memiliki kesempatan mencoba motor itu di Valencia dua hari setelah musim berakhir. Setelah itu saya tak boleh lagi menjajalnya hingga akhir Januari mendatang. Jadi saya menjalani penantian selama dua bulan yang panjang,” kata pebalap asal Spanyol ini. Dengan kondisi tersebut, maka Lorenzo memanfaatkan waktu yang ada untuk liburan dan melepaskan penat. “Setidaknya apa yang terjadi pada saya saat ini sangat bagus karena saya jadi memiliki waktu bebas dan sedikit liburan.” “Namun tentunya saya tak akan larut dalam liburan karena saya harus lebih bersiap, terutama dalam kondisi fisik dibandingkan sebelumnya, karena saya akan menunggangi motor yang sulit dikendarai,” ucap Lorenzo. Selama sembilan musim bersama Yamaha, Lorenzo sendiri sudah tiga kali jadi juara dunia, yaitu pada 2010, 2012, dan 2015. (kid)'}
```

### Data Fields
- `id`: id of the sample
- `url`: the url to the original article
- `date`: the publishing date of the article
- `title`: the title of the article
- `content`: the content of the article

### Data Splits

The dataset contains train set of 499164 samples.

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

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License. The dataset is shared for the sole purpose of aiding open scientific research in Bahasa Indonesia (computing or linguistics), and can only be used for that purpose. The ownership of each article within the dataset belongs to the respective newspaper from which it was extracted; and the maintainer of the repository does not claim ownership of any of the content within it. If you think, by any means, that this dataset breaches any established copyrights; please contact the repository maintainer.

### Citation Information

[N/A]

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) for adding this dataset.