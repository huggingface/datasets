---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found
languages:
- ko
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
paperswithcode_id: korean-hatespeech-dataset
---

# Dataset Card for [Dataset Name]

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

- **Homepage: [Korean HateSpeech Dataset](https://github.com/kocohub/korean-hate-speech)**
- **Repository: [Korean HateSpeech Dataset](https://github.com/kocohub/korean-hate-speech)**
- **Paper: [BEEP! Korean Corpus of Online News Comments for Toxic Speech Detection](https://arxiv.org/abs/2005.12503)**
- **Point of Contact: [Steven Liu](stevhliu@gmail.com)**

### Dataset Summary

The Korean HateSpeech Dataset is a dataset of 8367 human-labeled entertainment news comments from a popular Korean news aggregation platform. Each comment was evaluated for either social bias (labels: `gender`, `others` `none`), hate speech (labels: `hate`, `offensive`, `none`) or gender bias (labels: `True`, `False`). The dataset was created to support the identification of toxic comments on online platforms where users can remain anonymous. 

### Supported Tasks and Leaderboards

* `multi-label classification`: The dataset can be used to train a model for hate speech detection. A BERT model can be presented with a Korean entertainment news comment and be asked to label whether it contains social bias, gender bias and hate speech. Users can participate in a Kaggle leaderboard [here](https://www.kaggle.com/c/korean-hate-speech-detection/overview).

### Languages

The text in the dataset is in Korean and the associated is BCP-47 code is `ko-KR`.	

## Dataset Structure

### Data Instances

An example data instance contains a `comments` containing the text of the news comment and then labels for each of the following fields: `contain_gender_bias`, `bias` and `hate`.

```python
{'comments':'설마 ㅈ 현정 작가 아니지??'
 'contain_gender_bias': 'True',
 'bias': 'gender',
 'hate': 'hate'
}
```

### Data Fields

* `comments`: text from the Korean news comment
* `contain_gender_bias`: a binary `True`/`False` label for the presence of gender bias
* `bias`: determines the type of social bias, which can be:
  * `gender`: if the text includes bias for gender role, sexual orientation, sexual identity, and any thoughts on gender-related acts
  * `others`: other kinds of factors that are considered not gender-related but social bias, including race, background, nationality, ethnic group, political stance, skin color, religion, handicaps, age, appearance, richness, occupations, the absence of military service experience
  * `none`: a comment that does not incorporate the bias
* `hate`: determines how aggressive the comment is, which can be:
  * `hate`: if the text is defined as an expression that display aggressive stances towards individuals/groups with certain characteristics (gender role, sexual orientation, sexual identity, any thoughts on gender-related acts, race, background, nationality, ethnic group, political stance, skin color, religion, handicaps, age, appearance, richness, occupations, the absence of military service experience, etc.)
  * `offensive`: if the text contains rude or aggressive contents, can emit sarcasm through rhetorical question or irony, encompass an unethical expression or conveys unidentified rumors
  * `none`: a comment that does not incorporate hate

### Data Splits

The data is split into a training and development (test) set. It contains 8371 annotated comments that are split into 7896 comments in the training set and 471 comments in the test set.

## Dataset Creation

### Curation Rationale

The dataset was created to provide the first human-labeled Korean corpus for toxic speech detection from a Korean online entertainment news aggregator. Recently, two young Korean celebrities suffered from a series of tragic incidents that led to two major Korean web portals to close the comments section on their platform. However, this only serves as a temporary solution, and the fundamental issue has not been solved yet. This dataset hopes to improve Korean hate speech detection.  

### Source Data

#### Initial Data Collection and Normalization

A total of 10.4 million comments were collected from an online Korean entertainment news aggregator between Jan. 1, 2018 and Feb. 29, 2020. 1,580 articles were drawn using stratified sampling and the top 20 comments were extracted ranked in order of their Wilson score on the downvote for each article. Duplicate comments, single token comments and comments with more than 100 characters were removed (because they could convey various opinions). From here, 10K comments were randomly chosen for annotation.

#### Who are the source language producers?

The language producers are users of the Korean online news platform between 2018 and 2020. 

### Annotations

#### Annotation process

Each comment was assigned to three random annotators to assign a majority decision. For more ambiguous comments, annotators were allowed to skip the comment. See Appendix A in the [paper](https://arxiv.org/pdf/2005.12503.pdf) for more detailed guidelines.

#### Who are the annotators?

Annotation was performed by 32 annotators, consisting of 29 annotators from the crowdsourcing platform DeepNatural AI and three NLP researchers. 

### Personal and Sensitive Information

[N/A]

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to tackle the social issue of users creating toxic comments on online platforms. This dataset aims to improve detection of toxic comments online.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset is curated by Jihyung Moon, Won Ik Cho and Junbum Lee.

### Licensing Information

[N/A]

### Citation Information

```
@inproceedings
{moon-et-al-2020-beep
    title = "{BEEP}! {K}orean Corpus of Online News Comments for Toxic Speech Detection",
    author = "Moon, Jihyung  and
      Cho, Won Ik  and
      Lee, Junbum",
    booktitle = "Proceedings of the Eighth International Workshop on Natural Language Processing for Social Media",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.socialnlp-1.4",
    pages = "25--31",
    abstract = "Toxic comments in online platforms are an unavoidable social issue under the cloak of anonymity. Hate speech detection has been actively done for languages such as English, German, or Italian, where manually labeled corpus has been released. In this work, we first present 9.4K manually labeled entertainment news comments for identifying Korean toxic speech, collected from a widely used online news platform in Korea. The comments are annotated regarding social bias and hate speech since both aspects are correlated. The inter-annotator agreement Krippendorff{'}s alpha score is 0.492 and 0.496, respectively. We provide benchmarks using CharCNN, BiLSTM, and BERT, where BERT achieves the highest score on all tasks. The models generally display better performance on bias identification, since the hate speech detection is a more subjective issue. Additionally, when BERT is trained with bias label for hate speech detection, the prediction score increases, implying that bias and hate are intertwined. We make our dataset publicly available and open competitions with the corpus and benchmarks.",
}
```

### Contributions

Thanks to [@stevhliu](https://github.com/stevhliu) for adding this dataset.