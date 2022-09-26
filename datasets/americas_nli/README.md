---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- ay
- bzd
- cni
- gn
- hch
- nah
- oto
- qu
- shp
- tar
license:
- unknown
multilinguality:
- multilingual
- translation
pretty_name: 'AmericasNLI: A NLI Corpus of 10 Indigenous Low-Resource Languages.'
size_categories:
- unknown
source_datasets:
- extended|xnli
task_categories:
- text-classification
task_ids:
- natural-language-inference
---

# Dataset Card for AmericasNLI

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

- **Homepage:** [Needs More Information]
- **Repository:** https://github.com/nala-cub/AmericasNLI
- **Paper:** https://arxiv.org/abs/2104.08726
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

AmericasNLI is an extension of XNLI (Conneau et al., 2018) a natural language inference (NLI) dataset covering 15 high-resource languages to 10 low-resource indigenous languages spoken in the Americas: Ashaninka, Aymara, Bribri, Guarani, Nahuatl, Otomi, Quechua, Raramuri, Shipibo-Konibo, and Wixarika. As with MNLI, the goal is to predict textual entailment (does sentence A imply/contradict/neither sentence B) and is a classification task (given two sentences, predict one of three labels).


### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

- aym
- bzd
- cni
- gn
- hch
- nah
- oto
- quy
- shp
- tar

## Dataset Structure

### Data Instances

#### all_languages

An example of the test split looks as follows:

```
{'language': 'aym', 'premise': "Ukhamaxa, janiw ukatuqits lup'kayätti, ukhamarus wali phiñasitayätwa, ukatx jupampiw mayamp aruskipañ qallanttha.", 'hypothesis': 'Janiw mayamp jupampix p
arlxapxti.', 'label': 2}
```

#### aym

An example of the test split looks as follows:

```
{'premise': "Ukhamaxa, janiw ukatuqits lup'kayätti, ukhamarus wali phiñasitayätwa, ukatx jupampiw mayamp aruskipañ qallanttha.", 'hypothesis': 'Janiw mayamp jupampix parlxapxti.', 'label
': 2}
```

#### bzd

An example of the test split looks as follows:

```
{'premise': "Bua', kèq ye' kũ e' bikeitsök erë ye' chkénãwã tã ye' ujtémĩne ie' tã páxlĩnẽ.", 'hypothesis': "Kèq ye' ùtẽnẽ ie' tã páxlĩ.", 'label': 2}
```

#### cni

An example of the test split looks as follows:

```
{'premise': 'Kameetsa, tee nokenkeshireajeroji, iro kantaincha tee nomateroji aisati nintajaro noñanatajiri iroakera.', 'hypothesis': 'Tee noñatajeriji.', 'label': 2}
```

#### gn

An example of the test split looks as follows:

```
{'premise': "Néi, ni napensaikurihína upéva rehe, ajepichaiterei ha añepyrûjey añe'ê hendive.", 'hypothesis': "Nañe'êvéi hendive.", 'label': 2}
```

#### hch

An example of the test split looks as follows:

```
{'premise': 'mu hekwa.', 'hypothesis': 'neuka tita xatawe m+k+ mat+a.', 'label': 2}
```

#### nah

An example of the test split looks as follows:

```
{'premise': 'Cualtitoc, na axnimoihliaya ino, nicualaniztoya queh naha nicamohuihqui', 'hypothesis': 'Ayoc nicamohuihtoc', 'label': 2}
```

#### oto

An example of the test split looks as follows:

```
{'premise': 'mi-ga, nin mibⴘy mbô̮nitho ane guenu, guedi mibⴘy nho ⴘnmⴘy xi di mⴘdi o ñana nen nⴘua manaigui', 'hypothesis': 'hin din bi pengui nen nⴘa', 'label': 2}
```

#### quy

An example of the test split looks as follows:

``` {'premise': 'Allinmi, manam chaypiqa hamutachkarqanichu, ichaqa manam allinchu tarikurqani chaymi kaqllamanta paywan rimarqani.', 'hypothesis': 'Manam paywanqa kaqllamantaqa rimarqani
.', 'label': 2}
```

#### shp

An example of the test split looks as follows:

```
{'premise': 'Jakon riki, ja shinanamara ea ike, ikaxbi kikin frustradara ea ike jakopira ea jabe yoyo iribake.', 'hypothesis': 'Eara jabe yoyo iribiama iki.', 'label': 2}
```

#### tar

An example of the test split looks as follows:

```
{'premise': 'Ga’lá ju, ke tási newalayé nejé echi kítira, we ne majáli, a’lí ko uchécho ne yua ku ra’íchaki.', 'hypothesis': 'Tási ne uchecho yua ra’ícha échi rejói.', 'label': 2}
```

### Data Fields

#### all_languages
    - language: a multilingual string variable, with languages including ar, bg, de, el, en.
    - premise: a multilingual string variable, with languages including ar, bg, de, el, en.
    - hypothesis: a multilingual string variable, with possible languages including ar, bg, de, el, en.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### aym
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### bzd
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### cni
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### hch
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### nah
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### oto
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### quy
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### shp
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).
#### tar
    - premise: a string feature.
    - hypothesis: a string feature.
    - label: a classification label, with possible values including entailment (0), neutral (1), contradiction (2).

### Data Splits

| Language          | ISO | Family       | Dev  | Test |
|-------------------|-----|:-------------|-----:|-----:|
| all_languages     | --  | --           | 6457 | 7486 |
| Aymara            | aym | Aymaran      | 743  | 750  |
| Ashaninka         | cni | Arawak       | 658  | 750  |
| Bribri            | bzd | Chibchan     | 743  | 750  |
| Guarani           | gn  | Tupi-Guarani | 743  | 750  |
| Nahuatl           | nah | Uto-Aztecan  | 376  | 738  |
| Otomi             | oto | Oto-Manguean | 222  | 748  |
| Quechua           | quy | Quechuan     | 743  | 750  |
| Raramuri          | tar | Uto-Aztecan  | 743  | 750  |
| Shipibo-Konibo    | shp | Panoan       | 743  | 750  |
| Wixarika          | hch | Uto-Aztecan  | 743  | 750  |

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

The authors translate from the Spanish subset of XNLI.

> AmericasNLI is the translation of a subset of XNLI (Conneau et al., 2018). As translators between Spanish and the target languages are more frequently available than those for English, we translate from the Spanish version.

As per paragraph 3.1 of the [original paper](https://arxiv.org/abs/2104.08726).

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

The dataset comprises expert translations from Spanish XNLI. 

> Additionally, some translators reported that code-switching is often used to describe certain topics, and, while many words without an exact equivalence in the target language are worked in through translation or interpretation, others are kept in Spanish. To minimize the amount of Spanish vocabulary in the translated examples, we choose sentences from genres that we judged to be relatively easy to translate into the target languages: “face-to-face,” “letters,” and “telephone.”

As per paragraph 3.1 of the [original paper](https://arxiv.org/abs/2104.08726).

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```
@article{DBLP:journals/corr/abs-2104-08726,
  author    = {Abteen Ebrahimi and
               Manuel Mager and
               Arturo Oncevay and
               Vishrav Chaudhary and
               Luis Chiruzzo and
               Angela Fan and
               John Ortega and
               Ricardo Ramos and
               Annette Rios and
               Ivan Vladimir and
               Gustavo A. Gim{\'{e}}nez{-}Lugo and
               Elisabeth Mager and
               Graham Neubig and
               Alexis Palmer and
               Rolando A. Coto Solano and
               Ngoc Thang Vu and
               Katharina Kann},
  title     = {AmericasNLI: Evaluating Zero-shot Natural Language Understanding of
               Pretrained Multilingual Models in Truly Low-resource Languages},
  journal   = {CoRR},
  volume    = {abs/2104.08726},
  year      = {2021},
  url       = {https://arxiv.org/abs/2104.08726},
  eprinttype = {arXiv},
  eprint    = {2104.08726},
  timestamp = {Mon, 26 Apr 2021 17:25:10 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2104-08726.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@fdschmidt93](https://github.com/fdschmidt93) for adding this dataset.
