---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- ur
license:
- mit
multilinguality:
- monolingual
pretty_name: roman_urdu_hate_speech
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
- text-classification-other-binary classification
---

# Dataset Card for roman_urdu_hate_speech

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

- **Homepage:** [roman_urdu_hate_speech homepage](https://aclanthology.org/2020.emnlp-main.197/)
- **Repository:** [roman_urdu_hate_speech repository](https://github.com/haroonshakeel/roman_urdu_hate_speech)
- **Paper:** [Hate-Speech and Offensive Language Detection in Roman Urdu](https://aclanthology.org/2020.emnlp-main.197.pdf)
- **Leaderboard:** [N/A]
- **Point of Contact:** [M. Haroon Shakeel](mailto:m.shakeel@lums.edu.pk)

### Dataset Summary

The Roman Urdu Hate-Speech and Offensive Language Detection (RUHSOLD) dataset is a Roman Urdu dataset of tweets annotated by experts in the relevant language. The authors develop the gold-standard for two sub-tasks. First sub-task is based on binary labels of Hate-Offensive content and Normal content (i.e., inoffensive language). These labels are self-explanatory. The authors refer to this sub-task as coarse-grained classification. Second sub-task defines Hate-Offensive content with four labels at a granular level. These labels are the most relevant for the demographic of users who converse in RU and are defined in related literature. The authors refer to this sub-task as fine-grained classification. The objective behind creating two gold-standards is to enable the researchers to evaluate the hate speech detection approaches on both easier (coarse-grained) and challenging (fine-grained) scenarios.  

### Supported Tasks and Leaderboards

- 'multi-class-classification', 'text-classification-other-binary classification': The dataset can be used for both multi class classification as well as for binary classification as it contains both coarse grained and fine grained labels.

### Languages

The text of this dataset is Roman Urdu. The associated BCP-47 code is 'ur'.

## Dataset Structure

### Data Instances

The dataset consists of two parts divided as a set of two types, Coarse grained examples and Fine Grained examples. The difference is that in the coarse grained example the tweets are labelled as abusive or normal whereas in the fine grained version there are several classes of hate associated with a tweet.

For the Coarse grained segment of the dataset the label mapping is:-
Task 1: Coarse-grained Classification Labels
0:  Abusive/Offensive
1:  Normal

Whereas for the Fine Grained segment of the dataset the label mapping is:-
Task 2: Fine-grained Classification Labels
0:  Abusive/Offensive
1:  Normal
2:  Religious Hate
3:  Sexism
4:  Profane/Untargeted

An example from Roman Urdu Hate Speech looks as follows:
```
{
  'tweet': 'there are some yahodi daboo like imran chore zakat khore'
  'label': 0
}
```

### Data Fields

-tweet:a string denoting the tweet which has been selected by using a random sampling from a tweet base of 50000 tweets to select 10000 tweets and annotated for the dataset.

-label:An annotation manually labeled by three independent annotators, during the annotation process, all conflicts are resolved by a majority vote among three annotators. 

### Data Splits

The data of each of the segments, Coarse Grained and Fine Grained is further split into training, validation and test set. The data  is split in train, test, and validation sets with 70,20,10 split ratio using stratification based on fine-grained labels.

The use of stratified sampling is deemed necessary to preserve the same labels ratio across all splits. 

The Final split sizes are as follows:

Train Valid Test
7209 2003 801


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

The dataset was created by Hammad Rizwan, Muhammad Haroon Shakeel, Asim Karim during work done at Department of Computer Science, Lahore University of Management Sciences (LUMS), Lahore, Pakistan.

### Licensing Information

The licensing status of the dataset hinges on the legal status of the [Roman Urdu Hate Speech Dataset Repository](https://github.com/haroonshakeel/roman_urdu_hate_speech) which is under MIT License.

### Citation Information

```bibtex
@inproceedings{rizwan2020hate,
  title={Hate-speech and offensive language detection in roman Urdu},
  author={Rizwan, Hammad and Shakeel, Muhammad Haroon and Karim, Asim},
  booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  pages={2512--2522},
  year={2020}
}
```

### Contributions

Thanks to [@bp-high](https://github.com/bp-high), for adding this dataset.