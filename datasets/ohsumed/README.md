---
pretty_name: Ohsumed
annotations_creators:
- human-annotated
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-label-classification
paperswithcode_id: null
---

# Dataset Card for ohsumed

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

- **Homepage: http://davis.wpi.edu/xmdv/datasets/ohsumed.html**
- **Repository: https://trec.nist.gov/data/filtering/t9.filtering.tar.gz**
- **Paper: https://link.springer.com/chapter/10.1007/978-1-4471-2099-5_20**
- **Leaderboard:**
- **Point of Contact: [William Hersh](mailto:hersh@OHSU.EDU) [Aakash Gupta](mailto:aakashg80@gmail.com)**

### Dataset Summary

The OHSUMED test collection is a set of 348,566 references from
MEDLINE, the on-line medical information database, consisting of
titles and/or abstracts from 270 medical journals over a five-year
period (1987-1991). The available fields are title, abstract, MeSH
indexing terms, author, source, and publication type. The National
Library of Medicine has agreed to make the MEDLINE references in the
test database available for experimentation, restricted to the
following conditions:

1. The data will not be used in any non-experimental clinical,
library, or other setting.
2.  Any human users of the data will explicitly be told that the data
is incomplete and out-of-date.

Please check this [readme](https://trec.nist.gov/data/filtering/README.t9.filtering) for more details


### Supported Tasks and Leaderboards

[Text Classification](https://paperswithcode.com/sota/text-classification-on-ohsumed)

### Languages

The text is primarily in English. The BCP 47 code is `en`

## Dataset Structure

### Data Instances

```
{'seq_id': 7770,
  'medline_ui': 87120420,
  'mesh_terms': 'Adult; Aged; Aneurysm/CO; Arteriovenous Fistula/*TH; Carotid Arteries; Case Report; Female; Human; Jugular Veins; Male; Methods; Middle Age; Neck/*BS; Vertebral Artery.',
  'title': 'Arteriovenous fistulas of the large vessels of the neck: nonsurgical percutaneous occlusion.',
  'publication_type': 'JOURNAL ARTICLE.',
  'abstract': 'We describe the nonsurgical treatment of arteriovenous fistulas of the large vessels in the neck using three different means of endovascular occlusion of these large lesions, which are surgically difficult to approach and treat.',
  'author': 'Vitek JJ; Keller FS.',
  'source': 'South Med J 8705; 80(2):196-200'}

```


### Data Fields

Here are the field definitions:

- seg_id: sequential identifier 
   (important note: documents should be processed in this order)
- medline_ui: MEDLINE identifier (UI) 
   (<DOCNO> used for relevance judgements)
 - mesh_terms: Human-assigned MeSH terms (MH)
- title: Title (TI)
- publication_type : Publication type (PT)
- abstract: Abstract (AB)
- author: Author (AU)
- source: Source (SO)

Note: some abstracts are truncated at 250 words and some references
have no abstracts at all (titles only). We do not have access to the
full text of the documents.

### Data Splits

The files are Train/ Test. Where the training has files from 1987 while the test files has abstracts from 1988-91

Total number of files:
Train: 54710
Test: 348567


## Dataset Creation

### Curation Rationale

The OHSUMED document collection was obtained by William Hersh
(hersh@OHSU.EDU) and colleagues for the experiments described in the
papers below. [Check citation](#citation-information)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The test collection was built as part of a study assessing the use of
MEDLINE by physicians in a clinical setting (Hersh and Hickam, above).
Novice physicians using MEDLINE generated 106 queries. Only a subset
of these queries were used in the TREC-9 Filtering Track. Before
they searched, they were asked to provide a statement of information
about their patient as well as their information need.
The data was collected by William Hersh & colleagues

### Annotations

#### Annotation process

The existing OHSUMED topics describe actual information needs, but the
relevance judgements probably do not have the same coverage provided
by the TREC pooling process. The MeSH terms do not directly represent
information needs, rather they are controlled indexing terms. However,
the assessment should be more or less complete and there are a lot of
them, so this provides an unusual opportunity to work with a very
large topic sample.

The topic statements are provided in the standard TREC format 

#### Who are the annotators?

Each query was replicated by four searchers, two physicians
experienced in searching and two medical librarians.  The results were
assessed for relevance by a different group of physicians, using a
three point scale: definitely, possibly, or not relevant.  The list of
documents explicitly judged to be not relevant is not provided here.
Over 10% of the query-document pairs were judged in duplicate to
assess inter-observer reliability.  For evaluation, all documents
judged here as either possibly or definitely relevant were
considered relevant.  TREC-9 systems were allowed to distinguish
between these two categories during the learning process if desired.

### Personal and Sensitive Information

No PII data is present in the train, test or query files. 

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[Aakash Gupta](mailto:aakashg80@gmail.com) 
*Th!nkEvolve Consulting* and Researcher at CoronaWhy

### Licensing Information

CC BY-NC 4.0

### Citation Information

Hersh WR, Buckley C, Leone TJ, Hickam DH, OHSUMED: An interactive
retrieval evaluation and new large test collection for research, 
Proceedings of the 17th Annual ACM SIGIR Conference, 1994, 192-201.

Hersh WR, Hickam DH, Use of a multi-application computer workstation
in a clinical setting, Bulletin of the Medical Library Association,
1994, 82: 382-389.

### Contributions

Thanks to [@skyprince999](https://github.com/skyprince999) for adding this dataset.