---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-MS^2
- extended|other-Cochrane
task_categories:
- summarization
- text2text-generation
task_ids:
- summarization-other-query-based-summarization 
- summarization-other-query-based-multi-document-summarization
- summarization-other-scientific-documents-summarization
paperswithcode_id: multi-document-summarization
pretty_name: MSLR Shared Task
---

# Dataset Card for MSLR2022

## Table of Contents
- [Dataset Card for MSLR2022](#dataset-card-for-mslr2022)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://github.com/allenai/mslr-shared-task
- **Repository:** https://github.com/allenai/mslr-shared-task
- **Paper:** https://aclanthology.org/2021.emnlp-main.594
- **Leaderboard:** https://github.com/allenai/mslr-shared-task#leaderboard
- **Point of Contact:** https://github.com/allenai/mslr-shared-task#contact-us

### Dataset Summary

The Multidocument Summarization for Literature Review (MSLR) Shared Task aims to study how medical evidence from different clinical studies are summarized in literature reviews. Reviews provide the highest quality of evidence for clinical care, but are expensive to produce manually. (Semi-)automation via NLP may facilitate faster evidence synthesis without sacrificing rigor. The MSLR shared task uses two datasets to assess the current state of multidocument summarization for this task, and to encourage the development of modeling contributions, scaffolding tasks, methods for model interpretability, and improved automated evaluation methods in this domain.

### Supported Tasks and Leaderboards

This dataset is used for the MSLR2022 Shared Task. For information on the shared task leaderboard, please refer [here](https://github.com/allenai/mslr-shared-task#leaderboard).

### Languages

English

## Dataset Structure

More information on dataset structure [here](https://github.com/allenai/mslr-shared-task#data-structure).

### Data Instances

[Needs More Information]

### Data Fields

[Needs More Information]

### Data Splits

[Needs More Information]

## Dataset Creation

Please refer to the following papers for details about dataset curation:

[MSˆ2: A Dataset for Multi-Document Summarization of Medical Studies](https://aclanthology.org/2021.emnlp-main.594.pdf)

[Generating (Factual?) Narrative Summaries of RCTs: Experiments with Neural Multi-Document Summarization](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8378607/)

### Curation Rationale

[Needs More Information]

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

[Needs More Information]

### Licensing Information

Licensing information can be found [here](https://github.com/allenai/mslr-shared-task/blob/main/LICENSE).

### Citation Information

**DeYoung, Jay, Iz Beltagy, Madeleine van Zuylen, Bailey Kuehl and Lucy Lu Wang. "MS2: A Dataset for Multi-Document Summarization of Medical Studies." EMNLP (2021).**

```bibtex
@inproceedings{DeYoung2021MS2MS,
  title={MSˆ2: Multi-Document Summarization of Medical Studies},
  author={Jay DeYoung and Iz Beltagy and Madeleine van Zuylen and Bailey Kuehl and Lucy Lu Wang},
  booktitle={EMNLP},
  year={2021}
}
```

**Byron C. Wallace, Sayantani Saha, Frank Soboczenski, and Iain James Marshall. (2020). "Generating (factual?) narrative summaries of RCTs: Experiments with neural multi-document summarization." AMIA Annual Symposium.**

```bibtex
@article{Wallace2020GeneratingN,
  title={Generating (Factual?) Narrative Summaries of RCTs: Experiments with Neural Multi-Document Summarization},
  author={Byron C. Wallace and Sayantani Saha and Frank Soboczenski and Iain James Marshall},
  journal={AMIA Annual Symposium},
  year={2020},
  volume={abs/2008.11293}
}
```