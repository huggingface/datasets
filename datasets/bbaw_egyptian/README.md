---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
languages:
- de, en
licenses:
- cc-by-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1000K
source_datasets:
- extended|wikipedia
task_categories:
- question-answering
task_ids:
- extractive-qadownloads/2019-10-23_Programm_IWSLT_2019_002.pdf
---

# Dataset Card for "bbaw_egyptian"

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

## Dataset Description

- **Homepage:** [https://edoc.bbaw.de/frontdoor/index/index/docId/2919](https://edoc.bbaw.de/frontdoor/index/index/docId/2919)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [Multi-Task Modeling of Phonographic Languages: Translating Middle Egyptian Hieroglyph](https://zenodo.org/record/3524924)
- **Point of Contact:** [Philipp Wiesenbach](https://www.cl.uni-heidelberg.de/~wiesenbach/index.html)
- **Size of downloaded dataset files:** 34 MB


### Dataset Summary

This dataset comprises parallel sentences of hieroglyphic encodings, transcription and translation as used in the paper [Multi-Task Modeling of Phonographic Languages: Translating Middle Egyptian Hieroglyph](https://zenodo.org/record/3524924). The data triples are extracted from the [digital corpus of Egyptian texts](https://edoc.bbaw.de/frontdoor/index/index/docId/2919) compiled by the project "Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache".

### Supported Tasks

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

The dataset is not divided into 'train', 'dev' and 'test' split as it is not built for competitive purposes and we ask all scientists to build use partitioning for their needs. Due to the low resource setting it will probably advisable to use cross validation. The only available split 'all' therefore comprises the full 100,708 translation triples, 35,503 of which possess hieroglyphic encodings (the remaining 65,205 triples have empty `hieroglyph` entries).

### Data Instances

An example of 'all' looks as follows.
```
{                                                                                                  
    "transcription": "n rḏi̯(.w) gꜣ =j r dbḥ.t m pr-ḥḏ",                                            
    "translation": "I was not let to suffer lack in the treasury with respect to what was needed;",
    "hieroglyphs": "D35 D21 -D37 G1&W11 -V32B A1 D21 D46 -D58 *V28 -F18 *X1 -A2 G17 [? *O2 *?]"    
}                                                                                              

```

### Data Fields

#### plain_text
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### Data Splits Sample Size

|   name   |all|
|----------|----:|
|plain_text|100708|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@article{2016arXiv160605250R,
       author = {{Rajpurkar}, Pranav and {Zhang}, Jian and {Lopyrev},
                 Konstantin and {Liang}, Percy},
        title = "{SQuAD: 100,000+ Questions for Machine Comprehension of Text}",
      journal = {arXiv e-prints},
         year = 2016,
          eid = {arXiv:1606.05250},
        pages = {arXiv:1606.05250},
archivePrefix = {arXiv},
       eprint = {1606.05250},
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@albertvillanova](https://github.com/albertvillanova), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
