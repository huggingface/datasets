---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- other-
multilinguality:
- monolingual
pretty_name: The Pile
size_categories:
- unknown
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for The Pile

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** https://pile.eleuther.ai/
- **Repository:** https://github.com/EleutherAI/the-pile
- **Paper:** [The Pile: An 800GB Dataset of Diverse Text for Language Modeling](https://arxiv.org/abs/2101.00027)
- **Leaderboard:**
- **Point of Contact:** [EleutherAI](mailto:contact@eleuther.ai)

### Dataset Summary

The Pile is a 825 GiB diverse, open source language modelling data set that consists of 22 smaller, high-quality
datasets combined together.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

#### all
```
{
  'meta': {'pile_set_name': 'Pile-CC'},
  'text': 'It is done, and submitted. You can play “Survival of the Tastiest” on Android, and on the web. Playing on...'
}
```

#### pubmed_central
```
{
  'id': 'PMC5595690',
  'text': 'Introduction {#acel12642-sec-0001}\n============\n\nAlzheimer\\\'s disease (AD), the most common cause of...'
}
```

### Data Fields

#### all

- `meta` (dict): Metadata of the data instance, with keys:
   - pile_set_name: Name of the subset.
- `text` (str): Text.

### Data Splits

The "all" configuration is composed of 3 splits: train, validation and test.

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

Please refer to the specific license depending on the subset you use:
- PubMed Central: [MIT License](https://github.com/EleutherAI/pile-pubmedcentral/blob/master/LICENSE)

### Citation Information

```
@misc{gao2020pile,
      title={The Pile: An 800GB Dataset of Diverse Text for Language Modeling},
      author={Leo Gao and Stella Biderman and Sid Black and Laurence Golding and Travis Hoppe and Charles Foster and Jason Phang and Horace He and Anish Thite and Noa Nabeshima and Shawn Presser and Connor Leahy},
      year={2020},
      eprint={2101.00027},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@github-username](https://github.com/<github-username>) for adding this dataset.
