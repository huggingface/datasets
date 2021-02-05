---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
  kannada:
  - en
  - kn
  malayalam:
  - en
  - ml
  tamil:
  - en
  - ta
licenses:
- cc-by-4.0
multilinguality:
- multilingual
size_categories:
  kannada:
  - 1K<n<10K
  malayalam:
  - 10K<n<100K
  tamil:
  - 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-offensive-language
---

# Dataset Card for Offenseval Dravidian

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://competitions.codalab.org/competitions/27654#learn_the_details
- **Repository:** https://competitions.codalab.org/competitions/27654#participate-get_data
- **Paper:** Findings of the Shared Task on {O}ffensive {L}anguage {I}dentification in {T}amil, {M}alayalam, and {K}annada
- **Leaderboard:** https://competitions.codalab.org/competitions/27654#results
- **Point of Contact:** [Bharathi Raja Chakravarthi](mailto:bharathiraja.akr@gmail.com)

### Dataset Summary

Offensive language identification is classification task in natural language processing (NLP) where the aim is to moderate and minimise offensive content in social media. It has been an active area of research in both academia and industry for the past two decades. There is an increasing demand for offensive language identification on social media texts which are largely code-mixed. Code-mixing is a prevalent phenomenon in a multilingual community and the code-mixed texts are sometimes written in non-native scripts. Systems trained on monolingual data fail on code-mixed data due to the complexity of code-switching at different linguistic levels in the text. This shared task presents a new gold standard corpus for offensive language identification of code-mixed text in Dravidian languages (Tamil-English, Malayalam-English, and Kannada-English).

### Supported Tasks and Leaderboards

The goal of this task is to identify offensive language content of the code-mixed dataset of comments/posts in Dravidian Languages ( (Tamil-English, Malayalam-English, and Kannada-English)) collected from social media. The comment/post may contain more than one sentence but the average sentence length of the corpora is 1. Each comment/post is annotated at the comment/post level. This dataset also has class imbalance problems depicting real-world scenarios.

### Languages

Code-mixed text in Dravidian languages (Tamil-English, Malayalam-English, and Kannada-English).

## Dataset Structure

### Data Instances

An example from the Tamil dataset looks as follows:

| text   | label |
| :------ | :----- |
| படம் கண்டிப்பாக வெற்றி பெற வேண்டும் செம்ம vara level           | Not_offensive |
| Avasara patutiya editor uhh antha bullet sequence aa nee soliruka kudathu, athu sollama iruntha movie ku konjam support aa surprise element aa irunthurukum | Not_offensive |

An example from the Malayalam dataset looks as follows:

| text   | label |
| :------ | :----- |
| ഷൈലോക്ക് ന്റെ നല്ല ടീസർ ആയിട്ട് പോലും ട്രോളി നടന്ന ലാലേട്ടൻ ഫാൻസിന് കിട്ടിയൊരു നല്ലൊരു തിരിച്ചടി തന്നെ ആയിരിന്നു ബിഗ് ബ്രദർ ന്റെ ട്രെയ്‌ലർ           | Not_offensive |
| Marana mass  Ekka kku kodukku oru | Not_offensive |


An example from the Kannada dataset looks as follows:

| text   | label |
| :------ | :----- |
| ನಿಜವಾಗಿಯೂ  ಅದ್ಭುತ heartly heltidini... plz avrigella namma nimmellara supprt beku          | Not_offensive |
| Next song gu kuda alru andre evaga yar comment  madidera alla alrru like madi share madi nam industry na next level ge togond hogaona.      | Not_offensive |


### Data Fields

Tamil
- `text`: Tamil-English code mixed comment.
- `label`: integer from 0 to 5 that corresponds to these values: "Not_offensive", "Offensive_Untargetede", "Offensive_Targeted_Insult_Individual",  "Offensive_Targeted_Insult_Group", "Offensive_Targeted_Insult_Other", "not-Tamil"

Malayalam
- `text`: Malayalam-English code mixed comment.
- `label`: integer from 0 to 5 that corresponds to these values: "Not_offensive", "Offensive_Untargetede", "Offensive_Targeted_Insult_Individual",  "Offensive_Targeted_Insult_Group", "Offensive_Targeted_Insult_Other", "not-malayalam"

Kannada
- `text`: Kannada-English code mixed comment.
- `label`: integer from 0 to 5 that corresponds to these values: "Not_offensive", "Offensive_Untargetede", "Offensive_Targeted_Insult_Individual",  "Offensive_Targeted_Insult_Group", "Offensive_Targeted_Insult_Other", "not-Kannada"


### Data Splits

|              | Tain   | Valid |
| -----        | ------: | -----: |
| Tamil      |  35139 |  4388 |
| Malayalam        |  16010 |  1999 |
| Kannada    |  6217  |  777 |

## Dataset Creation

### Curation Rationale

There is an increasing demand for offensive language identification on social media texts which are largely code-mixed. Code-mixing is a prevalent phenomenon in a multilingual community and the code-mixed texts are sometimes written in non-native scripts. Systems trained on monolingual data fail on code-mixed data due to the complexity of code-switching at different linguistic levels in the text.

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

Youtube users

### Annotations

#### Annotation process

[Needs More Information]

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

This work is licensed under a [Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by/4.0/.)

### Citation Information

```
@inproceedings{dravidianoffensive-eacl,
title={Findings of the Shared Task on {O}ffensive {L}anguage {I}dentification in {T}amil, {M}alayalam, and {K}annada},
author={Chakravarthi, Bharathi Raja and
Priyadharshini, Ruba and
Jose, Navya and
M, Anand Kumar and
Mandl, Thomas and
Kumaresan, Prasanna Kumar and
Ponnsamy, Rahul and
V,Hariharan and
Sherly, Elizabeth and
McCrae, John Philip },
booktitle = "Proceedings of the First Workshop on Speech and Language Technologies for Dravidian Languages",
month = April,
year = "2021",
publisher = "Association for Computational Linguistics",
year={2021}
}
```

### Contributions

Thanks to [@jamespaultg](https://github.com/jamespaultg) for adding this dataset.