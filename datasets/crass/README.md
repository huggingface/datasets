---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- expert-generated
- machine-generated
languages:
- en-US
licenses:
- apache-2.0
multilinguality:
- monolingual
pretty_name: CRASS
size_categories:
- unknown
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- natural-language-inference
---

# Dataset Card for CRASS

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

## Dataset Description

- **Homepage:** https://www.crass.ai
- **Repository:** https://github.com/apergo-ai/CRASS-data-set
- **Paper:** [Needs More Information]
- **Leaderboard:** https://www.crass.ai/ledger.php
- **Point of Contact:** j.frohberg@apergo.net

### Dataset Summary

The data consists of so-called PCTs (Premise-Counterfactual Tuples). They contrast a hypothetical situation using a counterfactual conditional against a base premise. In the fixed target mode there is one correct answer and two alternative incorrect answers.

### Supported Tasks and Leaderboards

zero-shot-classification: The dataset can be used to benchmark a model for zero-shot or few-shot classification tasks, which consists in selecting the correct answer out of three possible answers. Success on this task is typically measured by achieving a high T1 accuracy. A [BART-based model] (https://huggingface.co/facebook/bart-large-mnli) model trained on MNLI currently achieves a [T1 accuracy of 0.48]. GPT-3 family accessed via OpenAI beta API using davinchi model currently achieves a [T1 accuracy of 0.56].

### Languages

en-US

## Dataset Structure

### Data Instances

  {
    "PCTID": 6,
    "BatchID": 1,
    "Premise": "A woman sees a fire.",
    "QCC": "What would have happened if the woman had touched the fire?",
    "CorrectAnswer": "She would have been burned.",
    "Answer1": "She would not have been burned.",
    "Answer2": "That is not possible.",
    "PossibleAnswer3": "She would have seen fire.",
    "canary_string": ""
}

### Data Fields

PCTID: The ID of the item
BatchID: A ID referencing creation process. Can be ignored.
Premise: The description of the base premise that is the reference event against which the hypothetical event is compared.
QCC: The so called questionized counterfactual conditional is a question creating a hypothetical event and contrasting it in a query-styled natural language form to the base premise event.
CorrectAnswer: The correct answer
Answer1: Incorrect answer
Answer2: Incorrect answer
PossibleAnswer3: Sometimes a third alternative incorrect answer is given
canary_string: The first element contains the BIG Bench canary string to prevent data leackage

### Data Splits

As the dataset is used for zero-shot classification, the whole dataset is one singular test split.

## Dataset Creation

### Curation Rationale

The CRASS benchmarks aims to develop a new test suite for the evaluation of the performance of current large language models (LLMs) by utilizing so called questionized counterfactual conditionals (QCC).

### Source Data

#### Initial Data Collection and Normalization

The data set was created, first, by expert creation. This small initial sample was given to a qualified mechanical turk workers to come up with more examples with the same pattern. These examples were subsequently rated by different mechanical turk workers to exclude deviant or incomprehensible examples.

#### Who are the source language producers?

The language producers are Amazon mechanical turk users. Subjects were adults living in the United States who speak proficient English and have 99% approval rate for correctly completing tasks on AMT and have completed at least 100 approved HITs. A total of 58 annotators were screened using a qualification survey consisting of basic logical reasoning and coherence questions as well as eight sample PCTs. 13 annotators were selected who performed best across all categories. 

### Annotations

#### Annotation process

see above

#### Who are the annotators?

see above

### Personal and Sensitive Information

The dataset does not contain personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop better LLMs. In that pursuit, the hypothetical situations mentioned in the PCTs contain some descriptions of potentially harmful events.

### Discussion of Biases

The dataset was designed to contain as minimal biases as possible. For instance, the mentioning of male and female gender persons is balanced. Nevertheless, there is no guarantee that the dataset is completely bias-free.

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The dataset is currated by Jörg Frohberg from apergo UG (http://www.apergo.ai)

### Licensing Information

The CRASS benchmark data set is released under the Apache License 2.0.

### Citation Information

```
@misc{frohberg2021crass,
      title={CRASS: A Novel Data Set and Benchmark to Test Counterfactual Reasoning of Large Language Models}, 
      author={Jörg Frohberg and Frank Binder},
      year={2021},
      eprint={2112.11941},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@apergo-ai](https://github.com/apergo-ai) for adding this dataset.
