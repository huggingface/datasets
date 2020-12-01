---
YAML tags:
- copy-paste the tags obtained with the tagging app: http://34.68.228.168:8501/
---

# Dataset Card for WebNLG

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [WebNLG challenge website](https://webnlg-challenge.loria.fr/)
- **Repository:** [WebNLG GitLab repository](https://gitlab.com/shimorina/webnlg-dataset/-/tree/master/)
- **Paper:** [Creating Training Corpora for NLG Micro-Planning](https://www.aclweb.org/anthology/P17-1017.pdf)
- **Leaderboard:** [WebNLG leaderboards](https://gerbil-nlg.dice-research.org/gerbil/webnlg2020results)
- **Point of Contact:** [anastasia.shimorina@loria.fr](anastasia.shimorina@loria.fr)

### Dataset Summary

The WebNLG challenge consists in mapping data to text. The training data consists
of Data/Text pairs where the data is a set of triples extracted from DBpedia and the text is a verbalisation
of these triples. For instance, given the 3 DBpedia triples shown in (a), the aim is to generate a text such as (b).

```
a. (John_E_Blaha birthDate 1942_08_26) (John_E_Blaha birthPlace San_Antonio) (John_E_Blaha occupation Fighter_pilot)
b. John E Blaha, born in San Antonio on 1942-08-26, worked as a fighter pilot
```

As the example illustrates, the task involves specific NLG subtasks such as sentence segmentation
(how to chunk the input data into sentences), lexicalisation (of the DBpedia properties),
aggregation (how to avoid repetitions) and surface realisation
(how to build a syntactically correct and natural sounding text).

### Supported Tasks and Leaderboards

The dataset supports a `data-to-text` task 

### Languages

[More Information Needed]

## Dataset Structure

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

- If you use the WebNLG corpus, cite:
```
@inproceedings{web_nlg,
  author    = {Claire Gardent and
               Anastasia Shimorina and
               Shashi Narayan and
               Laura Perez{-}Beltrachini},
  editor    = {Regina Barzilay and
               Min{-}Yen Kan},
  title     = {Creating Training Corpora for {NLG} Micro-Planners},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2017, Vancouver, Canada, July 30 - August 4, Volume
               1: Long Papers},
  pages     = {179--188},
  publisher = {Association for Computational Linguistics},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-1017},
  doi       = {10.18653/v1/P17-1017}
}
```

- If you use *release\_v2\_constrained* in particular, cite:
```
@InProceedings{shimorina2018handling,
  author = 	"Shimorina, Anastasia
		and Gardent, Claire",
  title = 	"Handling Rare Items in Data-to-Text Generation",
  booktitle = 	"Proceedings of the 11th International Conference on Natural Language Generation",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"360--370",
  location = 	"Tilburg University, The Netherlands",
  url = 	"http://aclweb.org/anthology/W18-6543"
}
```
