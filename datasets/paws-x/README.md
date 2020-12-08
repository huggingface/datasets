---
annotations_creators:
- expert-generated
- machine-generated
language_creators:
- expert-generated
- machine-generated
languages:
- de
- en
- es
- fr
- ja
- ko
- zh
licenses:
- other
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-paws
task_categories:
- text-classification
- text-scoring
task_ids:
- semantic-similarity-classification
- semantic-similarity-scoring
- text-scoring-other-paraphrase-identification
---

# Dataset Card Creation Guide

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

- **Homepage:** [PAWS-X](https://github.com/google-research-datasets/paws/tree/master/pawsx)
- **Repository:** [PAWS-X](https://github.com/google-research-datasets/paws/tree/master/pawsx)
- **Paper:** [PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification](https://arxiv.org/abs/1908.11828)
- **Point of Contact:** [Yinfei Yang](yinfeiy@google.com)

### Dataset Summary

This dataset contains 23,659 **human** translated PAWS evaluation pairs and
296,406 **machine** translated training pairs in six typologically distinct
languages: French, Spanish, German, Chinese, Japanese, and Korean. All
translated pairs are sourced from examples in
[PAWS-Wiki](https://github.com/google-research-datasets/paws#paws-wiki).

For further details, see the accompanying paper:
[PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase
Identification](https://arxiv.org/abs/1908.11828)

### Supported Tasks and Leaderboards

It has been majorly used for paraphrase identification for English and other 6 languages namely French, Spanish, German, Chinese, Japanese, and Korean

### Languages

The dataset is in English, French, Spanish, German, Chinese, Japanese, and Korean

## Dataset Structure

### Data Instances

For en:
```
id		    :   1
sentence1	:	In Paris , in October 1560 , he secretly met the English ambassador , Nicolas Throckmorton , asking him for a passport to return to England through Scotland .
sentence2	:	In October 1560 , he secretly met with the English ambassador , Nicolas Throckmorton , in Paris , and asked him for a passport to return to Scotland through England .
label       :   0
```
For fr:
```
id		    :   1
sentence1	:	À Paris, en octobre 1560, il rencontra secrètement l'ambassadeur d'Angleterre, Nicolas Throckmorton, lui demandant un passeport pour retourner en Angleterre en passant par l'Écosse.
sentence2	:	En octobre 1560, il rencontra secrètement l'ambassadeur d'Angleterre, Nicolas Throckmorton, à Paris, et lui demanda un passeport pour retourner en Écosse par l'Angleterre.
label       :   0
```

### Data Fields

All files are in tsv format with four columns:

Column Name | Data
:---------- | :--------------------------------------------------------
id          | An ID that matches the ID of the source pair in PAWS-Wiki
sentence1   | The first sentence
sentence2   | The second sentence
label       | Label for each pair

The source text of each translation can be retrieved by looking up the ID in the
corresponding file in PAWS-Wiki.

### Data Splits

The numbers of examples for each of the six languages are shown below:

Language | Train   | Dev    | Test
:------- | ------: | -----: | -----:
fr       | 49,401  | 1,992  | 1,985
es       | 49,401  | 1,962  | 1,999
de       | 49,401  | 1,932  | 1,967
zh       | 49,401  | 1,984  | 1,975
ja       | 49,401  | 1,980  | 1,946
ko       | 49,401  | 1,965  | 1,972
Total    | 296,406 | 11,815 | 11,844

> **Caveat**: please note that the dev and test sets of PAWS-X are both sourced
> from the dev set of PAWS-Wiki. As a consequence, the same `sentence 1` may
> appear in both the dev and test sets. Nevertheless our data split guarantees
> that there is no overlap on sentence pairs (`sentence 1` + `sentence 2`)
> between dev and test.

## Dataset Creation

### Curation Rationale

Most existing work on adversarial data generation focuses on English. For example, PAWS (Paraphrase Adversaries from Word Scrambling) (Zhang et al., 2019) consists of challenging English paraphrase identification pairs from Wikipedia and Quora. They remedy this gap with PAWS-X, a new dataset of 23,659 human translated PAWS evaluation pairs in six typologically distinct languages: French, Spanish, German, Chinese, Japanese, and Korean. They provide baseline numbers for three models with different capacity to capture non-local context and sentence structure, and using different multilingual training and evaluation regimes. Multilingual BERT (Devlin et al., 2019) fine-tuned on PAWS English plus machine-translated data performs the best, with a range of 83.1-90.8 accuracy across the non-English languages and an average accuracy gain of 23% over the next best model. PAWS-X shows the effectiveness of deep, multilingual pre-training while also leaving considerable headroom as a new challenge to drive multilingual research that better captures structure and contextual information.

### Source Data

PAWS (Paraphrase Adversaries from Word Scrambling)

#### Initial Data Collection and Normalization

All translated pairs are sourced from examples in [PAWS-Wiki](https://github.com/google-research-datasets/paws#paws-wiki)

#### Who are the source language producers?

This dataset contains 23,659 human translated PAWS evaluation pairs and 296,406 machine translated training pairs in six typologically distinct languages: French, Spanish, German, Chinese, Japanese, and Korean.

### Annotations

#### Annotation process

If applicable, describe the annotation process and any tools used, or state otherwise. Describe the amount of data annotated, if not all. Describe or reference annotation guidelines provided to the annotators. If available, provide interannotator statistics. Describe any annotation validation processes.

#### Who are the annotators?

The paper mentions the translate team, especially Mengmeng Niu, for the help with the annotations.

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

List the people involved in collecting the dataset and their affiliation(s). If funding information is known, include it here.

### Licensing Information

The dataset may be freely used for any purpose, although acknowledgement of Google LLC ("Google") as the data source would be appreciated. The dataset is provided "AS IS" without any warranty, express or implied. Google disclaims all liability for any damages, direct or indirect, resulting from the use of the dataset.

### Citation Information

```
@InProceedings{pawsx2019emnlp,
  title = {{PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification}},
  author = {Yang, Yinfei and Zhang, Yuan and Tar, Chris and Baldridge, Jason},
  booktitle = {Proc. of EMNLP},
  year = {2019}
}
```