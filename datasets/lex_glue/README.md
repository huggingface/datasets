---
pretty_name: LexGLUE
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended
task_categories:
  ecthr_a:
  - text-classification
  ecthr_b:
  - text-classification
  eurlex:
  - text-classification
  scotus:
  - text-classification
  unfair_tos:
  - text-classification
  ledgar:
  - text-classification
  case_hold:
  - question-answering
task_ids:
  ecthr_a:
  - multi-label-classification
  ecthr_b:
  - multi-label-classification
  eurlex:
  - multi-label-classification
  - topic-classification
  scotus:
  - multi-class-classification
  - topic-classification
  ledgar:
  - multi-class-classification
  - topic-classification
  unfair_tos:
  - multi-label-classification
  case_hold:
  - multiple-choice-qa
---

# Dataset Card for "LexGLUE"

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

- **Homepage:** https://github.com/coastalcph/lex-glue
- **Repository:** https://github.com/coastalcph/lex-glue
- **Paper:** https://arxiv.org/abs/2110.00976
- **Leaderboard:** https://github.com/coastalcph/lex-glue
- **Point of Contact:** [Ilias Chalkidis](mailto:ilias.chalkidis@di.ku.dk)

### Dataset Summary

Inspired by the recent widespread use of the GLUE multi-task benchmark NLP dataset (Wang et al., 2018), the subsequent more difficult SuperGLUE (Wang et al., 2019), other previous multi-task NLP benchmarks (Conneau and Kiela, 2018; McCann et al., 2018), and similar initiatives in other domains (Peng et al., 2019), we introduce the *Legal General Language Understanding Evaluation (LexGLUE) benchmark*, a benchmark dataset to evaluate the performance of NLP methods in legal tasks. LexGLUE is based on seven existing legal NLP datasets, selected using criteria largely from SuperGLUE.

As in GLUE and SuperGLUE (Wang et al., 2019b,a), one of our goals is to push towards generic (or ‘foundation’) models that can cope with multiple NLP tasks, in our case legal NLP tasks possibly with limited task-specific fine-tuning. Another goal is to provide a convenient and informative entry point for NLP researchers and practitioners wishing to explore or develop methods for legalNLP. Having these goals in mind, the datasets we include in LexGLUE and the tasks they address have been simplified in several ways to make it easier for newcomers and generic models to address all tasks.

LexGLUE benchmark is accompanied by experimental infrastructure that relies on Hugging Face Transformers library and resides at: https://github.com/coastalcph/lex-glue.

### Supported Tasks and Leaderboards

The supported tasks are the following:

| Dataset | Source | Sub-domain | Task Type | Classes |
| --- | --- | --- | --- | --- |
| ECtHR (Task A) | [Chalkidis et al. (2019)](https://aclanthology.org/P19-1424/) | ECHR | Multi-label classification | 10+1 |
| ECtHR (Task B) | [Chalkidis et al. (2021a)](https://aclanthology.org/2021.naacl-main.22/)  | ECHR | Multi-label classification  | 10 | 
| SCOTUS | [Spaeth et al. (2020)](http://scdb.wustl.edu) | US Law | Multi-class classification | 14 | 
| EUR-LEX | [Chalkidis et al. (2021b)](https://arxiv.org/abs/2109.00904) | EU Law | Multi-label classification | 100 |
| LEDGAR | [Tuggener et al. (2020)](https://aclanthology.org/2020.lrec-1.155/) | Contracts | Multi-class classification | 100 |
| UNFAIR-ToS | [Lippi et al. (2019)](https://arxiv.org/abs/1805.01217) | Contracts | Multi-label classification | 8 |
| CaseHOLD | [Zheng et al. (2021)](https://arxiv.org/abs/2104.08671) | US Law | Multiple choice QA | n/a |

#### ecthr_a

The European Court of Human Rights (ECtHR) hears allegations that a state has breached human rights provisions of the European Convention of Human Rights (ECHR). For each case, the dataset provides a list of factual paragraphs (facts) from the case description. Each case is mapped to articles of the ECHR that were violated (if any).

#### ecthr_b

The European Court of Human Rights (ECtHR) hears allegations that a state has breached human rights provisions of the European Convention of Human Rights (ECHR). For each case, the dataset provides a list of factual paragraphs (facts) from the case description. Each case is mapped to articles of ECHR that were allegedly violated (considered by the court).

#### scotus

The US Supreme Court (SCOTUS) is the highest federal court in the United States of America and generally hears only the most controversial or otherwise complex cases which have not been sufficiently well solved by lower courts. This is a single-label multi-class classification task, where given a document (court opinion), the task is to predict the relevant issue areas. The 14 issue areas cluster 278 issues whose focus is on the subject matter of the controversy (dispute).

#### eurlex

European Union (EU) legislation is published in EUR-Lex portal. All EU laws are annotated by EU's Publications Office with multiple concepts from the EuroVoc thesaurus, a multilingual thesaurus maintained by the Publications Office. The current version of EuroVoc contains more than 7k concepts referring to various activities of the EU and its Member States (e.g., economics, health-care, trade). Given a document, the task is to predict its EuroVoc labels (concepts).

#### ledgar

LEDGAR dataset aims contract provision (paragraph) classification. The contract provisions come from contracts obtained from the US Securities and Exchange Commission (SEC) filings, which are publicly available from EDGAR. Each label represents the single main topic (theme) of the corresponding contract provision.

#### unfair_tos

The UNFAIR-ToS dataset contains 50 Terms of Service (ToS) from on-line platforms (e.g., YouTube, Ebay, Facebook, etc.). The dataset has been annotated on the sentence-level with 8 types of unfair contractual terms (sentences), meaning terms that potentially violate user rights according to the European consumer law.

#### case_hold

The CaseHOLD (Case Holdings on Legal Decisions) dataset includes multiple choice questions about holdings of US court cases from the Harvard Law Library case law corpus. Holdings are short summaries of legal rulings accompany referenced decisions relevant for the present case. The input consists of an excerpt (or prompt) from a court decision, containing a reference to a particular case, while the holding statement is masked out. The model must identify the correct (masked) holding statement from a selection of five choices.


The current leaderboard includes several Transformer-based (Vaswaniet al., 2017) pre-trained language models, which achieve state-of-the-art performance in most NLP tasks (Bommasani et al., 2021) and NLU benchmarks (Wang et al., 2019a).


|Dataset | ECtHR Task A  | ECtHR Task B  | SCOTUS  | EUR-LEX | LEDGAR  | UNFAIR-ToS  | CaseHOLD |
| --- | ---- | --- | --- | --- | --- | --- | --- |
| Model | μ-F1  / m-F1  | μ-F1  / m-F1  | μ-F1  / m-F1  | μ-F1  / m-F1  | μ-F1  / m-F1  | μ-F1  / m-F1 | μ-F1 / m-F1   | 
|  BERT  | **71.4**  / 64.0   | 87.6  / **77.8**  | 70.5   / 60.9  | 71.6  / 55.6  | 87.7   / 82.2  | 87.5  / 81.0 | 70.7    | 
|  RoBERTa  | 69.5  / 60.7  | 87.2  / 77.3  | 70.8   / 61.2  | 71.8  / **57.5**  | 87.9  /  82.1  | 87.7 / 81.5 | 71.7  | 
|  DeBERTa  | 69.1   / 61.2  | 87.4   / 77.3  | 70.0  / 60.0  | **72.3**  / 57.2  | 87.9   / 82.0  | 87.2 / 78.8 | 72.1   | 
|  Longformer  | 69.6  / 62.4  | 88.0  / **77.8**  | 72.2  / 62.5  | 71.9  / 56.7  | 87.7  / 82.3  | 87.7 / 80.1 | 72.0   | 
|  BigBird  | 70.5  / 63.8  | **88.1**  / 76.6  | 71.7  / 61.4  | 71.8  / 56.6  | 87.7 / 82.1  | 87.7 / 80.2 | 70.4   | 
|  Legal-BERT  | 71.2  / **64.6**  | 88.0  / 77.2  | 76.2  / 65.8  | 72.2  / 56.2  | **88.1**  / **82.7** | **88.6**  / **82.3** | 75.1 | 
|  CaseLaw-BERT  | 71.2   / 64.2  | 88.0   / 77.5  | **76.4**  / **66.2**  | 71.0  / 55.9  | 88.0  / 82.3 | 88.3  / 81.0 | **75.6**   | 

### Languages

We only consider English datasets, to make experimentation easier for researchers across the globe.

## Dataset Structure

### Data Instances

#### ecthr_a

An example of 'train' looks as follows. 
```json
{
  "text": ["8. The applicant was arrested in the early morning of 21 October 1990 ...", ...],
  "label_ids": [6]
}
```

#### ecthr_b

An example of 'train' looks as follows.
```json
{
  "text": ["8. The applicant was arrested in the early morning of 21 October 1990 ...", ...],
  "label": [5, 6]
}
```

#### scotus

An example of 'train' looks as follows.
```json
{
  "text": "Per Curiam\nSUPREME COURT OF THE UNITED STATES\nRANDY WHITE, WARDEN v. ROGER L. WHEELER\n Decided December 14, 2015\nPER CURIAM.\nA death sentence imposed by a Kentucky trial court and\naffirmed by the ...",
  "label": 8
}
```

#### eurlex

An example of 'train' looks as follows.
```json
{
  "text": "COMMISSION REGULATION (EC) No 1629/96 of 13 August 1996 on an invitation to tender for the refund on export of wholly milled round grain rice to certain third countries ...",
  "label_ids": [2, 42, 72, 76, 86]
}
```

#### ledgar

An example of 'train' looks as follows.
```json
{
  "text": "All Taxes shall be the financial responsibility of the party obligated to pay such Taxes as determined by applicable law and neither party is or shall be liable at any time for any of the other party ...",
  "label": 32
}
```

#### unfair_tos

An example of 'train' looks as follows.
```json
{
  "text": "tinder may terminate your account at any time without notice if it believes that you have violated this agreement.",
  "label": 2
}
```

#### casehold

An example of 'test' looks as follows.
```json
{
  "contexts": ["In Granato v. City and County of Denver, No. CIV 11-0304 MSK/BNB, 2011 WL 3820730 (D.Colo. Aug. 20, 2011), the Honorable Marcia S. Krieger, now-Chief United States District Judge for the District of Colorado, ruled similarly: At a minimum, a party asserting a Mo-nell claim must plead sufficient facts to identify ... to act pursuant to City or State policy, custom, decision, ordinance, re d 503, 506-07 (3d Cir.l985)(<HOLDING>).",
  "In Granato v. City and County of Denver, No. CIV 11-0304 MSK/BNB, 2011 WL 3820730 (D.Colo. Aug. 20, 2011), the Honorable Marcia S. Krieger, now-Chief United States District Judge for the District of Colorado, ruled similarly: At a minimum, a party asserting a Mo-nell claim must plead sufficient facts to identify ... to act pursuant to City or State policy, custom, decision, ordinance, re d 503, 506-07 (3d Cir.l985)(<HOLDING>).",
  "In Granato v. City and County of Denver, No. CIV 11-0304 MSK/BNB, 2011 WL 3820730 (D.Colo. Aug. 20, 2011), the Honorable Marcia S. Krieger, now-Chief United States District Judge for the District of Colorado, ruled similarly: At a minimum, a party asserting a Mo-nell claim must plead sufficient facts to identify ... to act pursuant to City or State policy, custom, decision, ordinance, re d 503, 506-07 (3d Cir.l985)(<HOLDING>).",
  "In Granato v. City and County of Denver, No. CIV 11-0304 MSK/BNB, 2011 WL 3820730 (D.Colo. Aug. 20, 2011), the Honorable Marcia S. Krieger, now-Chief United States District Judge for the District of Colorado, ruled similarly: At a minimum, a party asserting a Mo-nell claim must plead sufficient facts to identify ... to act pursuant to City or State policy, custom, decision, ordinance, re d 503, 506-07 (3d Cir.l985)(<HOLDING>).",
  "In Granato v. City and County of Denver, No. CIV 11-0304 MSK/BNB, 2011 WL 3820730 (D.Colo. Aug. 20, 2011), the Honorable Marcia S. Krieger, now-Chief United States District Judge for the District of Colorado, ruled similarly: At a minimum, a party asserting a Mo-nell claim must plead sufficient facts to identify ... to act pursuant to City or State policy, custom, decision, ordinance, re d 503, 506-07 (3d Cir.l985)(<HOLDING>).",
  ],
  "endings": ["holding that courts are to accept allegations in the complaint as being true including monell policies and writing that a federal court reviewing the sufficiency of a complaint has a limited task",
    "holding that for purposes of a class certification motion the court must accept as true all factual allegations in the complaint and may draw reasonable inferences therefrom", 
    "recognizing that the allegations of the complaint must be accepted as true on a threshold motion to dismiss", 
    "holding that a court need not accept as true conclusory allegations which are contradicted by documents referred to in the complaint", 
    "holding that where the defendant was in default the district court correctly accepted the fact allegations of the complaint as true"
  ],
  "label": 0
}
```

### Data Fields

#### ecthr_a
- `text`: a list of `string` features.
- `label_ids`: a list of classification labels.

#### ecthr_a
- `text`: a list of `string` features.
- `label_ids`: a list of classification labels.

#### scotus
- `text`: a `string` feature.
- `label`: a classification label.

#### eurlex
- `text`: a `string` feature.
- `label_ids`: a list of classification labels.

#### ledgar
- `text`: a `string` feature.
- `label`: a classification label.

#### unfair_tos
- `text`: a `string` feature.
- `label_ids`: a list of classification labels.

#### casehold
- `contexts`: a list of `string` features.
- `endings`:a list of `string` features.
- `label`: a classification label.


### Data Splits

| Dataset  | Training | Development | Test | Total | 
| --- | --- | --- | --- | --- |
| ECtHR (Task A) | 9,000 | 1,000 | 1,000 | 11,000 |
| ECtHR (Task B)| 9,000 | 1,000 | 1,000 | 11,000 |
| SCOTUS | 5,000 | 1,400 | 1,400 | 7,800 |
| EUR-LEX | 55,000 | 5,000 | 5,000 | 65,000 |
| LEDGAR | 60,000 | 10,000 | 10,000 | 80,000 |
| UNFAIR-ToS | 5,532 | 2,275 | 1,607 | 9,414 |
| CaseHOLD | 45,000 | 3,900 | 3,900 | 52,800 |

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data
| Dataset | Source (Original paper) |
| --- | --- | 
| ECtHR (Task A) | [Chalkidis et al. (2019)](https://aclanthology.org/P19-1424/) | ECHR | Multi-label classification | 10+1 |
| ECtHR (Task B) | [Chalkidis et al. (2021a)](https://aclanthology.org/2021.naacl-main.22/)  | ECHR | Multi-label classification  | 10 | 
| SCOTUS | [Spaeth et al. (2020)](http://scdb.wustl.edu) | US Law | Multi-class classification | 14 | 
| EUR-LEX | [Chalkidis et al. (2021b)](https://arxiv.org/abs/2109.00904) | EU Law | Multi-label classification | 100 |
| LEDGAR | [Tuggener et al. (2020)](https://aclanthology.org/2020.lrec-1.155/) | Contracts | Multi-class classification | 100 |
| UNFAIR-ToS | [Lippi et al. (2019)](https://arxiv.org/abs/1805.01217) | Contracts | Multi-label classification | 8 |
| CaseHOLD | [Zheng et al. (2021)](https://arxiv.org/abs/2104.08671) | US Law | Multiple choice QA | n/a |


#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


## Additional Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)


### Dataset Curators

*Ilias Chalkidis, Abhik Jana, Dirk Hartung, Michael Bommarito, Ion Androutsopoulos, Daniel Martin Katz, and Nikolaos Aletras.*
*LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.*
*Arxiv Preprint. 2021*


### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

[*Ilias Chalkidis, Abhik Jana, Dirk Hartung, Michael Bommarito, Ion Androutsopoulos, Daniel Martin Katz, and Nikolaos Aletras.*
*LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.*
*2021. arXiv: 2110.00976.*](https://arxiv.org/abs/2110.00976)
```
@article{chalkidis-etal-2021-lexglue,
        title={{LexGLUE}: A Benchmark Dataset for Legal Language Understanding in English}, 
        author={Chalkidis, Ilias and
        Jana, Abhik and
        Hartung, Dirk and
        Bommarito, Michael and
        Androutsopoulos, Ion and
        Katz, Daniel Martin and
        Aletras, Nikolaos},
        year={2021},
        eprint={2110.00976},
        archivePrefix={arXiv},
        primaryClass={cs.CL},
        note = {arXiv: 2110.00976},
}
```

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.
