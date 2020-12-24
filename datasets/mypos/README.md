---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- my
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
---

# Dataset Card for mypos

## Table of Contents
- [Dataset Card for mypos](#dataset-card-for-mypos)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** [myPOS homepage](https://github.com/ye-kyaw-thu/myPOS)
- **Repository:** [myPOS repository](https://github.com/hungluumfc/burmese-data/tree/main/myPOS)
- **Paper:** [Comparison of Six POS Tagging Methods on 10K Sentences Myanmar Language (Burmese) POS Tagged Corpus](https://github.com/ye-kyaw-thu/myPOS/blob/master/CICLING2017/10K-POS-tagging-CICLing2017.pdf)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** yktnlp@gmail.com, hunglv54.vnu@gmail.com

### Dataset Summary

myPOS Corpus (Myanmar Part-of-Speech Corpus) for Myanmar language NLP Research and Developments. The dataset was originaly published online by [Ye Kyaw Thu](https://sites.google.com/site/yekyawthunlp/) which contains the training set, close test set (subset of training set) and open test set. The dataset provided in this repo contains the training set (equivalent to training set in original paper), test set (equipvalent of open test set in original paper), and dev set (subset of test set).

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text in the dataset is in Burmese collected from Wikipedia that include various area such as economics, history, news, politics and philosophy. 
The associated BCP-47 code is `my`

## Dataset Structure

### Data Instances

{'id': '0', 'pos_tags': [6, 6, 9, 6, 3, 6, 8, 9, 14, 8, 9, 8, 14, 8, 9, 11], 'tokens': ['ယခု', 'လ', 'တွင်', 'ပျားရည်', 'နှင့်', 'ပျားဖယောင်း', 'များ', 'ကို', 'စုဆောင်း', 'ကြ', 'သည်', 'ဟု', 'ခန့်မှန်း', 'နိုင်', 'သည်', '။']}

### Data Fields

- `id`: a `string` feature.
- `tokens`: a `list` of `string` features.
- `pos_tags`: a `list` of classification labels, with possible values including `abb`, `adj`, `adv`, `conj`, `fw`.

### Data Splits

[Needs More Information]

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

[Needs More Information]

### Citation Information

Khin War War Htike, Ye Kyaw Thu, Zuping Zhang, Win Pa Pa, Yoshinori Sagisaka and Naoto Iwahashi, "Comparison of Six POS Tagging Methods on 10K Sentences Myanmar Language (Burmese) POS Tagged Corpus", at 18th International Conference on Computational Linguistics and Intelligent Text Processing (CICLing 2017), April 17~23, 2017, Budapest, Hungary
