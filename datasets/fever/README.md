---
---

# Dataset Card for "fever"

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

- **Homepage:** [https://fever.ai/](https://fever.ai/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1677.26 MB
- **Size of the generated dataset:** 6959.34 MB
- **Total amount of disk used:** 8636.60 MB

### [Dataset Summary](#dataset-summary)

With billions of individual pages on the web providing information on almost every conceivable topic, we should have the ability to collect facts that answer almost every conceivable question. However, only a small fraction of this information is contained in structured sources (Wikidata, Freebase, etc.) – we are therefore limited by our ability to transform free-form text to structured knowledge. There is, however, another problem that has become the focus of a lot of recent research and media coverage: false information coming from unreliable sources. [1] [2]

The FEVER workshops are a venue for work in verifiable knowledge extraction and to stimulate progress in this direction.

FEVER  V1.0

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### v1.0

- **Size of downloaded dataset files:** 42.78 MB
- **Size of the generated dataset:** 38.39 MB
- **Total amount of disk used:** 81.17 MB

An example of 'train' looks as follows.
```

```

#### v2.0

- **Size of downloaded dataset files:** 0.37 MB
- **Size of the generated dataset:** 0.29 MB
- **Total amount of disk used:** 0.67 MB

An example of 'validation' looks as follows.
```

```

#### wiki_pages

- **Size of downloaded dataset files:** 1634.11 MB
- **Size of the generated dataset:** 6920.65 MB
- **Total amount of disk used:** 8554.76 MB

An example of 'wikipedia_pages' looks as follows.
```

```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### v1.0
- `id`: a `int32` feature.
- `label`: a `string` feature.
- `claim`: a `string` feature.
- `evidence_annotation_id`: a `int32` feature.
- `evidence_id`: a `int32` feature.
- `evidence_wiki_url`: a `string` feature.
- `evidence_sentence_id`: a `int32` feature.

#### v2.0
- `id`: a `int32` feature.
- `label`: a `string` feature.
- `claim`: a `string` feature.
- `evidence_annotation_id`: a `int32` feature.
- `evidence_id`: a `int32` feature.
- `evidence_wiki_url`: a `string` feature.
- `evidence_sentence_id`: a `int32` feature.

#### wiki_pages
- `id`: a `string` feature.
- `text`: a `string` feature.
- `lines`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

#### v1.0

|    |train |unlabelled_dev|labelled_dev|paper_dev|unlabelled_test|paper_test|
|----|-----:|-------------:|-----------:|--------:|--------------:|---------:|
|v1.0|311431|         19998|       37566|    18999|          19998|     18567|

#### v2.0

|    |validation|
|----|---------:|
|v2.0|      2384|

#### wiki_pages

|          |wikipedia_pages|
|----------|--------------:|
|wiki_pages|        5416537|

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

@inproceedings{Thorne18Fever,
    author = {Thorne, James and Vlachos, Andreas and Christodoulopoulos, Christos and Mittal, Arpit},
    title = {{FEVER}: a Large-scale Dataset for Fact Extraction and VERification},
    booktitle = {NAACL-HLT},
    year = {2018}
}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lhoestq](https://github.com/lhoestq), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun) for adding this dataset.