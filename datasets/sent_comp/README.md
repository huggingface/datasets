---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-sentence-compression
paperswithcode_id: sentence-compression
---

# Dataset Card for Google Sentence Compression

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

- **Homepage:[https://github.com/google-research-datasets/sentence-compression](https://github.com/google-research-datasets/sentence-compression)**
- **Repository:[https://github.com/google-research-datasets/sentence-compression](https://github.com/google-research-datasets/sentence-compression)**
- **Paper:[https://www.aclweb.org/anthology/D13-1155/](https://www.aclweb.org/anthology/D13-1155/)**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

A major challenge in supervised sentence compression is making use of rich feature representations because of very scarce parallel data. We address this problem and present a method to automatically build a compression corpus with hundreds of thousands of instances on which deletion-based algorithms can be trained. In our corpus, the syntactic trees of the compressions are subtrees of their uncompressed counterparts, and hence supervised systems which require a structural alignment between the input and output can be successfully trained. We also extend an existing unsupervised compression method with a learning module. The new system uses structured prediction to learn from lexical, syntactic and other features. An evaluation with human raters shows that the presented data harvesting method indeed produces a parallel corpus of high quality. Also, the supervised system trained on this corpus gets high scores both from human raters and in an automatic evaluation setting, significantly outperforming a strong baseline.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

### Data Instances

Each data instance should contains the information about the original sentence in `instance["graph"]["sentence"]` as well as the compressed sentence in `instance["compression"]["text"]`. As this dataset was created by pruning dependency connections, the author also includes the dependency tree and transformed graph of the original sentence and compressed sentence.

### Data Fields

Each instance should contains these information:

- `graph` (`Dict`): the transformation graph/tree for extracting compression (a modified version of a dependency tree).
  - This will have features similar to a dependency tree (listed bellow)
- `compression` (`Dict`)
  - `text` (`str`)
  - `edge` (`List`)
- `headline` (`str`): the headline of the original news page.
- `compression_ratio` (`float`): the ratio between compressed sentence vs original sentence.
- `doc_id` (`str`): url of the original news page.
- `source_tree` (`Dict`): the original dependency tree (features listed bellow).
- `compression_untransformed` (`Dict`)
  - `text` (`str`)
  - `edge` (`List`)

Dependency tree features:

- `id` (`str`)
- `sentence` (`str`)
- `node` (`List`): list of nodes, each node represent a word/word phrase in the tree.
  - `form` (`string`)
  - `type` (`string`): the enity type of a node. Defaults to `""` if it's not an entity.
  - `mid` (`string`)
  - `word` (`List`): list of words the node contains.
    - `id` (`int`)
    - `form` (`str`): the word from the sentence.
    - `stem` (`str`): the stemmed/lemmatized version of the word.
    - `tag` (`str`): dependency tag of the word.
  - `gender` (`int`)
  - `head_word_index` (`int`)
- `edge`: list of the dependency connections between words.
  - `parent_id` (`int`)
  - `child_id` (`int`)
  - `label` (`str`)
- `entity_mention` list of the entities in the sentence.
  - `start` (`int`)
  - `end` (`int`)
  - `head` (`str`)
  - `name` (`str`)
  - `type` (`str`)
  - `mid` (`str`)
  - `is_proper_name_entity` (`bool`)
  - `gender` (`int`)

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.