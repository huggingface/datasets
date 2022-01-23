---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en-US
licenses:
- upl-1.0
multilinguality:
- monolingual
pretty_name: consumer-finance-complaints
size_categories:
- unknown
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
---

# Dataset Card for Consumer Finance Complaints

## Table of Contents
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

- **Homepage:**
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary


| Field      | name | Description | Data Type |
| ----------- | ----------- |----------- | ----------- |
| Date received | The date the CFPB received the complaint       | date & time       |        |
| Product   | The type of product the consumer identified in the complaint        | plain text        | This field is a categorical variable.        |
| Sub-product   | The type of sub-product the consumer identified in the complaint        | plain text        | This field is a categorical variable. Not all Products have Sub-products.        |
| Issue   | The issue the consumer identified in the complaint        | plain text        | This field is a categorical variable. Possible values are dependent on Product.        |
| Sub-issue   | The sub-issue the consumer identified in the complaint        | plain text        | This field is a categorical variable. Possible values are dependent on product and issue. Not all Issues have corresponding Sub-issues.        |
| Consumer complaint narrative   | Consumer complaint narrative is the consumer-submitted description of "what happened" from the complaint. Consumers must opt-in to share their narrative. We will not publish the narrative unless the consumer consents, and consumers can opt-out at any time. The CFPB takes reasonable steps to scrub personal information from each complaint that could be used to identify the consumer.        | plain text        | Consumers' descriptions of what happened are included if consumers consent to publishing the description and after we take steps to remove personal information.        |
| Company public response   | The company's optional, public-facing response to a consumer's complaint. Companies can choose to select a response from a pre-set list of options that will be posted on the public database. For example, "Company believes complaint is the result of an isolated error."        | plain text        | Companies' public-facing responses to complaints are included if companies choose to publish one. Companies may select a public response from a set list of options as soon as they respond to the complaint, but no later than 180 days after the complaint was sent to the company for response.        |
| Company   | The complaint is about this company        | plain text        | This field is a categorical variable.        |
| State   | The state of the mailing address provided by the consumer        | plain text        | This field is a categorical variable.        |
| ZIP code   | The mailing ZIP code provided by the consumer        | plain text        | Mailing ZIP code provided by the consumer. This field may: i) include the first five digits of a ZIP code; ii) include the first three digits of a ZIP code (if the consumer consented to publication of their complaint narrative); or iii) be blank (if ZIP codes have been submitted with non-numeric values, if there are less than 20,000 people in a given ZIP code, or if the complaint has an address outside of the United States). For example, complaints where the submitter reports the age of the consumer as 62 years or older are tagged, ‘Older American.’ Complaints submitted by or on behalf of a servicemember or the spouse or dependent of a servicemember are tagged, ‘Servicemember.’ Servicemember includes anyone who is active duty, National Guard, or Reservist, as well as anyone who previously served and is a Veteran or retiree.       |
| Tags   | Data that supports easier searching and sorting of complaints submitted by or on behalf of consumers.        | plain text        |         |
| Consumer consent provided?   | Identifies whether the consumer opted in to publish their complaint narrative. We do not publish the narrative unless the consumer consents and consumers can opt-out at any time.        | plain text        | This field shows whether a consumer provided consent to publish their complaint narrative        |
| Submitted via   | How the complaint was submitted to the CFPB        | plain text        | This field is a categorical variable.        |
| Date sent to company   | The date the CFPB sent the complaint to the company        | date & time        |         |
| Company response to consumer   | This is how the company responded. For example, "Closed with explanation."        | plain text        | This field is a categorical variable.        |
| Timely response?   | Whether the company gave a timely response        | plain text        | yes/no        |
| Consumer disputed?   | Whether the consumer disputed the company’s response        | plain text        | YES/ NO/ N/A: The Bureau discontinued the consumer dispute option on April 24, 2017.        |
| Complaint ID   | The unique identification number for a complaint        | number        |         |


### Supported Tasks and Leaderboards

Text Classification Tasks

| Task      | Label Name | Description | SOTA |
| ----------- | ----------- |----------- | ----------- |
| Text Classification      | Product| Predict the related product of a complaint | N/A |

| Task      | Label Name | Description | SOTA |
| ----------- | ----------- |----------- | ----------- |
| Text Classification      | Sub-Product| Predict the related sub product of a complaint | N/A |

| Task      | Label Name | Description | SOTA |
| ----------- | ----------- |----------- | ----------- |
| Text Classification      | Tags | Predict whether a complaint has been made by someone elderly or a service person| N/A |

### Languages

English

## Dataset Structure

### Data Instances

This dataset is a point in time extract of the database, the database increases in size every day

### Data Fields

[More Information Needed]

### Data Splits

This dataset only contains a TRAIN set - this can be further split into TRAIN, TEST and VALIDATE subsets with the datasets library

## Dataset Creation

### Curation Rationale

Open sourcing customer complaints

### Source Data

https://cfpb.github.io/api/ccdb/

#### Initial Data Collection and Normalization

This database is maintained by the Consumer Financial Protection Bureau

#### Who are the source language producers?

Englisgh

### Annotations

#### Annotation process

User submitted to the CFPB

#### Who are the annotators?

N/A

### Personal and Sensitive Information

All PII data has been anonymised

## Considerations for Using the Data

### Social Impact of Dataset

N/A

### Discussion of Biases

N/A

### Other Known Limitations

N/A

## Additional Information

### Dataset Curators

https://cfpb.github.io/api/ccdb/

### Licensing Information

https://cfpb.github.io/source-code-policy/

### Citation Information

N/A

### Contributions

Thanks to [@kayvane1](https://github.com/kayvane1) for adding this dataset and to the [Consumer Financial Protection Bureau](https://cfpb.github.io/) for publishing it.