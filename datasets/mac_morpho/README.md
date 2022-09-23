---
pretty_name: Mac-Morpho
annotations_creators:
- expert-generated
language_creators:
- found
language:
- pt
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- part-of-speech
paperswithcode_id: null
dataset_info:
  features:
  - name: id
    dtype: string
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: PREP+PROADJ
          1: IN
          2: PREP+PRO-KS
          3: NPROP
          4: PREP+PROSUB
          5: KC
          6: PROPESS
          7: NUM
          8: PROADJ
          9: PREP+ART
          10: KS
          11: PRO-KS
          12: ADJ
          13: ADV-KS
          14: N
          15: PREP
          16: PROSUB
          17: PREP+PROPESS
          18: PDEN
          19: V
          20: PREP+ADV
          21: PCP
          22: CUR
          23: ADV
          24: PU
          25: ART
  splits:
  - name: test
    num_bytes: 3095292
    num_examples: 9987
  - name: train
    num_bytes: 12635011
    num_examples: 37948
  - name: validation
    num_bytes: 671356
    num_examples: 1997
  download_size: 2463485
  dataset_size: 16401659
---

# Dataset Card for Mac-Morpho

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

- **Homepage:** [Mac-Morpho homepage](http://nilc.icmc.usp.br/macmorpho/)
- **Repository:** [Mac-Morpho repository](http://nilc.icmc.usp.br/macmorpho/)
- **Paper:** [Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese](https://journal-bcs.springeropen.com/articles/10.1186/s13173-014-0020-x)
- **Point of Contact:** [Erick R Fonseca](mailto:erickrfonseca@gmail.com)

### Dataset Summary

Mac-Morpho is a corpus of Brazilian Portuguese texts annotated with part-of-speech tags. 
Its first version was released in 2003 [1], and since then, two revisions have been made in order 
to improve the quality of the resource [2, 3].
The corpus is available for download split into train, development and test sections. 
These are 76%, 4% and 20% of the corpus total, respectively (the reason for the unusual numbers 
is that the corpus was first split into 80%/20% train/test, and then 5% of the train section was 
set aside for development). This split was used in [3], and new POS tagging research with Mac-Morpho 
is encouraged to follow it in order to make consistent comparisons possible.


[1] Aluísio, S., Pelizzoni, J., Marchi, A.R., de Oliveira, L., Manenti, R., Marquiafável, V. 2003. 
An account of the challenge of tagging a reference corpus for brazilian portuguese. 
In: Proceedings of the 6th International Conference on Computational Processing of the Portuguese Language. PROPOR 2003

[2] Fonseca, E.R., Rosa, J.L.G. 2013. Mac-morpho revisited: Towards robust part-of-speech. 
In: Proceedings of the 9th Brazilian Symposium in Information and Human Language Technology – STIL

[3] Fonseca, E.R., Aluísio, Sandra Maria, Rosa, J.L.G. 2015. 
Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese. 
Journal of the Brazilian Computer Society.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Portuguese

## Dataset Structure

### Data Instances

An example from the Mac-Morpho dataset looks as follows:

```
{
    "id": "0",
    "pos_tags": [14, 19, 14, 15, 22, 7, 14, 9, 14, 9, 3, 15, 3, 3, 24],
    "tokens": ["Jersei", "atinge", "média", "de", "Cr$", "1,4", "milhão", "na", "venda", "da", "Pinhal", "em", "São", "Paulo", "."]
}
```

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `pos`: the PoS tags of each token

The PoS tags correspond to this list:
```
"PREP+PROADJ", "IN", "PREP+PRO-KS", "NPROP", "PREP+PROSUB", "KC", "PROPESS", "NUM", "PROADJ", "PREP+ART", "KS", 
"PRO-KS", "ADJ", "ADV-KS", "N", "PREP", "PROSUB", "PREP+PROPESS", "PDEN", "V", "PREP+ADV", "PCP", "CUR", "ADV", "PU", "ART"
```

### Data Splits

The data is split into train, validation and test set. The split sizes are as follow:

| Train  | Val   | Test  |
| ------ | ----- | ----- |
| 37948  | 1997  | 9987  |

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

```
@article{fonseca2015evaluating,
  title={Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese},
  author={Fonseca, Erick R and Rosa, Jo{\~a}o Lu{\'\i}s G and Alu{\'\i}sio, Sandra Maria},
  journal={Journal of the Brazilian Computer Society},
  volume={21},
  number={1},
  pages={2},
  year={2015},
  publisher={Springer}
}
```

### Contributions

Thanks to [@jonatasgrosman](https://github.com/jonatasgrosman) for adding this dataset.