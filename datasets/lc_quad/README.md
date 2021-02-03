---
---

# Dataset Card for "lc_quad"

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

- **Homepage:** [http://lc-quad.sda.tech/](http://lc-quad.sda.tech/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3.69 MB
- **Size of the generated dataset:** 19.77 MB
- **Total amount of disk used:** 23.46 MB

### [Dataset Summary](#dataset-summary)

LC-QuAD 2.0 is a Large Question Answering dataset with 30,000 pairs of question and its corresponding SPARQL query. The target knowledge base is Wikidata and DBpedia, specifically the 2018 version. Please see our paper for details about the dataset creation process and framework.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 3.69 MB
- **Size of the generated dataset:** 19.77 MB
- **Total amount of disk used:** 23.46 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "NNQT_question": "What is the {periodical literature} for {mouthpiece} of {Delta Air Lines}",
    "paraphrased_question": "What is Delta Air Line's periodical literature mouthpiece?",
    "question": "What periodical literature does Delta Air Lines use as a moutpiece?",
    "sparql_dbpedia18": "\"select distinct ?obj where { ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resou...",
    "sparql_wikidata": " select distinct ?obj where { wd:Q188920 wdt:P2813 ?obj . ?obj wdt:P31 wd:Q1002697 } ",
    "subgraph": "simple question right",
    "template": " <S P ?O ; ?O instanceOf Type>",
    "template_index": 65,
    "uid": 19719
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `NNQT_question`: a `string` feature.
- `uid`: a `int32` feature.
- `subgraph`: a `string` feature.
- `template_index`: a `int32` feature.
- `question`: a `string` feature.
- `sparql_wikidata`: a `string` feature.
- `sparql_dbpedia18`: a `string` feature.
- `template`: a `string` feature.
- `paraphrased_question`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train|test|
|-------|----:|---:|
|default|19293|4781|

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

@inproceedings{dubey2017lc2,
title={LC-QuAD 2.0: A Large Dataset for Complex Question Answering over Wikidata and DBpedia},
author={Dubey, Mohnish and Banerjee, Debayan and Abdelkawi, Abdelrahman and Lehmann, Jens},
booktitle={Proceedings of the 18th International Semantic Web Conference (ISWC)},
year={2019},
organization={Springer}
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@patrickvonplaten](https://github.com/patrickvonplaten) for adding this dataset.