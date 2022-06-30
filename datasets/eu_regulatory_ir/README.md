---
annotations_creators:
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
- text-retrieval
task_ids:
- document-retrieval
- text-retrieval-other-document-to-document-retrieval
paperswithcode_id: null
pretty_name: the RegIR datasets
---

# Dataset Card for the RegIR datasets

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

- **Homepage:** https://archive.org/details/eacl2021_regir_datasets
- **Repository:** https://archive.org/details/eacl2021_regir_datasets
- **Paper:** https://arxiv.org/abs/2101.10726
- **Leaderboard:** N/A
- **Point of Contact:** [Ilias Chalkidis](mailto:ihalk@aueb.gr)

### Dataset Summary

The European Union (EU) has a legislation scheme analogous to regulatory compliance for organizations. According to the Treaty on the Functioning of the European Union (TFEU), all published EU directives must take effect at the national level. Thus, all EU member states must adopt a law to transpose a newly issued directive within the period set by the directive (typically 2 years).

Here, we have two datasets, EU2UK and UK2EU, containing EU directives and UK regulations, which can serve both as queries and documents under the ground truth assumption that a UK law is relevant to the EU directives it transposes and vice versa.



### Supported Tasks and Leaderboards

The dataset supports:

**EU2UK** (`eu2uk`): Given an EU directive *Q*, retrieve the set of relevant documents from the pool of all available UK regulations. Relevant documents are those that transpose the EU directive (*Q*).

**UK2EU** (`uk2eu`): Given a UK regulation *Q*, retrieve the set of relevant documents from the pool of all available EU directives. Relevant documents are those that are being transposed by the UK regulations (*Q*).


### Languages

All documents are written in English.

## Dataset Structure

### Data Instances

```json
{
  "document_id": "31977L0794",
  "publication_year": "1977",
  "text": "Commission Directive 77/794/EEC ... of agricultural levies and customs duties",
  "relevant_documents": ["UKPGA19800048", "UKPGA19770036"]
}
```

### Data Fields

The following data fields are provided for query documents (`train`, `dev`, `test`):

`document_id`: (**str**) The ID of the document.\
`publication_year`: (**str**) The publication year of the document.\
`text`: (**str**) The text of the document.\
`relevant_documents`: (**List[str]**)  The list of relevant documents, as represented by their `document_id`.

The following data fields are provided for corpus documents (`corpus`):

`document_id`: (**str**) The ID of the document.\
`publication_year`: (**str**) The publication year of the document.\
`text`: (**str**) The text of the document.\

### Data Splits

#### EU2UK dataset

| Split         | No of Queries                        | Avg. relevant documents |
| ------------------- | ------------------------------------  |  --- |
| Train | 1,400 | 1.79 |
|Development | 300 | 2.09 |
|Test | 300  | 1.74 |
Document Pool (Corpus): 52,515 UK regulations

#### UK2EU dataset

| Split         | No of Queries                         | Avg. relevant documents |
| ------------------- | ------------------------------------  |  --- |
| Train | 1,500 | 1.90 |
|Development | 300 | 1.46 |
|Test | 300  | 1.29 |
Document Pool (Corpus): 3,930 EU directives

## Dataset Creation

### Curation Rationale

The dataset was curated by Chalkidis et al. (2021).\
The transposition pairs are publicly available by the Publications Office of EU (https://publications.europa.eu/en).

### Source Data

#### Initial Data Collection and Normalization

The original data are available at EUR-Lex portal (https://eur-lex.europa.eu) and Legislation.GOV.UK (http://legislation.gov.uk/) in an unprocessed format.\
The transposition pairs are provided by the EU member states (in our case, UK) and were downloaded from the SPARQL endpoint of the Publications Office of EU (http://publications.europa.eu/webapi/rdf/sparql).\
For more information on the dataset curation, read Chalkidis et al. (2021).

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

* The original data are available at EUR-Lex portal (https://eur-lex.europa.eu) and Legislation.GOV.UK (http://legislation.gov.uk/) in an unprocessed format.
* The transposition pairs are provided by the EU member states (in our case, UK) and were downloaded from the SPARQL endpoint of the Publications Office of EU (http://publications.europa.eu/webapi/rdf/sparql).


#### Who are the annotators?

Publications Office of EU (https://publications.europa.eu/en)

### Personal and Sensitive Information

The dataset does not include personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Chalkidis et al. (2021)

### Licensing Information

**EU Data**

© European Union, 1998-2021

The Commission’s document reuse policy is based on Decision 2011/833/EU. Unless otherwise specified, you can re-use the legal documents published in EUR-Lex for commercial or non-commercial purposes.

The copyright for the editorial content of this website, the summaries of EU legislation and the consolidated texts, which is owned by the EU, is licensed under the Creative Commons Attribution 4.0 International licence​​ . This means that you can re-use the content provided you acknowledge the source and indicate any changes you have made.

Source: https://eur-lex.europa.eu/content/legal-notice/legal-notice.html \
Read more:  https://eur-lex.europa.eu/content/help/faq/reuse-contents-eurlex.html

**UK Data**

You are encouraged to use and re-use the Information that is available under this licence freely and flexibly, with only a few conditions.

You are free to:

- copy, publish, distribute and transmit the Information;
- adapt the Information;
- exploit the Information commercially and non-commercially for example, by combining it with other Information, or by including it in your own product or application.

You must (where you do any of the above):

acknowledge the source of the Information in your product or application by including or linking to any attribution statement specified by the Information Provider(s) and, where possible, provide a link to this licence: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/.

### Citation Information

*Ilias Chalkidis, Manos Fergadiotis, Nikos Manginas, Eva Katakalou and Prodromos Malakasiotis.*
*Regulatory Compliance through Doc2Doc Information Retrieval: A case study in EU/UK legislation where text similarity has limitations* 
*Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021). Online. 2021*
```
@inproceedings{chalkidis-etal-2021-regir,
    title = "Regulatory Compliance through Doc2Doc Information Retrieval: A case study in EU/UK legislation where text similarity has limitations",
    author = "Chalkidis, Ilias  and Fergadiotis, Manos and Manginas, Nikos and Katakalou, Eva,  and Malakasiotis, Prodromos",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021)",
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/2101.10726",
}
```

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.
