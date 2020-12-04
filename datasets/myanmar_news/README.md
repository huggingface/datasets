---
annotations_creators: []
language_creators: []
languages:
- my
licenses:
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
---

# Dataset Card for Myanmar_News

## Dataset Description

- **Repository: ** https://github.com/ayehninnkhine/MyanmarNewsClassificationSystem

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
