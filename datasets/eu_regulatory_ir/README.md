---
annotations_creators:
- found

language_creators:
- found

languages:
- en

licenses:
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
- document-to-document-retrieval
---

# Dataset Card for the RegIR datasets

## Table of Contents
- [Dataset Card for the RegIR datasets](#dataset-card-for-ecthr-cases)
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

- **Homepage:** https://archive.org/details/eacl2021_regir_datasets
- **Repository:** https://archive.org/details/eacl2021_regir_datasets
- **Paper:** https://arxiv.org/abs/2101.10726
- **Leaderboard:** N/A
- **Point of Contact:** Ilias Chalkidis ( ihalk[at]aueb.gr )

### Dataset Summary

The European Union (EU) has a legislation scheme analogous to regulatory compliance for organizations. According to the Treaty on the Functioning of the European Union (TFEU), all published EU directives must take effect at the national level. Thus, all EU member states must adopt a law to transpose a newly issued directive within the period set by the directive (typically 2 years).

Here, we have two datasets, EU2UK and UK2EU, containing EU directives and UK regulations, which can serve both as queries and documents under the ground truth assumption that a UK law is relevant to the EU directives it transposes and vice versa.



### Supported Tasks and Leaderboards

The dataset supports:

**EU2UK**: Given an EU directive *Q*, retrieve the set of relevant documents from the pool of all available UK regulations. Relevant documents are those that transpose the EU directive (*Q*).

**UK2EU**: Given a UK regulation *Q*, retrieve the set of relevant documents from the pool of all available EU directives. Relevant documents are those that are being transposed by the UK regulations (*Q*).


### Languages

All documents are written in English.

## Dataset Structure

### Data Instances

```json
{
  "document_id": "31977L0794",
  "publication_year": "1977",
  "text": "Commission Directive 77/794/EEC of 4 November 1977 laying down detailed rules for implementing certain provisions of Directive 76/308/EEC on mutual assistance for the recovery of claims resulting from operations forming part of the system of financing the European Agricultural Guidance and Guarantee Fund, and of agricultural levies and customs duties\nHaving regard to the Treaty establishing the European Economic Community,\nHaving regard to Council Directive 76/308/EEC of 15 March 1976 on mutual assistance for the recovery of claims resulting from operations forming part of the system of financing the European Agricultural Guidance and Guarantee Fund, and of agricultural levies and customs duties (1), and in particular Article 22 (1) thereof,\nWhereas the abovementioned Directive introduced a system of mutual assistance between the competent authorities of Member States for the purpose of supplying the applicant authority with all the information which it needs, for notifying the addressee concerned of instruments and decisions which are applicable, for the taking of precautionary measures, and for the recovery by the requested authority of claims on behalf of the applicant authority;\nWhereas the detailed rules of operation of such mutual assistance must be laid down in each of these fields in order to render it fully effective;\nWhereas the measures provided for in this Directive are in accordance with the opinion of the Committee on Recovery,\nArticle 1\n1. This Directive lays the detailed rules for implementing Articles 4 (2) and (4), 5 (2) and (3), 7 (1), (3) and (5), 9 and 12 (1) of Directive 76/308/EEC, hereinafter called \"the basic Directive\".\n2. This Directive also lays down the detailed rules on conversion, transfer of sums recovered and the fixing of a minimum amount for claims which may give rise to a request for assistance.\nTITLE I Request for information\nArticle 2\n1. The request for information referred to in Article 4 of the basic Directive shall be made out in (1)OJ No L 73, 19.3.1976, p. 18.\nwriting in accordance with the model in Annex I. The said request shall bear the official stamp of the applicant authority and shall be signed by an official thereof duly authorized to make such a request.\n2. The applicant authority shall, where appropriate, indicate in its request for information the name of any other requested authority to which a similar request for information has been addressed.\nArticle 3\nThe request for information may relate to\n(a) the debtor ; or\n(b) any person liable for settlement of the claim under the law in force in the Member State where the applicant authority is situated.\nWhere the applicant authority knows that a third party holds assets belonging to one of the persons mentioned in the foregoing paragraph, the request may also relate to that third party.\nArticle 4\nThe requested authority shall acknowledge receipt of the request for information in writing (if possible by telex) as soon as possible and in any event within seven days of such receipt.\nArticle 5\n1. The requested authority shall transmit each item of requested information to the applicant authority as and when it is obtained.\n2. Where all or part of the requested information cannot be obtained within a reasonable time, having regard to the particular case, the requested authority shall so inform the applicant authority, indicating the reasons therefor.\nIn any event, at the end of six months from the date of acknowledgement of receipt of the request, the requested authority shall inform the applicant authority of the outcome of the investigations which it has conducted in order to obtain the information requested.\nIn the light of the information received from the requested authority, the applicant authority may request the latter to continue its investigations. This request shall be made in writing (if possible by telex) within two months from the receipt of the notification of the outcome of the investigations carried out by the requested authority, and shall be treated by the requested authority in accordance with the provisions applying to the initial request.\nArticle 6\nWhen the requested authority decides not to comply with the request for information addressed to it, it shall notify the applicant authority in writing of the reasons for the refusal to comply with the request, specifying the particular provisions of Article 4 of the basic Directive which it invokes. This notification shall be given by the requested authority as soon as it has taken its decision and in any event within six months from the date of the acknowledgement of the receipt of the request.\nArticle 7\nThe applicant authority may at any time withdraw the request for information which it has sent to the requested authority. The decision to withdraw shall be transmitted to the requested authority in writing (if possible by telex).\nTITLE II Request for notification\nArticle 8\nThe request for notification referred to in Article 5 of the basic Directive shall be made out in writing in duplicate in accordance with the model in Annex II. The said request shall bear the official stamp of the applicant authority and shall be signed by an official thereof duly authorized to make such a request.\nTwo copies of the instrument (or decision), notification of which is requested, shall be attached to the request referred to in the foregoing paragraph.\nArticle 9\nThe request for notification may relate to any natural or legal person who, in accordance with the law in force in the Member State where the applicant authority is situated, shall be informed of any instrument or decision which concerns him.\nArticle 10\n1. Immediately upon receipt of the request for notification, the requested authority shall take the necessary measures to effect that notification in accordance with the law in force in the Member State in which it is situated.\n2. The requested authority shall inform the applicant authority of the date of notification as soon as this has been done, by returning to it one of the copies of its request with the certificate on the reverse side duly completed.\nTITLE III Request for recovery and/or for the taking of precautionary measures\nArticle 11\n1. The request for recovery and/or for the taking of precautionary measures referred to in Articles 6 and 13 of the basic Directive shall be made out in writing in accordance with the model Annex III. The request, which shall include a declaration that the conditions laid down in the basic Directive for initiating the mutual assistance procedure in the particular case have been fulfilled, shall bear the official stamp of the applicant authority and shall be signed by an official thereof duly authorized to make such a request.\n2. The instrument permitting enforcement which shall accompany the request for recovery and/or for the taking of precautionary measures may be issued in respect of several claims where it concerns one and the same person.\nFor the purposes of Articles 12 to 19, all claims which are covered by the same instrument permitting enforcement shall be deemed to constitute a single claim.\nArticle 12\n1. The request for recovery and/or for the taking of precautionary measures may relate to (a) the debtor ; or\n(b) any person liable for settlement of the claim under the law in force in the Member State in which it is situated.\n2. Where appropriate, the applicant authority shall inform the requested authority of any assets of the persons referred to in paragraph 1 which to its knowledge are held by a third party.\nArticle 13\n1. The applicant authority shall state the amounts of the claim to be recovered both in the currency of the Member State in which it is situated and also in the currency of the Member State in which the requested authority is situated.\n2. The rate of exchange to be used for the purposes of paragraph 1 shall be the latest selling rate recorded on the most representative exchange market or markets of the Member State in which the applicant authority is situated on the date when the request for recovery is signed.\nArticle 14\nThe requested authority shall acknowledge receipt of the request for recovery and/or for the taking of precautionary measures in writing (if possible by telex) as soon as possible and in any event within seven days of its receipt.\nArticle 15\nWhere, within a reasonable time having regard to the particular case, all or part of the claim cannot be recovered or precautionary measures cannot be taken, the requested authority shall so inform the applicant authority, indicating the reasons therefor.\nIn any event, at the end of one year from the date of acknowledgement of the receipt of the request, the requested authority shall inform the applicant authority of the outcome of the procedure which it has undertaken for recovery and/or for the taking of precautionary measures.\nIn the light of the information received from the requested authority, the applicant authority may request the latter to continue the procedure which it has undertaken for recovery and/or for the taking of precautionary measures. This request shall be made in writing (if possible by telex) within two months from the receipt of the notification of the outcome of the procedure undertaken by the requested authority for recovery and/or for the taking of precautionary measures, and shall be treated by the requested authority in accordance with the provisions applying to the initial request.\nArticle 16\nAny action contesting the claim or the instrument permitting its enforcement which is taken in the Member State in which the applicant authority is situated shall be notified to the requested authority in writing (if possible by telex) by the applicant authority immediately after it has been informed of such action.\nArticle 17\n1. If the request for recovery and/or for the taking of precautionary measures becomes nugatory as a result of payment of the claim or of its cancellation or for any other reason, the applicant authority shall immediately inform the requested authority in writing (if possible by telex) so that the latter may stop any action which it has undertaken.\n2. Where the amount of the claim which is the subject of the request for recovery and/or for the taking of precautionary measures is amended for any reason, the applicant authority shall immediately inform the requested authority in writing (if possible by telex).\nIf the amendment consists of a reduction in the amount of the claim, the requested authority shall continue the action which it has undertaken with a view to recovery and/or to the taking of precautionary measures, but that action shall be limited to the amount still outstanding if, at the time the requested authority is informed of the reduction of the amount of the claim, the original amount has already been recovered by it but the transfer procedure referred to in Article 18 has not yet been initiated, the requested authority shall repay the amount overpaid to the person entitled thereto.\nIf the amendment consists of an increase in the amount of the claim, the applicant authority shall as soon as possible address to the requested authority an additional request for recovery and/or for the taking of precautionary measures. This additional request shall, as far as possible be dealt with by the requested authority at the same time as the original request of the applicant authority. Where, in view of the state of progress of the existing procedure, the joinder of the additional request and the original request is not possible, the requested authority shall only be required to comply with the additional request if it concerns an amount not less than that referred to in Article 20.\n3. To convert the amended amount of the claim into the currency of the Member State in which the requested authority is situated, the applicant authority shall use the exchange rate used in its original request.\nArticle 18\nAny sum recovered by the requested authority, including, where applicable, the interest referred to in Article 9 (2) of the basic Directive, shall be the subject of a transfer to the applicant authority in the currency of the Member State in which the requested authority is situated. This transfer shall take place within one month of the date on which the recovery was effected.\nArticle 19\nIrrespective of any amounts collected by the requested authority by way of interest referred to in Article 9 (2) of the basic Directive, the claim shall be deemed to have been recovered in proportion to the recovery of the amount expressed in the national currency of the Member State in which the requested authority is situated, on the basis of the exchange rate referred to in Article 13 (2).\nTITLE IV General and final provisions\nArticle 20\n1. A request for assistance may be made by the applicant authority in respect of either a single claim or several claims where these are recoverable from one and the same person.\n2. No request for assistance may be made if the amount of the relevant claim or claims is less than 750 European units of account.\nArticle 21\nInformation and other particulars communicated by the requested authority to the applicant authority shall be made out in the official language or one of the official languages of the Member State in which the requested authority is situated.\nArticle 22\nThe Member States shall bring into force not later than 1 January 1978 the measures necessary to comply with this Directive.\nArticle 23\nEach Member State shall inform the Commission of the measures which it takes for implementing this Directive. The Commission shall communicate such information to the other Member States.\nArticle 24\nThis Directive is addressed to the Member States." ,
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

N/A

### Discussion of Biases

N/A

### Other Known Limitations

N/A

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
