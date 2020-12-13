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
    'link': 'https://fa.wikipedia.org/wiki/'FBD'(_1917_1H3�G',
    'title': ''FBD'( 1917 1H3�G',
    'article': 'F.3* 'FBD'( AH1�G ���� 1. /'/ . /1 '�F 'FBD'( ~3 '2 ̩31� '9*5'('*  *8'G1'* H /1��1�G'  F̩HD'� /HE  ".1�F *2'1 1H3�G '2 3D7F* .D9 4/ H ̩ /HD* EHB* (G B/1* 13�/ . /HD* EHB* 2�1 F81 �&H1�� DHHA H 'D�3'F/1 �1F3�� *4��D 4/ . '�+1 '96'� /HD* EHB*  '2 4'.G EF4H̩ -2( 3H3�'D /EH�1'* �'1�1� 1H3�G (H/F/ . /HE�F E1-DG  'FBD'( '�*(1 ���� (H/ . 'FBD'( '�*(1  *-* F8'1* -2( (D4H̩ (4'.G 1'/̩'D '2 -2( 3H3�'D /EH�1'* �'1�1� 1H3�G) H (G 1G(1� HD'/�E�1 DF�F (G ~�4 1A* H 7� ̩ �H14 F8'E� GEG,'F(G (G �'. 2E3*'F� 3F ~*12(H1� H 3'�1 'E'�F EGE  B/1* 1' '2 /HD* EHB* �1A* . /1 '�F 'FBD'( 'A1'/ (3�'1 �E� �4*G 4/F/ . '2 2E'F 4�3* 1H3�G /1 ,F� ���� (' �'~F  'H6'9 (/ 'B*5'/�  �13F��  9B(E'F/�� H 31E'�G/'1� H F'16'�*�G'� �HF'�HF /1 (�F E1/E  31('2'F  �'1�1'F  �4'H12'F H F.(�'F 1H3�G (GH,H/ "E/G(H/ . 31�H(G'� *2'1 H '�,'/ E,D3 /HE' F8'E E41H7G -'5D "F /H1'F '3* . -2( 3H3�'D /EH�1'*  '5D�*1�F E9*16 (G 3�'3*G'� F̩D'� /HE (H/ �G (G7H1 �3*1/G (�F /GB'F'F �4'H12'F H �'1�1'F �'1.'F,'* 5F9*� 9D�G 3�'3*G'� 3�3*E *2'1 A9'D�* /'4* . /1 'H* ���� E�D'/�  'E~1'*H1� 1H3�G (G /3*H1 *2'1 HB* H (G EF8H1 -E'�* '2 '3D'HG'� 51(3*'F H'1/ ,F� ,G'F� 'HD /1 (1'(1 'E~1'*H1� "DE'F H 'E~1'*H1� '*1�4-E,'13*'F 4/ . F.3* AB7 (D4H̩G'  E.'DA H1H/ 1H3�G (G '�F ,F� (H/F/ H E��A*F/ �G '�F ,F�  3(( (/*1 4/F 'H6'9 F'(3'E'F 'B*5'/� H ',*E'9� 1H3�G .H'G/ 4/ . /1 3'D ���� E�D'/�  �9F� /1 ":'2 ,F� ,G'F� 'HD  1H3�G (21�*1�F '1*4 ,G'F 1' /'4*  -/H/ �� E�D�HF 31('2 H � E�D�HF 31('2 0.�1G  HD� /1 ~'�'F 3'D ���� E�D'/�  ~F, E�D�HF FA1 '2 31('2'F 1H3�G �4*G  2.E� �' '3�1 4/G (H/F/ . -/H/ /H E�D�HF 31('2 F�2 E-D ./E* .H/ 1' *1� �1/G H :'D(' (' '3D-G (G 4G1 H /�'1 .H/ ('2�4*G (H/F/ . /1 E�'F �� �' �� E�D�HF 31('2 ('B�E'F/G F�2  '9*('1 *2'1 H 3D3DG E1'*( '1*4 H '*H1�*G 'A31'F ('D' /3* '2 (�F 1A*G (H/ . 9H'ED F'(3'E'F /'.D� '9E '2 ',*E'9� �4'H12� H A1E'F/G� F8'E� /1 4�3*G'� 1H3�G (3�'1 E$+1 (H/ . 4�3*G'� 1H3�G /1 ,F� ,G'F� 'HD  -'E�'F F̩D'� /HE /1 1H3�G 1' (G -/'BD .H/ 13'F/ . /1 'H'�D AH1�G ���� E�D'/� '�+1 �'1�1'F 5F9*� /1 ~*1H�1'/ H E3�H /3* (G '9*5'( 2/F/ . 3~3 4H14 (G ~'/�'FG' H 31('2'F 13�/ . '9*1'6'* /GB'F'F F�2 �3*14 �'A* . 3H3�'D /EH�1'*G' G/'�* '9*1'6'* 1' /1 /3* �1A*F/ . /1 �� E'13 ���� E�D'/�  *2'1 HB* 1H3�G  F̩D'� /HE  A1E'F 'F-D'D E,D3 1H3�G 1' 5'/1 �1/  'E' '�+1 FE'�F/�'F E,D3 E*A1B F4/F/ H (' *5E�E'* F̩D'� /HE E.'DA* �1/F/ . 31'F,'E /1 ~� *8'G1'* �3*1/G �'1�1'F H 3~3 F'A1E'F� 31('2'F /1 31�H( *8'G1�FF/�'F /1 ~*1H�1'/  F̩D'� /HE '2 EB'E .H/ '3*9A' /'/ . (/�F *1*�( -�E1'F� /H/E'F 1HE'FHAG' (1 1H3�G ~3 '2 -/H/ 3�5/ 3'D ~'�'F �'A* .',
    'highlights': ''FBD'( ���� 1H3�G  ,F(4� '9*1'6�  6/ 'E~1'*H1� 1H3�G (H/ �G /1 3'D ���� 1. /'/ H (G 31F�HF� -�HE* *2'1G' H (1~'�� '*-'/ ,E'G�1 4H1H� 'F,'E�/ . E('F� 'FBD'( (1 ~'�G 5D--F'F-2E�F '3*H'1 (H/ . '�F 'FBD'( /1 /H E1-DG 5H1* �1A* : /1 7HD '�F 'FBD'( /1 4G1G'� '5D� 1H3�G GE'FF/ E3�H H 3F ~*12(H1� 1H�/'/G'� *'1�.� (1,3*G'� 1. /'/ . 'FBD'( /1 EF'7B 1H3*'�� H 19�*� F�2 ~' (G ~'� EF'7B 4G1� /1 -'D ~�41H� (H/ H /GB'F'F 2E�FG' 1' *51A �1/G H /1 -'D ('2*H2�9 "F /1 E�'F .H/ (H/F/ .'
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