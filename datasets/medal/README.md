---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-disambiguation
paperswithcode_id: medal
pretty_name: MeDAL
---
# Dataset Card for the MeDAL dataset

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

- **Homepage:** []()
- **Repository:** [https://github.com/BruceWen120/medal]()
- **Paper:** [https://www.aclweb.org/anthology/2020.clinicalnlp-1.15/]()
- **Dataset (Kaggle):** [https://www.kaggle.com/xhlulu/medal-emnlp]()
- **Dataset (Zenodo):** [https://zenodo.org/record/4265632]()
- **Pretrained model:** [https://huggingface.co/xhlu/electra-medal]()
- **Leaderboard:** []()
- **Point of Contact:** []()

### Dataset Summary

A large medical text dataset (14Go) curated to 4Go for abbreviation disambiguation, designed for natural language understanding pre-training in the medical domain. For example, DHF can be disambiguated to dihydrofolate, diastolic heart failure, dengue hemorragic fever or dihydroxyfumarate

### Supported Tasks and Leaderboards

Medical abbreviation disambiguation

### Languages

English (en)

## Dataset Structure

Each file is a table consisting of three columns:
* text: The normalized content of an abstract
* location: The location (index) of each abbreviation that was substituted
* label: The word at that was substituted at the given location


### Data Instances

An example from the train split is:

```
{'abstract_id': 14145090,
 'text': 'velvet antlers vas are commonly used in traditional chinese medicine and invigorant and contain many PET components for health promotion the velvet antler peptide svap is one of active components in vas based on structural study the svap interacts with tgfÎ² receptors and disrupts the tgfÎ² pathway we hypothesized that svap prevents cardiac fibrosis from pressure overload by blocking tgfÎ² signaling SDRs underwent TAC tac or a sham operation T3 one month rats received either svap mgkgday or vehicle for an additional one month tac surgery induced significant cardiac dysfunction FB activation and fibrosis these effects were improved by treatment with svap in the heart tissue tac remarkably increased the expression of tgfÎ² and connective tissue growth factor ctgf ROS species C2 and the phosphorylation C2 of smad and ERK kinases erk svap inhibited the increases in reactive oxygen species C2 ctgf expression and the phosphorylation of smad and erk but not tgfÎ² expression in cultured cardiac fibroblasts angiotensin ii ang ii had similar effects compared to tac surgery such as increases in Î±smapositive CFs and collagen synthesis svap eliminated these effects by disrupting tgfÎ² IB to its receptors and blocking ang iitgfÎ² downstream signaling these results demonstrated that svap has antifibrotic effects by blocking the tgfÎ² pathway in CFs',
 'location': [63],
 'label': ['transverse aortic constriction']}
 ```

### Data Fields

The column types are:
* text: content of the abstract as a string
* location: index of the substitution as an integer
* label: substitued word as a string

### Data Splits

The following files are present:

* `full_data.csv`: The full dataset with all 14M abstracts.
* `train.csv`: The subset used to train the baseline and proposed models.
* `valid.csv`: The subset used to validate the model during training for hyperparameter selection.
* `test.csv`: The subset used to evaluate the model and report the results in the tables.

## Dataset Creation


### Curation Rationale

[More Information Needed]

### Source Data

The original dataset was retrieved and modified from the [NLM website](https://www.nlm.nih.gov/databases/download/pubmed_medline.html).

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

Details on how the abbreviations were created can be found in section 2.2 (Dataset Creation) of the [ACL ClinicalNLP paper](https://aclanthology.org/2020.clinicalnlp-1.15.pdf).

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

Since the abstracts are written in English, the data is biased towards anglo-centric medical research. If you plan to use a model pre-trained on this dataset for a predominantly non-English community, it is important to verify whether there are negative biases present in your model, and ensure that they are correctly mitigated. For instance, you could fine-tune your dataset on a multilingual medical disambiguation dataset, or collect a dataset specific to your use case.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The ELECTRA model is licensed under [Apache 2.0](https://github.com/google-research/electra/blob/master/LICENSE). The license for the libraries used in this project (`transformers`, `pytorch`, etc.) can be found in their respective GitHub repository. Our model is released under a MIT license.


The original dataset was retrieved and modified from the [NLM website](https://www.nlm.nih.gov/databases/download/pubmed_medline.html). By using this dataset, you are bound by the [terms and conditions](https://www.nlm.nih.gov/databases/download/terms_and_conditions_pubmed.html) specified by NLM:

> INTRODUCTION
> 
> Downloading data from the National Library of Medicine FTP servers indicates your acceptance of the following Terms and Conditions: No charges, usage fees or royalties are paid to NLM for this data.
> 
> MEDLINE/PUBMED SPECIFIC TERMS
> 
> NLM freely provides PubMed/MEDLINE data. Please note some PubMed/MEDLINE abstracts may be protected by copyright.  
> 
> GENERAL TERMS AND CONDITIONS
> 
>    * Users of the data agree to:
>        * acknowledge NLM as the source of the data by including the phrase "Courtesy of the U.S. National Library of Medicine" in a clear and conspicuous manner,
>        * properly use registration and/or trademark symbols when referring to NLM products, and
>        * not indicate or imply that NLM has endorsed its products/services/applications. 
>
>    * Users who republish or redistribute the data (services, products or raw data) agree to:
>        * maintain the most current version of all distributed data, or
>        * make known in a clear and conspicuous manner that the products/services/applications do not reflect the most current/accurate data available from NLM.
>
>    * These data are produced with a reasonable standard of care, but NLM makes no warranties express or implied, including no warranty of merchantability or fitness for particular purpose, regarding the accuracy or completeness of the data. Users agree to hold NLM and the U.S. Government harmless from any liability resulting from errors in the data. NLM disclaims any liability for any consequences due to use, misuse, or interpretation of information contained or not contained in the data.
>
>    * NLM does not provide legal advice regarding copyright, fair use, or other aspects of intellectual property rights. See the NLM Copyright page.
>
>    * NLM reserves the right to change the type and format of its machine-readable data. NLM will take reasonable steps to inform users of any changes to the format of the data before the data are distributed via the announcement section or subscription to email and RSS updates.

### Citation Information

```
@inproceedings{wen-etal-2020-medal,
    title = "{M}e{DAL}: Medical Abbreviation Disambiguation Dataset for Natural Language Understanding Pretraining",
    author = "Wen, Zhi  and
      Lu, Xing Han  and
      Reddy, Siva",
    booktitle = "Proceedings of the 3rd Clinical Natural Language Processing Workshop",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.clinicalnlp-1.15",
    pages = "130--135",
    abstract = "One of the biggest challenges that prohibit the use of many current NLP methods in clinical settings is the availability of public datasets. In this work, we present MeDAL, a large medical text dataset curated for abbreviation disambiguation, designed for natural language understanding pre-training in the medical domain. We pre-trained several models of common architectures on this dataset and empirically showed that such pre-training leads to improved performance and convergence speed when fine-tuning on downstream medical tasks.",
}
```

### Contributions

Thanks to [@Narsil](https://github.com/Narsil) and [@xhlulu](https://github.com/xhlulu)) for adding this dataset.
