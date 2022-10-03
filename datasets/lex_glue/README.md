---
pretty_name: LexGLUE
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended
task_categories:
- question-answering
- text-classification
task_ids:
- multi-class-classification
- multi-label-classification
- multiple-choice-qa
- topic-classification
configs:
- case_hold
- ecthr_a
- ecthr_b
- eurlex
- ledgar
- scotus
- unfair_tos
dataset_info:
- config_name: ecthr_a
  features:
  - name: text
    sequence: string
  - name: labels
    sequence:
      class_label:
        names:
          0: '2'
          1: '3'
          2: '5'
          3: '6'
          4: '8'
          5: '9'
          6: '10'
          7: '11'
          8: '14'
          9: P1-1
  splits:
  - name: test
    num_bytes: 11884180
    num_examples: 1000
  - name: train
    num_bytes: 89637461
    num_examples: 9000
  - name: validation
    num_bytes: 10985180
    num_examples: 1000
  download_size: 32852475
  dataset_size: 112506821
- config_name: ecthr_b
  features:
  - name: text
    sequence: string
  - name: labels
    sequence:
      class_label:
        names:
          0: '2'
          1: '3'
          2: '5'
          3: '6'
          4: '8'
          5: '9'
          6: '10'
          7: '11'
          8: '14'
          9: P1-1
  splits:
  - name: test
    num_bytes: 11886940
    num_examples: 1000
  - name: train
    num_bytes: 89657661
    num_examples: 9000
  - name: validation
    num_bytes: 10987828
    num_examples: 1000
  download_size: 32852475
  dataset_size: 112532429
- config_name: eurlex
  features:
  - name: text
    dtype: string
  - name: labels
    sequence:
      class_label:
        names:
          0: '100163'
          1: '100164'
          2: '100165'
          3: '100166'
          4: '100167'
          5: '100168'
          6: '100169'
          7: '100170'
          8: '100171'
          9: '100172'
          10: '100173'
          11: '100174'
          12: '100175'
          13: '100176'
          14: '100177'
          15: '100178'
          16: '100179'
          17: '100180'
          18: '100181'
          19: '100182'
          20: '100183'
          21: '100184'
          22: '100185'
          23: '100186'
          24: '100187'
          25: '100188'
          26: '100189'
          27: '100190'
          28: '100191'
          29: '100192'
          30: '100193'
          31: '100194'
          32: '100195'
          33: '100196'
          34: '100197'
          35: '100198'
          36: '100199'
          37: '100200'
          38: '100201'
          39: '100202'
          40: '100203'
          41: '100204'
          42: '100205'
          43: '100206'
          44: '100207'
          45: '100208'
          46: '100209'
          47: '100210'
          48: '100211'
          49: '100212'
          50: '100213'
          51: '100214'
          52: '100215'
          53: '100216'
          54: '100217'
          55: '100218'
          56: '100219'
          57: '100220'
          58: '100221'
          59: '100222'
          60: '100223'
          61: '100224'
          62: '100225'
          63: '100226'
          64: '100227'
          65: '100228'
          66: '100229'
          67: '100230'
          68: '100231'
          69: '100232'
          70: '100233'
          71: '100234'
          72: '100235'
          73: '100236'
          74: '100237'
          75: '100238'
          76: '100239'
          77: '100240'
          78: '100241'
          79: '100242'
          80: '100243'
          81: '100244'
          82: '100245'
          83: '100246'
          84: '100247'
          85: '100248'
          86: '100249'
          87: '100250'
          88: '100251'
          89: '100252'
          90: '100253'
          91: '100254'
          92: '100255'
          93: '100256'
          94: '100257'
          95: '100258'
          96: '100259'
          97: '100260'
          98: '100261'
          99: '100262'
          100: '100263'
          101: '100264'
          102: '100265'
          103: '100266'
          104: '100267'
          105: '100268'
          106: '100269'
          107: '100270'
          108: '100271'
          109: '100272'
          110: '100273'
          111: '100274'
          112: '100275'
          113: '100276'
          114: '100277'
          115: '100278'
          116: '100279'
          117: '100280'
          118: '100281'
          119: '100282'
          120: '100283'
          121: '100284'
          122: '100285'
          123: '100286'
          124: '100287'
          125: '100288'
          126: '100289'
  splits:
  - name: test
    num_bytes: 59742502
    num_examples: 5000
  - name: train
    num_bytes: 390789505
    num_examples: 55000
  - name: validation
    num_bytes: 41546764
    num_examples: 5000
  download_size: 125413277
  dataset_size: 492078771
- config_name: scotus
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '1'
          1: '2'
          2: '3'
          3: '4'
          4: '5'
          5: '6'
          6: '7'
          7: '8'
          8: '9'
          9: '10'
          10: '11'
          11: '12'
          12: '13'
  splits:
  - name: test
    num_bytes: 76213283
    num_examples: 1400
  - name: train
    num_bytes: 178959320
    num_examples: 5000
  - name: validation
    num_bytes: 75600247
    num_examples: 1400
  download_size: 104763335
  dataset_size: 330772850
- config_name: ledgar
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Adjustments
          1: Agreements
          2: Amendments
          3: Anti-Corruption Laws
          4: Applicable Laws
          5: Approvals
          6: Arbitration
          7: Assignments
          8: Assigns
          9: Authority
          10: Authorizations
          11: Base Salary
          12: Benefits
          13: Binding Effects
          14: Books
          15: Brokers
          16: Capitalization
          17: Change In Control
          18: Closings
          19: Compliance With Laws
          20: Confidentiality
          21: Consent To Jurisdiction
          22: Consents
          23: Construction
          24: Cooperation
          25: Costs
          26: Counterparts
          27: Death
          28: Defined Terms
          29: Definitions
          30: Disability
          31: Disclosures
          32: Duties
          33: Effective Dates
          34: Effectiveness
          35: Employment
          36: Enforceability
          37: Enforcements
          38: Entire Agreements
          39: Erisa
          40: Existence
          41: Expenses
          42: Fees
          43: Financial Statements
          44: Forfeitures
          45: Further Assurances
          46: General
          47: Governing Laws
          48: Headings
          49: Indemnifications
          50: Indemnity
          51: Insurances
          52: Integration
          53: Intellectual Property
          54: Interests
          55: Interpretations
          56: Jurisdictions
          57: Liens
          58: Litigations
          59: Miscellaneous
          60: Modifications
          61: No Conflicts
          62: No Defaults
          63: No Waivers
          64: Non-Disparagement
          65: Notices
          66: Organizations
          67: Participations
          68: Payments
          69: Positions
          70: Powers
          71: Publicity
          72: Qualifications
          73: Records
          74: Releases
          75: Remedies
          76: Representations
          77: Sales
          78: Sanctions
          79: Severability
          80: Solvency
          81: Specific Performance
          82: Submission To Jurisdiction
          83: Subsidiaries
          84: Successors
          85: Survival
          86: Tax Withholdings
          87: Taxes
          88: Terminations
          89: Terms
          90: Titles
          91: Transactions With Affiliates
          92: Use Of Proceeds
          93: Vacations
          94: Venues
          95: Vesting
          96: Waiver Of Jury Trials
          97: Waivers
          98: Warranties
          99: Withholdings
  splits:
  - name: test
    num_bytes: 6845585
    num_examples: 10000
  - name: train
    num_bytes: 43358315
    num_examples: 60000
  - name: validation
    num_bytes: 7143592
    num_examples: 10000
  download_size: 16255623
  dataset_size: 57347492
- config_name: unfair_tos
  features:
  - name: text
    dtype: string
  - name: labels
    sequence:
      class_label:
        names:
          0: Limitation of liability
          1: Unilateral termination
          2: Unilateral change
          3: Content removal
          4: Contract by using
          5: Choice of law
          6: Jurisdiction
          7: Arbitration
  splits:
  - name: test
    num_bytes: 303107
    num_examples: 1607
  - name: train
    num_bytes: 1041790
    num_examples: 5532
  - name: validation
    num_bytes: 452119
    num_examples: 2275
  download_size: 511342
  dataset_size: 1797016
- config_name: case_hold
  features:
  - name: context
    dtype: string
  - name: endings
    sequence: string
  - name: label
    dtype:
      class_label:
        names:
          0: '0'
          1: '1'
          2: '2'
          3: '3'
          4: '4'
  splits:
  - name: test
    num_bytes: 5989964
    num_examples: 3600
  - name: train
    num_bytes: 74781766
    num_examples: 45000
  - name: validation
    num_bytes: 6474615
    num_examples: 3900
  download_size: 30422703
  dataset_size: 87246345
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

<table>
<tr><td>Dataset</td><td>Source</td><td>Sub-domain</td><td>Task Type</td><td>Classes</td><tr>
<tr><td>ECtHR (Task A)</td><td> <a href="https://aclanthology.org/P19-1424/">Chalkidis et al. (2019)</a> </td><td>ECHR</td><td>Multi-label classification</td><td>10+1</td></tr>
<tr><td>ECtHR (Task B)</td><td> <a href="https://aclanthology.org/2021.naacl-main.22/">Chalkidis et al. (2021a)</a> </td><td>ECHR</td><td>Multi-label classification </td><td>10+1</td></tr>
<tr><td>SCOTUS</td><td> <a href="http://scdb.wustl.edu">Spaeth et al. (2020)</a></td><td>US Law</td><td>Multi-class classification</td><td>14</td></tr>
<tr><td>EUR-LEX</td><td> <a href="https://arxiv.org/abs/2109.00904">Chalkidis et al. (2021b)</a></td><td>EU Law</td><td>Multi-label classification</td><td>100</td></tr>
<tr><td>LEDGAR</td><td> <a href="https://aclanthology.org/2020.lrec-1.155/">Tuggener et al. (2020)</a></td><td>Contracts</td><td>Multi-class classification</td><td>100</td></tr>
<tr><td>UNFAIR-ToS</td><td><a href="https://arxiv.org/abs/1805.01217"> Lippi et al. (2019)</a></td><td>Contracts</td><td>Multi-label classification</td><td>8+1</td></tr>
<tr><td>CaseHOLD</td><td><a href="https://arxiv.org/abs/2104.08671">Zheng et al. (2021)</a></td><td>US Law</td><td>Multiple choice QA</td><td>n/a</td></tr>
</table>

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


The current leaderboard includes several Transformer-based (Vaswaniet al., 2017) pre-trained language models, which achieve state-of-the-art performance in most NLP tasks (Bommasani et al., 2021) and NLU benchmarks (Wang et al., 2019a). Results reported by [Chalkidis et al. (2021)](https://arxiv.org/abs/2110.00976):

*Task-wise Test Results*

<table>
        <tr><td><b>Dataset</b></td><td><b>ECtHR A</b></td><td><b>ECtHR B</b></td><td><b>SCOTUS</b></td><td><b>EUR-LEX</b></td><td><b>LEDGAR</b></td><td><b>UNFAIR-ToS</b></td><td><b>CaseHOLD</b></td></tr>
<tr><td><b>Model</b></td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1</td><td>μ-F1 / m-F1  </td></tr>
<tr><td>TFIDF+SVM</td><td> 64.7 / 51.7  </td><td>74.6 / 65.1 </td><td> <b>78.2</b> / <b>69.5</b> </td><td>71.3  / 51.4 </td><td>87.2   / 82.4 </td><td>95.4  / 78.8</td><td>n/a   </td></tr>
<tr><td colspan="8" style='text-align:center'><b>Medium-sized Models (L=12, H=768, A=12)</b></td></tr>
<td>BERT</td> <td> 71.2 /  63.6 </td> <td> 79.7 /  73.4 </td> <td> 68.3 /  58.3 </td> <td> 71.4 /  57.2 </td> <td> 87.6 /  81.8 </td> <td> 95.6 /  81.3 </td> <td> 70.8 </td> </tr>
<td>RoBERTa</td> <td> 69.2 /  59.0 </td> <td> 77.3 /  68.9 </td> <td> 71.6 /  62.0 </td> <td> 71.9 /  <b>57.9</b> </td> <td> 87.9 /  82.3 </td> <td> 95.2 /  79.2 </td> <td> 71.4 </td> </tr>
<td>DeBERTa</td> <td> 70.0 /  60.8 </td> <td> 78.8 /  71.0 </td> <td> 71.1 /  62.7 </td> <td> <b>72.1</b> /  57.4 </td> <td> 88.2 /  83.1 </td> <td> 95.5 /  80.3 </td> <td> 72.6 </td> </tr>
<td>Longformer</td> <td> 69.9 / 64.7 </td> <td> 79.4 /  71.7 </td> <td> 72.9 /  64.0 </td> <td> 71.6 /  57.7 </td> <td> 88.2 /  83.0 </td> <td> 95.5 /  80.9 </td> <td> 71.9 </td> </tr>
<td>BigBird</td> <td> 70.0 /  62.9 </td> <td> 78.8 /  70.9 </td> <td> 72.8 /  62.0 </td> <td> 71.5 /  56.8 </td> <td> 87.8 /  82.6 </td> <td> 95.7 /  81.3 </td> <td> 70.8 </td> </tr>
<td>Legal-BERT</td> <td> 70.0 /  64.0 </td> <td> <b>80.4</b> /  <b>74.7</b> </td> <td> 76.4 /  66.5 </td> <td> <b>72.1</b> /  57.4 </td> <td> 88.2 /  83.0 </td> <td> <b>96.0</b> /  <b>83.0</b> </td> <td> 75.3 </td> </tr>
<td>CaseLaw-BERT</td> <td> 69.8 /  62.9 </td> <td> 78.8 /  70.3 </td> <td> 76.6 /  65.9 </td> <td> 70.7 /  56.6 </td> <td> 88.3 /  83.0 </td> <td> <b>96.0</b> /  82.3 </td> <td> <b>75.4</b> </td> </tr>
<tr><td colspan="8" style='text-align:center'><b>Large-sized Models (L=24, H=1024, A=18)</b></td></tr>
<tr><td>RoBERTa</td> <td> <b>73.8</b> /  <b>67.6</b> </td> <td> 79.8 /  71.6 </td> <td> 75.5 /  66.3 </td> <td> 67.9 /  50.3 </td> <td> <b>88.6</b> /  <b>83.6</b> </td> <td> 95.8 /  81.6 </td> <td> 74.4 </td> </tr>
</table>

*Averaged (Mean over Tasks) Test Results*

<table>
<tr><td><b>Averaging</b></td><td><b>Arithmetic</b></td><td><b>Harmonic</b></td><td><b>Geometric</b></td></tr>
<tr><td><b>Model</b></td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1 </td><td>μ-F1  / m-F1 </td></tr>
<tr><td colspan="4" style='text-align:center'><b>Medium-sized Models (L=12, H=768, A=12)</b></td></tr>
<tr><td>BERT</td><td> 77.8 /  69.5 </td><td> 76.7 /  68.2 </td><td> 77.2 /  68.8 </td></tr>
<tr><td>RoBERTa</td><td> 77.8 /  68.7 </td><td> 76.8 /  67.5 </td><td> 77.3 /  68.1 </td></tr>
<tr><td>DeBERTa</td><td> 78.3 /  69.7 </td><td> 77.4 /  68.5 </td><td> 77.8 /  69.1 </td></tr>
<tr><td>Longformer</td><td> 78.5 /  70.5 </td><td> 77.5 /  69.5 </td><td> 78.0 /  70.0 </td></tr>
<tr><td>BigBird</td><td> 78.2 /  69.6 </td><td> 77.2 /  68.5 </td><td> 77.7 /  69.0 </td></tr>
<tr><td>Legal-BERT</td><td> <b>79.8</b> /  <b>72.0</b> </td><td> <b>78.9</b> /  <b>70.8</b> </td><td> <b>79.3</b> /  <b>71.4</b> </td></tr>
<tr><td>CaseLaw-BERT</td><td> 79.4 /  70.9 </td><td> 78.5 /  69.7 </td><td> 78.9 /  70.3 </td></tr> 
<tr><td colspan="4" style='text-align:center'><b>Large-sized Models (L=24, H=1024, A=18)</b></td></tr>
<tr><td>RoBERTa</td><td> 79.4 /  70.8 </td><td> 78.4 /  69.1 </td><td> 78.9 /  70.0 </td></tr>
</table>

### Languages

We only consider English datasets, to make experimentation easier for researchers across the globe.

## Dataset Structure

### Data Instances

#### ecthr_a

An example of 'train' looks as follows. 
```json
{
  "text": ["8. The applicant was arrested in the early morning of 21 October 1990 ...", ...],
  "labels": [6]
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
  "labels": [4, 20, 21, 35, 68]
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
  "context": "In Granato v. City and County of Denver, No. CIV 11-0304 MSK/BNB, 2011 WL 3820730 (D.Colo. Aug. 20, 2011), the Honorable Marcia S. Krieger, now-Chief United States District Judge for the District of Colorado, ruled similarly: At a minimum, a party asserting a Mo-nell claim must plead sufficient facts to identify ... to act pursuant to City or State policy, custom, decision, ordinance, re d 503, 506-07 (3d Cir.l985)(<HOLDING>).",
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
- `text`: a list of `string` features (list of factual paragraphs (facts) from the case description).
- `labels`: a list of classification labels (a list of violated ECHR articles, if any) .
<details>
  <summary>List of ECHR articles</summary>
 "Article 2", "Article 3", "Article 5", "Article 6", "Article 8", "Article 9", "Article 10", "Article 11", "Article 14", "Article 1 of Protocol 1"
</details>

#### ecthr_b
- `text`: a list of `string` features (list of factual paragraphs (facts) from the case description)
- `labels`: a list of classification labels (a list of articles considered).
<details>
  <summary>List of ECHR articles</summary>
 "Article 2", "Article 3", "Article 5", "Article 6", "Article 8", "Article 9", "Article 10", "Article 11", "Article 14", "Article 1 of Protocol 1"
</details>

#### scotus
- `text`: a `string` feature (the court opinion).
- `label`: a classification label (the relevant issue area).
<details>
  <summary>List of issue areas</summary>
(1, Criminal Procedure), (2, Civil Rights), (3, First Amendment), (4, Due Process), (5, Privacy), (6, Attorneys), (7, Unions), (8, Economic Activity), (9, Judicial Power), (10, Federalism), (11, Interstate Relations), (12, Federal Taxation), (13, Miscellaneous), (14, Private Action)
</details>

#### eurlex
- `text`: a `string` feature (an EU law).
- `labels`: a list of classification labels (a list of relevant EUROVOC concepts).
<details>
  <summary>List of EUROVOC concepts</summary>
  The list is very long including 100 EUROVOC concepts. You can find the EUROVOC concepts descriptors <a href="https://raw.githubusercontent.com/nlpaueb/multi-eurlex/master/data/eurovoc_descriptors.json">here</a>.
</details>

#### ledgar
- `text`: a `string` feature (a contract provision/paragraph).
- `label`: a classification label (the type of contract provision).
<details>
  <summary>List of contract provision types</summary>
"Adjustments", "Agreements", "Amendments", "Anti-Corruption Laws", "Applicable Laws", "Approvals", "Arbitration", "Assignments", "Assigns", "Authority", "Authorizations", "Base Salary", "Benefits", "Binding Effects", "Books", "Brokers", "Capitalization", "Change In Control", "Closings", "Compliance With Laws", "Confidentiality", "Consent To Jurisdiction", "Consents", "Construction", "Cooperation", "Costs", "Counterparts", "Death", "Defined Terms", "Definitions", "Disability", "Disclosures", "Duties", "Effective Dates", "Effectiveness", "Employment", "Enforceability", "Enforcements", "Entire Agreements", "Erisa", "Existence", "Expenses", "Fees", "Financial Statements", "Forfeitures", "Further Assurances", "General", "Governing Laws", "Headings", "Indemnifications", "Indemnity", "Insurances", "Integration", "Intellectual Property", "Interests", "Interpretations", "Jurisdictions", "Liens", "Litigations", "Miscellaneous", "Modifications", "No Conflicts", "No Defaults", "No Waivers", "Non-Disparagement", "Notices", "Organizations", "Participations", "Payments", "Positions", "Powers", "Publicity", "Qualifications", "Records", "Releases", "Remedies", "Representations", "Sales", "Sanctions", "Severability", "Solvency", "Specific Performance", "Submission To Jurisdiction", "Subsidiaries", "Successors", "Survival", "Tax Withholdings", "Taxes", "Terminations", "Terms", "Titles", "Transactions With Affiliates", "Use Of Proceeds", "Vacations", "Venues", "Vesting", "Waiver Of Jury Trials", "Waivers", "Warranties", "Withholdings",
</details>

#### unfair_tos
- `text`: a `string` feature (a ToS sentence)
- `labels`: a list of classification labels (a list of unfair types, if any).
<details>
  <summary>List of unfair types</summary>
    "Limitation of liability", "Unilateral termination", "Unilateral change", "Content removal", "Contract by using", "Choice of law", "Jurisdiction", "Arbitration"
</details>

#### casehold
- `context`: a `string` feature (a context sentence incl. a masked holding statement).
- `holdings`: a list of `string` features (a list of candidate holding statements).
- `label`: a classification label (the id of the original/correct holding).


### Data Splits

<table>
<tr><td>Dataset </td><td>Training</td><td>Development</td><td>Test</td><td>Total</td></tr>
<tr><td>ECtHR (Task A)</td><td>9,000</td><td>1,000</td><td>1,000</td><td>11,000</td></tr>
<tr><td>ECtHR (Task B)</td><td>9,000</td><td>1,000</td><td>1,000</td><td>11,000</td></tr>
<tr><td>SCOTUS</td><td>5,000</td><td>1,400</td><td>1,400</td><td>7,800</td></tr>
<tr><td>EUR-LEX</td><td>55,000</td><td>5,000</td><td>5,000</td><td>65,000</td></tr>
<tr><td>LEDGAR</td><td>60,000</td><td>10,000</td><td>10,000</td><td>80,000</td></tr>
<tr><td>UNFAIR-ToS</td><td>5,532</td><td>2,275</td><td>1,607</td><td>9,414</td></tr>
<tr><td>CaseHOLD</td><td>45,000</td><td>3,900</td><td>3,900</td><td>52,800</td></tr>
</table>

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data 
<table>
<tr><td>Dataset</td><td>Source</td><td>Sub-domain</td><td>Task Type</td><tr>
<tr><td>ECtHR (Task A)</td><td> <a href="https://aclanthology.org/P19-1424/">Chalkidis et al. (2019)</a> </td><td>ECHR</td><td>Multi-label classification</td></tr>
<tr><td>ECtHR (Task B)</td><td> <a href="https://aclanthology.org/2021.naacl-main.22/">Chalkidis et al. (2021a)</a> </td><td>ECHR</td><td>Multi-label classification </td></tr>
<tr><td>SCOTUS</td><td> <a href="http://scdb.wustl.edu">Spaeth et al. (2020)</a></td><td>US Law</td><td>Multi-class classification</td></tr>
<tr><td>EUR-LEX</td><td> <a href="https://arxiv.org/abs/2109.00904">Chalkidis et al. (2021b)</a></td><td>EU Law</td><td>Multi-label classification</td></tr>
<tr><td>LEDGAR</td><td> <a href="https://aclanthology.org/2020.lrec-1.155/">Tuggener et al. (2020)</a></td><td>Contracts</td><td>Multi-class classification</td></tr>
<tr><td>UNFAIR-ToS</td><td><a href="https://arxiv.org/abs/1805.01217"> Lippi et al. (2019)</a></td><td>Contracts</td><td>Multi-label classification</td></tr>
<tr><td>CaseHOLD</td><td><a href="https://arxiv.org/abs/2104.08671">Zheng et al. (2021)</a></td><td>US Law</td><td>Multiple choice QA</td></tr>
</table>

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
*2022. In the Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics. Dublin, Ireland.*


### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

[*Ilias Chalkidis, Abhik Jana, Dirk Hartung, Michael Bommarito, Ion Androutsopoulos, Daniel Martin Katz, and Nikolaos Aletras.*
*LexGLUE: A Benchmark Dataset for Legal Language Understanding in English.*
*2022. In the Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics. Dublin, Ireland.*](https://arxiv.org/abs/2110.00976)
```
@inproceedings{chalkidis-etal-2021-lexglue,
        title={LexGLUE: A Benchmark Dataset for Legal Language Understanding in English}, 
        author={Chalkidis, Ilias and Jana, Abhik and Hartung, Dirk and
        Bommarito, Michael and Androutsopoulos, Ion and Katz, Daniel Martin and
        Aletras, Nikolaos},
        year={2022},
        booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics},
        address={Dubln, Ireland},
}
```

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.