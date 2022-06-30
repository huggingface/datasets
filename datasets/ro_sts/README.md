---
annotations_creators: 
- crowdsourced
language_creators:
- crowdsourced
language:
- ro
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-sts-b
task_categories:
- text-classification
task_ids:
- text-scoring
- semantic-similarity-scoring
paperswithcode_id: null
pretty_name: RO-STS
---

# Dataset Card for RO-STS

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

- **Homepage:** [GitHub](https://github.com/dumitrescustefan/RO-STS)
- **Repository:** [GitHub](https://github.com/dumitrescustefan/RO-STS)
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [email](dumitrescu.stefan@gmail.com)

### Dataset Summary

We present RO-STS - the Semantic Textual Similarity dataset for the Romanian language. It is a high-quality translation of the [STS English dataset](https://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark). RO-STS contains 8,628 sentence pairs with their similarity scores. The original English sentences were collected from news headlines, captions of images and user forums, and are categorized accordingly. The Romanian release follows this categorization and provides the same train/validation/test split with 5,749/1,500/1,379 sentence pairs in each subset.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text dataset is in Romanian (`ro`)

## Dataset Structure

### Data Instances

An example looks like this:

```
{'score': 1.5,
 'sentence1': 'Un bărbat cântă la harpă.',
 'sentence2': 'Un bărbat cântă la claviatură.',
}
```

### Data Fields

- `score`: a float representing the semantic similarity score where 0.0 is the lowest score and 5.0 is the highest
- `sentence1`: a string representing a text
- `sentence2`: another string to compare the previous text with

### Data Splits

The train/validation/test split contain 5,749/1,500/1,379 sentence pairs.

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

[Needs More Information]

#### Initial Data Collection and Normalization

*To construct the dataset, we first obtained automatic translations using Google's translation engine. These were then manually checked, corrected, and cross-validated by human volunteers. *

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

#### Who are the annotators?

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

[Needs More Information]

### Licensing Information

CC BY-SA 4.0 License

### Citation Information

[Needs More Information]

### Contributions

Thanks to [@lorinczb](https://github.com/lorinczb) for adding this dataset.
