---
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
pretty_name: Text-based NP Enrichment
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-retrieval
task_ids:
- document-retrieval
---

# Dataset Card for Text-based NP Enrichment

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

- **Homepage:** https://yanaiela.github.io/TNE/
- **Repository:** https://github.com/yanaiela/TNE
- **Paper:** https://arxiv.org/abs/2109.12085
- **Leaderboard:** [TNE OOD](https://leaderboard.allenai.org/tne-ood/submissions/public)
[TNE](https://leaderboard.allenai.org/tne/submissions/public)
- **Point of Contact:** [Yanai Elazar](mailto:yanaiela@gmail.com)

### Dataset Summary

Text-based NP Enrichment (TNE) is a natural language understanding (NLU) task, which focus on relations between noun phrases (NPs) that can be mediated via prepositions. The dataset contains 5,497 documents, annotated exhaustively with all possible links between the NPs in each document.

The main data comes from WikiNews, which is used for train/dev/test. We also collected an additional set of 509 documents to serve as out of distribution (OOD) data points, from the Book Corpus, IMDB reviews and Reddit.

### Supported Tasks and Leaderboards

The data contain both the main data for the TNE task, as well as coreference resolution data.
There are two leaderboards for the TNE data, one for the standard test set, and another one for the OOD test set:
- [TNE Leaderboard](https://leaderboard.allenai.org/tne/submissions/public)
- [TNE OOD Leaderboard](https://leaderboard.allenai.org/tne-ood/submissions/public)

### Languages

The text in the dataset is in English, as spoken in the different domains we include. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

The original files are in a jsonl format, containing a dictionary of a single document, in each line.
Each document contain a different amount of labels, due to the different amount of NPs.
The test and ood splits come without the annotated labels.

### Data Fields

A document consists of:

* `id`: a unique identifier of a document, beginning with `r` and followed by a number
* `text`: the text of the document. The title and subtitles (if exists) are separated with two new lines. The paragraphs
are separated by a single new line.
* `tokens`: a list of string, containing the tokenized tokens
* `nps`: a list of dictionaries, containing the following entries:
  * `text`: the text of the np
  * `start_index`: an integer indicating the starting index in the text
  * `end_index`: an integer indicating the ending index in the text
  * `start_token`: an integer indicating the first token of the np out of the tokenized tokens
  * `end_token`: an integer indicating the last token of the np out of the tokenized tokens
  * `id`: the id of the np
* `np_relations`: these are the relation labels of the document. It is a list of dictionaries, where each
dictionary contains:
  * `anchor`: the id of the anchor np
  * `complement`: the id of the complement np
  * `preposition`: the preposition that links between the anchor and the complement. This can take one out of 24 pre-defined preposition (23 + member(s)-of)
  * `complement_coref_cluster_id`: the coreference id, which the complement is part of.
* `coref`: the coreference labels. It contains a list of dictionaries, where each dictionary contains:
  * `id`: the id of the coreference cluster
  * `members`: the ids of the nps members of such cluster
  * `np_type`: the type of cluster. It can be either 
    * `standard`: regular coreference cluster
    * `time/date/measurement`: a time / date / measurement np. These will be singletons.
    * `idiomatic`: an idiomatic expression
* `metadata`: metadata of the document. It contains the following:
  * `annotators`: a dictionary with anonymized annotators id
    * `coref_worker`: the coreference worker id
    * `consolidator_worker`: the consolidator worker id
    * `np-relations_worker`: the np relations worker id
  * `url`: the url where the document was taken from (not always existing)
  * `source`: the original file name where the document was taken from


### Data Splits

The dataset is spread across four files, for the four different splits: train, dev, test and test_ood.
Additional details on the data statistics can be found in the [paper](https://arxiv.org/abs/2109.12085)

## Dataset Creation

### Curation Rationale

TNE was build as a new task for language understanding, focusing on extracting relations between nouns, moderated by prepositions.

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

The dataset was created by Yanai Elazar, Victoria Basmov, Yoav Goldberg, Reut Tsarfaty, during work done at Bar-Ilan University, and AI2.

### Licensing Information

The data is released under the MIT license.

### Citation Information

```bibtex
@article{tne,
    author = {Elazar, Yanai and Basmov, Victoria and Goldberg, Yoav and Tsarfaty, Reut},
    title = "{Text-based NP Enrichment}",
    journal = {Transactions of the Association for Computational Linguistics},
    year = {2022},
}
```

### Contributions

Thanks to [@yanaiela](https://github.com/yanaiela), who is also the first author of the paper, for adding this dataset.
