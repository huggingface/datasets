---
annotations_creators: []
language_creators: []
languages:
- es
licenses:
- cc-by-2.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
- conditional-text-generation
task_ids:
- sentiment-classification
- summarization
---

# Dataset Card for Muchocine

## Dataset Description

- **Homepage: ** http://www.lsi.us.es/~fermin/index.php/Datasets

### Dataset Summary

The Muchocine reviews dataset contains 3,872 longform movie reviews in Spanish language,
each with a shorter summary review, and a rating on a 1-5 scale.

### Languages

Spanish

## Dataset Structure

### Data Fields

- review_body - longform review
- review_summary - shorter-form review
- star_rating - an integer star rating (1-5)

The original source also includes part-of-speech tagging for body and summary fields.

### Data Splits

One split (train) with 3,872 reviews

### Source Data

#### Initial Data Collection and Normalization

Data was collected from www.muchocine.net and uploaded by Dr. Fermín L. Cruz Mata
of La Universidad de Sevilla

### Annotations

The reviews came with star ratings, so no additional annotation was needed.

## Additional Information

### Dataset Curators

- Dr. Fermín L. Cruz Mata

### Licensing Information

CC-BY-2.1

### Citation Information

See http://www.lsi.us.es/~fermin/index.php/Datasets
