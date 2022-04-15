---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- af
- ar
- ast
- azb
- be
- bg
- bn
- br
- ca
- cs
- cy
- da
- de
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fr
- fy
- ga
- gl
- hr
- hu
- hy
- id
- it
- iw
- ja
- ka
- ko
- la
- lt
- lv
- mk
- ml
- ms
- nl
- nn
- 'no'
- pl
- pt
- ro
- ru
- sk
- sl
- sr
- sv
- th
- tr
- uk
- ur
- vi
- vo
- zh
licenses:
- cc-by-sa-3.0
multilinguality:
- multilingual
paperswithcode_id: wit
pretty_name: Wikipedia-based Image Text
size_categories:
- 10M<n<100M
source_datasets:
- original
- extended|wikipedia
task_categories:
- text-retrieval
- image-to-text
task_ids:
- text-retrieval-other-text-image-retrieval
- image-captioning
---

# Dataset Card for WIT

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

- **Homepage:** [WIT homepage](https://github.com/google-research-datasets/wit)
- **Repository:** [WIT repository](https://github.com/google-research-datasets/wit)
- **Paper:** [WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning
](https://arxiv.org/abs/2103.01913)
- **Leaderboard:** [WIT leaderboard](https://www.kaggle.com/c/wikipedia-image-caption)
- **Point of Contact:** [WIT e-mail](mailto:wit-dataset@google.com)

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

```
{
  'language': 'en', '
  'page_url': 'https://en.wikipedia.org/wiki/Oxydactylus',
  'image_url': 'https://upload.wikimedia.org/wikipedia/commons/5/5f/Oxydactylus_longipes_fm.jpg',
  'page_title': 'Oxydactylus',
  'section_title': None,
  'hierarchical_section_title': 'Oxydactylus',
  'caption_reference_description': None,
  'caption_attribution_description': 'English: Mounted skeleton of Oxydactylus longipes in the Field Museum of Natural History.',
  'caption_alt_text_description': None,
  'mime_type': 'image/jpeg',
  'original_height': 3564,
  'original_width': 2748,
  'is_main_image': True,
  'attribution_passes_lang_id': True,
  'page_changed_recently': True,
  'context_page_description': 'Oxydactylus is an extinct genus of camelid endemic to North America. It lived from the Late Oligocene to the Middle Miocene, existing for approximately 14 million years. The name is from the Ancient Greek οξύς and δάκτυλος.\nThey had very long legs and necks, and were probably adapted to eating high vegetation, much like modern giraffes. Unlike modern camelids, they had hooves, rather than tough sole-pads, and splayed toes.',
  'context_section_description': 'Oxydactylus is an extinct genus of camelid endemic to North America. It lived from the Late Oligocene to the Middle Miocene (28.4–13.7 mya), existing for approximately 14 million years. The name is from the Ancient Greek οξύς (oxys, "sharp")and δάκτυλος (daktylos, "finger").\n \nThey had very long legs and necks, and were probably adapted to eating high vegetation, much like modern giraffes. Unlike modern camelids, they had hooves, rather than tough sole-pads, and splayed toes.'
}
```
### Data Fields

- `language`
- `page_url`
- `image_url`
- `page_title`
- `section_title`
- `hierarchical_section_title`
- `caption_reference_description`
- `caption_attribution_description`
- `caption_alt_text_description`
- `mime_type`
- `original_height`
- `original_width`
- `is_main_image`
- `attribution_passes_lang_id`
- `page_changed_recently`
- `context_page_description`
- `context_section_description`

Details on the field content can be found directly in the [paper, figure 5 and table 12.](https://arxiv.org/abs/2103.01913)

### Data Splits

All data is held in `train` split, with a total of 37046386 rows.

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
}
```

### Contributions

Thanks to [@thomasw21](https://github.com/thomasw21), [@nateraw](https://github.com/nateraw) and [hassiahk](https://github.com/hassiahk) for adding this dataset.