---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- extractive-qa
- open-domain-qa
---

# Dataset Card for adversarialQA

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

- **Homepage:** [adversarialQA homepage](https://adversarialqa.github.io/)
- **Repository:** [adversarialQA repository](https://github.com/maxbartolo/adversarialQA)
- **Paper:** [Beat the AI: Investigating Adversarial Human Annotation for Reading Comprehension](https://arxiv.org/abs/2002.00293)
- **Leaderboard:** [Dynabench QA Round 1 Leaderboard](https://dynabench.org/tasks/2#overall)
- **Point of Contact:** [Max Bartolo](max.bartolo@ucl.ac.uk)

### Dataset Summary

We have created three new Reading Comprehension datasets constructed using an adversarial model-in-the-loop.

We use three different models; BiDAF (Seo et al., 2016), BERTLarge (Devlin et al., 2018), and RoBERTaLarge (Liu et al., 2019) in the annotation loop and construct three datasets; D(BiDAF), D(BERT), and D(RoBERTa), each with 10,000 training examples, 1,000 validation, and 1,000 test examples.

The adversarial human annotation paradigm ensures that these datasets consist of questions that current state-of-the-art models (at least the ones used as adversaries in the annotation loop) find challenging. The three AdversarialQA round 1 datasets provide a training and evaluation resource for such methods.

### Supported Tasks and Leaderboards

`extractive-qa`: The dataset can be used to train a model for Extractive Question Answering, which consists in selecting the answer to a question from a passage. Success on this task is typically measured by achieving a high word-overlap [F1 score](https://huggingface.co/metrics/f1). The [RoBERTa-Large](https://huggingface.co/roberta-large) model trained on all the data combined with [SQuAD](https://arxiv.org/abs/1606.05250) currently achieves 64.35% F1. This task has an active leaderboard and is available as round 1 of the QA task on [Dynabench](https://dynabench.org/tasks/2#overall) and ranks models based on F1 score.

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

Data is provided in the same format as SQuAD 1.1. An example is shown below:

```
{
  "data": [
    {
      "title": "Oxygen",
      "paragraphs": [
        {
          "context": "Among the most important classes of organic compounds that contain oxygen are (where \"R\" is an organic group): alcohols (R-OH); ethers (R-O-R); ketones (R-CO-R); aldehydes (R-CO-H); carboxylic acids (R-COOH); esters (R-COO-R); acid anhydrides (R-CO-O-CO-R); and amides (R-C(O)-NR2). There are many important organic solvents that contain oxygen, including: acetone, methanol, ethanol, isopropanol, furan, THF, diethyl ether, dioxane, ethyl acetate, DMF, DMSO, acetic acid, and formic acid. Acetone ((CH3)2CO) and phenol (C6H5OH) are used as feeder materials in the synthesis of many different substances. Other important organic compounds that contain oxygen are: glycerol, formaldehyde, glutaraldehyde, citric acid, acetic anhydride, and acetamide. Epoxides are ethers in which the oxygen atom is part of a ring of three atoms.",
          "qas": [
            {
              "id": "22bbe104aa72aa9b511dd53237deb11afa14d6e3",
              "question": "In addition to having oxygen, what do alcohols, ethers and esters have in common, according to the article?",
              "answers": [
                {
                  "answer_start": 36,
                  "text": "organic compounds"
                }
              ]
            },
            {
              "id": "4240a8e708c703796347a3702cf1463eed05584a",
              "question": "What letter does the abbreviation for acid anhydrides both begin and end in?",
              "answers": [
                {
                  "answer_start": 244,
                  "text": "R"
                }
              ]
            },
            {
              "id": "0681a0a5ec852ec6920d6a30f7ef65dced493366",
              "question": "Which of the organic compounds, in the article, contains nitrogen?",
              "answers": [
                {
                  "answer_start": 262,
                  "text": "amides"
                }
              ]
            },
            {
              "id": "2990efe1a56ccf81938fa5e18104f7d3803069fb",
              "question": "Which of the important classes of organic compounds, in the article, has a number in its abbreviation?",
              "answers": [
                {
                  "answer_start": 262,
                  "text": "amides"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Data Fields

- title: the title of the Wikipedia page from which the context is sourced
- context: the context/passage
- id: a string identifier for each question
- answers: a list of all provided answers (one per question in our case, but multiple may exist in SQuAD) with an `answer_start` field which is the character index of the start of the answer span, and a `text` field which is the answer text

### Data Splits

The dataset is composed of three different datasets constructed using different models in the loop: BiDAF, BERT-Large, and RoBERTa-Large. Each of these has 10,000 training examples, 1,000 validation examples, and 1,000 test examples for a total of 30,000/3,000/3,000 train/validation/test examples.

## Dataset Creation

### Curation Rationale

This dataset was collected to provide a more challenging and diverse Reading Comprehension dataset to state-of-the-art models.

### Source Data

#### Initial Data Collection and Normalization

The source passages are from Wikipedia and are the same as those used in [SQuAD v1.1](https://arxiv.org/abs/1606.05250).

#### Who are the source language producers?

The source language produces are Wikipedia editors for the passages, and human annotators on Mechanical Turk for the questions.

### Annotations

#### Annotation process

The dataset is collected through an adversarial human annotation process which pairs a human annotator and a reading comprehension model in an interactive setting. The human is presented with a passage for which they write a question and highlight the correct answer. The model then tries to answer the question, and, if it fails to answer correctly, the human wins. Otherwise, the human modifies or re-writes their question until the successfully fool the model.

#### Who are the annotators?

The annotators are from Amazon Mechanical Turk, geographically restricted the the USA, UK and Canada, having previously successfully completed at least 1,000 HITs, and having a HIT approval rate greater than 98%. Crowdworkers undergo intensive training and qualification prior to annotation.

### Personal and Sensitive Information

No annotator identifying details are provided.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop better question answering systems.

A system that succeeds at the supported task would be able to provide an accurate extractive answer from a short passage. This dataset is to be seen as a test bed for questions which contemporary state-of-the-art models struggle to answer correctly, thus often requiring more complex comprehension abilities than say detecting phrases explicitly mentioned in the passage with high overlap to the question.

It should be noted, however, that the the source passages are both domain-restricted and linguistically specific, and that provided questions and answers do not constitute any particular social application.


### Discussion of Biases

The dataset may exhibit various biases in terms of the source passage selection, annotated questions and answers, as well as algorithmic biases resulting from the adversarial annotation protocol.

### Other Known Limitations

N/a

## Additional Information

### Dataset Curators

This dataset was initially created by Max Bartolo, Alastair Roberts, Johannes Welbl, Sebastian Riedel, and Pontus Stenetorp, during work carried out at University College London (UCL).

### Licensing Information

This dataset is distributed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).

### Citation Information

```
@article{bartolo2020beat,
    author = {Bartolo, Max and Roberts, Alastair and Welbl, Johannes and Riedel, Sebastian and Stenetorp, Pontus},
    title = {Beat the AI: Investigating Adversarial Human Annotation for Reading Comprehension},
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {8},
    number = {},
    pages = {662-678},
    year = {2020},
    doi = {10.1162/tacl\_a\_00338},
    URL = { https://doi.org/10.1162/tacl_a_00338 },
    eprint = { https://doi.org/10.1162/tacl_a_00338 },
    abstract = { Innovations in annotation methodology have been a catalyst for Reading Comprehension (RC) datasets and models. One recent trend to challenge current RC models is to involve a model in the annotation process: Humans create questions adversarially, such that the model fails to answer them correctly. In this work we investigate this annotation methodology and apply it in three different settings, collecting a total of 36,000 samples with progressively stronger models in the annotation loop. This allows us to explore questions such as the reproducibility of the adversarial effect, transfer from data collected with varying model-in-the-loop strengths, and generalization to data collected without a model. We find that training on adversarially collected samples leads to strong generalization to non-adversarially collected datasets, yet with progressive performance deterioration with increasingly stronger models-in-the-loop. Furthermore, we find that stronger models can still learn from datasets collected with substantially weaker models-in-the-loop. When trained on data collected with a BiDAF model in the loop, RoBERTa achieves 39.9F1 on questions that it cannot answer when trained on SQuAD—only marginally lower than when trained on data collected using RoBERTa itself (41.0F1). }
}
```
### Contributions

Thanks to [@maxbartolo](https://github.com/maxbartolo) for adding this dataset.