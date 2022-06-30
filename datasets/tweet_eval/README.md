---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- extended|other-tweet-datasets
task_categories:
- text-classification
task_ids:
- intent-classification
- multi-class-classification
- sentiment-classification
paperswithcode_id: tweeteval
pretty_name: TweetEval
train-eval-index:
- config: emotion
  task: text-classification
  task_id: multi_class_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 macro
      args:
        average: macro
    - type: f1
      name: F1 micro
      args:
        average: micro
    - type: f1
      name: F1 weighted
      args:
        average: weighted
    - type: precision
      name: Precision macro
      args:
        average: macro
    - type: precision
      name: Precision micro
      args:
        average: micro
    - type: precision
      name: Precision weighted
      args:
        average: weighted
    - type: recall
      name: Recall macro
      args:
        average: macro
    - type: recall
      name: Recall micro
      args:
        average: micro
    - type: recall
      name: Recall weighted
      args:
        average: weighted
- config: hate
  task: text-classification
  task_id: binary_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 binary
      args:
        average: binary
    - type: precision
      name: Precision macro
      args:
        average: macro
    - type: precision
      name: Precision micro
      args:
        average: micro
    - type: precision
      name: Precision weighted
      args:
        average: weighted
    - type: recall
      name: Recall macro
      args:
        average: macro
    - type: recall
      name: Recall micro
      args:
        average: micro
    - type: recall
      name: Recall weighted
      args:
        average: weighted
- config: irony
  task: text-classification
  task_id: binary_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 binary
      args:
        average: binary
    - type: precision
      name: Precision macro
      args:
        average: macro
    - type: precision
      name: Precision micro
      args:
        average: micro
    - type: precision
      name: Precision weighted
      args:
        average: weighted
    - type: recall
      name: Recall macro
      args:
        average: macro
    - type: recall
      name: Recall micro
      args:
        average: micro
    - type: recall
      name: Recall weighted
      args:
        average: weighted
- config: offensive
  task: text-classification
  task_id: binary_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 binary
      args:
        average: binary
    - type: precision
      name: Precision macro
      args:
        average: macro
    - type: precision
      name: Precision micro
      args:
        average: micro
    - type: precision
      name: Precision weighted
      args:
        average: weighted
    - type: recall
      name: Recall macro
      args:
        average: macro
    - type: recall
      name: Recall micro
      args:
        average: micro
    - type: recall
      name: Recall weighted
      args:
        average: weighted
- config: sentiment
  task: text-classification
  task_id: multi_class_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    text: text
    label: target
  metrics:
    - type: accuracy
      name: Accuracy
    - type: f1
      name: F1 macro
      args:
        average: macro
    - type: f1
      name: F1 micro
      args:
        average: micro
    - type: f1
      name: F1 weighted
      args:
        average: weighted
    - type: precision
      name: Precision macro
      args:
        average: macro
    - type: precision
      name: Precision micro
      args:
        average: micro
    - type: precision
      name: Precision weighted
      args:
        average: weighted
    - type: recall
      name: Recall macro
      args:
        average: macro
    - type: recall
      name: Recall micro
      args:
        average: micro
    - type: recall
      name: Recall weighted
      args:
        average: weighted
configs:
- emoji
- emotion
- hate
- irony
- offensive
- sentiment
- stance_abortion
- stance_atheism
- stance_climate
- stance_feminist
- stance_hillary
---

# Dataset Card for tweet_eval

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

- **Homepage:** [Needs More Information]
- **Repository:** [GitHub](https://github.com/cardiffnlp/tweeteval)
- **Paper:** [EMNLP Paper](https://arxiv.org/pdf/2010.12421.pdf)
- **Leaderboard:** [GitHub Leaderboard](https://github.com/cardiffnlp/tweeteval)
- **Point of Contact:** [Needs More Information]

### Dataset Summary

TweetEval consists of seven heterogenous tasks in Twitter, all framed as multi-class tweet classification. The tasks include - irony, hate, offensive, stance, emoji, emotion, and sentiment. All tasks have been unified into the same benchmark, with each dataset presented in the same format and with fixed training, validation and test splits.

### Supported Tasks and Leaderboards

- `text_classification`: The dataset can be trained using a SentenceClassification model from HuggingFace transformers.

### Languages

The text in the dataset is in English, as spoken by Twitter users.

## Dataset Structure

### Data Instances

An instance from `emoji` config:

```
{'label': 12, 'text': 'Sunday afternoon walking through Venice in the sun with @user ️ ️ ️ @ Abbot Kinney, Venice'}
```

An instance from `emotion` config:

```
{'label': 2, 'text': "“Worry is a down payment on a problem you may never have'. \xa0Joyce Meyer.  #motivation #leadership #worry"}
```

An instance from `hate` config:

```
{'label': 0, 'text': '@user nice new signage. Are you not concerned by Beatlemania -style hysterical crowds crongregating on you…'}
```

An instance from `irony` config:

```
{'label': 1, 'text': 'seeing ppl walking w/ crutches makes me really excited for the next 3 weeks of my life'}
```

An instance from `offensive` config:

```
{'label': 0, 'text': '@user Bono... who cares. Soon people will understand that they gain nothing from following a phony celebrity. Become a Leader of your people instead or help and support your fellow countrymen.'}
```

An instance from `sentiment` config:

```
{'label': 2, 'text': '"QT @user In the original draft of the 7th book, Remus Lupin survived the Battle of Hogwarts. #HappyBirthdayRemusLupin"'}
```

An instance from `stance_abortion` config:

```
{'label': 1, 'text': 'we remind ourselves that love means to be willing to give until it hurts - Mother Teresa'}
```

An instance from `stance_atheism` config:

```
{'label': 1, 'text': '@user Bless Almighty God, Almighty Holy Spirit and the Messiah. #SemST'}
```

An instance from `stance_climate` config:

```
{'label': 0, 'text': 'Why Is The Pope Upset?  via @user #UnzippedTruth #PopeFrancis #SemST'}
```

An instance from `stance_feminist` config:

```
{'label': 1, 'text': "@user @user is the UK's answer to @user and @user  #GamerGate #SemST"}
```

An instance from `stance_hillary` config:

```
{'label': 1, 'text': "If a man demanded staff to get him an ice tea he'd be called a sexists elitist pig.. Oink oink #Hillary #SemST"}
```

### Data Fields
For `emoji` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: ❤

    `1`: 😍

    `2`: 😂

    `3`: 💕

    `4`: 🔥

    `5`: 😊

    `6`: 😎

    `7`: ✨

    `8`: 💙

    `9`: 😘

    `10`: 📷

    `11`: 🇺🇸

    `12`: ☀

    `13`: 💜

    `14`: 😉

    `15`: 💯

    `16`: 😁

    `17`: 🎄

    `18`: 📸

    `19`: 😜

For `emotion` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: anger

    `1`: joy

    `2`: optimism

    `3`: sadness

For `hate` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: non-hate

    `1`: hate

For `irony` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: non_irony

    `1`: irony

For `offensive` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: non-offensive

    `1`: offensive

For `sentiment` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: negative

    `1`: neutral

    `2`: positive

For `stance_abortion` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: none

    `1`: against

    `2`: favor

For `stance_atheism` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: none

    `1`: against

    `2`: favor

For `stance_climate` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: none

    `1`: against

    `2`: favor

For `stance_feminist` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: none

    `1`: against

    `2`: favor

For `stance_hillary` config:

- `text`: a `string` feature containing the tweet.

- `label`: an `int` classification label with the following mapping:

    `0`: none

    `1`: against

    `2`: favor



### Data Splits

| name            | train | validation | test  |
| --------------- | ----- | ---------- | ----- |
| emoji           | 45000 | 5000       | 50000 |
| emotion         | 3257  | 374        | 1421  |
| hate            | 9000  | 1000       | 2970  |
| irony           | 2862  | 955        | 784   |
| offensive       | 11916 | 1324       | 860   |
| sentiment       | 45615 | 2000       | 12284 |
| stance_abortion | 587   | 66         | 280   |
| stance_atheism  | 461   | 52         | 220   |
| stance_climate  | 355   | 40         | 169   |
| stance_feminist | 597   | 67         | 285   |
| stance_hillary  | 620   | 69         | 295   |

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

Francesco Barbieri, Jose Camacho-Collados, Luis Espiinosa-Anke and Leonardo Neves through Cardiff NLP.

### Licensing Information

This is not a single dataset, therefore each subset has its own license (the collection itself does not have additional restrictions).

All of the datasets require complying with Twitter [Terms Of Service](https://twitter.com/tos) and Twitter API [Terms Of Service](https://developer.twitter.com/en/developer-terms/agreement-and-policy)

Additionally the license are:
- emoji: Undefined
- emotion(EmoInt): Undefined
- hate (HateEval): Need permission [here](http://hatespeech.di.unito.it/hateval.html)
- irony: Undefined
- Offensive: Undefined
- Sentiment: [Creative Commons Attribution 3.0 Unported License](https://groups.google.com/g/semevaltweet/c/k5DDcvVb_Vo/m/zEOdECFyBQAJ)
- Stance: Undefined


### Citation Information

```
@inproceedings{barbieri2020tweeteval,
title={{TweetEval:Unified Benchmark and Comparative Evaluation for Tweet Classification}},
author={Barbieri, Francesco and Camacho-Collados, Jose and Espinosa-Anke, Luis and Neves, Leonardo},
booktitle={Proceedings of Findings of EMNLP},
year={2020}
}
```

If you use any of the TweetEval datasets, please cite their original publications:

#### Emotion Recognition:
```
@inproceedings{mohammad2018semeval,
  title={Semeval-2018 task 1: Affect in tweets},
  author={Mohammad, Saif and Bravo-Marquez, Felipe and Salameh, Mohammad and Kiritchenko, Svetlana},
  booktitle={Proceedings of the 12th international workshop on semantic evaluation},
  pages={1--17},
  year={2018}
}

```
#### Emoji Prediction:
```
@inproceedings{barbieri2018semeval,
  title={Semeval 2018 task 2: Multilingual emoji prediction},
  author={Barbieri, Francesco and Camacho-Collados, Jose and Ronzano, Francesco and Espinosa-Anke, Luis and
    Ballesteros, Miguel and Basile, Valerio and Patti, Viviana and Saggion, Horacio},
  booktitle={Proceedings of The 12th International Workshop on Semantic Evaluation},
  pages={24--33},
  year={2018}
}
```

#### Irony Detection:
```
@inproceedings{van2018semeval,
  title={Semeval-2018 task 3: Irony detection in english tweets},
  author={Van Hee, Cynthia and Lefever, Els and Hoste, V{\'e}ronique},
  booktitle={Proceedings of The 12th International Workshop on Semantic Evaluation},
  pages={39--50},
  year={2018}
}
```

#### Hate Speech Detection:
```
@inproceedings{basile-etal-2019-semeval,
    title = "{S}em{E}val-2019 Task 5: Multilingual Detection of Hate Speech Against Immigrants and Women in {T}witter",
    author = "Basile, Valerio  and Bosco, Cristina  and Fersini, Elisabetta  and Nozza, Debora and Patti, Viviana and
      Rangel Pardo, Francisco Manuel  and Rosso, Paolo  and Sanguinetti, Manuela",
    booktitle = "Proceedings of the 13th International Workshop on Semantic Evaluation",
    year = "2019",
    address = "Minneapolis, Minnesota, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/S19-2007",
    doi = "10.18653/v1/S19-2007",
    pages = "54--63"
}
```
#### Offensive Language Identification:
```
@inproceedings{zampieri2019semeval,
  title={SemEval-2019 Task 6: Identifying and Categorizing Offensive Language in Social Media (OffensEval)},
  author={Zampieri, Marcos and Malmasi, Shervin and Nakov, Preslav and Rosenthal, Sara and Farra, Noura and Kumar, Ritesh},
  booktitle={Proceedings of the 13th International Workshop on Semantic Evaluation},
  pages={75--86},
  year={2019}
}
```

#### Sentiment Analysis:
```
@inproceedings{rosenthal2017semeval,
  title={SemEval-2017 task 4: Sentiment analysis in Twitter},
  author={Rosenthal, Sara and Farra, Noura and Nakov, Preslav},
  booktitle={Proceedings of the 11th international workshop on semantic evaluation (SemEval-2017)},
  pages={502--518},
  year={2017}
}
```

#### Stance Detection:
```
@inproceedings{mohammad2016semeval,
  title={Semeval-2016 task 6: Detecting stance in tweets},
  author={Mohammad, Saif and Kiritchenko, Svetlana and Sobhani, Parinaz and Zhu, Xiaodan and Cherry, Colin},
  booktitle={Proceedings of the 10th International Workshop on Semantic Evaluation (SemEval-2016)},
  pages={31--41},
  year={2016}
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) and [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.
