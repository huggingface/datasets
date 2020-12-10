---
languages:
- id
licenses:
- CC BY-SA 4.0
multilinguality:
- monolingual
task_categories:
- summarization
---

# Dataset Card for Indosum

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
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

## Dataset Description

- **Homepage: [Indosum Homepage](https://github.com/kata-ai/indosum)**  
- **Repository: [Indosum Repository](https://github.com/kata-ai/indosum)**  
- **Paper: [Indosum: A New Benchmark Dataset for Indonesian Text Summarization](https://doi.org/10.1109/IALP.2018.8629109)**  

### Dataset Summary

Indosum contains Indonesian extractive text summarization dataset, roughly 19K tokenized news articles from (formerly) Shortir.com, a news aggregator site. 

This dataset contains pre-tokenized sentences for the paragraphs and summary text, the authors didn't provide the raw sentences.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Indosum is a dataset contains Indonesian text summarization dataset.

## Dataset Structure

### Data Instances
```
{
  "category": "tajuk utama",
  "gold_labels": [[False, True],
    [True, True],
    [False, False, False],
    [False, False],
    [False, False],
    [False, False],
    [False, False],
    [False],
    [False, False]],
  "id": "1501893029-lula-kamal-dokter-ryan-thamrin-sakit-sejak-setahun",
  "paragraphs": [
    [
      ['Jakarta', ',', 'CNN', 'Indonesia', '-', '-', 'Dokter', 'Ryan', 'Thamrin', ',', 'yang', 'terkenal', 'lewat', 'acara', 'Dokter', 'Oz', 'Indonesia', ',', 'meninggal', 'dunia', 'pada', 'Jumat', '(', '4', '/', '8', ')', 'dini', 'hari', '.'], ['Dokter', 'Lula', 'Kamal', 'yang', 'merupakan', 'selebriti', 'sekaligus', 'rekan', 'kerja', 'Ryan', 'menyebut', 'kawannya', 'itu', 'sudah', 'sakit', 'sejak', 'setahun', 'yang', 'lalu', '.']
    ], 
    [
      ['Lula', 'menuturkan', ',', 'sakit', 'itu', 'membuat', 'Ryan', 'mesti', 'vakum', 'dari', 'semua', 'kegiatannya', ',', 'termasuk', 'menjadi', 'pembawa', 'acara', 'Dokter', 'Oz', 'Indonesia', '.'], 
      ['Kondisi', 'itu', 'membuat', 'Ryan', 'harus', 'kembali', 'ke', 'kampung', 'halamannya', 'di', 'Pekanbaru', ',', 'Riau', 'untuk', 'menjalani', 'istirahat', '.']
    ], 
    [
      ['"', 'Setahu', 'saya', 'dia', 'orangnya', 'sehat', ',', 'tapi', 'tahun', 'lalu', 'saya', 'dengar', 'dia', 'sakit', '.'], 
      ['(', 'Karena', ')', 'sakitnya', ',', 'ia', 'langsung', 'pulang', 'ke', 'Pekanbaru', ',', 'jadi', 'kami', 'yang', 'mau', 'jenguk', 'juga', 'susah', '.'], 
      ['Barangkali', 'mau', 'istirahat', ',', 'ya', 'betul', 'juga', ',', 'kalau', 'di', 'Jakarta', 'susah', 'isirahatnya', ',', '"', 'kata', 'Lula', 'kepada', 'CNNIndonesia.com', ',', 'Jumat', '(', '4', '/', '8', ')', '.']
    ]...],
  "source": "cnn indonesia",
  "source_url": "https://www.cnnindonesia.com/hiburan/20170804120703-234-232443/lula-kamal-dokter-ryan-thamrin-sakit-sejak-setahun-lalu/",
  "summary": [
    ['Dokter', 'Lula', 'Kamal', 'yang', 'merupakan', 'selebriti', 'sekaligus', 'rekan', 'kerja', 'Ryan', 'Thamrin', 'menyebut', 'kawannya', 'itu', 'sudah', 'sakit', 'sejak', 'setahun', 'yang', 'lalu', '.'], ['Lula', 'menuturkan', ',', 'sakit', 'itu', 'membuat', 'Ryan', 'mesti', 'vakum', 'dari', 'semua', 'kegiatannya', ',', 'termasuk', 'menjadi', 'pembawa', 'acara', 'Dokter', 'Oz', 'Indonesia', '.'], ['Kondisi', 'itu', 'membuat', 'Ryan', 'harus', 'kembali', 'ke', 'kampung', 'halamannya', 'di', 'Pekanbaru', ',', 'Riau', 'untuk', 'menjalani', 'istirahat', '.']
  ]
}
```

### Data Fields

* id - unique identifier of the article
* paragraphs - a list of paragraphs of the original article
* summary - gold summary of the article, given as a list of sentences
* gold_labels - gold extractive labels of the sentences in the article
* category - category to which the article belongs (in Indonesian)
* source - source of the article
* source_url - url of the original article

### Data Splits

**The original datasets**  
The original dataset is split into 5 cross-validation folds, where each fold consists of a training set, a development set,
and a test set. The filenames have the following format (where X is a fold number 1-5):

* train.0X.jsonl - training set for fold X
* dev.0X.jsonl - development set for fold X
* test.0X.jsonl - test set for fold X

**The HuggingFace datasets** 
For HuggingFace datasets, the 5 cross-validation folds are concatenated for each split. 
The final split sizes are as follow:

|                            | Tain   | Dev  | Test  |
| -----                      | -----  | ---- | ----- |
| # of articles              | 71353  | 3743 | 18774 |

## Dataset Creation

[More Information Needed]

### Curation Rationale

[More Information Needed]

### Source Data

The dataset was curated from (formerly) Shortir.com, a news aggregator site.  
There are 6 categories in total: Entertainment, Inspiration, Sport, Showbiz, Headline, and Tech. 

#### Initial Data Collection and Normalization

The initial dataset contains roughly 20K news articles.  Some articles have a very long text and some summaries have too many sentences. Articles with a long text are mostly articles containing a list, e.g., list of songs played in a concert, list of award nominations, and so on. After removing such articles, the authors ended up with roughly 19K articles in total.

The authors used NLTK and spaCy for sentence and word tokenization respectively.

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

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License. See http://creativecommons.org/licenses/by-sa/4.0/.

### Citation Information
```
@inproceedings{kurniawan2018,
  place={Bandung, Indonesia},
  title={IndoSum: A New Benchmark Dataset for Indonesian Text Summarization},
  url={https://ieeexplore.ieee.org/document/8629109},
  DOI={10.1109/IALP.2018.8629109},
  booktitle={2018 International Conference on Asian Language Processing (IALP)},
  publisher={IEEE},
  author={Kurniawan, Kemal and Louvan, Samuel},
  year={2018},
  month={Nov},
  pages={215-220}
}
```