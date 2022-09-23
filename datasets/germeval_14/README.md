---
paperswithcode_id: null
pretty_name: GermEval14
dataset_info:
  features:
  - name: id
    dtype: string
  - name: source
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-LOC
          2: I-LOC
          3: B-LOCderiv
          4: I-LOCderiv
          5: B-LOCpart
          6: I-LOCpart
          7: B-ORG
          8: I-ORG
          9: B-ORGderiv
          10: I-ORGderiv
          11: B-ORGpart
          12: I-ORGpart
          13: B-OTH
          14: I-OTH
          15: B-OTHderiv
          16: I-OTHderiv
          17: B-OTHpart
          18: I-OTHpart
          19: B-PER
          20: I-PER
          21: B-PERderiv
          22: I-PERderiv
          23: B-PERpart
          24: I-PERpart
  - name: nested_ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-LOC
          2: I-LOC
          3: B-LOCderiv
          4: I-LOCderiv
          5: B-LOCpart
          6: I-LOCpart
          7: B-ORG
          8: I-ORG
          9: B-ORGderiv
          10: I-ORGderiv
          11: B-ORGpart
          12: I-ORGpart
          13: B-OTH
          14: I-OTH
          15: B-OTHderiv
          16: I-OTHderiv
          17: B-OTHpart
          18: I-OTHpart
          19: B-PER
          20: I-PER
          21: B-PERderiv
          22: I-PERderiv
          23: B-PERpart
          24: I-PERpart
  config_name: germeval_14
  splits:
  - name: test
    num_bytes: 2943201
    num_examples: 5100
  - name: train
    num_bytes: 13816714
    num_examples: 24000
  - name: validation
    num_bytes: 1266974
    num_examples: 2200
  download_size: 10288972
  dataset_size: 18026889
---

# Dataset Card for "germeval_14"

## Table of Contents
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

- **Homepage:** [https://sites.google.com/site/germeval2014ner/](https://sites.google.com/site/germeval2014ner/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 9.81 MB
- **Size of the generated dataset:** 17.19 MB
- **Total amount of disk used:** 27.00 MB

### Dataset Summary

The GermEval 2014 NER Shared Task builds on a new dataset with German Named Entity annotation with the following properties:    - The data was sampled from German Wikipedia and News Corpora as a collection of citations.    - The dataset covers over 31,000 sentences corresponding to over 590,000 tokens.    - The NER annotation uses the NoSta-D guidelines, which extend the Tübingen Treebank guidelines,      using four main NER categories with sub-structure, and annotating embeddings among NEs      such as [ORG FC Kickers [LOC Darmstadt]].

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### germeval_14

- **Size of downloaded dataset files:** 9.81 MB
- **Size of the generated dataset:** 17.19 MB
- **Total amount of disk used:** 27.00 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "id": "11",
    "ner_tags": [13, 14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 19, 20, 13, 0, 1, 0, 0, 0, 0, 0, 19, 20, 20, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "nested_ner_tags": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "source": "http://de.wikipedia.org/wiki/Liste_von_Filmen_mit_homosexuellem_Inhalt [2010-01-11] ",
    "tokens": "[\"Scenes\", \"of\", \"a\", \"Sexual\", \"Nature\", \"(\", \"GB\", \"2006\", \")\", \"-\", \"Regie\", \":\", \"Ed\", \"Blum\", \"Shortbus\", \"(\", \"USA\", \"2006..."
}
```

### Data Fields

The data fields are the same among all splits.

#### germeval_14
- `id`: a `string` feature.
- `source`: a `string` feature.
- `tokens`: a `list` of `string` features.
- `ner_tags`: a `list` of classification labels, with possible values including `O` (0), `B-LOC` (1), `I-LOC` (2), `B-LOCderiv` (3), `I-LOCderiv` (4).
- `nested_ner_tags`: a `list` of classification labels, with possible values including `O` (0), `B-LOC` (1), `I-LOC` (2), `B-LOCderiv` (3), `I-LOCderiv` (4).

### Data Splits

|   name    |train|validation|test|
|-----------|----:|---------:|---:|
|germeval_14|24000|      2200|5100|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

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
@inproceedings{benikova-etal-2014-nosta,
    title = {NoSta-D Named Entity Annotation for German: Guidelines and Dataset},
    author = {Benikova, Darina  and
      Biemann, Chris  and
      Reznicek, Marc},
    booktitle = {Proceedings of the Ninth International Conference on Language Resources and Evaluation ({LREC}'14)},
    month = {may},
    year = {2014},
    address = {Reykjavik, Iceland},
    publisher = {European Language Resources Association (ELRA)},
    url = {http://www.lrec-conf.org/proceedings/lrec2014/pdf/276_Paper.pdf},
    pages = {2524--2531},
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jplu](https://github.com/jplu), [@lewtun](https://github.com/lewtun), [@lhoestq](https://github.com/lhoestq), [@stefan-it](https://github.com/stefan-it), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.