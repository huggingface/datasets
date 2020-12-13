---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
languages:
- fa
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- question-answering
task_ids:
- abstractive-qa
- explanation-generation
- extractive-qa
- machine-translation
- open-domain-qa
- summarization
- text-simplification
---

# Dataset Card for [Needs More Information]

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

- **Homepage:** https://github.com/m3hrdadfi/wiki-summary
- **Repository:** https://github.com/m3hrdadfi/wiki-summary
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [Mehrdad Farahani](mailto:m3hrdadphi@gmail.com)

### Dataset Summary

The dataset extracted from Persian Wikipedia into the form of articles and highlights and cleaned the dataset into pairs of articles and highlights and reduced the articles' length (only version 1.0.0) and highlights' length to a maximum of 512 and 128, respectively, suitable for parsBERT. This dataset is created to achieve state-of-the-art results on some interesting NLP tasks like Text Summarization.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in Percy.

## Dataset Structure

### Data Instances

{
    'id' :'0598cfd2ac491a928615945054ab7602034a8f4f',
    'link': 'https://fa.wikipedia.org/wiki/'FBD'(_1917_1H3ÌG',
    'title': ''FBD'( 1917 1H3ÌG',
    'article': 'F.3* 'FBD'( AH1ÌG ñùñ÷ 1. /'/ . /1 'ÌF 'FBD'( ~3 '2 Ì©31Ì '9*5'('*  *8'G1'* H /1¯Ì1ÌG'  FÌ©HD'Ì /HE  ".1ÌF *2'1 1H3ÌG '2 3D7F* .D9 4/ H Ì© /HD* EHB* (G B/1* 13Ì/ . /HD* EHB* 2Ì1 F81 ¯&H1¯Ì DHHA H 'D©3'F/1 ©1F3©Ì *4©ÌD 4/ . '©+1 '96'Ì /HD* EHB*  '2 4'.G EF4HÌ© -2( 3H3Ì'D /EH©1'* ©'1¯1Ì 1H3ÌG (H/F/ . /HEÌF E1-DG  'FBD'( '©*(1 ñùñ÷ (H/ . 'FBD'( '©*(1  *-* F8'1* -2( (D4HÌ© (4'.G 1'/Ì©'D '2 -2( 3H3Ì'D /EH©1'* ©'1¯1Ì 1H3ÌG) H (G 1G(1Ì HD'/ÌEÌ1 DFÌF (G ~Ì4 1A* H 7Ì Ì© ÌH14 F8'EÌ GEG,'F(G (G ©'. 2E3*'FÌ 3F ~*12(H1¯ H 3'Ì1 'E'©F EGE  B/1* 1' '2 /HD* EHB* ¯1A* . /1 'ÌF 'FBD'( 'A1'/ (3Ì'1 ©EÌ ©4*G 4/F/ . '2 2E'F 4©3* 1H3ÌG /1 ,F¯ ñùðõ (' ˜'~F  'H6'9 (/ 'B*5'/Ì  ¯13F¯Ì  9B(E'F/¯Ì H 31E'ÌG/'1Ì H F'16'Ì*ÌG'Ì ¯HF'¯HF /1 (ÌF E1/E  31('2'F  ©'1¯1'F  ©4'H12'F H F.(¯'F 1H3ÌG (GH,H/ "E/G(H/ . 31©H(G'Ì *2'1 H 'Ì,'/ E,D3 /HE' F8'E E41H7G -'5D "F /H1'F '3* . -2( 3H3Ì'D /EH©1'*  '5DÌ*1ÌF E9*16 (G 3Ì'3*G'Ì FÌ©D'Ì /HE (H/ ©G (G7H1 ¯3*1/G (ÌF /GB'F'F ©4'H12'F H ©'1¯1'F ©'1.'F,'* 5F9*Ì 9DÌG 3Ì'3*G'Ì 3Ì3*E *2'1 A9'DÌ* /'4* . /1 'H* ñùñô EÌD'/Ì  'E~1'*H1Ì 1H3ÌG (G /3*H1 *2'1 HB* H (G EF8H1 -E'Ì* '2 '3D'HG'Ì 51(3*'F H'1/ ,F¯ ,G'FÌ 'HD /1 (1'(1 'E~1'*H1Ì "DE'F H 'E~1'*H1Ì '*1Ì4-E,'13*'F 4/ . F.3* AB7 (D4HÌ©G'  E.'DA H1H/ 1H3ÌG (G 'ÌF ,F¯ (H/F/ H EÌ¯A*F/ ©G 'ÌF ,F¯  3(( (/*1 4/F 'H6'9 F'(3'E'F 'B*5'/Ì H ',*E'9Ì 1H3ÌG .H'G/ 4/ . /1 3'D ñùñô EÌD'/Ì  Ì9FÌ /1 ":'2 ,F¯ ,G'FÌ 'HD  1H3ÌG (21¯*1ÌF '1*4 ,G'F 1' /'4*  -/H/ ñò EÌDÌHF 31('2 H ö EÌDÌHF 31('2 0.Ì1G  HDÌ /1 ~'Ì'F 3'D ñùñö EÌD'/Ì  ~F, EÌDÌHF FA1 '2 31('2'F 1H3ÌG ©4*G  2.EÌ Ì' '3Ì1 4/G (H/F/ . -/H/ /H EÌDÌHF 31('2 FÌ2 E-D ./E* .H/ 1' *1© ©1/G H :'D(' (' '3D-G (G 4G1 H /Ì'1 .H/ ('2¯4*G (H/F/ . /1 EÌ'F ñð Ì' ññ EÌDÌHF 31('2 ('BÌE'F/G FÌ2  '9*('1 *2'1 H 3D3DG E1'*( '1*4 H '*H1Ì*G 'A31'F ('D' /3* '2 (ÌF 1A*G (H/ . 9H'ED F'(3'E'F /'.DÌ '9E '2 ',*E'9Ì ©4'H12Ì H A1E'F/GÌ F8'EÌ /1 4©3*G'Ì 1H3ÌG (3Ì'1 E$+1 (H/ . 4©3*G'Ì 1H3ÌG /1 ,F¯ ,G'FÌ 'HD  -'EÌ'F FÌ©D'Ì /HE /1 1H3ÌG 1' (G -/'BD .H/ 13'F/ . /1 'H'ÌD AH1ÌG ñùñ÷ EÌD'/Ì '©+1 ©'1¯1'F 5F9*Ì /1 ~*1H¯1'/ H E3©H /3* (G '9*5'( 2/F/ . 3~3 4H14 (G ~'/¯'FG' H 31('2'F 13Ì/ . '9*1'6'* /GB'F'F FÌ2 ¯3*14 Ì'A* . 3H3Ì'D /EH©1'*G' G/'Ì* '9*1'6'* 1' /1 /3* ¯1A*F/ . /1 ññ E'13 ñùñ÷ EÌD'/Ì  *2'1 HB* 1H3ÌG  FÌ©D'Ì /HE  A1E'F 'F-D'D E,D3 1H3ÌG 1' 5'/1 ©1/  'E' '©+1 FE'ÌF/¯'F E,D3 E*A1B F4/F/ H (' *5EÌE'* FÌ©D'Ì /HE E.'DA* ©1/F/ . 31'F,'E /1 ~Ì *8'G1'* ¯3*1/G ©'1¯1'F H 3~3 F'A1E'FÌ 31('2'F /1 31©H( *8'G1©FF/¯'F /1 ~*1H¯1'/  FÌ©D'Ì /HE '2 EB'E .H/ '3*9A' /'/ . (/ÌF *1*Ì( -©E1'FÌ /H/E'F 1HE'FHAG' (1 1H3ÌG ~3 '2 -/H/ 3Ì5/ 3'D ~'Ì'F Ì'A* .',
    'highlights': ''FBD'( ñùñ÷ 1H3ÌG  ,F(4Ì '9*1'6Ì  6/ 'E~1'*H1Ì 1H3ÌG (H/ ©G /1 3'D ñùñ÷ 1. /'/ H (G 31F¯HFÌ -©HE* *2'1G' H (1~'ÌÌ '*-'/ ,E'GÌ1 4H1HÌ 'F,'EÌ/ . E('FÌ 'FBD'( (1 ~'ÌG 5D--F'F-2EÌF '3*H'1 (H/ . 'ÌF 'FBD'( /1 /H E1-DG 5H1* ¯1A* : /1 7HD 'ÌF 'FBD'( /1 4G1G'Ì '5DÌ 1H3ÌG GE'FF/ E3©H H 3F ~*12(H1¯ 1HÌ/'/G'Ì *'1Ì.Ì (1,3*G'Ì 1. /'/ . 'FBD'( /1 EF'7B 1H3*'ÌÌ H 19Ì*Ì FÌ2 ~' (G ~'Ì EF'7B 4G1Ì /1 -'D ~Ì41HÌ (H/ H /GB'F'F 2EÌFG' 1' *51A ©1/G H /1 -'D ('2*H2Ì9 "F /1 EÌ'F .H/ (H/F/ .'
}

### Data Fields

- `id`: Article id
- `link`: Article link
- `title`: Title of the article
- `article`: Full text content in the article
- `highlights`: Summary of the article

### Data Splits

|    Train    |     Test    |  Validation |
|-------------|-------------|-------------| 
|   43,457    |     4,801   |    5,352    |

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

No annotations.

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

The dataset was created by Mehrdad Farahani.

### Licensing Information

[Apache License 2.0](https://github.com/m3hrdadfi/wiki-summary/blob/master/LICENSE)

### Citation Information

```
@misc{Bert2BertWikiSummaryPersian,
  author = {Mehrdad Farahani},
  title = {Summarization using Bert2Bert model on WikiSummary dataset},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/m3hrdadfi/wiki-summary},
}
```