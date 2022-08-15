---
annotations_creators:
- other
language_creators:
- other
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- acceptability-classification
- natural-language-inference
- semantic-similarity-scoring
- sentiment-classification
- text-classification-other-coreference-nli
- text-classification-other-paraphrase-identification
- text-classification-other-qa-nli
- text-scoring
paperswithcode_id: glue
pretty_name: GLUE (General Language Understanding Evaluation benchmark)
train-eval-index:
- config: sst2
  task: text-classification
  task_id: multi_class_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    sentence: text
    label: target
  metrics:
    - type: glue
      name: GLUE
      config:
        sst2
- config: cola
  task: text-classification
  task_id: multi_class_classification
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    sentence: text
    label: target
  metrics:
    - type: glue
      name: GLUE
      config:
        cola
configs:
- ax
- cola
- mnli
- mnli_matched
- mnli_mismatched
- mrpc
- qnli
- qqp
- rte
- sst2
- stsb
- wnli
---

# Dataset Card for GLUE

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

- **Homepage:** [https://nyu-mll.github.io/CoLA/](https://nyu-mll.github.io/CoLA/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 955.33 MB
- **Size of the generated dataset:** 229.68 MB
- **Total amount of disk used:** 1185.01 MB

### Dataset Summary

GLUE, the General Language Understanding Evaluation benchmark (https://gluebenchmark.com/) is a collection of resources for training, evaluating, and analyzing natural language understanding systems.

### Supported Tasks and Leaderboards

The leaderboard for the GLUE benchmark can be found [at this address](https://gluebenchmark.com/). It comprises the following tasks:

#### ax

A manually-curated evaluation dataset for fine-grained analysis of system performance on a broad range of linguistic phenomena. This dataset evaluates sentence understanding through Natural Language Inference (NLI) problems. Use a model trained on MulitNLI to produce predictions for this dataset.

#### cola

The Corpus of Linguistic Acceptability consists of English acceptability judgments drawn from books and journal articles on linguistic theory. Each example is a sequence of words annotated with whether it is a grammatical English sentence.

#### mnli

The Multi-Genre Natural Language Inference Corpus is a crowdsourced collection of sentence pairs with textual entailment annotations. Given a premise sentence and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis (entailment), contradicts the hypothesis (contradiction), or neither (neutral). The premise sentences are gathered from ten different sources, including transcribed speech, fiction, and government reports. The authors of the benchmark use the standard test set, for which they obtained private labels from the RTE authors, and evaluate on both the matched (in-domain) and mismatched (cross-domain) section. They also uses and recommend the SNLI corpus as 550k examples of auxiliary training data.

#### mnli_matched

The matched validation and test splits from MNLI. See the "mnli" BuilderConfig for additional information.

#### mnli_mismatched

The mismatched validation and test splits from MNLI. See the "mnli" BuilderConfig for additional information.

#### mrpc

The Microsoft Research Paraphrase Corpus (Dolan & Brockett, 2005) is a corpus of sentence pairs automatically extracted from online news sources, with human annotations for whether the sentences in the pair are semantically equivalent.

#### qnli

The Stanford Question Answering Dataset is a question-answering dataset consisting of question-paragraph pairs, where one of the sentences in the paragraph (drawn from Wikipedia) contains the answer to the corresponding question (written by an annotator). The authors of the benchmark convert the task into sentence pair classification by forming a pair between each question and each sentence in the corresponding context, and filtering out pairs with low lexical overlap between the question and the context sentence. The task is to determine whether the context sentence contains the answer to the question. This modified version of the original task removes the requirement that the model select the exact answer, but also removes the simplifying assumptions that the answer is always present in the input and that lexical overlap is a reliable cue.

#### qqp

The Quora Question Pairs2 dataset is a collection of question pairs from the community question-answering website Quora. The task is to determine whether a pair of questions are semantically equivalent.

#### rte

The Recognizing Textual Entailment (RTE) datasets come from a series of annual textual entailment challenges. The authors of the benchmark combined the data from RTE1 (Dagan et al., 2006), RTE2 (Bar Haim et al., 2006), RTE3 (Giampiccolo et al., 2007), and RTE5 (Bentivogli et al., 2009). Examples are constructed based on news and Wikipedia text. The authors of the benchmark convert all datasets to a two-class split, where for three-class datasets they collapse neutral and contradiction into not entailment, for consistency.

#### sst2

The Stanford Sentiment Treebank consists of sentences from movie reviews and human annotations of their sentiment. The task is to predict the sentiment of a given sentence. It uses the two-way (positive/negative) class split, with only sentence-level labels.

#### stsb

The Semantic Textual Similarity Benchmark (Cer et al., 2017) is a collection of sentence pairs drawn from news headlines, video and image captions, and natural language inference data. Each pair is human-annotated with a similarity score from 1 to 5.

#### wnli

The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task in which a system must read a sentence with a pronoun and select the referent of that pronoun from a list of choices. The examples are manually constructed to foil simple statistical methods: Each one is contingent on contextual information provided by a single word or phrase in the sentence. To convert the problem into sentence pair classification, the authors of the benchmark construct sentence pairs by replacing the ambiguous pronoun with each possible referent. The task is to predict if the sentence with the pronoun substituted is entailed by the original sentence. They use a small evaluation set consisting of new examples derived from fiction books that was shared privately by the authors of the original corpus. While the included training set is balanced between two classes, the test set is imbalanced between them (65% not entailment). Also, due to a data quirk, the development set is adversarial: hypotheses are sometimes shared between training and development examples, so if a model memorizes the training examples, they will predict the wrong label on corresponding development set example. As with QNLI, each example is evaluated separately, so there is not a systematic correspondence between a model's score on this task and its score on the unconverted original task. The authors of the benchmark call converted dataset WNLI (Winograd NLI).

### Languages

The language data in GLUE is in English (BCP-47 `en`)

## Dataset Structure

### Data Instances

#### ax

- **Size of downloaded dataset files:** 0.21 MB
- **Size of the generated dataset:** 0.23 MB
- **Total amount of disk used:** 0.44 MB

An example of 'test' looks as follows.
```
{
  "premise": "The cat sat on the mat.",
  "hypothesis": "The cat did not sit on the mat.",
  "label": -1,
  "idx: 0
}
```

#### cola

- **Size of downloaded dataset files:** 0.36 MB
- **Size of the generated dataset:** 0.58 MB
- **Total amount of disk used:** 0.94 MB

An example of 'train' looks as follows.
```
{
  "sentence": "Our friends won't buy this analysis, let alone the next one we propose.",
  "label": 1,
  "id": 0
}
```

#### mnli

- **Size of downloaded dataset files:** 298.29 MB
- **Size of the generated dataset:** 78.65 MB
- **Total amount of disk used:** 376.95 MB

An example of 'train' looks as follows.
```
{
  "premise": "Conceptually cream skimming has two basic dimensions - product and geography.",
  "hypothesis": "Product and geography are what make cream skimming work.",
  "label": 1,
  "idx": 0
}
```

#### mnli_matched

- **Size of downloaded dataset files:** 298.29 MB
- **Size of the generated dataset:** 3.52 MB
- **Total amount of disk used:** 301.82 MB

An example of 'test' looks as follows.
```
{
  "premise": "Hierbas, ans seco, ans dulce, and frigola are just a few names worth keeping a look-out for.",
  "hypothesis": "Hierbas is a name worth looking out for.",
  "label": -1,
  "idx": 0
}
```

#### mnli_mismatched

- **Size of downloaded dataset files:** 298.29 MB
- **Size of the generated dataset:** 3.73 MB
- **Total amount of disk used:** 302.02 MB

An example of 'test' looks as follows.
```
{
  "premise": "What have you decided, what are you going to do?",
  "hypothesis": "So what's your decision?,
  "label": -1,
  "idx": 0
}
```

#### mrpc

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### qnli

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### qqp

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### rte

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### sst2

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### stsb

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### wnli

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Data Fields

The data fields are the same among all splits.

#### ax
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### cola
- `sentence`: a `string` feature.
- `label`: a classification label, with possible values including `unacceptable` (0), `acceptable` (1).
- `idx`: a `int32` feature.

#### mnli
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### mnli_matched
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### mnli_mismatched
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2).
- `idx`: a `int32` feature.

#### mrpc

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### qnli

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### qqp

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### rte

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### sst2

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### stsb

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### wnli

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Data Splits

#### ax

|   |test|
|---|---:|
|ax |1104|

#### cola

|    |train|validation|test|
|----|----:|---------:|---:|
|cola| 8551|      1043|1063|

#### mnli

|    |train |validation_matched|validation_mismatched|test_matched|test_mismatched|
|----|-----:|-----------------:|--------------------:|-----------:|--------------:|
|mnli|392702|              9815|                 9832|        9796|           9847|

#### mnli_matched

|            |validation|test|
|------------|---------:|---:|
|mnli_matched|      9815|9796|

#### mnli_mismatched

|               |validation|test|
|---------------|---------:|---:|
|mnli_mismatched|      9832|9847|

#### mrpc

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### qnli

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### qqp

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### rte

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### sst2

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### stsb

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### wnli

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

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
@article{warstadt2018neural,
  title={Neural Network Acceptability Judgments},
  author={Warstadt, Alex and Singh, Amanpreet and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1805.12471},
  year={2018}
}
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}

Note that each GLUE dataset has its own citation. Please see the source to see
the correct citation for each contained dataset.
```


### Contributions

Thanks to [@patpizio](https://github.com/patpizio), [@jeswan](https://github.com/jeswan), [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.
