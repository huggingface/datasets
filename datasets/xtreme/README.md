---
annotations_creators:
- found
language_creators:
- found
language:
- af
- ar
- bg
- bn
- de
- el
- en
- es
- et
- eu
- fa
- fa-IR
- fi
- fr
- he
- hi
- hu
- id
- it
- ja
- jv
- ka
- kk
- ko
- ml
- mr
- ms
- my
- nl
- pt
- ru
- sw
- ta
- te
- th
- tl
- tr
- ur
- vi
- yo
- zh
license:
- apache-2.0
- cc-by-4.0
- cc-by-2.0
- cc-by-sa-4.0
- other
- cc-by-nc-4.0
license_details: "Licence Universal Dependencies v2.5"
multilinguality:
- multilingual
- translation
pretty_name: XTREME
size_categories:
- n<1K
- 1K<n<10K
- 10K<n<100K
- 100K<n<1M
source_datasets:
- extended|xnli
- extended|paws-x
- extended|wikiann
- extended|xquad
- extended|mlqa
- extended|tydiqa
- extended|tatoeba
- extended|squad
task_categories:
- multiple-choice
- question-answering
- token-classification
- text-classification
- text-retrieval
- token-classification
task_ids:
- multiple-choice-qa
- extractive-qa
- open-domain-qa
- natural-language-inference
- text-classification-other-paraphrase-identification
- text-retrieval-other-parallel-sentence-retrieval
- named-entity-recognition
- part-of-speech-tagging
paperswithcode_id: xtreme
configs:
- MLQA.ar.ar
- MLQA.ar.de
- MLQA.ar.en
- MLQA.ar.es
- MLQA.ar.hi
- MLQA.ar.vi
- MLQA.ar.zh
- MLQA.de.ar
- MLQA.de.de
- MLQA.de.en
- MLQA.de.es
- MLQA.de.hi
- MLQA.de.vi
- MLQA.de.zh
- MLQA.en.ar
- MLQA.en.de
- MLQA.en.en
- MLQA.en.es
- MLQA.en.hi
- MLQA.en.vi
- MLQA.en.zh
- MLQA.es.ar
- MLQA.es.de
- MLQA.es.en
- MLQA.es.es
- MLQA.es.hi
- MLQA.es.vi
- MLQA.es.zh
- MLQA.hi.ar
- MLQA.hi.de
- MLQA.hi.en
- MLQA.hi.es
- MLQA.hi.hi
- MLQA.hi.vi
- MLQA.hi.zh
- MLQA.vi.ar
- MLQA.vi.de
- MLQA.vi.en
- MLQA.vi.es
- MLQA.vi.hi
- MLQA.vi.vi
- MLQA.vi.zh
- MLQA.zh.ar
- MLQA.zh.de
- MLQA.zh.en
- MLQA.zh.es
- MLQA.zh.hi
- MLQA.zh.vi
- MLQA.zh.zh
- PAN-X.af
- PAN-X.ar
- PAN-X.bg
- PAN-X.bn
- PAN-X.de
- PAN-X.el
- PAN-X.en
- PAN-X.es
- PAN-X.et
- PAN-X.eu
- PAN-X.fa
- PAN-X.fi
- PAN-X.fr
- PAN-X.he
- PAN-X.hi
- PAN-X.hu
- PAN-X.id
- PAN-X.it
- PAN-X.ja
- PAN-X.jv
- PAN-X.ka
- PAN-X.kk
- PAN-X.ko
- PAN-X.ml
- PAN-X.mr
- PAN-X.ms
- PAN-X.my
- PAN-X.nl
- PAN-X.pt
- PAN-X.ru
- PAN-X.sw
- PAN-X.ta
- PAN-X.te
- PAN-X.th
- PAN-X.tl
- PAN-X.tr
- PAN-X.ur
- PAN-X.vi
- PAN-X.yo
- PAN-X.zh
- PAWS-X.de
- PAWS-X.en
- PAWS-X.es
- PAWS-X.fr
- PAWS-X.ja
- PAWS-X.ko
- PAWS-X.zh
- SQuAD
- XNLI
- XQuAD
- bucc18.de
- bucc18.fr
- bucc18.ru
- bucc18.zh
- tatoeba.afr
- tatoeba.ara
- tatoeba.ben
- tatoeba.bul
- tatoeba.cmn
- tatoeba.deu
- tatoeba.ell
- tatoeba.est
- tatoeba.eus
- tatoeba.fin
- tatoeba.fra
- tatoeba.heb
- tatoeba.hin
- tatoeba.hun
- tatoeba.ind
- tatoeba.ita
- tatoeba.jav
- tatoeba.jpn
- tatoeba.kat
- tatoeba.kaz
- tatoeba.kor
- tatoeba.mal
- tatoeba.mar
- tatoeba.nld
- tatoeba.pes
- tatoeba.por
- tatoeba.rus
- tatoeba.spa
- tatoeba.swh
- tatoeba.tam
- tatoeba.tel
- tatoeba.tgl
- tatoeba.tha
- tatoeba.tur
- tatoeba.urd
- tatoeba.vie
- tydiqa
- udpos.Afrikans
- udpos.Arabic
- udpos.Basque
- udpos.Bulgarian
- udpos.Chinese
- udpos.Dutch
- udpos.English
- udpos.Estonian
- udpos.Finnish
- udpos.French
- udpos.German
- udpos.Greek
- udpos.Hebrew
- udpos.Hindi
- udpos.Hungarian
- udpos.Indonesian
- udpos.Italian
- udpos.Japanese
- udpos.Kazakh
- udpos.Korean
- udpos.Marathi
- udpos.Persian
- udpos.Portuguese
- udpos.Russian
- udpos.Spanish
- udpos.Tagalog
- udpos.Tamil
- udpos.Telugu
- udpos.Thai
- udpos.Turkish
- udpos.Urdu
- udpos.Vietnamese
- udpos.Yoruba
---

# Dataset Card for "xtreme"

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

- **Homepage:** [https://github.com/google-research/xtreme](https://github.com/google-research/xtreme)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 15143.21 MB
- **Size of the generated dataset:** 1027.42 MB
- **Total amount of disk used:** 16170.64 MB

### Dataset Summary

The Cross-lingual Natural Language Inference (XNLI) corpus is a crowd-sourced collection of 5,000 test and
2,500 dev pairs for the MultiNLI corpus. The pairs are annotated with textual entailment and translated into
14 languages: French, Spanish, German, Greek, Bulgarian, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese,
Hindi, Swahili and Urdu. This results in 112.5k annotated pairs. Each premise can be associated with the
corresponding hypothesis in the 15 languages, summing up to more than 1.5M combinations. The corpus is made to
evaluate how to perform inference in any language (including low-resources ones like Swahili or Urdu) when only
English NLI data is available at training time. One solution is cross-lingual sentence encoding, for which XNLI
is an evaluation benchmark.
The Cross-lingual TRansfer Evaluation of Multilingual Encoders (XTREME) benchmark is a benchmark for the evaluation of
the cross-lingual generalization ability of pre-trained multilingual models. It covers 40 typologically diverse languages
(spanning 12 language families) and includes nine tasks that collectively require reasoning about different levels of
syntax and semantics. The languages in XTREME are selected to maximize language diversity, coverage in existing tasks,
and availability of training data. Among these are many under-studied languages, such as the Dravidian languages Tamil
(spoken in southern India, Sri Lanka, and Singapore), Telugu and Malayalam (spoken mainly in southern India), and the
Niger-Congo languages Swahili and Yoruba, spoken in Africa.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### MLQA.ar.ar

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 8.77 MB
- **Total amount of disk used:** 80.98 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.de

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 2.43 MB
- **Total amount of disk used:** 74.64 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.en

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 8.62 MB
- **Total amount of disk used:** 80.83 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.es

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 3.12 MB
- **Total amount of disk used:** 75.33 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.hi

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 3.17 MB
- **Total amount of disk used:** 75.38 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### MLQA.ar.ar
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.de
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.en
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.es
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.hi
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

### Data Splits

|   name   |validation|test|
|----------|---------:|---:|
|MLQA.ar.ar|       517|5335|
|MLQA.ar.de|       207|1649|
|MLQA.ar.en|       517|5335|
|MLQA.ar.es|       161|1978|
|MLQA.ar.hi|       186|1831|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
  @InProceedings{conneau2018xnli,
  author = {Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin},
  title = {XNLI: Evaluating Cross-lingual Sentence Representations},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing},
  year = {2018},
  publisher = {Association for Computational Linguistics},
  location = {Brussels, Belgium},
}
@article{hu2020xtreme,
      author    = {Junjie Hu and Sebastian Ruder and Aditya Siddhant and Graham Neubig and Orhan Firat and Melvin Johnson},
      title     = {XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization},
      journal   = {CoRR},
      volume    = {abs/2003.11080},
      year      = {2020},
      archivePrefix = {arXiv},
      eprint    = {2003.11080}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jplu](https://github.com/jplu), [@lewtun](https://github.com/lewtun), [@lvwerra](https://github.com/lvwerra), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.