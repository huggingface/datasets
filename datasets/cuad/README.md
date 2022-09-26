---
annotations_creators:
- expert-generated
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
- original
task_categories:
- question-answering
task_ids:
- closed-domain-qa
- extractive-qa
paperswithcode_id: cuad
pretty_name: CUAD
train-eval-index:
- config: default
  task: question-answering
  task_id: extractive_question_answering
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    question: question
    context: context
    answers:
      text: text
      answer_start: answer_start
  metrics:
    - type: cuad
      name: CUAD
---

# Dataset Card for CUAD

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

- **Homepage:** [Contract Understanding Atticus Dataset](https://www.atticusprojectai.org/cuad)
- **Repository:** [Contract Understanding Atticus Dataset](https://github.com/TheAtticusProject/cuad/)
- **Paper:** [CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review](https://arxiv.org/abs/2103.06268)
- **Point of Contact:** [Atticus Project Team](info@atticusprojectai.org)

### Dataset Summary

Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of more than 13,000 labels in 510 commercial legal contracts that have been manually labeled to identify 41 categories of important clauses that lawyers look for when reviewing contracts in connection with corporate transactions.

CUAD is curated and maintained by The Atticus Project, Inc. to support NLP research and development in legal contract review. Analysis of CUAD can be found at https://arxiv.org/abs/2103.06268. Code for replicating the results and the trained model can be found at https://github.com/TheAtticusProject/cuad.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset contains samples in English only.

## Dataset Structure

### Data Instances

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "answers": {
        "answer_start": [44],
        "text": ['DISTRIBUTOR AGREEMENT']
    },
    "context": 'EXHIBIT 10.6\n\n DISTRIBUTOR AGREEMENT\n\n THIS  DISTRIBUTOR  AGREEMENT (the  "Agreement")  is made by and between Electric City Corp.,  a Delaware  corporation  ("Company")  and Electric City of Illinois LLC ("Distributor") this 7th day of September, 1999...',
    "id": "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT__Document Name_0",
    "question": "Highlight the parts (if any) of this contract related to "Document Name" that should be reviewed by a lawyer. Details: The name of the contract",
    "title": "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT"
}
```

### Data Fields

- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `text`: a `string` feature.
  - `answer_start`: a `int32` feature.

### Data Splits

This dataset is split into train/test set. Number of samples in each set is given below:

|                            | Train  |  Test |
| -----                      | ------ |  ---- |
| CUAD                       |  22450 |  4182 |

## Dataset Creation

### Curation Rationale

A highly valuable specialized task without a public large-scale dataset is contract review, which costs humans substantial time, money, and attention. Many law firms spend approximately 50% of their time reviewing contracts (CEB, 2017). Due to the specialized training necessary to understand and interpret contracts, the billing rates for lawyers at large law firms are typically around $500-$900 per hour in the US. As a result, many transactions cost companies hundreds of thousands of dollars just so that lawyers can verify that there are no problematic obligations or requirements included in the contracts. Contract review can be a source of drudgery and, in comparison to other legal tasks, is widely considered to be especially boring.

Contract review costs also affect consumers. Since contract review costs are so prohibitive, contract review is not often performed outside corporate transactions. Small companies and individuals consequently often sign contracts without even reading them, which can result in predatory behavior that harms consumers. Automating contract review by openly releasing high-quality data and fine-tuned models can increase access to legal support for small businesses and individuals, so that legal support is not exclusively available to wealthy companies.

To reduce the disparate societal costs of contract review, and to study how well NLP models generalize to specialized domains, the authors introduced a new large-scale dataset for contract review. As part of The Atticus Project, a non-profit organization of legal experts, CUAD is introduced, the Contract Understanding Atticus Dataset. This dataset was created with a year-long effort pushed forward by dozens of law student annotators, lawyers, and machine learning researchers. The dataset includes more than 500 contracts and more than 13,000 expert annotations that span 41 label categories. For each of 41 different labels, models must learn to highlight the portions of a contract most salient to that label. This makes the task a matter of finding needles in a haystack.

### Source Data

#### Initial Data Collection and Normalization

The CUAD includes commercial contracts selected from 25 different types of contracts based on the contract names as shown below. Within each type, the creators randomly selected contracts based on the names of the filing companies across the alphabet.

Type of Contracts:			# of Docs

	Affiliate Agreement:		10
	Agency Agreement:		    13
	Collaboration/Cooperation Agreement: 26
	Co-Branding Agreement:		22
	Consulting Agreement:		11
	Development Agreement:		29
	Distributor Agreement:		32
	Endorsement Agreement:		24
	Franchise Agreement:		15
	Hosting Agreement:		20
	IP Agreement:			17
	Joint Venture Agreemen:		23
	License Agreement:		33
	Maintenance Agreement:		34
	Manufacturing Agreement:	17
	Marketing Agreement:		17
	Non-Compete/No-Solicit/Non-Disparagement Agreement: 3
	Outsourcing Agreement:		18
	Promotion Agreement:		12
	Reseller Agreement:		12
	Service Agreement:		28
	Sponsorship Agreement:		31
	Supply Agreement:		18
	Strategic Alliance Agreement:	32
	Transportation Agreement:	13
	TOTAL:				510

#### Who are the source language producers?

The contracts were sourced from EDGAR, the Electronic Data Gathering, Analysis, and Retrieval system used at the U.S. Securities and Exchange Commission (SEC). Publicly traded companies in the United States are required to file certain contracts under the SEC rules. Access to these contracts is available to the public for free at https://www.sec.gov/edgar. Please read the Datasheet at https://www.atticusprojectai.org/ for information on the intended use and limitations of the CUAD.

### Annotations

#### Annotation process

The labeling process included multiple steps to ensure accuracy:
1. Law Student Training: law students attended training sessions on each of the categories that included a summary, video instructions by experienced attorneys, multiple quizzes and workshops. Students were then required to label sample contracts in eBrevia, an online contract review tool. The initial training took approximately 70-100 hours.
2. Law Student Label: law students conducted manual contract review and labeling in eBrevia.
3. Key Word Search: law students conducted keyword search in eBrevia to capture additional categories that have been missed during the “Student Label” step.
4. Category-by-Category Report Review: law students exported the labeled clauses into reports, review each clause category-by-category and highlight clauses that they believe are mislabeled.
5. Attorney Review: experienced attorneys reviewed the category-by-category report with students comments, provided comments and addressed student questions. When applicable, attorneys discussed such results with the students and reached consensus. Students made changes in eBrevia accordingly.
6. eBrevia Extras Review. Attorneys and students used eBrevia to generate a list of “extras”, which are clauses that eBrevia AI tool identified as responsive to a category but not labeled by human annotators. Attorneys and students reviewed all of the “extras” and added the correct ones. The process is repeated until all or substantially all of the “extras” are incorrect labels.
7. Final Report: The final report was exported into a CSV file. Volunteers manually added the “Yes/No” answer column to categories that do not contain an answer.

#### Who are the annotators?

Answered in above section.

### Personal and Sensitive Information

Some clauses in the files are redacted because the party submitting these contracts redacted them to protect confidentiality. Such redaction may show up as asterisks (\*\*\*) or underscores (\_\_\_) or blank spaces. The dataset and the answers reflect such redactions. For example, the answer for “January \_\_ 2020” would be “1/[]/2020”).

For any categories that require an answer of “Yes/No”, annotators include full sentences as text context in a contract. To maintain consistency and minimize inter-annotator disagreement, annotators select text for the full sentence, under the instruction of “from period to period”.

For the other categories, annotators selected segments of the text in the contract that are responsive to each such category. One category in a contract may include multiple labels. For example, “Parties” may include 4-10 separate text strings that are not continuous in a contract. The answer is presented in the unified format separated by semicolons of “Party A Inc. (“Party A”); Party B Corp. (“Party B”)”.

Some sentences in the files include confidential legends that are not part of the contracts. An example of such confidential legend is as follows:

THIS EXHIBIT HAS BEEN REDACTED AND IS THE SUBJECT OF A CONFIDENTIAL TREATMENT REQUEST. REDACTED MATERIAL IS MARKED WITH [* * *] AND HAS BEEN FILED SEPARATELY WITH THE SECURITIES AND EXCHANGE COMMISSION.

Some sentences in the files contain irrelevant information such as footers or page numbers. Some sentences may not be relevant to the corresponding category. Some sentences may correspond to a different category. Because many legal clauses are very long and contain various sub-parts, sometimes only a sub-part of a sentence is responsive to a category.

To address the foregoing limitations, annotators manually deleted the portion that is not responsive, replacing it with the symbol "<omitted>" to indicate that the two text segments do not appear immediately next to each other in the contracts. For example, if a “Termination for Convenience” clause starts with “Each Party may terminate this Agreement if” followed by three subparts “(a), (b) and (c)”, but only subpart (c) is responsive to this category, the authors manually deleted subparts (a) and (b) and replaced them with the symbol "<omitted>”. Another example is for “Effective Date”, the contract includes a sentence “This Agreement is effective as of the date written above” that appears after the date “January 1, 2010”. The annotation is as follows: “January 1, 2010 <omitted> This Agreement is effective as of the date written above.”

Because the contracts were converted from PDF into TXT files, the converted TXT files may not stay true to the format of the original PDF files. For example, some contracts contain inconsistent spacing between words, sentences and paragraphs. Table format is not maintained in the TXT files.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Attorney Advisors
Wei Chen, John Brockland, Kevin Chen, Jacky Fink, Spencer P. Goodson, Justin Haan, Alex Haskell, Kari Krusmark, Jenny Lin, Jonas Marson, Benjamin Petersen, Alexander Kwonji Rosenberg, William R. Sawyers, Brittany Schmeltz, Max Scott, Zhu Zhu

Law Student Leaders
John Batoha, Daisy Beckner, Lovina Consunji, Gina Diaz, Chris Gronseth, Calvin Hannagan, Joseph Kroon, Sheetal Sharma Saran

Law Student Contributors
Scott Aronin, Bryan Burgoon, Jigar Desai, Imani Haynes, Jeongsoo Kim, Margaret Lynch, Allison Melville, Felix Mendez-Burgos, Nicole Mirkazemi, David Myers, Emily Rissberger, Behrang Seraj, Sarahginy Valcin

Technical Advisors & Contributors
Dan Hendrycks, Collin Burns, Spencer Ball, Anya Chen

### Licensing Information

CUAD is licensed under the Creative Commons Attribution 4.0 (CC BY 4.0) license and free to the public for commercial and non-commercial use.

The creators make no representations or warranties regarding the license status of the underlying contracts, which are publicly available and downloadable from EDGAR.
Privacy Policy & Disclaimers

The categories or the contracts included in the dataset are not comprehensive or representative. The authors encourage the public to help improve them by sending them your comments and suggestions to info@atticusprojectai.org. Comments and suggestions will be reviewed by The Atticus Project at its discretion and will be included in future versions of Atticus categories once approved.

The use of CUAD is subject to their privacy policy https://www.atticusprojectai.org/privacy-policy and disclaimer https://www.atticusprojectai.org/disclaimer.

### Citation Information

```
@article{hendrycks2021cuad,
      title={CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review},
      author={Dan Hendrycks and Collin Burns and Anya Chen and Spencer Ball},
      journal={arXiv preprint arXiv:2103.06268},
      year={2021}
}
```

### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.
