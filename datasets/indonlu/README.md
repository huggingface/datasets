---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- id
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  bapos:
  - 10K<n<100K
  casa:
  - 1K<n<10K
  emot:
  - 1K<n<10K
  facqa:
  - 1K<n<10K
  hoasa:
  - 1K<n<10K
  keps:
  - 1K<n<10K
  nergrit:
  - 1K<n<10K
  nerp:
  - 1K<n<10K
  posp:
  - 1K<n<10K
  smsa:
  - 10K<n<100K
  terma:
  - 1K<n<10K
  wrete:
  - n<1K
source_datasets:
- original
task_categories:
  bapos:
  - structure-prediction
  casa:
  - text-classification
  emot:
  - text-classification
  facqa:
  - question-answering
  hoasa:
  - text-classification
  keps:
  - structure-prediction
  nergrit:
  - structure-prediction
  nerp:
  - structure-prediction
  posp:
  - structure-prediction
  smsa:
  - text-classification
  terma:
  - structure-prediction
  wrete:
  - text-classification
task_ids:
  bapos:
  - part-of-speech-tagging
  casa:
  - text-classification-other-aspect-based-sentiment-analysis
  emot:
  - multi-class-classification
  facqa:
  - closed-domain-qa
  hoasa:
  - text-classification-other-aspect-based-sentiment-analysis
  keps:
  - structure-prediction-other-keyphrase-extraction
  nergrit:
  - named-entity-recognition
  nerp:
  - named-entity-recognition
  posp:
  - part-of-speech-tagging
  smsa:
  - sentiment-classification
  terma:
  - structure-prediction-other-span-extraction
  wrete:
  - semantic-similarity-classification
paperswithcode_id: indonlu-benchmark
---


# Dataset Card for IndoNLU

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

- **Homepage:** [IndoNLU Website](https://www.indobenchmark.com/)
- **Repository:** [IndoNLU GitHub](https://github.com/indobenchmark/indonlu)
- **Paper:** [IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding](https://www.aclweb.org/anthology/2020aacl-main.85.pdf)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The IndoNLU benchmark is a collection of resources for training, evaluating, and analyzing natural language understanding systems for Bahasa Indonesia (Indonesian language).
There are 12 datasets in IndoNLU benchmark for Indonesian natural language understanding.
1. `EmoT`: An emotion classification dataset collected from the social media platform Twitter. The dataset consists of around 4000 Indonesian colloquial language tweets, covering five different emotion labels: anger, fear, happy, love, and sadness
2. `SmSA`: This sentence-level sentiment analysis dataset is a collection of comments and reviews in Indonesian obtained from multiple online platforms. The text was crawled and then annotated by several Indonesian linguists to construct this dataset. There are three possible sentiments on the `SmSA` dataset: positive, negative, and neutral
3. `CASA`: An aspect-based sentiment analysis dataset consisting of around a thousand car reviews collected from multiple Indonesian online automobile platforms. The dataset covers six aspects of car quality. We define the task to be a multi-label classification task, where each label represents a sentiment for a single aspect with three possible values: positive, negative, and neutral.
4. `HoASA`: An aspect-based sentiment analysis dataset consisting of hotel reviews collected from the hotel aggregator platform, [AiryRooms](https://github.com/annisanurulazhar/absa-playground). The dataset covers ten different aspects of hotel quality. Similar to the `CASA` dataset, each review is labeled with a single sentiment label for each aspect. There are four possible sentiment classes for each sentiment label: positive, negative, neutral, and positive-negative. The positivenegative label is given to a review that contains multiple sentiments of the same aspect but for different objects (e.g., cleanliness of bed and toilet).
5. `WReTE`: The Wiki Revision Edits Textual Entailment dataset consists of 450 sentence pairs constructed from Wikipedia revision history. The dataset contains pairs of sentences and binary semantic relations between the pairs. The data are labeled as entailed when the meaning of the second sentence can be derived from the first one, and not entailed otherwise.
6. `POSP`: This Indonesian part-of-speech tagging (POS) dataset is collected from Indonesian news websites. The dataset consists of around 8000 sentences with 26 POS tags. The POS tag labels follow the [Indonesian Association of Computational Linguistics (INACL) POS Tagging Convention](http://inacl.id/inacl/wp-content/uploads/2017/06/INACL-POS-Tagging-Convention-26-Mei.pdf).
7. `BaPOS`: This POS tagging dataset contains about 1000 sentences, collected from the [PAN Localization Project](http://www.panl10n.net/). In this dataset, each word is tagged by one of [23 POS tag classes](https://bahasa.cs.ui.ac.id/postag/downloads/Tagset.pdf). Data splitting used in this benchmark follows the experimental setting used by [Kurniawan and Aji (2018)](https://arxiv.org/abs/1809.03391).
8. `TermA`: This span-extraction dataset is collected from the hotel aggregator platform, [AiryRooms](https://github.com/jordhy97/final_project). The dataset consists of thousands of hotel reviews, which each contain a span label for aspect and sentiment words representing the opinion of the reviewer on the corresponding aspect. The labels use Inside-Outside-Beginning (IOB) tagging representation with two kinds of tags, aspect and sentiment.
9. `KEPS`: This keyphrase extraction dataset consists of text from Twitter discussing banking products and services and is written in the Indonesian language. A phrase containing important information is considered a keyphrase. Text may contain one or more keyphrases since important phrases can be located at different positions. The dataset follows the IOB chunking format, which represents the position of the keyphrase.
10. `NERGrit`: This NER dataset is taken from the [Grit-ID repository](https://github.com/grit-id/nergrit-corpus), and the labels are spans in IOB chunking representation. The dataset consists of three kinds of named entity tags, PERSON (name of person), PLACE (name of location), and ORGANIZATION (name of organization).
11. `NERP`: This NER dataset (Hoesen and Purwarianti, 2018) contains texts collected from several Indonesian news websites. There are five labels available in this dataset, PER (name of person), LOC (name of location), IND (name of product or brand), EVT (name of the event), and FNB (name of food and beverage). Similar to the `TermA` dataset, the `NERP` dataset uses the IOB chunking format.
12. `FacQA`: The goal of the FacQA dataset is to find the answer to a question from a provided short passage from a news article. Each row in the FacQA dataset consists of a question, a short passage, and a label phrase, which can be found inside the corresponding short passage. There are six categories of questions: date, location, name, organization, person, and quantitative.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Indonesian

## Dataset Structure

### Data Instances

1. `EmoT` dataset

A data point consists of `tweet` and `label`. An example from the train set looks as follows:
```
{
  'tweet': 'Ini adalah hal yang paling membahagiakan saat biasku foto bersama ELF #ReturnOfTheLittlePrince #HappyHeeChulDay'
  'label': 4,
}
```

2. `SmSA` dataset

A data point consists of `text` and `label`. An example from the train set looks as follows:
```
{
  'text': 'warung ini dimiliki oleh pengusaha pabrik tahu yang sudah puluhan tahun terkenal membuat tahu putih di bandung . tahu berkualitas , dipadu keahlian memasak , dipadu kretivitas , jadilah warung yang menyajikan menu utama berbahan tahu , ditambah menu umum lain seperti ayam . semuanya selera indonesia . harga cukup terjangkau . jangan lewatkan tahu bletoka nya , tidak kalah dengan yang asli dari tegal !'
  'label': 0,
}
```

3. `CASA` dataset

A data point consists of `sentence` and multi-label `feature`, `machine`, `others`, `part`, `price`, and `service`. An example from the train set looks as follows:
```
{
  'sentence': 'Saya memakai Honda Jazz GK5 tahun 2014 ( pertama meluncur ) . Mobil nya bagus dan enak sesuai moto nya menyenangkan untuk dikendarai',
  'fuel': 1,
  'machine': 1,
  'others': 2,
  'part': 1,
  'price': 1,
  'service': 1
}
```

4. `HoASA` dataset

A data point consists of `sentence` and multi-label `ac`, `air_panas`, `bau`, `general`, `kebersihan`, `linen`, `service`, `sunrise_meal`, `tv`, and `wifi`. An example from the train set looks as follows:
```
{
  'sentence': 'kebersihan kurang...',
  'ac': 1,
  'air_panas': 1,
  'bau': 1,
  'general': 1,
  'kebersihan': 0,
  'linen': 1,
  'service': 1,
  'sunrise_meal': 1,
  'tv': 1,
  'wifi': 1
}
```

5. `WreTE` dataset

A data point consists of `premise`, `hypothesis`, `category`, and `label`. An example from the train set looks as follows:
```
{
  'premise': 'Pada awalnya bangsa Israel hanya terdiri dari satu kelompok keluarga di antara banyak kelompok keluarga yang hidup di tanah Kanan pada abad 18 SM .',
  'hypothesis': 'Pada awalnya bangsa Yahudi hanya terdiri dari satu kelompok keluarga di antara banyak kelompok keluarga yang hidup di tanah Kanan pada abad 18 SM .'
  'category': 'menolak perubahan teks terakhir oleh istimewa kontribusi pengguna 141 109 98 87 141 109 98 87 dan mengembalikan revisi 6958053 oleh johnthorne',
  'label': 0,
}
```

6. `POSP` dataset

A data point consists of `tokens` and `pos_tags`. An example from the train set looks as follows:
```
{
  'tokens': ['kepala', 'dinas', 'tata', 'kota', 'manado', 'amos', 'kenda', 'menyatakan', 'tidak', 'tahu', '-', 'menahu', 'soal', 'pencabutan', 'baliho', '.', 'ia', 'enggan', 'berkomentar', 'banyak', 'karena', 'merasa', 'bukan', 'kewenangannya', '.'],
  'pos_tags': [11, 6, 11, 11, 7, 7, 7, 9, 23, 4, 21, 9, 11, 11, 11, 21, 3, 2, 4, 1, 19, 9, 23, 11, 21]
}
```

7. `BaPOS` dataset

A data point consists of `tokens` and `pos_tags`. An example from the train set looks as follows:
```
{
  'tokens': ['Kera', 'untuk', 'amankan', 'pesta', 'olahraga'],
  'pos_tags': [27, 8, 26, 27, 30]
}
```

8. `TermA` dataset

A data point consists of `tokens` and `seq_label`. An example from the train set looks as follows:
```
{
  'tokens': ['kamar', 'saya', 'ada', 'kendala', 'di', 'ac', 'tidak', 'berfungsi', 'optimal', '.', 'dan', 'juga', 'wifi', 'koneksi', 'kurang', 'stabil', '.'],
  'seq_label': [1, 1, 1, 1, 1, 4, 3, 0, 0, 1, 1, 1, 4, 2, 3, 0, 1]
}
```

9. `KEPS` dataset

A data point consists of `tokens` and `seq_label`. An example from the train set looks as follows:
```
{
  'tokens': ['Setelah', 'melalui', 'proses', 'telepon', 'yang', 'panjang', 'tutup', 'sudah', 'kartu', 'kredit', 'bca', 'Ribet'],
  'seq_label': [0, 1, 1, 2, 0, 0, 1, 0, 1, 2, 2, 1]
}
```

10. `NERGrit` dataset

A data point consists of `tokens` and `ner_tags`. An example from the train set looks as follows:
```
{
  'tokens': ['Kontribusinya', 'terhadap', 'industri', 'musik', 'telah', 'mengumpulkan', 'banyak', 'prestasi', 'termasuk', 'lima', 'Grammy', 'Awards', ',', 'serta', 'dua', 'belas', 'nominasi', ';', 'dua', 'Guinness', 'World', 'Records', ';', 'dan', 'penjualannya', 'diperkirakan', 'sekitar', '64', 'juta', 'rekaman', '.'],
  'ner_tags': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]}
```

11. `NERP` dataset

A data point consists of `tokens` and `ner_tags`. An example from the train set looks as follows:
```
{
  'tokens': ['kepala', 'dinas', 'tata', 'kota', 'manado', 'amos', 'kenda', 'menyatakan', 'tidak', 'tahu', '-', 'menahu', 'soal', 'pencabutan', 'baliho', '.', 'ia', 'enggan', 'berkomentar', 'banyak', 'karena', 'merasa', 'bukan', 'kewenangannya', '.'],
  'ner_tags': [9, 9, 9, 9, 2, 7, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
}
```

12. `FacQA` dataset

A data point consists of `question`, `passage`, and `seq_label`. An example from the train set looks as follows:
```
{
  'passage': ['Lewat', 'telepon', 'ke', 'kantor', 'berita', 'lokal', 'Current', 'News', 'Service', ',', 'Hezb-ul', 'Mujahedeen', ',', 'kelompok', 'militan', 'Kashmir', 'yang', 'terbesar', ',', 'menyatakan', 'bertanggung', 'jawab', 'atas', 'ledakan', 'di', 'Srinagar', '.'],
  'question': ['Kelompok', 'apakah', 'yang', 'menyatakan', 'bertanggung', 'jawab', 'atas', 'ledakan', 'di', 'Srinagar', '?'],
  'seq_label': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```

### Data Fields

1. `EmoT` dataset

- `tweet`: a `string` feature.
- `label`: an emotion label, with possible values including `sadness`, `anger`, `love`, `fear`, `happy`.

2. `SmSA` dataset

- `text`: a `string` feature.
- `label`: a sentiment label, with possible values including `positive`, `neutral`, `negative`.

3. `CASA` dataset

- `sentence`: a `string` feature.
- `fuel`: a sentiment label, with possible values including `negative`, `neutral`, `positive`.
- `machine`: a sentiment label, with possible values including `negative`, `neutral`, `positive`.
- `others`: a sentiment label, with possible values including `negative`, `neutral`, `positive`.
- `part`: a sentiment label, with possible values including `negative`, `neutral`, `positive`.
- `price`: a sentiment label, with possible values including `negative`, `neutral`, `positive`.
- `service`: a sentiment label, with possible values including `negative`, `neutral`, `positive`.

4. `HoASA` dataset

- `sentence`: a `string` feature.
- `ac`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `air_panas`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `bau`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `general`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `kebersihan`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `linen`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `service`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `sunrise_meal`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `tv`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.
- `wifi`: a sentiment label, with possible values including `neg`, `neut`, `pos`, `neg_pos`.

5. `WReTE` dataset

- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `category`: a `string` feature.
- `label`: a classification label, with possible values including `NotEntail`, `Entail_or_Paraphrase`.

6. `POSP` dataset

- `tokens`: a `list` of `string` features.
- `pos_tags`: a `list` of POS tag labels, with possible values including `B-PPO`, `B-KUA`, `B-ADV`, `B-PRN`, `B-VBI`.

The POS tag labels follow the [Indonesian Association of Computational Linguistics (INACL) POS Tagging Convention](http://inacl.id/inacl/wp-content/uploads/2017/06/INACLPOS-Tagging-Convention-26-Mei.pdf).

7. `BaPOS` dataset

- `tokens`: a `list` of `string` features.
- `pos_tags`: a `list` of POS tag labels, with possible values including `B-PR`, `B-CD`, `I-PR`, `B-SYM`, `B-JJ`.

The POS tag labels from [Tagset UI](https://bahasa.cs.ui.ac.id/postag/downloads/Tagset.pdf).

8. `TermA` dataset

- `tokens`: a `list` of `string` features.
- `seq_label`: a `list` of classification labels, with possible values including `I-SENTIMENT`, `O`, `I-ASPECT`, `B-SENTIMENT`, `B-ASPECT`.

9. `KEPS` dataset

- `tokens`: a `list` of `string` features.
- `seq_label`: a `list` of classification labels, with possible values including `O`, `B`, `I`.

The labels use Inside-Outside-Beginning (IOB) tagging.

10. `NERGrit` dataset

- `tokens`: a `list` of `string` features.
- `ner_tags`: a `list` of NER tag labels, with possible values including `I-PERSON`, `B-ORGANISATION`, `I-ORGANISATION`, `B-PLACE`, `I-PLACE`.

The labels use Inside-Outside-Beginning (IOB) tagging.

11. `NERP` dataset

- `tokens`: a `list` of `string` features.
- `ner_tags`: a `list` of NER tag labels, with possible values including `I-PPL`, `B-EVT`, `B-PLC`, `I-IND`, `B-IND`.

12. `FacQA` dataset

- `question`: a `list` of `string` features.
- `passage`: a `list` of `string` features.
- `seq_label`: a `list` of classification labels, with possible values including `O`, `B`, `I`.

### Data Splits

The data is split into a training, validation and test set.

|    | dataset | Train | Valid | Test |
|----|---------|-------|-------|------|
| 1  | EmoT    | 3521  | 440   | 440  |
| 2  | SmSA    | 11000 | 1260  | 500  |
| 3  | CASA    | 810   | 90    | 180  |
| 4  | HoASA   | 2283  | 285   | 286  |
| 5  | WReTE   | 300   | 50    | 100  |
| 6  | POSP    | 6720  | 840   | 840  |
| 7  | BaPOS   | 8000  | 1000  | 1029 |
| 8  | TermA   | 3000  | 1000  | 1000 |
| 9  | KEPS    | 800   | 200   | 247  |
| 10 | NERGrit | 1672  | 209   | 209  |
| 11 | NERP    | 6720  | 840   | 840  |
| 12 | FacQA   | 2495  | 311   | 311  |

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

The licensing status of the IndoNLU benchmark datasets is under MIT License.

### Citation Information

IndoNLU citation
```
@inproceedings{wilie2020indonlu,
  title={IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding},
  author={Bryan Wilie and Karissa Vincentio and Genta Indra Winata and Samuel Cahyawijaya and X. Li and Zhi Yuan Lim and S. Soleman and R. Mahendra and Pascale Fung and Syafri Bahar and A. Purwarianti},
  booktitle={Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing},
  year={2020}
}
```

`EmoT` dataset citation
```
@inproceedings{saputri2018emotion,
  title={Emotion Classification on Indonesian Twitter Dataset},
  author={Mei Silviana Saputri, Rahmad Mahendra, and Mirna Adriani},
  booktitle={Proceedings of the 2018 International Conference on Asian Language Processing(IALP)},
  pages={90--95},
  year={2018},
  organization={IEEE}
}
```

`SmSA` dataset citation
```
@inproceedings{purwarianti2019improving,
  title={Improving Bi-LSTM Performance for Indonesian Sentiment Analysis Using Paragraph Vector},
  author={Ayu Purwarianti and Ida Ayu Putu Ari Crisdayanti},
  booktitle={Proceedings of the 2019 International Conference of Advanced Informatics: Concepts, Theory and Applications (ICAICTA)},
  pages={1--5},
  year={2019},
  organization={IEEE}
}
```

`CASA` dataset citation
```
@inproceedings{ilmania2018aspect,
  title={Aspect Detection and Sentiment Classification Using Deep Neural Network for Indonesian Aspect-based Sentiment Analysis},
  author={Arfinda Ilmania, Abdurrahman, Samuel Cahyawijaya, Ayu Purwarianti},
  booktitle={Proceedings of the 2018 International Conference on Asian Language Processing(IALP)},
  pages={62--67},
  year={2018},
  organization={IEEE}
}
```

`HoASA` dataset citation
```
@inproceedings{azhar2019multi,
  title={Multi-label Aspect Categorization with Convolutional Neural Networks and Extreme Gradient Boosting},
  author={A. N. Azhar, M. L. Khodra, and A. P. Sutiono}
  booktitle={Proceedings of the 2019 International Conference on Electrical Engineering and Informatics (ICEEI)},
  pages={35--40},
  year={2019}
}
```

`WReTE` dataset citation
```
@inproceedings{setya2018semi,
  title={Semi-supervised Textual Entailment on Indonesian Wikipedia Data},
  author={Ken Nabila Setya and Rahmad Mahendra},
  booktitle={Proceedings of the 2018 International Conference on Computational Linguistics and Intelligent Text Processing (CICLing)},
  year={2018}
}
```

`POSP` dataset citation
```
@inproceedings{hoesen2018investigating,
  title={Investigating Bi-LSTM and CRF with POS Tag Embedding for Indonesian Named Entity Tagger},
  author={Devin Hoesen and Ayu Purwarianti},
  booktitle={Proceedings of the 2018 International Conference on Asian Language Processing (IALP)},
  pages={35--38},
  year={2018},
  organization={IEEE}
}
```

`BaPOS` dataset citation
```
@inproceedings{dinakaramani2014designing,
  title={Designing an Indonesian Part of Speech Tagset and Manually Tagged Indonesian Corpus},
  author={Arawinda Dinakaramani, Fam Rashel, Andry Luthfi, and Ruli Manurung},
  booktitle={Proceedings of the 2014 International Conference on Asian Language Processing (IALP)},
  pages={66--69},
  year={2014},
  organization={IEEE}
}
@inproceedings{kurniawan2018toward,
  title={Toward a Standardized and More Accurate Indonesian Part-of-Speech Tagging},
  author={Kemal Kurniawan and Alham Fikri Aji},
  booktitle={Proceedings of the 2018 International Conference on Asian Language Processing (IALP)},
  pages={303--307},
  year={2018},
  organization={IEEE}
}
```

`TermA` dataset citation
```
@article{winatmoko2019aspect,
  title={Aspect and Opinion Term Extraction for Hotel Reviews Using Transfer Learning and Auxiliary Labels},
  author={Yosef Ardhito Winatmoko, Ali Akbar Septiandri, Arie Pratama Sutiono},
  journal={arXiv preprint arXiv:1909.11879},
  year={2019}
}
@article{fernando2019aspect,
  title={Aspect and Opinion Terms Extraction Using Double Embeddings and Attention Mechanism for Indonesian Hotel Reviews},
  author={Jordhy Fernando, Masayu Leylia Khodra, Ali Akbar Septiandri},
  journal={arXiv preprint arXiv:1908.04899},
  year={2019}
}
```

`KEPS` dataset citation
```
@inproceedings{mahfuzh2019improving,
  title={Improving Joint Layer RNN based Keyphrase Extraction by Using Syntactical Features},
  author={Miftahul Mahfuzh, Sidik Soleman, and Ayu Purwarianti},
  booktitle={Proceedings of the 2019 International Conference of Advanced Informatics: Concepts, Theory and Applications (ICAICTA)},
  pages={1--6},
  year={2019},
  organization={IEEE}
}
```

`NERGrit` dataset citation
```
@online{nergrit2019,
  title={NERGrit Corpus},
  author={NERGrit Developers},
  year={2019},
  url={https://github.com/grit-id/nergrit-corpus}
}
```

`NERP` dataset citation
```
@inproceedings{hoesen2018investigating,
  title={Investigating Bi-LSTM and CRF with POS Tag Embedding for Indonesian Named Entity Tagger},
  author={Devin Hoesen and Ayu Purwarianti},
  booktitle={Proceedings of the 2018 International Conference on Asian Language Processing (IALP)},
  pages={35--38},
  year={2018},
  organization={IEEE}
}
```

`FacQA` dataset citation
```
@inproceedings{purwarianti2007machine,
  title={A Machine Learning Approach for Indonesian Question Answering System},
  author={Ayu Purwarianti, Masatoshi Tsuchiya, and Seiichi Nakagawa},
  booktitle={Proceedings of Artificial Intelligence and Applications },
  pages={573--578},
  year={2007}
}
```

### Contributions

Thanks to [@yasirabd](https://github.com/yasirabd) for adding this dataset.