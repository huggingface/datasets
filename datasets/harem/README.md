---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- pt
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [HAREM homepage](https://www.linguateca.pt/primeiroHAREM/harem_coleccaodourada_en.html)
- **Repository:** [HAREM repository](https://www.linguateca.pt/primeiroHAREM/harem_coleccaodourada_en.html)
- **Paper:** [HAREM: An Advanced NER Evaluation Contest for Portuguese](http://comum.rcaap.pt/bitstream/10400.26/76/1/SantosSecoCardosoVilelaLREC2006.pdf)
- **Point of Contact:** [Diana Santos](mailto:diana.santos@sintef.no)

### Dataset Summary

The HAREM is a Portuguese language corpus commonly used for Named Entity Recognition tasks. It includes about 93k words, from 129 different texts,
from several genres, and language varieties. The split of this dataset version follows the division made by [1], where 7% HAREM
documents are the validation set and the miniHAREM corpus (with about 65k words) is the test set. There are two versions of the dataset set,
a version that has a total of 10 different named entity classes (Person, Organization, Location, Value, Date, Title, Thing, Event, 
Abstraction, and Other) and a "selective" version with only 5 classes (Person, Organization, Location, Value, and Date).

It's important to note that the original version of the HAREM dataset has 2 levels of NER details, namely "Category" and "Sub-type".
The dataset version processed here ONLY USE the "Category" level of the original dataset.

[1] Souza, Fábio, Rodrigo Nogueira, and Roberto Lotufo. "BERTimbau: Pretrained BERT Models for Brazilian Portuguese." Brazilian Conference on Intelligent Systems. Springer, Cham, 2020.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Portuguese

## Dataset Structure

### Data Instances

```
{
  "id": "HAREM-871-07800",
  "ner_tags": [3, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4,
  ],
  "tokens": [
    "Abraço", "Página", "Principal", "ASSOCIAÇÃO", "DE", "APOIO", "A", "PESSOAS", "COM", "VIH", "/", "SIDA"
  ]
}
```

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"O", "B-PESSOA", "I-PESSOA", "B-ORGANIZACAO", "I-ORGANIZACAO", "B-LOCAL", "I-LOCAL", "B-TEMPO", "I-TEMPO", "B-VALOR", "I-VALOR", "B-ABSTRACCAO", "I-ABSTRACCAO", "B-ACONTECIMENTO", "I-ACONTECIMENTO", "B-COISA", "I-COISA", "B-OBRA", "I-OBRA", "B-OUTRO", "I-OUTRO"
```

The NER tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any non-initial word.

### Data Splits

The data is split into train, validation and test set for each of the two versions (default and selective). The split sizes are as follow:

| Train  | Val   | Test |
| ------ | ----- | ---- |
| 121    | 8     | 128  |

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
@inproceedings{santos2006harem,
  title={Harem: An advanced ner evaluation contest for portuguese},
  author={Santos, Diana and Seco, Nuno and Cardoso, Nuno and Vilela, Rui},
  booktitle={quot; In Nicoletta Calzolari; Khalid Choukri; Aldo Gangemi; Bente Maegaard; Joseph Mariani; Jan Odjik; Daniel Tapias (ed) Proceedings of the 5 th International Conference on Language Resources and Evaluation (LREC'2006)(Genoa Italy 22-28 May 2006)},
  year={2006}
}
```

### Contributions

Thanks to [@jonatasgrosman](https://github.com/jonatasgrosman) for adding this dataset.