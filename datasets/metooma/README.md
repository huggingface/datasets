
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
- text-retrieval
task_ids:
- multi-class-classification
- multi-label-classification

# Dataset Card for [Dataset Name]

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

- **Homepage:** (https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JN4EYU)
- **Paper:** (https://ojs.aaai.org//index.php/ICWSM/article/view/7292)


### Dataset Summary

The dataset consists of tweets belonging to #MeToo movement on Twitter, labelled into different categories. Due to Twitters development policies, we only provide thetweet IDs and corresponding labels, other data can be fetched via Twitter API. The data has been labelled by experts, with the majority taken into the account for deciding the final label. We provide these labels for each of the tweets.
Relevance
Directed Hate
Generalized Hate
Sarcasm
Allegation
Justification
Refutation
Support
Oppose
There could be more than one label applicable for a single tweet, for detailed annotation information and usage guidelines please refer to the accompanying paper https://aaai.org/ojs/index.php/ICWSM/article/view/7292 

### Supported Tasks and Leaderboards

Multi Label and Multi-Class Classification

### Languages

English

## Dataset Structure

### Data Instances

Tweet ID and the apprpriate labels 

### Data Fields

Tweet ID and appropriate labels (binary label applicable for a data point) and multiple labels for each Tweet ID

### Data Splits

- Train: 7979
- Test: 1996

## Dataset Creation

### Curation Rationale
We expect this dataset would be of great interest and use to both computational and socio-linguists. For computational linguists, it provides an opportunity to model three new complex dialogue acts (allegation, refutation, and justification) and also to study how these acts interact with some of the other linguistic components like stance, hate, and sarcasm. For socio-linguists, it provides an opportunity to explore how a movement manifests in social media. 


### Source Data
- Twitter

#### Initial Data Collection and Normalization

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

#### Who are the source language producers?

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

### Annotations

#### Annotation process

Please refer to this paper for detailed annotation process and related information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

#### Who are the annotators?

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

### Personal and Sensitive Information

Considering Twitters policy for distribution of data, only Tweet ID and applicable labels are shared for the public use. 

## Considerations for Using the Data

### Social Impact of Dataset
Please refer to the ethics and discussion section of the mentioned publication for appropriate sharing of this dataset. 


### Discussion of Biases

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

### Other Known Limitations

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

## Additional Information

Please refer to this link: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JN4EYU

### Dataset Curators

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

### Licensing Information

[More Information Needed]

### Citation Information

@article{Gautam_Mathur_Gosangi_Mahata_Sawhney_Shah_2020, title={#MeTooMA: Multi-Aspect Annotations of Tweets Related to the MeToo Movement}, volume={14}, url={https://aaai.org/ojs/index.php/ICWSM/article/view/7292}, abstractNote={&lt;p&gt;In this paper, we present a dataset containing 9,973 tweets related to the MeToo movement that were manually annotated for five different linguistic aspects: relevance, stance, hate speech, sarcasm, and dialogue acts. We present a detailed account of the data collection and annotation processes. The annotations have a very high inter-annotator agreement (0.79 to 0.93 k-alpha) due to the domain expertise of the annotators and clear annotation instructions. We analyze the data in terms of geographical distribution, label correlations, and keywords. Lastly, we present some potential use cases of this dataset. We expect this dataset would be of great interest to psycholinguists, socio-linguists, and computational linguists to study the discursive space of digitally mobilized social movements on sensitive issues like sexual harassment.&lt;/p&#38;gt;}, number={1}, journal={Proceedings of the International AAAI Conference on Web and Social Media}, author={Gautam, Akash and Mathur, Puneet and Gosangi, Rakesh and Mahata, Debanjan and Sawhney, Ramit and Shah, Rajiv Ratn}, year={2020}, month={May}, pages={209-216} }