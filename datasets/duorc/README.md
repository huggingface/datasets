---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  ParaphraseRC:
  - 100K<n<1M
  SelfRC:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- abstractive-qa
- extractive-qa
---

# Dataset Card for duorc

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

- **Homepage:** [DuoRC](https://duorc.github.io/)
- **Repository:** [GitHub](https://github.com/duorc/duorc)
- **Paper:** [arXiv](https://arxiv.org/abs/1804.07927)
- **Leaderboard:** [DuoRC Leaderboard](https://duorc.github.io/#leaderboard)
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The DuoRC dataset is an English language dataset of questions and answers gathered from crowdsourced AMT workers on Wikipedia and IMDb movie plots. The workers were given freedom to pick answer from the plots or synthesize their own answers. It contains two sub-datasets - SelfRC and ParaphraseRC. SelfRC dataset is built on Wikipedia movie plots solely. ParaphraseRC has questions written from Wikipedia movie plots and the answers are given based on corresponding IMDb movie plots.

### Supported Tasks and Leaderboards

- `abstractive-qa` : The dataset can be used to train a model for Abstractive Question Answering. An abstractive question answering model is presented with a passage and a question and is expected to generate a multi-word answer. The model performance is measured by exact-match and F1 score, similar to [SQuAD V1.1](https://huggingface.co/metrics/squad) or [SQuAD V2](https://huggingface.co/metrics/squad_v2).   A [BART-based model](https://huggingface.co/yjernite/bart_eli5) with a [dense retriever](https://huggingface.co/yjernite/retribert-base-uncased) may be used for this task.

- `extractive-qa`: The dataset can be used to train a model for Extractive Question Answering. An extractive question answering model is presented with a passage and a question and is expected to predict the start and end of the answer span in the passage. The model performance is measured by exact-match and F1 score, similar to [SQuAD V1.1](https://huggingface.co/metrics/squad) or [SQuAD V2](https://huggingface.co/metrics/squad_v2).  [BertForQuestionAnswering](https://huggingface.co/transformers/model_doc/bert.html#bertforquestionanswering) or any other similar model may be used for this task.

### Languages

The text in the dataset is in English, as spoken by Wikipedia writers for movie plots.  The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

```
{'answers': ['They arrived by train.'], 'no_answer': False, 'plot': "200 years in the future, Mars has been colonized by a high-tech company.\nMelanie Ballard (Natasha Henstridge) arrives by train to a Mars mining camp which has cut all communication links with the company headquarters. She's not alone, as she is with a group of fellow police officers. They find the mining camp deserted except for a person in the prison, Desolation Williams (Ice Cube), who seems to laugh about them because they are all going to die. They were supposed to take Desolation to headquarters, but decide to explore first to find out what happened.They find a man inside an encapsulated mining car, who tells them not to open it. However, they do and he tries to kill them. One of the cops witnesses strange men with deep scarred and heavily tattooed faces killing the remaining survivors. The cops realise they need to leave the place fast.Desolation explains that the miners opened a kind of Martian construction in the soil which unleashed red dust. Those who breathed that dust became violent psychopaths who started to build weapons and kill the uninfected. They changed genetically, becoming distorted but much stronger.The cops and Desolation leave the prison with difficulty, and devise a plan to kill all the genetically modified ex-miners on the way out. However, the plan goes awry, and only Melanie and Desolation reach headquarters alive. Melanie realises that her bosses won't ever believe her. However, the red dust eventually arrives to headquarters, and Melanie and Desolation need to fight once again.", 'plot_id': '/m/03vyhn', 'question': 'How did the police arrive at the Mars mining camp?', 'question_id': 'b440de7d-9c3f-841c-eaec-a14bdff950d1', 'title': 'Ghosts of Mars'}
```

### Data Fields

- `plot_id`: a `string` feature containing the movie plot ID.
- `plot`: a `string` feature containing the movie plot text.
- `title`: a `string` feature containing the movie title.
- `question_id`: a `string` feature containing the question ID.
- `question`: a `string` feature containing the question text.
- `answers`: a `list` of `string` features containing list of answers.
- `no_answer`: a `bool` feature informing whether the question has no answer or not.


### Data Splits

The data is split into a training, dev and test set in such a way that the resulting sets contain 70%, 15%, and 15% of the total QA pairs and no QA pairs for any movie seen in train are included in the test set. The final split sizes are as follows:

Name Train Dec Test
SelfRC 60721 12961 12599
ParaphraseRC 69524 15591 15857
## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

Wikipedia and IMDb movie plots

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

For SelfRC, the annotators were allowed to mark an answer span in the plot or synthesize their own answers after reading Wikipedia movie plots. 
For ParaphraseRC, questions from the Wikipedia movie plots from SelfRC were used and the annotators were asked to answer based on IMDb movie plots.

#### Who are the annotators?

Amazon Mechanical Turk Workers

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

The dataset was intially created by Amrita Saha, Rahul Aralikatte, Mitesh M. Khapra, and Karthik Sankaranarayanan in a collaborated work between IIT Madras and IBM Research.

### Licensing Information

[MIT License](https://github.com/duorc/duorc/blob/master/LICENSE)

### Citation Information

```
@inproceedings{DuoRC,
author = { Amrita Saha and Rahul Aralikatte and Mitesh M. Khapra and Karthik Sankaranarayanan},
title = {{DuoRC: Towards Complex Language Understanding with Paraphrased Reading Comprehension}},
booktitle = {Meeting of the Association for Computational Linguistics (ACL)},
year = {2018}
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.