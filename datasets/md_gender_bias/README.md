---
annotations_creators:
  convai2_inferred:
  - machine-generated
  funpedia:
  - found
  gendered_words:
  - found
  image_chat:
  - found
  light_inferred:
  - machine-generated
  name_genders:
  - found
  new_data:
  - crowdsourced
  - found
  opensubtitles_inferred:
  - machine-generated
  wizard:
  - found
  yelp_inferred:
  - machine-generated
language_creators:
  convai2_inferred:
  - found
  funpedia:
  - found
  gendered_words:
  - found
  image_chat:
  - found
  light_inferred:
  - found
  name_genders:
  - found
  new_data:
  - crowdsourced
  - found
  opensubtitles_inferred:
  - found
  wizard:
  - found
  yelp_inferred:
  - found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  convai2_inferred:
  - 100K<n<1M
  funpedia:
  - 10K<n<100K
  gendered_words:
  - n<1K
  image_chat:
  - 100K<n<1M
  light_inferred:
  - 100K<n<1M
  name_genders:
  - n>1M
  new_data:
  - 1K<n<10K
  opensubtitles_inferred:
  - 100K<n<1M
  wizard:
  - 10K<n<100K
  yelp_inferred:
  - n>1M
source_datasets:
  convai2_inferred:
  - extended|other-convai2
  - original
  funpedia:
  - original
  gendered_words:
  - original
  image_chat:
  - original
  light_inferred:
  - extended|other-light
  - original
  name_genders:
  - original
  new_data:
  - original
  opensubtitles_inferred:
  - extended|other-opensubtitles
  - original
  wizard:
  - original
  yelp_inferred:
  - extended|other-yelp
  - original
task_categories:
- text-classification
task_ids:
- text-classification-other-gender-bias
---

# Dataset Card for Multi-Dimensional Gender Bias Classification

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

- **Homepage:** https://parl.ai/projects/md_gender/
- **Repository:** [Needs More Information]
- **Paper:** https://arxiv.org/abs/2005.00614
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** edinan@fb.com

### Dataset Summary

Machine learning models are trained to find patterns in data.
NLP models can inadvertently learn socially undesirable patterns when training on gender biased text.
In this work, we propose a general framework that decomposes gender bias in text along several pragmatic and semantic dimensions:
bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker.
Using this fine-grained framework, we automatically annotate eight large scale datasets with gender information.
In addition, we collect a novel, crowdsourced evaluation benchmark of utterance-level gender rewrites.
Distinguishing between gender bias along multiple dimensions is important, as it enables us to train finer-grained gender bias classifiers.
We show our classifiers prove valuable for a variety of important applications, such as controlling for gender bias in generative models,
detecting gender bias in arbitrary text, and shed light on offensive language in terms of genderedness.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The data is in English (`en`)

## Dataset Structure

### Data Instances

[Needs More Information]

### Data Fields

The data has the following features.

For the `new_data` config:
- `text`: the text to be classified
- `original`: the text before reformulation
- `labels`: a `list` of classification labels, with possible values including `ABOUT:female`, `ABOUT:male`, `PARTNER:female`, `PARTNER:male`, `SELF:female`.
- `class_type`: a classification label, with possible values including `about`, `partner`, `self`.
- `turker_gender`: a classification label, with possible values including `man`, `woman`, `nonbinary`, `prefer not to say`, `no answer`.

For the other annotated datasets:
- `text`: the text to be classified.
- `gender`: a classification label, with possible values including `gender-neutral`, `female`, `male`.

For the `_inferred` configurations:
- `text`: the text to be classified.
- `binary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`.
- `binary_score`: a score between 0 and 1.
- `ternary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`, `ABOUT:gender-neutral`.
- `ternary_score`: a score between 0 and 1.

### Data Splits

The different parts of the data can be accessed through the different configurations:
- `gendered_words`: A list of common nouns with a masculine and feminine variant.
- `new_data`: Sentences reformulated and annotated along all three axes.
- `funpedia`, `wizard`: Sentences from Funpedia and Wizards of Wikipedia annotated with ABOUT gender with entity gender information.
- `image_chat`: sentences about images annotated  with ABOUT gender based on gender information from the entities in the image
- `convai2_inferred`, `light_inferred`, `opensubtitles_inferred`, `yelp_inferred`:  Data from several source datasets with ABOUT annotations inferred by a trined classifier.


## Dataset Creation

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

[Needs More Information]

### Citation Information

[Needs More Information]
### Contributions

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.