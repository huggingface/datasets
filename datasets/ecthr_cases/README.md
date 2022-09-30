---
annotations_creators:
- expert-generated
- found
language_creators:
- found
language:
- en
license:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
- text-classification-other-rationale-extraction
- text-classification-other-legal-judgment-prediction
paperswithcode_id: ecthr
pretty_name: European Court of Human Rights Cases
---

# Dataset Card for the ECtHR cases dataset

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

- **Homepage:** http://archive.org/details/ECtHR-NAACL2021/
- **Repository:** http://archive.org/details/ECtHR-NAACL2021/
- **Paper:** https://arxiv.org/abs/2103.13084
- **Leaderboard:** TBA
- **Point of Contact:** [Ilias Chalkidis](mailto:ihalk@aueb.gr)

### Dataset Summary

The European Court of Human Rights (ECtHR) hears allegations regarding breaches in human rights provisions of the European Convention of Human Rights (ECHR) by European states. The Convention is available at https://www.echr.coe.int/Documents/Convention_ENG.pdf. 
The court rules on a subset of all ECHR articles, which are predefined (alleged) by the applicants (*plaintiffs*). 

Our dataset comprises 11k ECtHR cases and can be viewed as an enriched version of the ECtHR dataset of Chalkidis et al. (2019), which did not provide ground truth for alleged article violations (articles discussed) and rationales. The new dataset includes the following:

**Facts:** Each judgment includes a list of paragraphs that represent the facts of the case, i.e., they describe the main events that are relevant to the case, in numbered paragraphs. We hereafter call these paragraphs *facts* for simplicity. Note that the facts are presented in chronological order. Not all facts have the same impact or hold crucial information with respect to alleged article violations and the court's assessment; i.e., facts may refer to information that is trivial or otherwise irrelevant to the legally crucial allegations against *defendant* states.

**Allegedly violated articles:** Judges rule on specific accusations (allegations) made by the applicants (Harris, 2018). In ECtHR cases, the judges discuss and rule on the violation, or not, of specific articles of the Convention. The articles to be discussed (and ruled on) are put forward (as alleged article violations) by the applicants and are included in the dataset as ground truth; we identify 40 violable articles in total. The rest of the articles are procedural, i.e., the number of judges, criteria for office, election of judges, etc. In our experiments, however, the models are not aware of the allegations. They predict the Convention articles that will be discussed (the allegations) based on the case's facts, and they also produce rationales for their predictions. Models of this kind could be used by potential applicants to help them formulate future allegations (articles they could claim to have been violated), as already noted, but here we mainly use the task as a test-bed for rationale extraction.

**Violated articles:** The court decides which allegedly violated articles have indeed been violated. These decisions are also included in our dataset and could be used for full legal judgment prediction experiments (Chalkidis et al., 2019). However, they are not used in the experiments of this work.

**Silver allegation rationales:** Each decision of the ECtHR includes references to facts of the case (e.g., *"See paragraphs 2 and 4."*) and case law (e.g., *"See Draci vs. Russia (2010)"*.). We identified references to each case's facts and retrieved the corresponding paragraphs using regular expressions. These are included in the dataset as silver allegation rationales, on the grounds that the judges refer to these paragraphs when ruling on the allegations.

**Gold allegation rationales:** A legal expert with experience in ECtHR cases annotated a subset of 50 test cases to identify the relevant facts (paragraphs) of the case that support the allegations (alleged article violations). In other words, each identified fact justifies (hints) one or more alleged violations.

### Supported Tasks and Leaderboards

The dataset supports:

**Alleged violation prediction** (`alleged-violation-prediction`):  A multi-label text classification task where, given the facts of a ECtHR case, a model predicts which of the 40 violable ECHR articles were allegedly violated according to the applicant(s). Consult Chalkidis et al. (2021), for details.

**Violation prediction**  (`violation-prediction`): A multi-label text classification task where, given the facts of a ECtHR case, a model predicts which of the allegedly violated ECHR articles were violated, as decided (ruled) by the ECtHR court. Consult Chalkidis et al. (2019), for details.

**Rationale extraction:** A model can also predict the facts of the case that most prominently support its decision with respect to a classification task. Silver rationales can be used for both classification tasks, while gold rationales are only focused on the *alleged violation prediction* task.

### Languages

All documents are written in English.

## Dataset Structure

### Data Instances

This example was too long and was cropped:

```json
{
 "facts": [
  "8.  In 1991 Mr Dusan Slobodnik, a research worker in the field of literature, ...",
  "9.  On 20 July 1992 the newspaper Telegraf published a poem by the applicant.",
  "10.  The poem was later published in another newspaper.", 
   "...",
  "39.  The City Court further dismissed the claim in respect of non-pecuniary damage ... ",
  "40.  The City Court ordered the plaintiff to pay SKK 56,780 to the applicant ...",
  "41.  On 25 November 1998 the Supreme Court upheld the decision of the Bratislava City Court ..."
 ],
 "labels": ["14", "10", "9", "36"], 
 "silver_rationales": [27],
 "gold_rationales": []
}
```

### Data Fields

`facts`: (**List[str]**) The paragraphs (facts) of the case.\
`labels`: (**List[str]**) The ECHR articles under discussion (*Allegedly violated articles*); or the allegedly violated ECHR articles that found to be violated by the court (judges).\
`silver_rationales`: (**List[int]**) Indices of the paragraphs (facts) that are present in the court's assessment.\
`gold_rationales`: (**List[int]**) Indices of the paragraphs (facts) that support alleged violations, according to a legal expert.

### Data Splits

| Split         | No of ECtHR cases                         | Silver rationales ratio | Avg. allegations / case |
| ------------------- | ------------------------------------  |  --- | --- |
| Train | 9,000 | 24% | 1.8 |
|Development | 1,000 | 30% | 1.7 |
|Test | 1,000 | 31% | 1.7 |

## Dataset Creation

### Curation Rationale

The dataset was curated by Chalkidis et al. (2021).\
The annotations for the gold rationales are available thanks to Dimitris Tsarapatsanis (Lecturer, York Law School).

### Source Data

#### Initial Data Collection and Normalization

The original data are available at HUDOC database (https://hudoc.echr.coe.int/eng) in an unprocessed format. The data were downloaded and all information was extracted from the HTML files and several JSON metadata files.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

* The original documents are available in HTML format at HUDOC database (https://hudoc.echr.coe.int/eng), except the gold rationales. The metadata are provided by additional JSON files, produced by REST services.
* The annotations for the gold rationales are available thanks to Dimitris Tsarapatsanis (Lecturer, York Law School).


#### Who are the annotators?

Dimitris Tsarapatsanis (Lecturer, York Law School).

### Personal and Sensitive Information

Privacy statement / Protection of personal data from HUDOC (https://www.echr.coe.int/Pages/home.aspx?p=privacy)

```
The Court complies with the Council of Europe's policy on protection of personal data, in so far as this is consistent with exercising its functions under the European Convention on Human Rights.

The Council of Europe is committed to respect for private life. Its policy on protection of personal data is founded on the Secretary General’s Regulation of 17 April 1989 outlining a data protection system for personal data files in the Council of Europe. 

Most pages of the Council of Europe site require no personal information except in certain cases to allow requests for on-line services to be met. In such cases, the information is processed in accordance with the Confidentiality policy described below.
```

## Considerations for Using the Data

### Social Impact of Dataset

The publication of this dataset complies with the ECtHR data policy (https://www.echr.coe.int/Pages/home.aspx?p=privacy).

By no means do we aim to build a 'robot' lawyer or judge, and we acknowledge the possible harmful impact (Angwin et al., 2016, Dressel et al., 2018) of irresponsible deployment. 
Instead, we aim to support fair and explainable AI-assisted judicial decision making and empirical legal studies. 

For example, automated services can help applicants (plaintiffs) identify alleged violations that are supported by the facts of a case. They can help judges identify more quickly facts that support the alleged violations, contributing towards more informed judicial decision making (Zhong et al., 2020). They can also help legal experts identify previous cases related to particular allegations, helping analyze case law (Katz et al., 2012).  

Also, consider ongoing critical research on responsible AI (Elish et al., 2021) that aims to provide explainable and fair  systems to support human experts.

### Discussion of Biases

Consider the work of Chalkidis et al. (2019) for the identification of demographic bias by models.

### Other Known Limitations

N/A

## Additional Information

### Dataset Curators

Ilias Chalkidis and Dimitris Tsarapatsanis

### Licensing Information

**CC BY-NC-SA (Creative Commons / Attribution-NonCommercial-ShareAlike)**

Read  more: https://creativecommons.org/licenses/by-nc-sa/4.0/.

### Citation Information

*Ilias Chalkidis, Manos Fergadiotis, Dimitrios Tsarapatsanis, Nikolaos Aletras, Ion Androutsopoulos and Prodromos Malakasiotis. Paragraph-level Rationale Extraction through Regularization: A case study on European Court of Human Rights Cases.* 
*Proceedings of the Annual Conference of the North American Chapter of the Association for Computational Linguistics (NAACL 2021). Mexico City, Mexico. 2021.*

```
@InProceedings{chalkidis-et-al-2021-ecthr,
    title = "Paragraph-level Rationale Extraction through Regularization: A case study on European Court of Human Rights Cases",
    author = "Chalkidis, Ilias and Fergadiotis, Manos and Tsarapatsanis, Dimitrios and Aletras, Nikolaos and Androutsopoulos, Ion and Malakasiotis, Prodromos",
    booktitle = "Proceedings of the Annual Conference of the North American Chapter of the Association for Computational Linguistics",
    year = "2021",
    address = "Mexico City, Mexico",
    publisher = "Association for Computational Linguistics"
}
```

*Ilias Chalkidis, Ion Androutsopoulos and Nikolaos Aletras. Neural Legal Judgment Prediction in English.*
*Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL 2019). Florence, Italy. 2019.*

```
@InProceedings{chalkidis-etal-2019-neural,
    title = "Neural Legal Judgment Prediction in {E}nglish",
    author = "Chalkidis, Ilias  and Androutsopoulos, Ion  and Aletras, Nikolaos",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1424",
    doi = "10.18653/v1/P19-1424",
    pages = "4317--4323"
}
```

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.
