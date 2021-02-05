---
annotations_creators:
- found
language_creators:
- found
languages:
  neen:
  - en
  - ne
  sien:
  - en
  - si
licenses:
- cc-by-4.0
multilinguality:
- translation
size_categories:
- 1K<n<10K
source_datasets:
- extended|wikipedia
- extended|opus_gnome
- extended|opus_ubuntu
- extended|open_subtitles
- extended|paracrawl
- extended|bible_para
- extended|kde4
- extended|other-global-voices
- extended|other-common-crawl
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---

# Dataset Card for "flores"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://github.com/facebookresearch/flores/](https://github.com/facebookresearch/flores/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 2.94 MB
- **Size of the generated dataset:** 3.69 MB
- **Total amount of disk used:** 6.63 MB

### [Dataset Summary](#dataset-summary)

Evaluation datasets for low-resource machine translation: Nepali-English and Sinhala-English.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### neen

- **Size of downloaded dataset files:** 1.47 MB
- **Size of the generated dataset:** 1.77 MB
- **Total amount of disk used:** 3.24 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"en\": \"This is the wrong translation!\", \"ne\": \"यस वाहेक आगम पूजा, तारा पूजा, व्रत आदि पनि घरभित्र र वाहिर दुवै स्थानमा गरेको पा..."
}
```

#### sien

- **Size of downloaded dataset files:** 1.47 MB
- **Size of the generated dataset:** 1.92 MB
- **Total amount of disk used:** 3.40 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "translation": "{\"en\": \"This is the wrong translation!\", \"si\": \"එවැනි ආවරණයක් ලබාදීමට රක්ෂණ සපයන්නෙකු කැමති වුවත් ඒ සාමාන් යයෙන් බොහෝ රටවල පොදු ..."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### neen
- `translation`: a multilingual `string` variable, with possible languages including `ne`, `en`.

#### sien
- `translation`: a multilingual `string` variable, with possible languages including `si`, `en`.

### [Data Splits Sample Size](#data-splits-sample-size)

|name|validation|test|
|----|---------:|---:|
|neen|      2560|2836|
|sien|      2899|2767|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```
@misc{guzmn2019new,
    title={Two New Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English},
    author={Francisco Guzman and Peng-Jen Chen and Myle Ott and Juan Pino and Guillaume Lample and Philipp Koehn and Vishrav Chaudhary and Marc'Aurelio Ranzato},
    year={2019},
    eprint={1902.01382},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten), [@lewtun](https://github.com/lewtun) for adding this dataset.