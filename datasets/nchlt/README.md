---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- af
- nr
- nso
- ss
- tn
- ts
- ve
- xh
- zu
license:
- cc-by-2.5
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: null
pretty_name: NCHLT
dataset_info:
- config_name: af
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3955069
    num_examples: 8961
  download_size: 25748344
  dataset_size: 3955069
- config_name: nr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3188781
    num_examples: 9334
  download_size: 20040327
  dataset_size: 3188781
- config_name: xh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 2365821
    num_examples: 6283
  download_size: 14513302
  dataset_size: 2365821
- config_name: zu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3951366
    num_examples: 10955
  download_size: 25097584
  dataset_size: 3951366
- config_name: nso-sepedi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3322296
    num_examples: 7116
  download_size: 22077376
  dataset_size: 3322296
- config_name: nso-sesotho
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 4427898
    num_examples: 9471
  download_size: 30421109
  dataset_size: 4427898
- config_name: tn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3812339
    num_examples: 7943
  download_size: 25905236
  dataset_size: 3812339
- config_name: ss
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3431063
    num_examples: 10797
  download_size: 21882224
  dataset_size: 3431063
- config_name: ve
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3941041
    num_examples: 8477
  download_size: 26382457
  dataset_size: 3941041
- config_name: ts
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: OUT
          1: B-PERS
          2: I-PERS
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
          7: B-MISC
          8: I-MISC
  splits:
  - name: train
    num_bytes: 3941041
    num_examples: 8477
  download_size: 26382457
  dataset_size: 3941041
---
# Dataset Card for NCHLT

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

- **Homepage:** [link](https://repo.sadilar.org/handle/20.500.12185/7/discover?filtertype_0=database&filtertype_1=title&filter_relational_operator_1=contains&filter_relational_operator_0=equals&filter_1=&filter_0=Monolingual+Text+Corpora%3A+Annotated&filtertype=project&filter_relational_operator=equals&filter=NCHLT+Text+II)
- **Repository:** []()
- **Paper:** []()
- **Leaderboard:** []()
- **Point of Contact:** []()

### Dataset Summary

The development of linguistic resources for use in natural language processingis of utmost importance for the continued growth of research anddevelopment in the field, especially for resource-scarce languages. In this paper we describe the process and challenges of simultaneouslydevelopingmultiple linguistic resources for ten of the official languages of South Africa. The project focussed on establishing a set of foundational resources that can foster further development of both resources and technologies for the NLP industry in South Africa. The development efforts during the project included creating monolingual unannotated corpora, of which a subset of the corpora for each language was annotated on token, orthographic, morphological and morphosyntactic layers. The annotated subsetsincludes both development and test setsand were used in the creation of five core-technologies, viz. atokeniser, sentenciser,lemmatiser, part of speech tagger and morphological decomposer for each language. We report on the quality of these tools for each language and provide some more context of the importance of the resources within the South African context.



### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

[More Information Needed]

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation


### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

Martin.Puttkammer@nwu.ac.za

### Licensing Information

[More Information Needed]

### Citation Information

```
@inproceedings{eiselen2014developing,
  title={Developing Text Resources for Ten South African Languages.},
  author={Eiselen, Roald and Puttkammer, Martin J},
  booktitle={LREC},
  pages={3698--3703},
  year={2014}
}
```


### Contributions

Thanks to [@Narsil](https://github.com/Narsil) for adding this dataset.