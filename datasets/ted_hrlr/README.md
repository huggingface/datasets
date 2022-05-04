---
pretty_name: TEDHrlr
paperswithcode_id: null
---

# Dataset Card for "ted_hrlr"

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

- **Homepage:** [https://github.com/neulab/word-embeddings-for-nmt](https://github.com/neulab/word-embeddings-for-nmt)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1749.12 MB
- **Size of the generated dataset:** 268.61 MB
- **Total amount of disk used:** 2017.73 MB

### Dataset Summary

Data sets derived from TED talk transcripts for comparing similar language pairs
where one is high resource and the other is low resource.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### az_to_en

- **Size of downloaded dataset files:** 124.94 MB
- **Size of the generated dataset:** 1.46 MB
- **Total amount of disk used:** 126.40 MB

An example of 'train' looks as follows.
```
{
    "translation": {
        "az": "zəhmət olmasa , sizə xitab edən sözlər eşidəndə əlinizi qaldırın .",
        "en": "please raise your hand if something applies to you ."
    }
}
```

#### aztr_to_en

- **Size of downloaded dataset files:** 124.94 MB
- **Size of the generated dataset:** 38.28 MB
- **Total amount of disk used:** 163.22 MB

An example of 'train' looks as follows.
```
{
    "translation": {
        "az_tr": "zəhmət olmasa , sizə xitab edən sözlər eşidəndə əlinizi qaldırın .",
        "en": "please raise your hand if something applies to you ."
    }
}
```

#### be_to_en

- **Size of downloaded dataset files:** 124.94 MB
- **Size of the generated dataset:** 1.36 MB
- **Total amount of disk used:** 126.29 MB

An example of 'train' looks as follows.
```
{
    "translation": {
        "be": "zəhmət olmasa , sizə xitab edən sözlər eşidəndə əlinizi qaldırın .",
        "en": "please raise your hand if something applies to you ."
    }
}
```

#### beru_to_en

- **Size of downloaded dataset files:** 124.94 MB
- **Size of the generated dataset:** 57.41 MB
- **Total amount of disk used:** 182.35 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"be_ru\": \"11 yaşımdaydım . səhərin birində , evimizdəki sevinc səslərinə oyandığım indiki kimi yadımdadır .\", \"en\": \"when i was..."
}
```

#### es_to_pt

- **Size of downloaded dataset files:** 124.94 MB
- **Size of the generated dataset:** 8.71 MB
- **Total amount of disk used:** 133.65 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"es\": \"11 yaşımdaydım . səhərin birində , evimizdəki sevinc səslərinə oyandığım indiki kimi yadımdadır .\", \"pt\": \"when i was 11..."
}
```

### Data Fields

The data fields are the same among all splits.

#### az_to_en
- `translation`: a multilingual `string` variable, with possible languages including `az`, `en`.

#### aztr_to_en
- `translation`: a multilingual `string` variable, with possible languages including `az_tr`, `en`.

#### be_to_en
- `translation`: a multilingual `string` variable, with possible languages including `be`, `en`.

#### beru_to_en
- `translation`: a multilingual `string` variable, with possible languages including `be_ru`, `en`.

#### es_to_pt
- `translation`: a multilingual `string` variable, with possible languages including `es`, `pt`.

### Data Splits

|   name   |train |validation|test|
|----------|-----:|---------:|---:|
|az_to_en  |  5947|       672| 904|
|aztr_to_en|188397|       672| 904|
|be_to_en  |  4510|       249| 665|
|beru_to_en|212615|       249| 665|
|es_to_pt  | 44939|      1017|1764|

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
@inproceedings{Ye2018WordEmbeddings,
  author  = {Ye, Qi and Devendra, Sachan and Matthieu, Felix and Sarguna, Padmanabhan and Graham, Neubig},
  title   = {When and Why are pre-trained word embeddings useful for Neural Machine Translation},
  booktitle = {HLT-NAACL},
  year    = {2018},
  }

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.