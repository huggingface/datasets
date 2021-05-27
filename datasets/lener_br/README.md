---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- pt
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: lener-br
---

# Dataset Card for leNER-br

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

- **Homepage:** [leNER-BR homepage](https://cic.unb.br/~teodecampos/LeNER-Br/)
- **Repository:** [leNER-BR repository](https://github.com/peluz/lener-br)
- **Paper:** [leNER-BR: Long Form Question Answering](https://cic.unb.br/~teodecampos/LeNER-Br/luz_etal_propor2018.pdf)
- **Point of Contact:** [Pedro H. Luz de Araujo](mailto:pedrohluzaraujo@gmail.com)

### Dataset Summary

LeNER-Br is a Portuguese language dataset for named entity recognition 
applied to legal documents. LeNER-Br consists entirely of manually annotated 
legislation and legal cases texts and contains tags for persons, locations, 
time entities, organizations, legislation and legal cases.
To compose the dataset, 66 legal documents from several Brazilian Courts were
collected. Courts of superior and state levels were considered, such as Supremo
Tribunal Federal, Superior Tribunal de Justiça, Tribunal de Justiça de Minas
Gerais and Tribunal de Contas da União. In addition, four legislation documents
were collected, such as "Lei Maria da Penha", giving a total of 70 documents

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is Portuguese.

## Dataset Structure

### Data Instances

An example from the dataset looks as follows:

```
{
  "id": "0",
  "ner_tags": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
  "tokens": [
    "EMENTA", ":", "APELAÇÃO", "CÍVEL", "-", "AÇÃO", "DE", "INDENIZAÇÃO", "POR", "DANOS", "MORAIS", "-", "PRELIMINAR", "-", "ARGUIDA", "PELO", "MINISTÉRIO", "PÚBLICO", "EM", "GRAU", "RECURSAL"]
}
```
### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"O", "B-ORGANIZACAO", "I-ORGANIZACAO", "B-PESSOA", "I-PESSOA", "B-TEMPO", "I-TEMPO", "B-LOCAL", "I-LOCAL", "B-LEGISLACAO", "I-LEGISLACAO", "B-JURISPRUDENCIA", "I-JURISPRUDENCIA"
```
The NER tags have the same format as in the CoNLL shared task: a B denotes the first item of a phrase and an I any non-initial word.

### Data Splits

The data is split into train, validation and test set. The split sizes are as follow:

| Train  | Val   | Test |
| ------ | ----- | ---- |
| 7828   | 1177  | 1390 |

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
@inproceedings{luz_etal_propor2018,
      author = {Pedro H. {Luz de Araujo} and Te\'{o}filo E. {de Campos} and
      Renato R. R. {de Oliveira} and Matheus Stauffer and
      Samuel Couto and Paulo Bermejo},
      title = {{LeNER-Br}: a Dataset for Named Entity Recognition in {Brazilian} Legal Text},
      booktitle = {International Conference on the Computational Processing of Portuguese ({PROPOR})},
      publisher = {Springer},
      series = {Lecture Notes on Computer Science ({LNCS})},
      pages = {313--323},
      year = {2018},
      month = {September 24-26},
      address = {Canela, RS, Brazil},	  
      doi = {10.1007/978-3-319-99722-3_32},
      url = {https://cic.unb.br/~teodecampos/LeNER-Br/},
}	
```

### Contributions

Thanks to [@jonatasgrosman](https://github.com/jonatasgrosman) for adding this dataset.