---
paperswithcode_id: null
pretty_name: IWSLT 2017
license:
- cc-by-nc-nd-4.0
---

# Dataset Card for IWSLT 2017

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

- **Homepage:** [https://sites.google.com/site/iwsltevaluation2017/TED-tasks](https://sites.google.com/site/iwsltevaluation2017/TED-tasks)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 4046.89 MB
- **Size of the generated dataset:** 1087.28 MB
- **Total amount of disk used:** 5134.17 MB

### Dataset Summary

The IWSLT 2017 Evaluation Campaign includes a multilingual TED Talks MT task. The languages involved are five:

  German, English, Italian, Dutch, Romanian.

For each language pair, training and development sets are available through the entry of the table below: by clicking, an archive will be downloaded which contains the sets and a README file. Numbers in the table refer to millions of units (untokenized words) of the target side of all parallel training sets.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### iwslt2017-ar-en

- **Size of downloaded dataset files:** 26.46 MB
- **Size of the generated dataset:** 56.02 MB
- **Total amount of disk used:** 82.48 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"ar\": \"لقد طرت في \\\"القوات الجوية \\\" لمدة ثمان سنوات. والآن أجد نفسي مضطرا لخلع حذائي قبل صعود الطائرة!\", \"en\": \"I flew on Air ..."
}
```

#### iwslt2017-de-en

- **Size of downloaded dataset files:** 15.98 MB
- **Size of the generated dataset:** 42.37 MB
- **Total amount of disk used:** 58.35 MB

An example of 'train' looks as follows.
```
{
    "translation": {
        "de": "Es ist mir wirklich eine Ehre, zweimal auf dieser Bühne stehen zu dürfen. Tausend Dank dafür.",
        "en": "And it's truly a great honor to have the opportunity to come to this stage twice; I'm extremely grateful."
    }
}
```

#### iwslt2017-en-ar

- **Size of downloaded dataset files:** 27.97 MB
- **Size of the generated dataset:** 56.02 MB
- **Total amount of disk used:** 83.99 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"ar\": \"لقد طرت في \\\"القوات الجوية \\\" لمدة ثمان سنوات. والآن أجد نفسي مضطرا لخلع حذائي قبل صعود الطائرة!\", \"en\": \"I flew on Air ..."
}
```

#### iwslt2017-en-de

- **Size of downloaded dataset files:** 15.98 MB
- **Size of the generated dataset:** 42.37 MB
- **Total amount of disk used:** 58.35 MB

An example of 'validation' looks as follows.
```
{
    "translation": {
        "de": "Die nächste Folie, die ich Ihnen zeige, ist eine Zeitrafferaufnahme was in den letzten 25 Jahren passiert ist.",
        "en": "The next slide I show you will be  a rapid fast-forward of what's happened over the last 25 years."
    }
}
```

#### iwslt2017-en-fr

- **Size of downloaded dataset files:** 26.41 MB
- **Size of the generated dataset:** 48.87 MB
- **Total amount of disk used:** 75.28 MB

An example of 'validation' looks as follows.
```
{
    "translation": {
        "en": "But this understates the seriousness of this particular problem  because it doesn't show the thickness of the ice.",
        "fr": "Mais ceci tend à amoindrir le problème parce qu'on ne voit pas l'épaisseur de la glace."
    }
}
```

### Data Fields

The data fields are the same among all splits.

#### iwslt2017-ar-en
- `translation`: a multilingual `string` variable, with possible languages including `ar`, `en`.

#### iwslt2017-de-en
- `translation`: a multilingual `string` variable, with possible languages including `de`, `en`.

#### iwslt2017-en-ar
- `translation`: a multilingual `string` variable, with possible languages including `en`, `ar`.

#### iwslt2017-en-de
- `translation`: a multilingual `string` variable, with possible languages including `en`, `de`.

#### iwslt2017-en-fr
- `translation`: a multilingual `string` variable, with possible languages including `en`, `fr`.

### Data Splits

|     name      |train |validation|test|
|---------------|-----:|---------:|---:|
|iwslt2017-ar-en|231713|       888|8583|
|iwslt2017-de-en|206112|       888|8079|
|iwslt2017-en-ar|231713|       888|8583|
|iwslt2017-en-de|206112|       888|8079|
|iwslt2017-en-fr|232825|       890|8597|

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

Creative Commons BY-NC-ND

See the (TED Talks Usage Policy)[https://www.ted.com/about/our-organization/our-policies-terms/ted-talks-usage-policy].

### Citation Information

```
@inproceedings{cettoloEtAl:EAMT2012,
Address = {Trento, Italy},
Author = {Mauro Cettolo and Christian Girardi and Marcello Federico},
Booktitle = {Proceedings of the 16$^{th}$ Conference of the European Association for Machine Translation (EAMT)},
Date = {28-30},
Month = {May},
Pages = {261--268},
Title = {WIT$^3$: Web Inventory of Transcribed and Translated Talks},
Year = {2012}}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@Narsil](https://github.com/Narsil) for adding this dataset.
