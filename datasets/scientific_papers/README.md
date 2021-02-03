---
---

# Dataset Card for "scientific_papers"

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

- **Homepage:** [https://github.com/armancohan/long-summarization](https://github.com/armancohan/long-summarization)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 8591.93 MB
- **Size of the generated dataset:** 9622.19 MB
- **Total amount of disk used:** 18214.12 MB

### [Dataset Summary](#dataset-summary)

Scientific papers datasets contains two sets of long and structured documents.
The datasets are obtained from ArXiv and PubMed OpenAccess repositories.

Both "arxiv" and "pubmed" have two features:
  - article: the body of the document, pagragraphs seperated by "/n".
  - abstract: the abstract of the document, pagragraphs seperated by "/n".
  - section_names: titles of sections, seperated by "/n".

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### arxiv

- **Size of downloaded dataset files:** 4295.97 MB
- **Size of the generated dataset:** 7231.70 MB
- **Total amount of disk used:** 11527.66 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\" we have studied the leptonic decay @xmath0 , via the decay channel @xmath1 , using a sample of tagged @xmath2 decays collected...",
    "article": "\"the leptonic decays of a charged pseudoscalar meson @xmath7 are processes of the type @xmath8 , where @xmath9 , @xmath10 , or @...",
    "section_names": "[sec:introduction]introduction\n[sec:detector]data and the cleo- detector\n[sec:analysys]analysis method\n[sec:conclusion]summary"
}
```

#### pubmed

- **Size of downloaded dataset files:** 4295.97 MB
- **Size of the generated dataset:** 2390.49 MB
- **Total amount of disk used:** 6686.46 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\" background and aim : there is lack of substantial indian data on venous thromboembolism ( vte ) . \\n the aim of this study was...",
    "article": "\"approximately , one - third of patients with symptomatic vte manifests pe , whereas two - thirds manifest dvt alone .\\nboth dvt...",
    "section_names": "\"Introduction\\nSubjects and Methods\\nResults\\nDemographics and characteristics of venous thromboembolism patients\\nRisk factors ..."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### arxiv
- `article`: a `string` feature.
- `abstract`: a `string` feature.
- `section_names`: a `string` feature.

#### pubmed
- `article`: a `string` feature.
- `abstract`: a `string` feature.
- `section_names`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name |train |validation|test|
|------|-----:|---------:|---:|
|arxiv |203037|      6436|6440|
|pubmed|119924|      6633|6658|

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

@article{Cohan_2018,
   title={A Discourse-Aware Attention Model for Abstractive Summarization of
            Long Documents},
   url={http://dx.doi.org/10.18653/v1/n18-2097},
   DOI={10.18653/v1/n18-2097},
   journal={Proceedings of the 2018 Conference of the North American Chapter of
          the Association for Computational Linguistics: Human Language
          Technologies, Volume 2 (Short Papers)},
   publisher={Association for Computational Linguistics},
   author={Cohan, Arman and Dernoncourt, Franck and Kim, Doo Soon and Bui, Trung and Kim, Seokhwan and Chang, Walter and Goharian, Nazli},
   year={2018}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jplu](https://github.com/jplu), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.