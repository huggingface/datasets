---
pretty_name: "PAWS: Paraphrase Adversaries from Word Scrambling"
annotations_creators:
  labeled_final:
  - expert-generated
  labeled_swap:
  - expert-generated
  unlabeled_final:
  - machine-generated
language_creators:
- machine-generated
languages:
- en
licenses:
- other
multilinguality:
- monolingual
size_categories:
  labeled_final:
  - 10K<n<100K
  labeled_swap:
  - 10K<n<100K
  unlabeled_final:
  - 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
- text-scoring
task_ids:
- semantic-similarity-classification
- semantic-similarity-scoring
- text-scoring-other-paraphrase-identification
paperswithcode_id: paws
---

# Dataset Card for PAWS: Paraphrase Adversaries from Word Scrambling

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

- **Homepage:** [PAWS](https://github.com/google-research-datasets/paws)
- **Repository:** [PAWS](https://github.com/google-research-datasets/paws)
- **Paper:** [PAWS: Paraphrase Adversaries from Word Scrambling](https://arxiv.org/abs/1904.01130)
- **Point of Contact:** [Yuan Zhang](zhangyua@google.com)

### Dataset Summary

PAWS: Paraphrase Adversaries from Word Scrambling

This dataset contains 108,463 human-labeled and 656k noisily labeled pairs that feature the importance of modeling structure, context, and word order information for the problem of paraphrase identification. The dataset has two subsets, one based on Wikipedia and the other one based on the Quora Question Pairs (QQP) dataset.

For further details, see the accompanying paper: PAWS: Paraphrase Adversaries from Word Scrambling (https://arxiv.org/abs/1904.01130)

PAWS-QQP is not available due to license of QQP. It must be reconstructed by downloading the original data and then running our scripts to produce the data and attach the labels.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

Below are two examples from the dataset:

|     | Sentence 1                    | Sentence 2                    | Label |
| :-- | :---------------------------- | :---------------------------- | :---- |
| (1) | Although interchangeable, the body pieces on the 2 cars are not similar. | Although similar, the body parts are not interchangeable  on the 2 cars.  | 0     |
| (2) | Katz was born in Sweden in 1947 and moved to New York City at the age of 1.      | Katz was born in 1947 in Sweden and moved to New York at the age of one.   | 1     |

The first pair has different semantic meaning while the second pair is a paraphrase. State-of-the-art models trained on existing datasets have dismal performance on PAWS (<40% accuracy); however, including PAWS training data for these models improves their accuracy to 85% while maintaining performance on existing datasets such as the [Quora Question Pairs](https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs).


### Data Fields

This corpus contains pairs generated from Wikipedia pages, and can be downloaded
here:

*   **PAWS-Wiki Labeled (Final)**: containing pairs that are generated from both word swapping and back translation methods. All pairs have human judgements on both paraphrasing and fluency and they are split into Train/Dev/Test sections.

*   **PAWS-Wiki Labeled (Swap-only)**: containing pairs that have no back translation counterparts and therefore they are not included in the first set. Nevertheless, they are high-quality pairs with human judgements on both paraphrasing and fluency, and they can be included as an auxiliary training set.

*   **PAWS-Wiki Unlabeled (Final)**: Pairs in this set have noisy labels without human judgments and can also be used as an auxiliary training set. They are generated from both word swapping and back translation methods.

All files are in the tsv format with four columns:

Column Name   | Data
:------------ | :--------------------------
id            | A unique id for each pair
sentence1     | The first sentence
sentence2     | The second sentence
(noisy_)label | (Noisy) label for each pair

Each label has two possible values: `0` indicates the pair has different meaning, while `1` indicates the pair is a paraphrase.


### Data Splits

The number of examples and the proportion of paraphrase (Yes%) pairs are shown
below:

Data                | Train   | Dev    | Test  | Yes%
:------------------ | ------: | -----: | ----: | ----:
Labeled (Final)     | 49,401  | 8,000  | 8,000 | 44.2%
Labeled (Swap-only) | 30,397  | --     | --    | 9.6%
Unlabeled (Final)   | 645,652 | 10,000 | --    | 50.0%

## Dataset Creation

### Curation Rationale

Existing paraphrase identification datasets lack sentence pairs that have high lexical overlap without being paraphrases. Models trained on such data fail to distinguish pairs like *flights from New York to Florida* and *flights from Florida to New York*.

### Source Data

#### Initial Data Collection and Normalization

Their automatic generation method is based on two ideas. The first swaps words to generate a sentence pair with the same BOW, controlled by a language model. The second uses back translation to generate paraphrases with high BOW overlap but different word order. These two strategies generate high-quality, diverse PAWS pairs, balanced evenly between paraphrases and non-paraphrases.

#### Who are the source language producers?

Mentioned above.

### Annotations

#### Annotation process

Sentence pairs are presented to five annotators, each of which gives a binary judgment as to whether they are paraphrases or not. They chose binary judgments to make dataset have the same label schema as the QQP corpus. Overall, human agreement is high on both Quora (92.0%) and Wikipedia (94.7%) and each label only takes about 24 seconds. As such, answers are usually straight-forward to human raters.

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

List the people involved in collecting the dataset and their affiliation(s). If funding information is known, include it here.

### Licensing Information

The dataset may be freely used for any purpose, although acknowledgement of Google LLC ("Google") as the data source would be appreciated. The dataset is provided "AS IS" without any warranty, express or implied. Google disclaims all liability for any damages, direct or indirect, resulting from the use of the dataset.

### Citation Information

```
@InProceedings{paws2019naacl,
  title = {{PAWS: Paraphrase Adversaries from Word Scrambling}},
  author = {Zhang, Yuan and Baldridge, Jason and He, Luheng},
  booktitle = {Proc. of NAACL},
  year = {2019}
}
```
### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.