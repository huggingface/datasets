---
annotations_creators: []
language_creators: []
languages:
- th
licenses:
- lgpl-3.0-only
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for Wongnai_Reviews

## Dataset Description

- **Repository: ** https://github.com/wongnai/wongnai-corpus

### Dataset Summary

The Wongnai Review dataset contains restaurant reviews and ratings, almost entirely in Thai language.

The reviews are in 5 classes ranging from 1 to 5 stars.

This dataset was featured in a Kaggle challenge https://www.kaggle.com/c/wongnai-challenge-review-rating-prediction/overview

### Languages

Thai

## Dataset Structure

### Data Fields

- review_body - text of review
- star_rating - an integer star rating (1-5) or -1 (for test)

### Data Splits

Designated train (40,000 reviews) and test (6,204) sets.

Test splits do not have a star rating disclosed, so -1 will be returned.

### Source Data

#### Initial Data Collection and Normalization

Data was collected by Wongnai from business reviews on their website,
and shared on GitHub and Kaggle.

### Annotations

The reviews are users' own star ratings, so no additional annotation was needed.

## Additional Information

### Dataset Curators

Contributors to original GitHub repo:
- Ekkalak Thongthanomkul
- Tanapol Nearunchorn
- Yuwat Chuesathuchon

### Licensing Information

LGPL-3.0

### Citation Information

See https://github.com/wongnai/wongnai-corpus
