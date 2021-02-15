---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- da
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets: []
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- part-of-speech-tagging
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [Github](https://github.com/alexandrainst/danlp/blob/master/docs/docs/datasets.md#dane)
- **Repository:** [Github](https://github.com/alexandrainst/danlp)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/2020.lrec-1.565)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

Data Fields:
  - q_id: a string question identifier for each example, corresponding to its ID in the Pushshift.io Reddit submission dumps.
  - subreddit: One of explainlikeimfive, askscience, or AskHistorians, indicating which subreddit the question came from
  - title: title of the question, with URLs extracted and replaced by URL_n tokens
  - title_urls: list of the extracted URLs, the nth element of the list was replaced by URL_n
  - sent_id: a string identifier for each example
  - text: a string, the original sentence (not tokenized)
  - tok_ids: a list of ids (int), one for each token
  - tokens: a list of strings, the tokens
  - lemmas: a list of strings, the lemmas of the tokens
  - pos_tags: a list of strings, the part-of-speech tags of the tokens
  - morph_tags: a list of strings, the morphological tags of the tokens
  - dep_ids: a list of ids (int), the id of the head of the incoming dependency for each token
  - dep_labels: a list of strings, the dependency labels
  - ner_tags: a list of strings, the named entity tags (BIO format)

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

Thanks to [@ophelielacroix](https://github.com/ophelielacroix), [@lhoestq](https://github.com/lhoestq) for adding this dataset.