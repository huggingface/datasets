---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
languages:
- en
licenses:
- cc-by-3.0
- cc-by-sa-3.0-at
- mit
- other-Open Portion of the American National Corpus
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-scoring
- semantic-similarity-scoring
paperswithcode_id: multinli
pretty_name: Multi-Genre Natural Language Inference
---

# Dataset Card for Multi-Genre Natural Language Inference (MultiNLI)

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

- **Homepage:** [https://www.nyu.edu/projects/bowman/multinli/](https://www.nyu.edu/projects/bowman/multinli/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 216.34 MB
- **Size of the generated dataset:** 73.39 MB
- **Total amount of disk used:** 289.74 MB

### Dataset Summary

The Multi-Genre Natural Language Inference (MultiNLI) corpus is a
crowd-sourced collection of 433k sentence pairs annotated with textual
entailment information. The corpus is modeled on the SNLI corpus, but differs in
that covers a range of genres of spoken and written text, and supports a
distinctive cross-genre generalization evaluation. The corpus served as the
basis for the shared task of the RepEval 2017 Workshop at EMNLP in Copenhagen.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

The dataset contains samples in English only.

## Dataset Structure

### Data Instances

- **Size of downloaded dataset files:** 216.34 MB
- **Size of the generated dataset:** 73.39 MB
- **Total amount of disk used:** 289.74 MB

Example of a data instance:

```
{
    "promptID": 31193,
    "pairID": "31193n",
    "premise": "Conceptually cream skimming has two basic dimensions - product and geography.",
    "premise_binary_parse": "( ( Conceptually ( cream skimming ) ) ( ( has ( ( ( two ( basic dimensions ) ) - ) ( ( product and ) geography ) ) ) . ) )",
    "premise_parse": "(ROOT (S (NP (JJ Conceptually) (NN cream) (NN skimming)) (VP (VBZ has) (NP (NP (CD two) (JJ basic) (NNS dimensions)) (: -) (NP (NN product) (CC and) (NN geography)))) (. .)))",
    "hypothesis": "Product and geography are what make cream skimming work. ",
    "hypothesis_binary_parse": "( ( ( Product and ) geography ) ( ( are ( what ( make ( cream ( skimming work ) ) ) ) ) . ) )",
    "hypothesis_parse": "(ROOT (S (NP (NN Product) (CC and) (NN geography)) (VP (VBP are) (SBAR (WHNP (WP what)) (S (VP (VBP make) (NP (NP (NN cream)) (VP (VBG skimming) (NP (NN work)))))))) (. .)))",
    "genre": "government",
    "label": 1
}
```

### Data Fields

The data fields are the same among all splits.

- `promptID`: Unique identifier for prompt
- `pairID`: Unique identifier for pair
- `{premise,hypothesis}`: combination of `premise` and `hypothesis`
- `{premise,hypothesis} parse`: Each sentence as parsed by the Stanford PCFG Parser 3.5.2
- `{premise,hypothesis} binary parse`: parses in unlabeled binary-branching format
- `genre`: a `string` feature.
- `label`: a classification label, with possible values including `entailment` (0), `neutral` (1), `contradiction` (2). Dataset instances which don't have any gold label are marked with -1 label. Make sure you filter them before starting the training using `datasets.Dataset.filter`.

### Data Splits

|train |validation_matched|validation_mismatched|
|-----:|-----------------:|--------------------:|
|392702|              9815|                 9832|

## Dataset Creation

### Curation Rationale

They constructed MultiNLI so as to make it possible to explicitly evaluate models both on the quality of their sentence representations within the training domain and on their ability to derive reasonable representations in unfamiliar domains.

### Source Data

#### Initial Data Collection and Normalization

They created each sentence pair by selecting a premise sentence from a preexisting text source and asked a human annotator to compose a novel sentence to pair with it as a hypothesis.

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

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

The majority of the corpus is released under the OANC’s license, which allows all content to be freely used, modified, and shared under permissive terms. The data in the FICTION section falls under several permissive licenses; Seven Swords is available under a Creative Commons Share-Alike 3.0 Unported License, and with the explicit permission of the author, Living History and Password Incorrect are available under Creative Commons Attribution 3.0 Unported Licenses; the remaining works of fiction are in the public domain in the United States (but may be licensed differently elsewhere).

### Citation Information

```
@InProceedings{N18-1101,
  author = "Williams, Adina
            and Nangia, Nikita
            and Bowman, Samuel",
  title = "A Broad-Coverage Challenge Corpus for
           Sentence Understanding through Inference",
  booktitle = "Proceedings of the 2018 Conference of
               the North American Chapter of the
               Association for Computational Linguistics:
               Human Language Technologies, Volume 1 (Long
               Papers)",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  pages = "1112--1122",
  location = "New Orleans, Louisiana",
  url = "http://aclweb.org/anthology/N18-1101"
}
```

### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.
