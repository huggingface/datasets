---
annotations_creators:
- found

language_creators:
- found

languages:
- en

licenses:
- cc-by-sa-4.0

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
- legal-topic-classification
---

# Dataset Card for the EUR-Lex dataset

## Table of Contents
- [Dataset Card for the EUR-Lex dataset](#dataset-card-for-ecthr-cases)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** http://nlp.cs.aueb.gr/software_and_datasets/EURLEX57K/
- **Repository:** http://nlp.cs.aueb.gr/software_and_datasets/EURLEX57K/
- **Paper:** https://www.aclweb.org/anthology/P19-1636/
- **Leaderboard:** N/A
- **Point of Contact:** [Ilias Chalkidis](mailto:ihalk@aueb.gr)

### Dataset Summary

EURLEX57K can be viewed as an improved version of the dataset released by Mencia and Furnkranzand (2007), which has been widely used in Large-scale Multi-label Text Classification (LMTC) research, but is less than half the size of EURLEX57K (19.6k documents, 4k EUROVOC labels) and more than ten years old.
EURLEX57K contains 57k legislative documents in English from EUR-Lex (https://eur-lex.europa.eu) with an average length of 727 words. Each document contains four major zones: 

- the header, which includes the title and name of the legal body enforcing the legal act;
- the recitals, which are legal background references; and
- the main body, usually organized in articles.

**Labeling / Annotation**

All the documents of the dataset have been annotated by the Publications Office of EU (https://publications.europa.eu/en) with multiple concepts from EUROVOC (http://eurovoc.europa.eu/). 
While EUROVOC includes approx. 7k concepts (labels), only 4,271 (59.31%) are present in EURLEX57K, from which only 2,049 (47.97%) have been assigned to more than 10 documents.  The 4,271 labels are also divided into frequent (746 labels), few-shot (3,362), and zero- shot (163), depending on whether they were assigned to more than 50, fewer than 50 but at least one, or no training documents, respectively.


### Supported Tasks and Leaderboards

The dataset supports:

**Multi-label Text Classification:** Given the text of a document, a model predicts the relevant EUROVOC concepts.

**Few-shot and Zero-shot learning:** As already noted, the labels can be divided into three groups: frequent (746 labels), few-shot (3,362), and zero- shot (163), depending on whether they were assigned to more than 50, fewer than 50 but at least one, or no training documents, respectively.

### Languages

All documents are written in English.

## Dataset Structure

### Data Instances


```json
{
  "celex_id": "31979D0509", 
  "document_type": "Decision", 
  "title": "79/509/EEC: Council Decision of 24 May 1979 on financial aid from the Community for the eradication of African swine fever in Spain", 
  "header": "COUNCIL DECISION  of 24 May 1979  on financial aid from the Community for the eradication of African swine fever in Spain  (79/509/EEC)\nTHE COUNCIL OF THE EUROPEAN COMMUNITIES", 
  "recitals": "Having regard to the Treaty establishing the European Economic Community, and in particular Article 43 thereof,\nHaving regard to the proposal from the Commission (1),\nHaving regard to the opinion of the European Parliament (2),\nWhereas the Community should take all appropriate measures to protect itself against the appearance of African swine fever on its territory;\nWhereas to this end the Community has undertaken, and continues to undertake, action designed to contain outbreaks of this type of disease far from its frontiers by helping countries affected to reinforce their preventive measures ; whereas for this purpose Community subsidies have already been granted to Spain;\nWhereas these measures have unquestionably made an effective contribution to the protection of Community livestock, especially through the creation and maintenance of a buffer zone north of the river Ebro;\nWhereas, however, in the opinion of the Spanish authorities themselves, the measures so far implemented must be reinforced if the fundamental objective of eradicating the disease from the entire country is to be achieved;\nWhereas the Spanish authorities have asked the Community to contribute to the expenses necessary for the efficient implementation of a total eradication programme;\nWhereas a favourable response should be given to this request by granting aid to Spain, having regard to the undertaking given by that country to protect the Community against African swine fever and to eliminate completely this disease by the end of a five-year eradication plan;\nWhereas this eradication plan must include certain measures which guarantee the effectiveness of the action taken, and it must be possible to adapt these measures to developments in the situation by means of a procedure establishing close cooperation between the Member States and the Commission;\nWhereas it is necessary to keep the Member States regularly informed as to the progress of the action undertaken,", 
  "main_body": ["The Community shall make a financial contribution to the eradication of African swine fever in Spain.", "The contribution shall be given on the condition that the Spanish authorities establish an eradication plan designed to result in the elimination of the disease within five years and satisfying the conditions laid down in Article 3, and that this plan is approved in accordance with Article 4.\nThis plan must be put into operation no later than the date laid down by the Commission in its Decision approving the plan.", "The eradication plan mentioned in Article 2 must include the immediate slaughter and destruction of all pigs on those holdings where a case of African swine fever is diagnosed and in those holdings which as a result of an epidemiological enquiry can be considered as contaminated and in addition provide in particular for:    (a) the disinfection of, and elimination of insects and vermin from, the holding after the elimination of the pigs;\n(b) a delay before repopulation of clean holdings and a health control of pigs before they are introduced into these holdings;\n(c) the establishment throughout the country of a strict movement control of pigs, including those destined for slaughter;\n(d) the obligation to slaughter pigs in establishments under permanent veterinary control;  (1)OJ No C 44, 17.2.1979, p. 6. (2)OJ No C 127, 21.5.1979, p. 88.\n(e) the creation of disease-free zones and their protection by the development of integrated pig-farming enterprises, or if necessary the establishment of a control of the pig population of these enterprises by means of observation quarantine of animals at the place of origin and of their integration into the herd only after a further period of observation in isolation on arrival of a consignment;\n(f) the protection of disease-free zones by the strict control of the movement of pigs into these zones whatever their destination and by a prohibition on the straying of pigs and on pig markets;\n(g) compensation given for slaughter, to be calculated in such a way that farmers are appropriately compensated;\n(h) import surveillance;\n(i) any steps to prevent the spread of epizootic disease to the Community.", "After examination of the plan presented by the Spanish authorities and of any amendments to be made thereto, the Commission shall decide, in accordance with the procedure provided for in Article 5, whether or not to approve it.", "1. Where the procedure laid down in this Article is to be used, matters shall without delay be referred by the chairman, either on his own initiative or at the request of a Member State, to the Standing Veterinary Committee (hereinafter called the \"Committee\") set up by the Council Decision of 15 October 1968.\n2. Within the Committee the votes of Member States shall be weighted as provided for in Article 148 (2) of the Treaty. The chairman shall not vote.\n3. The representative of the Commission shall submit a draft of the measures to be adopted. The Committee shall deliver its opinion on such measures within a time limit set by the chairman according to the urgency of the matters concerned. Opinions shall be delivered by a majority of 41 votes.\n4. The Commission shall adopt the measures and shall apply them immediately where they are in accordance with the opinion of the Committee. Where they are not in accordance with the opinion of the Committee or if no opinion is delivered, the Commission shall without delay propose to the Council the measures to be adopted. The Council shall adopt the measures by a qualified majority.\nIf, within three months from the date on which the proposal was submitted to it, the Council has not adopted any measures, the Commission shall adopt the proposed measures and apply them immediately, save where the Council has decided by a simple majority against those measures.", "Article 5 shall apply until 21 June 1981.", "1. The estimated assistance of the Community shall be a maximum of 10 million European units of account for the period in question.\n2. Payments shall be made in annual instalments, within the limits of the budgetary appropriations, on presentation of the relevant supporting documents to the Commission.", "1. The Commission shall follow the development of African swine fever in Spain and the implementation of the eradication plan. It shall regularly inform, at least once a year, the Member States within the Committee of this development, in the light of the information given by the Spanish authorities and of any reports from experts who, acting on behalf of the Community and appointed by the Commission, have made on the spot visits.\n2. The Commission may suspend Community aid if it considers the development of the situation and the results obtained justify such a measure.\n3. Amendments made by the Spanish authorities to the plan as initially approved must also be approved in accordance with Article 4."], 
  "eurovoc_concepts": ["192", "2356", "2560", "862", "863"]
}
```

### Data Fields

The following data fields are provided for documents (`train`, `dev`, `test`):

`celex_id`: The official ID of the document. The CELEX number is the unique identifier for all publications in both Eur-Lex and CELLAR.\
`document_type`: The type of the document (e.g., Directive, Regulation, Decision)\
`title`: The title of the document.\
`header`: The first part of the document, which includes the title and name of the legal body enforcing the legal act.\
`recitals`: The second part of the document, which contains legal background references.\
`main_body`: The main part of the document, organized in articles or even bigger units (e.g., chapters, sections).\
`eurovoc_concepts`: The relevant EUROVOC concepts (labels).

For simplicity, we provide the full content (`text`) of each document, which is represented by its `header`, `recitals` and `main_body`.

If you want to use the descriptors of EUROVOC concepts, similar to Chalkidis et al. (2020), please load: https://archive.org/download/EURLEX57K/eurovoc_concepts.jsonl

```python
import json
with open('./eurovoc_concepts.jsonl') as jsonl_file:
    eurovoc_concepts =  {json.loads(concept) for concept in jsonl_file.readlines()}
```

### Data Splits

| Split         | No of Documents                         | Avg. words | Avg. labels |
| ------------------- | ------------------------------------  |  --- | --- |
| Train | 45,000 | 729 | 5 |
|Development | 6,000 | 714 | 5 |
|Test | 6,000 | 725 | 5 |

## Dataset Creation

### Curation Rationale

The dataset was curated by Chalkidis et al. (2019).\
The documents have been annotated by the Publications Office of EU (https://publications.europa.eu/en).

### Source Data

#### Initial Data Collection and Normalization

The original data are available at EUR-Lex portal (https://eur-lex.europa.eu) in an unprocessed format. 
The documents were downloaded from EUR-Lex portal in HTML format. 
The relevant metadata and EUROVOC concepts were downloaded from the SPARQL endpoint of the Publications Office of EU (http://publications.europa.eu/webapi/rdf/sparql).

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

* The original documents are available at EUR-Lex portal (https://eur-lex.europa.eu) in an unprocessed HTML format. The HTML code was striped and the documents split into sections. 
* The documents have been annotated by the Publications Office of EU (https://publications.europa.eu/en).


#### Who are the annotators?

Publications Office of EU (https://publications.europa.eu/en)

### Personal and Sensitive Information

The dataset does not include personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

N/A

### Discussion of Biases

N/A

### Other Known Limitations

N/A

## Additional Information

### Dataset Curators

Chalkidis et al. (2019)

### Licensing Information

© European Union, 1998-2021

The Commission’s document reuse policy is based on Decision 2011/833/EU. Unless otherwise specified, you can re-use the legal documents published in EUR-Lex for commercial or non-commercial purposes.

The copyright for the editorial content of this website, the summaries of EU legislation and the consolidated texts, which is owned by the EU, is licensed under the Creative Commons Attribution 4.0 International licence. This means that you can re-use the content provided you acknowledge the source and indicate any changes you have made.

Source: https://eur-lex.europa.eu/content/legal-notice/legal-notice.html \
Read more:  https://eur-lex.europa.eu/content/help/faq/reuse-contents-eurlex.html

### Citation Information

*Ilias Chalkidis, Manos Fergadiotis, Prodromos Malakasiotis and Ion Androutsopoulos.*
*Large-Scale Multi-Label Text Classification on EU Legislation.*
*Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL 2019). Florence, Italy. 2019*
```
@inproceedings{chalkidis-etal-2019-large,
    title = "Large-Scale Multi-Label Text Classification on {EU} Legislation",
    author = "Chalkidis, Ilias  and Fergadiotis, Manos  and Malakasiotis, Prodromos  and Androutsopoulos, Ion",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1636",
    doi = "10.18653/v1/P19-1636",
    pages = "6314--6322"
}
```

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.
