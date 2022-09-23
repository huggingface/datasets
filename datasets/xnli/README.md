---
language:
- en
paperswithcode_id: xnli
pretty_name: Cross-lingual Natural Language Inference
dataset_info:
- config_name: ar
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1294561
    num_examples: 5010
  - name: train
    num_bytes: 107399934
    num_examples: 392702
  - name: validation
    num_bytes: 633009
    num_examples: 2490
  download_size: 483963712
  dataset_size: 109327504
- config_name: bg
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1573042
    num_examples: 5010
  - name: train
    num_bytes: 125973545
    num_examples: 392702
  - name: validation
    num_bytes: 774069
    num_examples: 2490
  download_size: 483963712
  dataset_size: 128320656
- config_name: de
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 996496
    num_examples: 5010
  - name: train
    num_bytes: 84684460
    num_examples: 392702
  - name: validation
    num_bytes: 494612
    num_examples: 2490
  download_size: 483963712
  dataset_size: 86175568
- config_name: el
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1704793
    num_examples: 5010
  - name: train
    num_bytes: 139753678
    num_examples: 392702
  - name: validation
    num_bytes: 841234
    num_examples: 2490
  download_size: 483963712
  dataset_size: 142299705
- config_name: en
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 875142
    num_examples: 5010
  - name: train
    num_bytes: 74444346
    num_examples: 392702
  - name: validation
    num_bytes: 433471
    num_examples: 2490
  download_size: 483963712
  dataset_size: 75752959
- config_name: es
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 969821
    num_examples: 5010
  - name: train
    num_bytes: 81383604
    num_examples: 392702
  - name: validation
    num_bytes: 478430
    num_examples: 2490
  download_size: 483963712
  dataset_size: 82831855
- config_name: fr
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1029247
    num_examples: 5010
  - name: train
    num_bytes: 85809099
    num_examples: 392702
  - name: validation
    num_bytes: 510112
    num_examples: 2490
  download_size: 483963712
  dataset_size: 87348458
- config_name: hi
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 2073081
    num_examples: 5010
  - name: train
    num_bytes: 170594284
    num_examples: 392702
  - name: validation
    num_bytes: 1023923
    num_examples: 2490
  download_size: 483963712
  dataset_size: 173691288
- config_name: ru
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1603474
    num_examples: 5010
  - name: train
    num_bytes: 129859935
    num_examples: 392702
  - name: validation
    num_bytes: 786450
    num_examples: 2490
  download_size: 483963712
  dataset_size: 132249859
- config_name: sw
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 871659
    num_examples: 5010
  - name: train
    num_bytes: 69286045
    num_examples: 392702
  - name: validation
    num_bytes: 429858
    num_examples: 2490
  download_size: 483963712
  dataset_size: 70587562
- config_name: th
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 2147023
    num_examples: 5010
  - name: train
    num_bytes: 176063212
    num_examples: 392702
  - name: validation
    num_bytes: 1061168
    num_examples: 2490
  download_size: 483963712
  dataset_size: 179271403
- config_name: tr
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 934942
    num_examples: 5010
  - name: train
    num_bytes: 71637460
    num_examples: 392702
  - name: validation
    num_bytes: 459316
    num_examples: 2490
  download_size: 483963712
  dataset_size: 73031718
- config_name: ur
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1416249
    num_examples: 5010
  - name: train
    num_bytes: 96441806
    num_examples: 392702
  - name: validation
    num_bytes: 699960
    num_examples: 2490
  download_size: 483963712
  dataset_size: 98558015
- config_name: vi
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1190225
    num_examples: 5010
  - name: train
    num_bytes: 101417750
    num_examples: 392702
  - name: validation
    num_bytes: 590688
    num_examples: 2490
  download_size: 483963712
  dataset_size: 103198663
- config_name: zh
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 777937
    num_examples: 5010
  - name: train
    num_bytes: 72225161
    num_examples: 392702
  - name: validation
    num_bytes: 384859
    num_examples: 2490
  download_size: 483963712
  dataset_size: 73387957
- config_name: all_languages
  features:
  - name: premise
    dtype:
      translation:
        languages:
        - ar
        - bg
        - de
        - el
        - en
        - es
        - fr
        - hi
        - ru
        - sw
        - th
        - tr
        - ur
        - vi
        - zh
  - name: hypothesis
    dtype:
      translation_variable_languages:
        languages:
        - ar
        - bg
        - de
        - el
        - en
        - es
        - fr
        - hi
        - ru
        - sw
        - th
        - tr
        - ur
        - vi
        - zh
        num_languages: 15
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 19387508
    num_examples: 5010
  - name: train
    num_bytes: 1581474731
    num_examples: 392702
  - name: validation
    num_bytes: 9566255
    num_examples: 2490
  download_size: 483963712
  dataset_size: 1610428494
---

# Dataset Card for "xnli"

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

- **Homepage:** [https://www.nyu.edu/projects/bowman/xnli/](https://www.nyu.edu/projects/bowman/xnli/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 7384.70 MB
- **Size of the generated dataset:** 3076.99 MB
- **Total amount of disk used:** 10461.69 MB

### Dataset Summary

XNLI is a subset of a few thousand examples from MNLI which has been translated
into a 14 different languages (some low-ish resource). As with MNLI, the goal is
to predict textual entailment (does sentence A imply/contradict/neither sentence
B) and is a classification task (given two sentences, predict one of three
labels).

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### all_languages

- **Size of downloaded dataset files:** 461.54 MB
- **Size of the generated dataset:** 1535.82 MB
- **Total amount of disk used:** 1997.37 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "hypothesis": "{\"language\": [\"ar\", \"bg\", \"de\", \"el\", \"en\", \"es\", \"fr\", \"hi\", \"ru\", \"sw\", \"th\", \"tr\", \"ur\", \"vi\", \"zh\"], \"translation\": [\"احد اع...",
    "label": 0,
    "premise": "{\"ar\": \"واحدة من رقابنا ستقوم بتنفيذ تعليماتك كلها بكل دقة\", \"bg\": \"един от нашите номера ще ви даде инструкции .\", \"de\": \"Eine ..."
}
```

#### ar

- **Size of downloaded dataset files:** 461.54 MB
- **Size of the generated dataset:** 104.26 MB
- **Total amount of disk used:** 565.81 MB

An example of 'validation' looks as follows.
```
{
    "hypothesis": "اتصل بأمه حالما أوصلته حافلة المدرسية.",
    "label": 1,
    "premise": "وقال، ماما، لقد عدت للمنزل."
}
```

#### bg

- **Size of downloaded dataset files:** 461.54 MB
- **Size of the generated dataset:** 122.38 MB
- **Total amount of disk used:** 583.92 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "hypothesis": "\"губиш нещата на следното ниво , ако хората си припомнят .\"...",
    "label": 0,
    "premise": "\"по време на сезона и предполагам , че на твоето ниво ще ги загубиш на следващото ниво , ако те решат да си припомнят отбора на ..."
}
```

#### de

- **Size of downloaded dataset files:** 461.54 MB
- **Size of the generated dataset:** 82.18 MB
- **Total amount of disk used:** 543.73 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "hypothesis": "Man verliert die Dinge auf die folgende Ebene , wenn sich die Leute erinnern .",
    "label": 0,
    "premise": "\"Du weißt , während der Saison und ich schätze , auf deiner Ebene verlierst du sie auf die nächste Ebene , wenn sie sich entschl..."
}
```

#### el

- **Size of downloaded dataset files:** 461.54 MB
- **Size of the generated dataset:** 135.71 MB
- **Total amount of disk used:** 597.25 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "hypothesis": "\"Τηλεφώνησε στη μαμά του μόλις το σχολικό λεωφορείο τον άφησε.\"...",
    "label": 1,
    "premise": "Και είπε, Μαμά, έφτασα στο σπίτι."
}
```

### Data Fields

The data fields are the same among all splits.

#### all_languages
- `premise`: a multilingual `string` variable, with possible languages including `ar`, `bg`, `de`, `el`, `en`.
- `hypothesis`: a multilingual `string` variable, with possible languages including `ar`, `bg`, `de`, `el`, `en`.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

#### ar
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

#### bg
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

#### de
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

#### el
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).

### Data Splits

|    name     |train |validation|test|
|-------------|-----:|---------:|---:|
|all_languages|392702|      2490|5010|
|ar           |392702|      2490|5010|
|bg           |392702|      2490|5010|
|de           |392702|      2490|5010|
|el           |392702|      2490|5010|

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
```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@mariamabarham](https://github.com/mariamabarham), [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.