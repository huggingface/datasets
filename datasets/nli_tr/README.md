---
annotations_creators:
- expert-generated
language_creators:
- machine-generated
language:
- tr
license:
- cc-by-3.0
- cc-by-4.0
- cc-by-sa-3.0
- mit
- other
license_details: "Open Portion of the American National Corpus"
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|snli
- extended|multi_nli
task_categories:
- text-classification
task_ids:
- natural-language-inference
- semantic-similarity-scoring
- text-scoring
paperswithcode_id: nli-tr
pretty_name: Natural Language Inference in Turkish
configs:
- multinli_tr
- snli_tr
---

# Dataset Card for "nli_tr"

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

- **Homepage:** [https://github.com/boun-tabi/NLI-TR](https://github.com/boun-tabi/NLI-TR)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 110.48 MB
- **Size of the generated dataset:** 146.26 MB
- **Total amount of disk used:** 256.74 MB

### Dataset Summary

The Natural Language Inference in Turkish (NLI-TR) is a set of two large scale datasets that were obtained by translating the foundational NLI corpora (SNLI and MNLI) using Amazon Translate.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### multinli_tr

- **Size of downloaded dataset files:** 72.02 MB
- **Size of the generated dataset:** 75.79 MB
- **Total amount of disk used:** 147.81 MB

An example of 'validation_matched' looks as follows.
```
This example was too long and was cropped:

{
    "hypothesis": "Mrinal Sen'in çalışmalarının çoğu Avrupa koleksiyonlarında bulunabilir.",
    "idx": 7,
    "label": 1,
    "premise": "\"Kalküta, sanatsal yaratıcılığa dair herhangi bir iddiaya sahip olan tek diğer üretim merkezi gibi görünüyor, ama ironik bir şek..."
}
```

#### snli_tr

- **Size of downloaded dataset files:** 38.46 MB
- **Size of the generated dataset:** 70.47 MB
- **Total amount of disk used:** 108.93 MB

An example of 'train' looks as follows.
```
{
    "hypothesis": "Yaşlı bir adam, kızının işten çıkmasını bekçiyken suyunu içer.",
    "idx": 9,
    "label": 1,
    "premise": "Parlak renkli gömlek çalışanları arka planda gülümseme iken yaşlı bir adam bir kahve dükkanında küçük bir masada onun portakal suyu ile oturur."
}
```

### Data Fields

The data fields are the same among all splits.

#### multinli_tr
- `idx`: a `int32` feature.
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

#### snli_tr
- `idx`: a `int32` feature.
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

### Data Splits

#### multinli_tr

|           |train |validation_matched|validation_mismatched|
|-----------|-----:|-----------------:|--------------------:|
|multinli_tr|392702|             10000|                10000|

#### snli_tr

|       |train |validation|test |
|-------|-----:|---------:|----:|
|snli_tr|550152|     10000|10000|

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
@inproceedings{budur-etal-2020-data,
    title = "Data and Representation for Turkish Natural Language Inference",
    author = "Budur, Emrah and
      "{O}zçelik, Rıza and
      G"{u}ng"{o}r, Tunga",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    abstract = "Large annotated datasets in NLP are overwhelmingly in English. This is an obstacle to progress in other languages. Unfortunately, obtaining new annotated resources for each task in each language would be prohibitively expensive. At the same time, commercial machine translation systems are now robust. Can we leverage these systems to translate English-language datasets automatically? In this paper, we offer a positive response for natural language inference (NLI) in Turkish. We translated two large English NLI datasets into Turkish and had a team of experts validate their translation quality and fidelity to the original labels. Using these datasets, we address core issues of representation for Turkish NLI. We find that in-language embeddings are essential and that morphological parsing can be avoided where the training set is large. Finally, we show that models trained on our machine-translated datasets are successful on human-translated evaluation sets. We share all code, models, and data publicly.",
}

```


### Contributions

Thanks to [@e-budur](https://github.com/e-budur) for adding this dataset.
