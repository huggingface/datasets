---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- pt-BR
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
pretty_name: ToLD-Br
size_categories:
- 10K<n<100K 
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-hate-speech-detection
paperswithcode_id: told-br
---

# Dataset Card for "ToLD-Br"

## Table of Contents
- [Dataset Card for "ToLD-Br"](#dataset-card-for-told-br)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** https://paperswithcode.com/dataset/told-br
- **Repository:** https://github.com/JAugusto97/ToLD-Br
- **Paper:** https://arxiv.org/abs/2010.04543
- **Leaderboard:** https://paperswithcode.com/sota/hate-speech-detection-on-told-br
- **Point of Contact:** joao.leite@estudante.ufscar.br

### Dataset Summary

ToLD-Br is the biggest dataset for toxic tweets in Brazilian Portuguese, crowdsourced by 42 annotators selected from a pool of 129 volunteers. Annotators were selected aiming to create a plural group in terms of demographics (ethnicity, sexual orientation, age, gender). Each tweet was labeled by three annotators in 6 possible categories: LGBTQ+phobia, Xenophobia, Obscene, Insult, Misogyny and Racism.

### Supported Tasks and Leaderboards

-`text-classification-other-hate-speech-detection`: The dataset can be used to train a model for Hate Speech Detection, either using it's multi-label classes or by grouping them into a binary Hate vs. Non-Hate class. A [BERT](https://huggingface.co/docs/transformers/model_doc/bert) model can be fine-tuned to perform this task and achieve 0.75 F1-Score for it's binary version.

### Languages

The text in the dataset is in Brazilian Portuguese, as spoken by Tweet users. The associated BCP-47 code is `pt-BR`.

## Dataset Structure

### Data Instances
ToLD-Br has two versions: binary and multilabel.  

Multilabel:
A data point consists of the tweet text (string) followed by 6 categories that have values ranging from 0 to 3, meaning the amount of votes from annotators for that specific class on homophobia, obscene, insult, racism, misogyny and xenophobia.

An example from multilabel ToLD-Br looks as follows:
```
{'text': '@user bandido dissimulado. esse sérgio moro é uma espécie de mal carater com ditadura e pitadas de atraso'
'homophobia': 0
'obscene': 0
'insult': 2
'racism': 0
'misogyny': 0
'xenophobia': 0}
```

Binary:  
A data point consists of the tweet text (string) followed by a binary class "toxic" with values 0 or 1.

An example from binary ToLD-Br looks as follows:  
```
{'text': '@user bandido dissimulado. esse sérgio moro é uma espécie de mal carater com ditadura e pitadas de atraso'
'toxic': 1}
```
### Data Fields

Multilabel:  
- text: A string representing the tweet posted by a user. Mentions to other users are anonymized by replacing the mention with a @user tag.
- homophobia: numerical value {0, 1, 2, 3) representing the number of votes given by annotators flagging the respective tweet as homophobic.
- obscene: numerical value {0, 1, 2, 3) representing the number of votes given by annotators flagging the respective tweet as obscene.
- insult: numerical value {0, 1, 2, 3) representing the number of votes given by annotators flagging the respective tweet as insult.
- racism: numerical value {0, 1, 2, 3) representing the number of votes given by annotators flagging the respective tweet as racism.
- misogyny: numerical value {0, 1, 2, 3) representing the number of votes given by annotators flagging the respective tweet as misogyny.
- xenophobia: numerical value {0, 1, 2, 3) representing the number of votes given by annotators flagging the respective tweet as xenophobia.

Binary:  
- text: A string representing the tweet posted by a user. Mentions to other users are anonymized by replacing the mention with a @user tag.
- label: numerical binary value {0, 1} representing if the respective text is toxic/abusive or not. 

### Data Splits
Multilabel:  
The entire dataset consists of 21.000 examples.

Binary:  
The train set consists of 16.800 examples, validation set consists of 2.100 examples and test set consists of 2.100 examples.


## Dataset Creation

### Curation Rationale

Despite Portuguese being the 5th most spoken language in the world and Brazil being the 4th country with most unique users, Brazilian Portuguese was underrepresented in the hate-speech detection task. Only two other datasets were available, one of them being European Portuguese. ToLD-Br is 4x bigger than both these datasets combined. Also, none of them had multiple annotators per instance. Also, this work proposes a plural and diverse group of annotators carefully selected to avoid inserting bias into the annotation.

### Source Data

#### Initial Data Collection and Normalization

Data was collected in 15 days in August 2019 using Gate Cloud's Tweet Collector. Ten million tweets were collected using two methods: a keyword-based method and a user-mention method. The first method collected tweets mentioning the following keywords: 

viado,veado,viadinho,veadinho,viadao,veadao,bicha,bixa,bichinha,bixinha,bichona,bixona,baitola,sapatão,sapatao,traveco,bambi,biba,boiola,marica,gayzão,gayzao,flor,florzinha,vagabundo,vagaba,desgraçada,desgraçado,desgracado,arrombado,arrombada,foder,fuder,fudido,fodido,cú,cu,pinto,pau,pal,caralho,caraio,carai,pica,cacete,rola,porra,escroto,buceta,fdp,pqp,vsf,tnc,vtnc,puto,putinho,acéfalo,acefalo,burro,idiota,trouxa,estúpido,estupido,estúpida,canalha,demente,retardado,retardada,verme,maldito,maldita,ridículo,ridiculo,ridícula,ridicula,morfético,morfetico,morfética,morfetica,lazarento,lazarenta,lixo,mongolóide,mongoloide,mongol,asqueroso,asquerosa,cretino,cretina,babaca,pilantra,neguinho,neguinha,pretinho,pretinha,escurinho,escurinha,pretinha,pretinho,crioulo,criolo,crioula,criola,macaco,macaca,gorila,puta,vagabunda,vagaba,mulherzinha,piranha,feminazi,putinha,piriguete,vaca,putinha,bahiano,baiano,baianagem,xingling,xing ling,xing-ling,carioca,paulista,sulista,mineiro,gringo

The list of most followed Brazilian Twitter accounts can be found [here](https://assuperlistas.com/2022/01/21/os-100-brasileiros-mais-seguidos-do-twitter/).

#### Who are the source language producers?

The language producers are Twitter users from Brazil, speakers of Portuguese.

### Annotations

#### Annotation process

A form was published at the Federal University of São Carlos asking for volunteers to annotate our dataset. 129 people volunteered and 42 were selected according to their demographics in order to create a diverse and plural annotation group. Guidelines were produced and presented to the annotators. The entire process was done asynchronously because of the Covid-19 pandemic. The tool used was Google Sheets. Annotators were grouped into 14 teams of three annotators each. Each group annotated a respective file containing 1500 tweets. Annotators didn't have contact with each other, nor did they know that other annotators were labelling the same tweets as they were.

#### Who are the annotators?

Annotators were people from the Federal University of São Carlos' Facebook group. Their demographics are described below:  

| Gender |  |
|--------|--------|
| Male   | 18     |
| Female | 24     |

| Sexual Orientation |    |
|--------------------|----|
| Heterosexual       | 22 |
| Bisexual           | 12 |
| Homosexual         | 5  |
| Pansexual          | 3  |

| Ethnicity    |    |
|--------------|----|
| White        | 25 |
| Brown        | 9  |
| Black        | 5  |
| Asian        | 2  |
| Non-Declared | 1  |

Ages range from 18 to 37 years old.

Annotators were paid R$50 ($10) to label 1500 examples each.

### Personal and Sensitive Information

The dataset contains sensitive information for homophobia, obscene, insult, racism, misogyny and xenophobia.

Tweets were anonymized by replacing user mentions with a @user tag.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop better hate speech detection systems.

A system that succeeds at this task would be able to identify hate speech tweets associated with the classes available in the dataset.

### Discussion of Biases

An effort was made to reduce annotation bias by selecting annotators with a diverse demographic background. In terms of data collection, by using keywords and user mentions, we are introducing some bias to the data, restricting our scope to the list of keywords and users we created.

### Other Known Limitations

Because of the massive data skew for the multilabel classes, it is extremely hard to train a robust model for this version of the dataset. We advise using it for analysis and experimentation only. The binary version of the dataset is robust enough to train a classifier with up to 76% F1-score.

## Additional Information

### Dataset Curators

The dataset was created by João Augusto Leite, Diego Furtado Silva, both from the Federal University of São Carlos (BR), Carolina Scarton and Kalina Bontcheva both from the University of Sheffield (UK)

### Licensing Information

ToLD-Br is licensed under a Creative Commons BY-SA 4.0

### Citation Information

```
@article{DBLP:journals/corr/abs-2010-04543,
  author    = {Joao Augusto Leite and
               Diego F. Silva and
               Kalina Bontcheva and
               Carolina Scarton},
  title     = {Toxic Language Detection in Social Media for Brazilian Portuguese:
               New Dataset and Multilingual Analysis},
  journal   = {CoRR},
  volume    = {abs/2010.04543},
  year      = {2020},
  url       = {https://arxiv.org/abs/2010.04543},
  eprinttype = {arXiv},
  eprint    = {2010.04543},
  timestamp = {Tue, 15 Dec 2020 16:10:16 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2010-04543.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
### Contributions

Thanks to [@JAugusto97](https://github.com/JAugusto97) for adding this dataset.
