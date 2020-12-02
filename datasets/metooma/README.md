---
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
---

# Dataset Card for #MeTooMA dataset

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

- **Homepage:** https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JN4EYU
- **Paper:** https://ojs.aaai.org//index.php/ICWSM/article/view/7292
- **Point of Contact:** https://github.com/midas-research/MeTooMA


### Dataset Summary

- The dataset consists of tweets belonging to #MeToo movement on Twitter, labelled into different categories.
- This dataset includes more data points and has more labels than any of the previous datasets that contain social media
posts about sexual abuse discloures. Please refer to the Related Datasets of the publication for a detailed information about this.
- Due to Twitters development policies, the authors provide only the tweet IDs and corresponding labels,
other data can be fetched via Twitter API.
- The data has been labelled by experts, with the majority taken into the account for deciding the final label.
- The authors provide these labels for each of the tweets.
  - Relevance
  - Directed Hate
  - Generalized Hate
  - Sarcasm
  - Allegation
  - Justification
  - Refutation
  - Support
  - Oppose
- The definitions for each task/label is in the main publication.
- Please refer to the accompanying paper https://aaai.org/ojs/index.php/ICWSM/article/view/7292 for statistical analysis on the textual data
extracted from this dataset.
- The language of all the tweets in this dataset is English
- Time period: October 2018 - December 2018
- Suggested Use Cases of this dataset:
  - Evaluating usage of linguistic acts such as: hate-spech and sarcasm in the incontext of public sexual abuse discloures.
  - Extracting actionable insights and virtual dynamics of gender roles in sexual abuse revelations.
  - Identifying how influential people were potrayed on public platform in the
  events of mass social movements.
  - Polarization analysis based on graph simulations of social nodes of users involved
  in the #MeToo movement.


### Supported Tasks and Leaderboards

Multi Label and Multi-Class Classification

### Languages

English

## Dataset Structure
- The dataset is structured into CSV format with TweetID and accompanying labels.
- Train and Test sets are split into respective files.

### Data Instances

Tweet ID and the appropriate labels

### Data Fields

Tweet ID and appropriate labels (binary label applicable for a data point) and multiple labels for each Tweet ID

### Data Splits

- Train: 7979
- Test: 1996

## Dataset Creation

### Curation Rationale

- Twitter was the major source of all the public discloures of sexual abuse incidents during the #MeToo movement.
- People expressed their opinions over issues which were previously missing from the social media space.
- This provides an option to study the linguistic behaviours of social media users in an informal setting,
therefore the authors decide to curate this annotated dataset.
- The authors expect this dataset would be of great interest and use to both computational and socio-linguists.
- For computational linguists, it provides an opportunity to model three new complex dialogue acts (allegation, refutation, and justification) and also to study how these acts interact with some of the other linguistic components like stance, hate, and sarcasm. For socio-linguists, it provides an opportunity to explore how a movement manifests in social media.


### Source Data
- Source of all the data points in this dataset is Twitter social media platform.

#### Initial Data Collection and Normalization

- All the tweets are mined from Twitter with initial search paramters identified using keywords from the #MeToo movement.
- Redundant keywords were removed based on manual inspection.
- Public streaming APIs of Twitter were used for querying with the selected keywords.
- Based on text de-duplication and cosine similarity score, the set of tweets were pruned.
- Non english tweets were removed.
- The final set was labelled by experts with the majority label taken into the account for deciding the final label.
- Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

#### Who are the source language producers?

Please refer to this paper for detailed information: https://ojs.aaai.org//index.php/ICWSM/article/view/7292

### Annotations

#### Annotation process

- The authors chose against crowd sourcing for labeling this dataset due to its highly sensitive nature.
- The annotators are domain experts having degress in advanced clinical psychology and gender studies.
- They were provided a guidelines document with instructions about each task and its definitions, labels and examples.
- They studied the document, worked a few examples to get used to this annotation task.
- They also provided feedback for improving the class definitions.
- The annotation process is not mutually exclusive, implying that presence of one label does not mean the
absence of the other one.


#### Who are the annotators?

- The annotators are domain experts having a degree in clinical psychology and gender studies.
- Please refer to the accompnaying paper for a detailed annotation process.

### Personal and Sensitive Information

- Considering Twitters policy for distribution of data, only Tweet ID and applicable labels are shared for the public use.
- It is highly encouraged to use this dataset for scientific purposes only.
- This dataset collection completely follows the Twitter mandated guidelines for distribution and usage.

## Considerations for Using the Data

### Social Impact of Dataset

- The authors of this dataset do not intend to conduct a population centric analysis of #MeToo movement on Twitter.
- The authors acknowledge that findings from this dataset cannot be used as-is for any direct social intervention, these
should be used to assist already existing human intervention tools and therapies.
- Enough care has been taken to ensure that this work comes of as trying to target a specific person for their
personal stance of issues pertaining to the #MeToo movement.
- The authors of this work do not aim to vilify anyone accused in the #MeToo movement in any manner.
- Please refer to the ethics and discussion section of the mentioned publication for appropriate sharing of this dataset
and social impact of this work.


### Discussion of Biases

- The #MeToo movement acted as a catalyst for implementing social policy changes to benefit the members of
community affected by sexual abuse.
- Any work undertaken on this dataset should aim to minimize the bias against minority groups which
might amplified in cases of sudden outburst of public reactions over sensitive social media discussions.

### Other Known Limitations

- Considering privacy concerns, social media practitioners should be aware of making automated interventions
to aid the victims of sexual abuse as some people might not prefer to disclose their notions.
- Concerned social media users might also repeal their social information, if they found out that their
information is being used for computational purposes, hence it is important seek subtle individual consent
before trying to profile authors involved in online discussions to uphold personal privacy.

## Additional Information

Please refer to this link: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JN4EYU

### Dataset Curators

- If you use the corpus in a product or application, then please credit the authors
and [Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi]
(http://midas.iiitd.edu.in) appropriately.
Also, if you send us an email, we will be thrilled to know about how you have used the corpus.
- If interested in commercial use of the corpus, send email to midas@iiitd.ac.in.
- Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi, India
disclaims any responsibility for the use of the corpus and does not provide technical support.
However, the contact listed above will be happy to respond to queries and clarifications
- Please feel free to send us an email:
  - with feedback regarding the corpus.
  - with information on how you have used the corpus.
  - if interested in having us analyze your social media data.
  - if interested in a collaborative research project.

### Licensing Information

[More Information Needed]

### Citation Information

Please cite the following publication if you make use of the dataset: https://ojs.aaai.org/index.php/ICWSM/article/view/7292

```

@article{Gautam_Mathur_Gosangi_Mahata_Sawhney_Shah_2020, title={#MeTooMA: Multi-Aspect Annotations of Tweets Related to the MeToo Movement}, volume={14}, url={https://aaai.org/ojs/index.php/ICWSM/article/view/7292}, abstractNote={&lt;p&gt;In this paper, we present a dataset containing 9,973 tweets related to the MeToo movement that were manually annotated for five different linguistic aspects: relevance, stance, hate speech, sarcasm, and dialogue acts. We present a detailed account of the data collection and annotation processes. The annotations have a very high inter-annotator agreement (0.79 to 0.93 k-alpha) due to the domain expertise of the annotators and clear annotation instructions. We analyze the data in terms of geographical distribution, label correlations, and keywords. Lastly, we present some potential use cases of this dataset. We expect this dataset would be of great interest to psycholinguists, socio-linguists, and computational linguists to study the discursive space of digitally mobilized social movements on sensitive issues like sexual harassment.&lt;/p&#38;gt;}, number={1}, journal={Proceedings of the International AAAI Conference on Web and Social Media}, author={Gautam, Akash and Mathur, Puneet and Gosangi, Rakesh and Mahata, Debanjan and Sawhney, Ramit and Shah, Rajiv Ratn}, year={2020}, month={May}, pages={209-216} }

```
