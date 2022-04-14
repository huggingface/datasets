---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- af
- ' ar'
- ' ast'
- ' azb'
- ' be'
- ' bg'
- ' bn'
- ' br'
- ' ca'
- ' cs'
- ' cy'
- ' da'
- ' de'
- ' el'
- ' en'
- ' eo'
- ' es'
- ' et'
- ' eu'
- ' fa'
- ' fi'
- ' fr'
- ' fy'
- ' ga'
- ' gl'
- ' hr'
- ' hu'
- ' hy'
- ' id'
- ' it'
- ' iw'
- ' ja'
- ' ka'
- ' ko'
- ' la'
- ' lt'
- ' lv'
- ' mk'
- ' ml'
- ' ms'
- ' nl'
- ' nn'
- ' no'
- ' pl'
- ' pt'
- ' ro'
- ' ru'
- ' sk'
- ' sl'
- ' sr'
- ' sv'
- ' th'
- ' tr'
- ' uk'
- ' ur'
- ' vi'
- ' vo'
- ' zh'
licenses:
- cc-by-sa-4.0
multilinguality:
- multilingual
paperswithcode_id: wit
pretty_name: wikipedia_image_text
size_categories:
- 10M<n<100M
source_datasets:
- original
- extended|wikipedia
task_categories:
- text-retrieval
- other
task_ids:
- text-retrieval-other-text-image-retrieval
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

- **Homepage:** https://github.com/google-research-datasets/wit
- **Repository:** https://github.com/google-research-datasets/wit
- **Paper:** https://arxiv.org/abs/2103.01913
- **Leaderboard:** https://www.kaggle.com/c/wikipedia-image-caption
- **Point of Contact:** krishnaps@google.com

### Dataset Summary

Wikipedia-based Image Text (WIT) Dataset is a large multimodal multilingual dataset. WIT is composed of a curated set of 37.6 million entity rich image-text examples with 11.5 million unique images across 108 Wikipedia languages. Its size enables WIT to be used as a pretraining dataset for multimodal machine learning models.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset contains examples from all Wikipedia languages, with the following stats:

Image-Text   | # Lang | Uniq. Images  | # Lang
------------ | ------ | ------------- | ------
total > 1M   | 9      | images > 1M   | 6
total > 500K | 10     | images > 500K | 12
total > 100K | 36     | images > 100K | 35
total > 50K  | 15     | images > 50K  | 17
total > 14K  | 38     | images > 13K  | 38

## Dataset Structure

### Data Instances

Each instance is an image, its representation in bytes, a pre-computed embedding, and the set of captions attached to the image in Wikipedia.

### Data Fields

- `b64_bytes`
- `embedding`
- `image_url`
- `metadata_url`
- `original_height`
- `original_width`
- `mime_type`
- `caption_attribution_description`
- `wit_features`: sequence of captions with language, page URL, information about the page, caption text, etc.

### Data Splits

Type          | Train  | Val    | Test   | Total / Unique
------------- | ------ | ------ | ------ | --------------
Rows / Tuples | 37.13M | 261.8K | 210.7K | 37.6M
Unique Images | 11.4M  | 58K    | 57K    | 11.5M
Ref. Text     | 16.9M  | 150K   | 104K   | 17.2M / 16.7M
Attr. Text    | 34.8M  | 193K   | 200K   | 35.2M / 10.9M
Alt Text      | 5.3M   | 29K    | 29K    | 5.4M / 5.3M
Context Texts | -      | -      | -      | 119.8M

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

```bibtex
@article{srinivasan2021wit,
  title={WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning},
  author={Srinivasan, Krishna and Raman, Karthik and Chen, Jiecao and Bendersky, Michael and Najork, Marc},
  journal={arXiv preprint arXiv:2103.01913},
  year={2021}
}```

### Contributions

Thanks to [@thomasw21](https://github.com/thomasw21), [@nateraw](https://github.com/nateraw) and [hassiahk](https://github.com/hassiahk) for adding this dataset.