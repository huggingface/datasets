---
annotations_creators:
- found
language_creators:
- found
language:
- my
license:
- gpl-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
paperswithcode_id: null
pretty_name: MyanmarNews
dataset_info:
  features:
  - name: text
    dtype: string
  - name: category
    dtype:
      class_label:
        names:
          0: Sport
          1: Politic
          2: Business
          3: Entertainment
  splits:
  - name: train
    num_bytes: 3797368
    num_examples: 8116
  download_size: 610592
  dataset_size: 3797368
---

# Dataset Card for Myanmar_News

## Dataset Description

- **Repository:** https://github.com/ayehninnkhine/MyanmarNewsClassificationSystem

### Dataset Summary

The Myanmar news dataset contains article snippets in four categories:
Business, Entertainment, Politics, and Sport.

These were collected in October 2017 by Aye Hninn Khine

### Languages

Myanmar/Burmese language

## Dataset Structure

### Data Fields

- text - text from article
- category - a topic: Business, Entertainment, **Politic**, or **Sport** (note spellings)

### Data Splits

One training set (8,116 total rows)

### Source Data

#### Initial Data Collection and Normalization

Data was collected by Aye Hninn Khine
and shared on GitHub with a GPL-3.0 license.

Multiple text files were consolidated into one labeled CSV file by Nick Doiron.

## Additional Information

### Dataset Curators

Contributors to original GitHub repo:
- https://github.com/ayehninnkhine

### Licensing Information

GPL-3.0

### Citation Information

See https://github.com/ayehninnkhine/MyanmarNewsClassificationSystem

### Contributions

Thanks to [@mapmeld](https://github.com/mapmeld) for adding this dataset.