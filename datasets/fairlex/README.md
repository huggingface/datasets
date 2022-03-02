---
pretty_name: FairLex
annotations_creators:
- found
- machine-generated
language_creators:
- found
languages:
  ecthr:
  - en
  scotus:
  - en
  fscs:
  - de
  - fr
  - it
  cail:
  - zh
licenses:
- cc-by-nc-sa-4.0
multilinguality:
  ecthr:
  - monolingual
  scotus:
  - monolingual
  fscs:
  - multilingual
  cail:
  - monolingual
size_categories:
  ecthr:
  - 10K<n<100K
  scotus:
  - 1K<n<10K
  fscs:
    - 10K<n<100K
  cail:
    - 100K<n<1M
source_datasets:
- extended
task_categories:
  ecthr:
  - text-classification
  scotus:
  - text-classification
  fscs:
  - text-classification
  cail:
  - text-classification
task_ids:
  ecthr:
  - multi-label-classification
  - text-classification-other-bias
  - text-classification-other-gender-bias
  scotus:
  - multi-class-classification
  - topic-classification
  - text-classification-other-bias
  fscs:
  - multi-class-classification
  - text-classification-other-bias
  cail:
  - multi-class-classification
  - text-classification-other-bias
  - text-classification-other-gender-bias
---

# Dataset Card for "FairLex"

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

- **Homepage:** https://github.com/coastalcph/fairlex
- **Repository:** https://github.com/coastalcph/fairlex
- **Paper:** TBA
- **Leaderboard:** -
- **Point of Contact:** [Ilias Chalkidis](mailto:ilias.chalkidis@di.ku.dk)

### Dataset Summary

We present a benchmark suite of four datasets for evaluating the fairness of pre-trained legal language models and the techniques used to fine-tune them for downstream tasks. Our benchmarks cover four jurisdictions (European Council, USA, Swiss, and Chinese), five languages (English, German, French, Italian and Chinese) and fairness across five attributes (gender, age, nationality/region, language, and legal area). In our experiments, we evaluate pre-trained language models using several group-robust fine-tuning techniques and show that performance group disparities are vibrant in many cases, while none of these techniques guarantee fairness, nor consistently mitigate group disparities. Furthermore, we provide a quantitative and qualitative analysis of our results, highlighting open challenges in the development of robustness methods in legal NLP.

For the purpose of this work, we release four domain-specific BERT models with continued pre-training on the corpora of the examined datasets (ECtHR, SCOTUS, FSCS, CAIL). We train mini-sized BERT models with 6 Transformer blocks, 384 hidden units, and 12 attention heads. We warm-start all models from the public MiniLMv2 (Wang et al., 2021) using the distilled version of RoBERTa (Liu et al., 2019). For the English datasets (ECtHR, SCOTUS) and the one distilled from XLM-R (Conneau et al., 2021) for the rest (trilingual FSCS, and Chinese CAIL). [[Link to Models](https://huggingface.co/models?search=fairlex)]


### Supported Tasks and Leaderboards

The supported tasks are the following:

<table>
<tr><td>Dataset</td><td>Source</td><td>Sub-domain</td><td>Language</td><td>Task Type</td><td>Classes</td><tr>
<tr><td>ECtHR</td><td> <a href="https://aclanthology.org/P19-1424/">Chalkidis et al. (2019)</a> </td><td>ECHR</td><td>en</td><td>Multi-label classification</td><td>10+1</td></tr>
<tr><td>SCOTUS</td><td> <a href="http://scdb.wustl.edu">Spaeth et al. (2020)</a></td><td>US Law</td><td>en</td><td>Multi-class classification</td><td>11</td></tr>
<tr><td>FSCS</td><td> <a href="https://aclanthology.org/2021.nllp-1.3/">Niklaus et al. (2021)</a></td><td>Swiss Law</td><td>en, fr , it</td><td>Binary classification</td><td>2</td></tr>
<tr><td>CAIL</td><td> <a href="https://arxiv.org/abs/2103.13868">Wang et al. (2021)</a></td><td>Chinese Law</td><td>zh</td><td>Multi-class classification</td><td>6</td></tr>
</table>

#### ecthr

The European Court of Human Rights (ECtHR) hears allegations that a state has breached human rights provisions of the European Convention of Human Rights (ECHR). We use the dataset of Chalkidis et al. (2021), which contains 11K cases from ECtHR's public database.
Each case is mapped to *articles* of the ECHR that were violated (if any). This is a multi-label text classification task. Given the facts of a case, the goal is to predict the ECHR articles that were violated, if any, as decided (ruled) by the court. The cases are chronologically split into training (9k, 2001--16), development (1k, 2016--17), and test (1k, 2017--19) sets. 

To facilitate the study of fairness of text classifiers, we record for each case the following attributes: (a) The _defendant states_, which are the European states that allegedly violated the ECHR. The defendant states for each case is a subset of the 47 Member States of the Council of Europe; To have statistical support, we group defendant states in two groups:
Central-Eastern European states, on one hand, and all other states, as classified by the EuroVoc thesaurus. (b) The _applicant's age_ at the time of the decision. We extract the birth year of the applicant from the case facts, if possible, and classify its case in an age group (<=35, <=64, or older) ; and (c) the _applicant's gender_, extracted from the facts, if possible based on pronouns, classified in two categories (male, female).

#### scotus

The US Supreme Court (SCOTUS) is the highest federal court in the United States of America and generally hears only the most controversial or otherwise complex cases which have not been sufficiently well solved by lower courts.
We combine information from SCOTUS opinions with the Supreme Court DataBase (SCDB) (Spaeth, 2020). SCDB provides metadata (e.g., date of publication, decisions, issues, decision directions and many more) for all cases. We consider the available 14 thematic issue areas (e.g, Criminal Procedure, Civil Rights, Economic Activity, etc.). This is a single-label multi-class document classification task. Given the court opinion, the goal is to predict the issue area whose focus is on the subject matter of the controversy (dispute). SCOTUS contains a total of 9,262 cases that we split chronologically into 80% for training (7.4k, 1946--1982), 10% for development (914, 1982--1991) and 10% for testing (931, 1991--2016).

From SCDB, we also use the following attributes to study fairness: (a) the _type of respondent_, which is a manual categorization of respondents (defendants) in five categories (person, public entity, organization, facility and other); and (c) the _direction of the decision_, i.e., whether the decision is liberal, or conservative, provided by SCDB.

#### fscs

The Federal Supreme Court of Switzerland (FSCS) is the last level of appeal in Switzerland and similarly to SCOTUS, the court generally hears only the most controversial or otherwise complex cases which have not been sufficiently well solved by lower courts. The court often focus only on small parts of previous decision, where they discuss possible wrong reasoning by the lower court. The Swiss-Judgment-Predict dataset (Niklaus et al., 2021) contains more than 85K decisions from the FSCS written in one of three languages (50K German, 31K French, 4K Italian) from the years 2000 to 2020.
The dataset is not parallel, i.e., all cases are unique and decisions are written only in a single language. 
The dataset provides labels for a simplified binary (_approval_, _dismissal_) classification task. Given the facts of the case, the goal is to predict if the plaintiff's request is valid or partially valid. The cases are also chronologically split into training (59.7k, 2000-2014), development (8.2k, 2015-2016), and test (17.4k, 2017-2020) sets.

The dataset provides three additional attributes: (a) the _language_ of the FSCS written decision, in either German, French, or Italian; (b) the _legal area_ of the case (public, penal, social, civil, or insurance law) derived from the chambers where the decisions were heard; and (c) the _region_ that denotes in which federal region was the case originated.

#### cail

The Supreme People's Court of China (CAIL) is the last level of appeal in China and considers cases that originated from the high people's courts concerning matters of national importance. The Chinese AI and Law challenge (CAIL) dataset (Xiao et al., 2018) is a Chinese legal NLP dataset for judgment prediction and contains over 1m criminal cases. The dataset provides labels for *relevant article of criminal code* prediction, *charge* (type of crime) prediction, imprisonment *term* (period) prediction, and monetary *penalty* prediction. The publication of the original dataset has been the topic of an active debate in the NLP community(Leins et al., 2020; Tsarapatsanis and Aletras, 2021; Bender, 2021).

Recently, Wang et al. (2021) re-annotated a subset of approx. 100k cases with demographic attributes. Specifically the new dataset has been annotated with: (a) the _applicant's gender_, classified in two categories (male, female); and (b) the _region_ of the court that denotes in which out of the 7 provincial-level administrative regions was the case judged. We re-split the dataset chronologically into training (80k, 2013-2017), development (12k, 2017-2018), and test (12k, 2018) sets. In our study, we re-frame the imprisonment _term_ prediction and examine a soft version, dubbed _crime severity_ prediction task, a multi-class classification task, where given the facts of a case, the goal is to predict how severe was the committed crime with respect to the imprisonment term. We approximate crime severity by the length of imprisonment term, split in 6 clusters (0, <=12, <=36, <=60, <=120, >120 months).

### Languages

We consider datasets in English, German, French, Italian, and Chinese.

## Dataset Structure

### Data Instances

#### ecthr

An example of 'train' looks as follows. 
```json
{
  "text": "1.  At the beginning of the events relevant to the application, K. had a daughter, P., and a son, M., born in 1986 and 1988 respectively. ... ",
  "labels": [4],
  "defendant_state": 1,
  "applicant_gender": 0,
  "applicant_age": 0
}
```

#### scotus

An example of 'train' looks as follows.
```json
{
  "text": "United States Supreme Court MICHIGAN NAT. BANK v. MICHIGAN(1961) No. 155 Argued: Decided: March 6, 1961 </s> R.  S. 5219 permits States to tax the shares of national banks, but not at a greater rate than . . . other moneyed capital . . . coming into competition with the business of national banks ...",
  "label": 9,
  "decision_direction": 0,
  "respondent_type": 3
}
```

#### fscs

An example of 'train' looks as follows.
```json
{
  "text": "A.- Der 1955 geborene V._ war seit 1. September 1986 hauptberuflich als technischer Kaufmann bei der Firma A._ AG tätig und im Rahmen einer Nebenbeschäftigung (Nachtarbeit) ab Mai 1990 bei einem Bewachungsdienst angestellt gewesen, als er am 10....",
  "label": 0,
  "decision_language": 0,
  "legal_are": 5,
  "court_region": 2
}
```

#### cail

An example of 'train' looks as follows.
```json
{
  "text": "南宁市兴宁区人民检察院指控，2012年1月1日19时许，被告人蒋满德在南宁市某某路某号某市场内，因经营问题与被害人杨某某发生争吵并推打 ...",
  "label": 0,
  "defendant_gender": 0,
  "court_region": 5
}
```

### Data Fields

#### ecthr_a
- `text`: a `string` feature (factual paragraphs (facts) from the case description).
- `labels`: a list of classification labels (a list of violated ECHR articles, if any). The ECHR articles considered are 2, 3, 5, 6, 8, 9, 11, 14, P1-1.
- `defendant_state`: Defendant State group (C.E. European, Rest of Europe)
- `applicant_gender`: The gender of the applicant (N/A, Male, Female)
- `applicant_age`: The age group of the applicant (N/A, <=35, <=64, or older)

#### scotus
- `text`: a `string` feature (the court opinion).
- `label`: a classification label (the relevant issue area). The issue areas are: (1, Criminal Procedure), (2, Civil Rights), (3, First Amendment), (4, Due Process), (5, Privacy), (6, Attorneys), (7, Unions), (8, Economic Activity), (9, Judicial Power), (10, Federalism), (11, Interstate Relations), (12, Federal Taxation), (13, Miscellaneous), (14, Private Action).
- `respondent_type`:  the type of respondent, which is a manual categorization (clustering) of respondents (defendants) in five categories (person, public entity, organization, facility and other).
- `decision_direction`: the direction of the decision, i.e., whether the decision is liberal, or conservative, provided by SCDB.

#### fscs
- `text`: a `string` feature (an EU law).
- `label`: a classification label (approval or dismissal of the appeal).
- `language`: the language of the FSCS written decision, (German, French, or Italian).
- `legal_area`: the legal area of the case (public, penal, social, civil, or insurance law) derived from the chambers where the decisions were heard.
-  `region`: the region that denotes in which federal region was the case originated.

#### cail
- `text`: a `string` feature (the factual description of the case).
- `label`: a classification label (crime severity derived by the inprisonment term).
- `defendant_gender`: the gender of the defendant (Male or Female).
- `court_region`: the region of the court that denotes in which out of the 7 provincial-level administrative regions was the case judged.

### Data Splits

<table>
<tr><td>Dataset </td><td>Training</td><td>Development</td><td>Test</td><td>Total</td></tr>
<tr><td>ECtHR</td><td>9000</td><td>1000</td><td>1000</td><td>11000</td></tr>
<tr><td>SCOTUS</td><td>7417</td><td>914</td><td>931</td><td>9262</td></tr>
<tr><td>FSCS</td><td>59709</td><td>8208</td><td>17357</td><td>85274</td></tr>
<tr><td>CAIL</td><td>80000</td><td>12000</td><td>12000</td><td>104000</td></tr>
</table>

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data 
<table>
<tr><td>Dataset</td><td>Source</td><td>Sub-domain</td><td>Language</td><td>Task Type</td><td>Classes</td><tr>
<tr><td>ECtHR</td><td> <a href="https://aclanthology.org/P19-1424/">Chalkidis et al. (2019)</a> </td><td>ECHR</td><td>en</td><td>Multi-label classification</td><td>10+1</td></tr>
<tr><td>SCOTUS</td><td> <a href="http://scdb.wustl.edu">Spaeth et al. (2020)</a></td><td>US Law</td><td>en</td><td>Multi-class classification</td><td>14</td></tr>
<tr><td>FSCS</td><td> <a href="https://arxiv.org/abs/2109.00904">Chalkidis et al. (2021b)</a></td><td>Swiss Law</td><td>en, fr , it</td><td>Binary classification</td><td>2</td></tr>
<tr><td>CAIL</td><td> <a href="https://arxiv.org/abs/2105.03887">Wang et al. (2021)</a></td><td>Chinese Law</td><td>zh</td><td>Multi-class classification</td><td>6</td></tr>
</table>

#### Initial Data Collection and Normalization

We standardize and put together four datasets: ECtHR (Chalkidis et al., 2021), SCOTUS (Spaeth et al., 2020), FSCS (Niklaus et al., 2021), and CAIL (Xiao et al., 2018; Wang et al., 2021) that are already  publicly  available.

The benchmark is not a blind stapling of pre-existing resources, we augment previous datasets. In the case of ECtHR, previously unavailable demographic attributes have been released to make the original dataset amenable for fairness research. For SCOTUS, two resources (court opinions with SCDB) have been combined for the very same reason, while the authors provide a manual categorization (clustering) of respondents.

All datasets, except SCOTUS, are publicly available and have been previously published. If datasets or the papers where they were introduced in were not compiled or written by the authors, the original work is referenced and authors encourage FairLex users to do so as well. In fact, this work should only be referenced, in addition to citing the original work, when jointly experimenting with multiple FairLex datasets and using the FairLex evaluation framework and infrastructure, or use any newly introduced annotations (ECtHR, SCOTUS). Otherwise only the original work should be cited.

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

All classification labels rely on legal decisions (ECtHR, FSCS, CAIL), or are part of archival procedures (SCOTUS).

The demographic attributes and other metadata are either provided by the legal databases or have been extracted automatically from the text  by means of Regular Expressions. 

Consider the **Dataset Description** and **Discussion of Biases** sections, and the original publication for detailed information.

### Personal and Sensitive Information

ECtHR cases are partially annonymized by the court. Its data is processed and made public in accordance with the European Data Protection Law.
SCOTUS cases may also contain personal information and the data is processed and made available by the US Supreme Court, whose proceedings are public.  While this ensures compliance with US law, it is very likely that similarly to the ECtHR any processing could be justified by either implied consent or legitimate interest under European law. In FSCS, the names of the parties have been redacted by the court according to its official guidelines. To the best of our knowledge, same applies for CAIL.

## Considerations for Using the Data

### Social Impact of Dataset

This work can help practitioners to build assisting technology for legal professionals - with respect to the legal framework (jurisdiction) they operate -; technology that does not only rely on performance on majority groups, but also considering minorities and the robustness of the developed models across them. This is an important application field, where more research should be conducted (Tsarapatsanis and Aletras, 2021) in order to improve legal services and democratize law, but more importantly highlight (inform the audience on) the various multi-aspect shortcomings seeking a responsible and ethical (fair) deployment of technology.

### Discussion of Biases

The current version of FairLex covers a very small fraction of legal applications, jurisdictions, and protected attributes. The benchmark inevitably cannot cover "_everything in the whole wide (legal) world_" (Raji et al., 2021), but nonetheless we believe that the published resources will help critical research in the area of fairness. 

Some protected attributes within the datasets are extracted automatically, i.e., the gender and the age of the ECtHR dataset, by means of Regular Expressions, or manually clustered by the authors, such as the defendant state in the ECtHR dataset and the respondent attribute in the SCOTUS dataset. Those assumptions and simplifications can hold in an experimental setting only and by no means should be used in real-world applications where some simplifications, e.g., binary gender, would not be appropriate. By no means, the authors or future users have to endorse the law standards or framework of the examined datasets, to any degree rather than the publication and use of the data.

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


## Additional Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


### Dataset Curators

*Ilias Chalkidis, Tommaso Pasini, Sheng Zhang, Letizia Tomada, Letizia, Sebastian Felix Schwemer, Anders Søgaard.*
*FairLex: A Multilingual Benchmark for Evaluating Fairness in Legal Text Processing.*
*2022. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, Dublin, Ireland.*

**Note:** The original datasets have been originally curated by others, and further curated (updated) by means of this benchmark.


### Licensing Information

The benchmark is released under a [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. The licensing is compatible with the licensing of former material (remixed, transformed datasets).


### Citation Information

[*Ilias Chalkidis, Tommaso Pasini, Sheng Zhang, Letizia Tomada, Letizia, Sebastian Felix Schwemer, Anders Søgaard.*
*FairLex: A Multilingual Benchmark for Evaluating Fairness in Legal Text Processing.*
*2022. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, Dublin, Ireland.*](https://arxiv.org/abs/xxx/xxx)
```
@inproceedings{chalkidis-etal-2022-fairlex,
      author={Chalkidis, Ilias and Passini, Tommaso and Zhang, Sheng and
              Tomada, Letizia and Schwemer, Sebastian Felix and Søgaard, Anders},
      title={FairLex: A Multilingual Benchmark for Evaluating Fairness in Legal Text Processing},
      booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics},
      year={2022},
      address={Dublin, Ireland}
}
```

**Note:** Please consider citing and give credits to all publications releasing the examined datasets.

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.
