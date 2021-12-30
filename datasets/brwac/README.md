---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- pt
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: brwac
---

# Dataset Card for BrWaC

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

- **Homepage:** [BrWaC homepage](https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC)
- **Repository:** [BrWaC repository](https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC)
- **Paper:** [The brWaC Corpus: A New Open Resource for Brazilian Portuguese](https://www.aclweb.org/anthology/L18-1686/)
- **Point of Contact:** [Jorge A. Wagner Filho](mailto:jawfilho@inf.ufrgs.br)

### Dataset Summary

The BrWaC (Brazilian Portuguese Web as Corpus) is a large corpus constructed following the Wacky framework, 
which was made public for research purposes. The current corpus version, released in January 2017, is composed by 
3.53 million documents, 2.68 billion tokens and 5.79 million types. Please note that this resource is available 
solely for academic research purposes, and you agreed not to use it for any commercial applications.
Manually download at https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Portuguese

## Dataset Structure

### Data Instances

An example from the BrWaC dataset looks as follows:

```
{
  "doc_id": "netg-1afc73",
  "text": {
    "paragraphs": [
      [
        "Conteúdo recente"
      ],
      [
        "ESPUMA MARROM CHAMADA \"NINGUÉM MERECE\""
      ],
      [
        "31 de Agosto de 2015, 7:07 , por paulo soavinski - | No one following this article yet."
      ],
      [
        "Visualizado 202 vezes"
      ],
      [
        "JORNAL ELETRÔNICO DA ILHA DO MEL"
      ],
      [
        "Uma espuma marrom escuro tem aparecido com frequência na Praia de Fora.",
        "Na faixa de areia ela aparece disseminada e não chama muito a atenção.",
        "No Buraco do Aipo, com muitas pedras, ela aparece concentrada.",
        "É fácil saber que esta espuma estranha está lá, quando venta.",
        "Pequenos algodões de espuma começam a flutuar no espaço, pertinho da Praia do Saquinho.",
        "Quem pode ajudar na coleta deste material, envio a laboratório renomado e pagamento de análises, favor entrar em contato com o site."
      ]
    ]
  },
  "title": "ESPUMA MARROM CHAMADA ‟NINGUÃÂM MERECE‟ - paulo soavinski",
  "uri": "http://blogoosfero.cc/ilhadomel/pousadasilhadomel.com.br/espuma-marrom-chamada-ninguem-merece"
}
```

### Data Fields

- `doc_id`: The document ID
- `title`: The document title
- `uri`: URI where the document was extracted from
- `text`: A list of document paragraphs (with a list of sentences in it as a list of strings)

### Data Splits

The data is only split into train set with size of 3530796 samples.

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
@inproceedings{wagner2018brwac,
  title={The brwac corpus: A new open resource for brazilian portuguese},
  author={Wagner Filho, Jorge A and Wilkens, Rodrigo and Idiart, Marco and Villavicencio, Aline},
  booktitle={Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  year={2018}
}
```

### Contributions

Thanks to [@jonatasgrosman](https://github.com/jonatasgrosman) for adding this dataset.