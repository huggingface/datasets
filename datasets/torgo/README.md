---
TODO: Add YAML tags here. Copy-paste the tags obtained with the online tagging app: https://huggingface.co/spaces/huggingface/datasets-tagging
--- 
annotations_creators: 
  - expert-generated
language: 
  - en
language_creators: 
  - found
license: 
  - mit
multilinguality: 
  - monolingual
paperswithcode_id: acronym-identification
pretty_name: torgo
size_categories: 
  - 10K<n<100K
source_datasets: 
  - original
tags: 
  - dysarthria
task_categories: 
  - token-classification
  - audio-classification
task_ids: []
train-eval-index: 
  - 
    col_mapping: 
      labels: tags
      tokens: tokens
    config: default
    splits: 
      eval_split: test
    task: token-classification
    task_id: entity_extraction

---

# Dataset Card for [Dataset Name]

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

- **Homepage:**
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The TORGO database of dysarthric articulation consists of aligned acoustics and measured 3D articulatory features 
from speakers with either cerebral palsy (CP) or amyotrophic lateral sclerosis (ALS), which are two of the most 
prevalent causes of speech disability (Kent and Rosen, 2004), and matchd controls. This database, called TORGO, 
is the result of a collaboration between the departments of Computer Science and Speech-Language Pathology 
at the University of Toronto and the Holland-Bloorview Kids Rehab hospital in Toronto.

More info on TORGO dataset can be understood from the "README" which can be found here:
http://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

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

Apache License, Version 2.0 (the "License")

### Citation Information

@article{Rudzicz2012TheTD,
  title={The TORGO database of acoustic and articulatory speech from speakers with dysarthria},
  author={Frank Rudzicz and Aravind Kumar Namasivayam and Talya Wolff},
  journal={Language Resources and Evaluation},
  year={2012},
  volume={46},
  pages={523-541}
}

### Contributions

Thanks to [@github-username](https://github.com/YingLi001) for adding this dataset.
