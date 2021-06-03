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
paperswithcode_id: null
---

# Dataset Card for Offenseval Dravidian

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
@article{chakravarthi-etal-2021-lre,
title = "DravidianCodeMix: Sentiment Analysis and Offensive Language Identification Dataset for Dravidian Languages in Code-Mixed Text",
author = "Chakravarthi, Bharathi Raja  and
  Priyadharshini, Ruba  and
  Muralidaran, Vigneshwaran and
  Jose, Navya and
  Suryawanshi, Shardul and
  Sherly, Elizabeth  and
  McCrae, John P",
  journal={Language Resources and Evaluation},
  publisher={Springer}
}

```
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
```
@inproceedings{hande-etal-2020-kancmd,
    title = "{K}an{CMD}: {K}annada {C}ode{M}ixed Dataset for Sentiment Analysis and Offensive Language Detection",
    author = "Hande, Adeep  and
      Priyadharshini, Ruba  and
      Chakravarthi, Bharathi Raja",
    booktitle = "Proceedings of the Third Workshop on Computational Modeling of People's Opinions, Personality, and Emotion's in Social Media",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.peoples-1.6",
    pages = "54--63",
    abstract = "We introduce Kannada CodeMixed Dataset (KanCMD), a multi-task learning dataset for sentiment analysis and offensive language identification. The KanCMD dataset highlights two real-world issues from the social media text. First, it contains actual comments in code mixed text posted by users on YouTube social media, rather than in monolingual text from the textbook. Second, it has been annotated for two tasks, namely sentiment analysis and offensive language detection for under-resourced Kannada language. Hence, KanCMD is meant to stimulate research in under-resourced Kannada language on real-world code-mixed social media text and multi-task learning. KanCMD was obtained by crawling the YouTube, and a minimum of three annotators annotates each comment. We release KanCMD 7,671 comments for multitask learning research purpose.",
}
```

```
@inproceedings{chakravarthi-etal-2020-corpus,
    title = "Corpus Creation for Sentiment Analysis in Code-Mixed {T}amil-{E}nglish Text",
    author = "Chakravarthi, Bharathi Raja  and
      Muralidaran, Vigneshwaran  and
      Priyadharshini, Ruba  and
      McCrae, John Philip",
    booktitle = "Proceedings of the 1st Joint Workshop on Spoken Language Technologies for Under-resourced languages (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources association",
    url = "https://www.aclweb.org/anthology/2020.sltu-1.28",
    pages = "202--210",
    abstract = "Understanding the sentiment of a comment from a video or an image is an essential task in many applications. Sentiment analysis of a text can be useful for various decision-making processes. One such application is to analyse the popular sentiments of videos on social media based on viewer comments. However, comments from social media do not follow strict rules of grammar, and they contain mixing of more than one language, often written in non-native scripts. Non-availability of annotated code-mixed data for a low-resourced language like Tamil also adds difficulty to this problem. To overcome this, we created a gold standard Tamil-English code-switched, sentiment-annotated corpus containing 15,744 comment posts from YouTube. In this paper, we describe the process of creating the corpus and assigning polarities. We present inter-annotator agreement and show the results of sentiment analysis trained on this corpus as a benchmark.",
    language = "English",
    ISBN = "979-10-95546-35-1",
}
```

```
@inproceedings{chakravarthi-etal-2020-sentiment,
    title = "A Sentiment Analysis Dataset for Code-Mixed {M}alayalam-{E}nglish",
    author = "Chakravarthi, Bharathi Raja  and
      Jose, Navya  and
      Suryawanshi, Shardul  and
      Sherly, Elizabeth  and
      McCrae, John Philip",
    booktitle = "Proceedings of the 1st Joint Workshop on Spoken Language Technologies for Under-resourced languages (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources association",
    url = "https://www.aclweb.org/anthology/2020.sltu-1.25",
    pages = "177--184",
    abstract = "There is an increasing demand for sentiment analysis of text from social media which are mostly code-mixed. Systems trained on monolingual data fail for code-mixed data due to the complexity of mixing at different levels of the text. However, very few resources are available for code-mixed data to create models specific for this data. Although much research in multilingual and cross-lingual sentiment analysis has used semi-supervised or unsupervised methods, supervised methods still performs better. Only a few datasets for popular languages such as English-Spanish, English-Hindi, and English-Chinese are available. There are no resources available for Malayalam-English code-mixed data. This paper presents a new gold standard corpus for sentiment analysis of code-mixed text in Malayalam-English annotated by voluntary annotators. This gold standard corpus obtained a Krippendorff{'}s alpha above 0.8 for the dataset. We use this new corpus to provide the benchmark for sentiment analysis in Malayalam-English code-mixed texts.",
    language = "English",
    ISBN = "979-10-95546-35-1",
}
```
### Contributions

Thanks to [@jamespaultg](https://github.com/jamespaultg) for adding this dataset.
