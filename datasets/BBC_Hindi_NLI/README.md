---
YAML tags:
- copy-paste the tags obtained with the tagging app: http://34.68.228.168:8501/
---

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

- HomePage : https://github.com/midas-research/hindi-nli-data
- Paper : https://shagunuppal.github.io/pdf/AACL_IJCNLP_Hindi_NLI.pdf
- Point of Contact : https://github.com/midas-research/hindi-nli-data

### Dataset Summary

- Dataset for Natural Language Inference in Hindi Language. BBC Hindi Dataset consists of textual-entailment pairs.
- Each row of the Datasets if made up of 4 columns - Context, Hypothesis, Entailment_Label and Topic_Label.
- Context and Hypothesis is written in Hindi while Entailment_Label is in English.
- Entailment_label is of 2 types - entailed and not-entailed.
- Dataset can be used to train models for Natural Language Inference tasks in Hindi Language.
[More Information Needed]

### Supported Tasks and Leaderboards

- Natural Language Inference for Hindi

### Languages

Dataset is in Hindi

## Dataset Structure

- Data is structured in TSV format. 
- Train and Test files are in seperate files


### Data Fields

- Each row contatins 4 columns - Context, Hypothesis, Entailment_Label and Topic_Label.

### Data Splits

- Train : 15553
- Test : 2593

## Dataset Creation

- We employ a recasting technique from Poliak et al. (2018a,b) to convert publicly available BBC Hindi news text classification datasets in Hindi and pose them as TE problems
- In this recasting process, we build template hypotheses for each class in the label taxonomy
- Then, we pair the original annotated sentence with each of the template hypotheses to create TE samples.
- For more information on the recasting process, refer to paper https://shagunuppal.github.io/pdf/AACL_IJCNLP_Hindi_NLI.pdf

### Source Data

Source Dataset for the recasting process is the BBC Hindi Headlines Dataset(https://github.com/NirantK/hindi2vec/releases/tag/bbc-hindi-v0.1)

#### Initial Data Collection and Normalization

-  BBC Hindi News Classification Dataset contains 4, 335 Hindi news headlines tagged across 14 categories: India, Pakistan,news, International, entertainment, sport, science, China, learning english, social, southasia, business, institutional, multimedia
-  We processed this dataset to combine two sets of relevant but low prevalence classes.
- Namely, we merged the samples from Pakistan, China, international, and southasia as one class called international.
- Likewise, we also merged samples from news, business, social, learning english, and institutional as news.
- Lastly, we also removed the class multimedia because there were very few samples.

#### Who are the source language producers?

Pls refer to this paper: https://github.com/midas-research/hindi-nli-data

### Annotations

#### Annotation process

Annotation process has been described in Dataset Creation Section.

#### Who are the annotators?

Annotation is done automatically.

### Personal and Sensitive Information

No Personal and Sensitive Information is mentioned in the Datasets.

## Considerations for Using the Data

Pls refer to this paper: https://shagunuppal.github.io/pdf/AACL_IJCNLP_Hindi_NLI.pdf

### Discussion of Biases

Pls refer to this paper: https://shagunuppal.github.io/pdf/AACL_IJCNLP_Hindi_NLI.pdf

### Other Known Limitations

No other known limitations

## Additional Information

Pls refer to this link: https://github.com/midas-research/hindi-nli-data

### Dataset Curators

- If you use the corpus in a product or application, then please credit the authors and [Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi] (http://midas.iiitd.edu.in) appropriately. Also, if you send us an email, we will be thrilled to know about how you have used the corpus.
- If interested in commercial use of the corpus, send email to midas@iiitd.ac.in.
- Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi, India disclaims any responsibility for the use of the corpus and does not provide technical support. However, the contact listed above will be happy to respond to queries and clarifications
- Please feel free to send us an email:
  - with feedback regarding the corpus.
  - with information on how you have used the corpus.
  - if interested in a collaborative research project.


### Licensing Information

Copyright (C) 2019 Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi (MIDAS, IIIT-Delhi)

### Citation Information

Paper accepted at AACL-IJCNLP 2020. 
