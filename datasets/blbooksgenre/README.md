---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- expert-generated
language:
- en
- de
- fr
- nl
license:
- cc0-1.0
multilinguality:
- multilingual
pretty_name: British Library Books Genre
size_categories:
- 10K<n<100K
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
- text-generation
- fill-mask
task_ids:
- topic-classification
- multi-label-classification
- language-modeling
- masked-language-modeling
configs:
- annotated_raw
- raw
- title_genre_classifiction
---

# Dataset Card for blbooksgenre

## Table of Contents

- [Dataset Card for blbooksgenre](#dataset-card-for-blbooksgenre)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
      - [Supervised tasks](#supervised-tasks)
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
      - [Colonialism](#colonialism)
    - [Other Known Limitations](#other-known-limitations)
  - [Additional Information](#additional-information)
    - [Dataset Curators](#dataset-curators)
    - [Licensing Information](#licensing-information)
    - [Citation Information](#citation-information)
    - [Contributions](#contributions)

## Dataset Description

- **Homepage:**: [https://doi.org/10.23636/BKHQ-0312](https://doi.org/10.23636/BKHQ-0312)
- **Repository:** [https://doi.org/10.23636/BKHQ-0312](https://doi.org/10.23636/BKHQ-0312)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

This dataset consists of metadata relating to books [digitised by the British Library in partnership with Microsoft](https://www.bl.uk/collection-guides/google-books-digitised-printed-heritage). Some of this metadata was exported from the British Library catalogue whilst others was generated as part of a crowdsourcing project. The text of this book and other metadata can be found on the [date.bl](https://data.bl.uk/bl_labs_datasets/#3) website.

The majority of the books in this collection were published in the 18th and 19th Century but the collection also includes a smaller number of books from earlier periods. Items within this collection cover a wide range of subject areas including geography, philosophy, history, poetry and literature and are published in a variety of languages.

For the subsection of the data which contains additional crowsourced annotations the date of publication breakdown is as follows:

|      | Date of publication |
| ---- | ------------------- |
| 1630 | 8                   |
| 1690 | 4                   |
| 1760 | 10                  |
| 1770 | 5                   |
| 1780 | 5                   |
| 1790 | 18                  |
| 1800 | 45                  |
| 1810 | 96                  |
| 1820 | 152                 |
| 1830 | 182                 |
| 1840 | 259                 |
| 1850 | 400                 |
| 1860 | 377                 |
| 1870 | 548                 |
| 1880 | 776                 |
| 1890 | 1484                |
| 1900 | 17                  |
| 1910 | 1                   |
| 1970 | 1                   |

[More Information Needed]


### Supported Tasks and Leaderboards

The digitised books collection which this dataset describes has been used in a variety of digital history and humanities projects since being published.

This dataset is suitable for a variety of unsupervised tasks and for a 'genre classification task'.

#### Supervised tasks

The main possible use case for this dataset is to develop and evaluate 'genre classification' models. The dataset includes human generated labels for whether a book is 'fiction' or 'non-fiction'. This has been used to train models for genre classifcation which predict whether a book is 'fiction' or 'non-fiction' based on its title. 

### Languages

[More Information Needed]

## Dataset Structure

The dataset currently has three configurations intended to support a range of tasks for which this dataset could be used for:

- `title_genre_classifiction` : this creates a de-duplicated version of the dataset with the `BL record`, `title` and `label`.
- `annotated_raw`:  This version of the dataset includes all fields from the original dataset which are annotated.  This includes duplication from different annotators"
- `raw`: This version of the dataset includes all the data from the original data including data without annotations. 

### Data Instances

An example data instance from the `title_genre_classifiction` config:

```python
{'BL record ID': '014603046',
 'title': 'The Canadian farmer. A missionary incident [Signed: W. J. H. Y, i.e. William J. H. Yates.]',
 'label': 0}
```

An example data instance from the `annotated_raw` config:

```python
{'BL record ID': '014603046',
 'Name': 'Yates, William Joseph H.',
 'Dates associated with name': '',
 'Type of name': 'person',
 'Role': '',
 'All names': ['Yates, William Joseph H. [person] ', ' Y, W. J. H. [person]'],
 'Title': 'The Canadian farmer. A missionary incident [Signed: W. J. H. Y, i.e. William J. H. Yates.]',
 'Variant titles': '',
 'Series title': '',
 'Number within series': '',
 'Country of publication': ['England'],
 'Place of publication': ['London'],
 'Publisher': '',
 'Date of publication': '1879',
 'Edition': '',
 'Physical description': 'pages not numbered, 21 cm',
 'Dewey classification': '',
 'BL shelfmark': 'Digital Store 11601.f.36. (1.)',
 'Topics': '',
 'Genre': '',
 'Languages': ['English'],
 'Notes': 'In verse',
 'BL record ID for physical resource': '004079262',
 'classification_id': '267476823.0',
 'user_id': '15.0',
 'subject_ids': '44369003.0',
 'annotator_date_pub': '1879',
 'annotator_normalised_date_pub': '1879',
 'annotator_edition_statement': 'NONE',
 'annotator_FAST_genre_terms': '655 7 ‡aPoetry‡2fast‡0(OCoLC)fst01423828',
 'annotator_FAST_subject_terms': '60007 ‡aAlice,‡cGrand Duchess, consort of Ludwig IV, Grand Duke of Hesse-Darmstadt,‡d1843-1878‡2fast‡0(OCoLC)fst00093827',
 'annotator_comments': '',
 'annotator_main_language': '',
 'annotator_other_languages_summaries': 'No',
 'annotator_summaries_language': '',
 'annotator_translation': 'No',
 'annotator_original_language': '',
 'annotator_publisher': 'NONE',
 'annotator_place_pub': 'London',
 'annotator_country': 'enk',
 'annotator_title': 'The Canadian farmer. A missionary incident [Signed: W. J. H. Y, i.e. William J. H. Yates.]',
 'Link to digitised book': 'http://access.bl.uk/item/viewer/ark:/81055/vdc_00000002842E',
 'annotated': True,
 'Type of resource': 0,
 'created_at': datetime.datetime(2020, 8, 11, 14, 30, 33),
 'annotator_genre': 0}
```

### Data Fields

The data fields differ slightly between configs. All possible fields for the `annotated_raw` config are listed below. For the `raw` version of the dataset datatypes are usually string to avoid errors when processing missing values.

- `BL record ID`: an internal ID used by the British Library, this can be useful for linking this data to other BL collections.
- `Name`: name associated with the item (usually author)
- `Dates associated with name`: dates associated with above e.g. DOB
- `Type of name`: whether `Name` is a person or an organization etc. 
- `Role`: i.e. whether `Name` is `author`, `publisher` etc.
- `All names`: a fuller list of names associated with the item.
- `Title`: The title of the work
- `Variant titles`
- `Series title`
- `Number within series`
- `Country of publication`: encoded as a list of countries listed in the metadata
- `Place of publication`:  encoded as a list of places listed in the metadata 
- `Publisher`
- `Date of publication`: this is encoded as a string since this field can include data ranges i.e.`1850-1855`. 
- `Edition`
- `Physical description`: encoded as a string since the format of this field varies
- `Dewey classification`
- `BL shelfmark`: a British Library shelf mark
- `Topics`: topics included in the catalogue record
- `Genre` the genre information included in the original catalogue record note that this is often missing 
- Languages`; encoded as a list of languages 
- `Notes`: notes from the catalogue record
- `BL record ID for physical resource`

The following fields are all generated via the crowdsourcing task (discussed in more detail below)

- `classification_id`: ID for the classification in the annotation task
- `user_id` ID for the annotator
- `subject_ids`: internal annotation task ID
- `annotator_date_pub`: an updated publication data
- `annotator_normalised_date_pub`: normalized version of the above
- `annotator_edition_statement` updated edition 
- `annotator_FAST_genre_terms`: [FAST classification genre terms](https://www.oclc.org/research/areas/data-science/fast.html)
- `annotator_FAST_subject_terms`: [FAST subject terms](https://www.oclc.org/research/areas/data-science/fast.html)
- `annotator_comments`: free form comments 
- `annotator_main_language`
- `annotator_other_languages_summaries` 
- `'annotator_summaries_language`
- `annotator_translation`
- `annotator_original_language`
- `annotator_publisher`
- `annotator_place_pub`
- `annotator_country`
- `annotator_title`
- `Link to digitised book`
- `annotated`: `bool` flag to indicate if row has annotations or not
- `created_at`: when the annotation was created
- `annotator_genre`: the updated annotation for the `genre` of the book.

Finally the `label` field of the `title_genre_classifiction` configuration  is a class label with values 0 (Fiction) or 1 (Non-fiction).

[More Information Needed]

### Data Splits

This dataset contains a single split `train`.

## Dataset Creation

**Note** this section is a work in progress.

### Curation Rationale

The books in this collection were digitised as part of a project partnership between the British Library and Microsoft. [Mass digitisation](https://en.wikipedia.org/wiki/Category:Mass_digitization) i.e. projects where there is a goal to quickly digitise large volumes of materials shape the selection of materials to include in a number of ways. Some consideratoins which are often involved in the decision of whether to include items for digitization include (but are not limited to):

- copyright status
- preservation needs- the size of an item, very large and very small items are often hard to digitize quickly

These criteria can have knock-on effects on the makeup of a collection. For example systematically excluding large books may result in some types of book content not being digitized. Large volumes are likely to be correlated to content to at least some extent so excluding them from digitization will mean that material is under represented. Similarly copyright status is often (but not only) determined by publication data. This can often lead to a rapid fall in the number of items in a collection after a certain cut-off date.

All of the above is largely to make clear that this collection was not curated with the aim of creating a representative sample of the British Library's holdings. Some material will be over-represented and other under-represented. Similarly, the collection should not be considered a representative sample of what was published across the time period covered by the dataset (nor that that the relative proportions of the data for each time period represent a proportional sample of publications from that period). 

[More Information Needed]

### Source Data

The original source data (physical items) includes a variety of resources (predominantly monographs) held by the [British Library](bl.uk/](https://bl.uk/). The British Library is a [Legal Deposit](https://www.bl.uk/legal-deposit/about-legal-deposit) library. "Legal deposit requires publishers to provide a copy of every work they publish in the UK to the British Library. It's existed in English law since 1662."[source](https://www.bl.uk/legal-deposit/about-legal-deposit).

[More Information Needed]

#### Initial Data Collection and Normalization

This version of the dataset was created partially from data exported from British Library catalogue records and partially via data generated from a crowdsourcing task involving British Library staff.

#### Who are the source language producers?

[More Information Needed]

### Annotations

The data does includes metadata associated with the books these are produced by British Library staff. The additional annotations were carried out during 2020 as part of an internal crowdsourcing task.

#### Annotation process

New annotations were produced via a crowdsourcing tasks. Annotators have the option to pick titles from a particular language subset from the broader digitized 19th century books collection. As a result the annotations are not random and overrepresent some languages.

[More Information Needed]

#### Who are the annotators?

Staff working at the British Library. Most of these staff work with metadata as part of their jobs and so could be considered expert annotators. 

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

There a range of considerations around using the data. These include the representativeness of the dataset, the bias towards particular languages etc. 

It is also important to note that library metadata is not static. The metadata held in library catalogues is updated and changed over time for a variety of reasons. 

The way in which different institutions catalogue items also varies. As a result it is important to evaluate the performance of any models trained on this data before applying to a new collection.

[More Information Needed]

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

The text in this collection is derived from historic text. As a result the text will reflect to social beliefs and attitudes of this time period. The titles of the book give some sense of their content. Examples of book titles which appear in the data (these are randomly sampled from all titles):

- 'Rhymes and Dreams, Legends of Pendle Forest, and other poems',
 - "Précis of Information concerning the Zulu Country, with a map. Prepared in the Intelligence Branch of the Quarter-Master-General's Department, Horse Guards, War Office, etc",
- 'The fan. A poem',
- 'Grif; a story of Australian Life',
- 'Calypso; a masque: in three acts, etc', 
- 'Tales Uncle told [With illustrative woodcuts.]',
- 'Questings',
- 'Home Life on an Ostrich Farm. With ... illustrations',
- 'Bulgarya i Bulgarowie', 
- 'Εἰς τα βαθη της Ἀφρικης [In darkest Africa.] ... Μεταφρασις Γεωρ. Σ. Βουτσινα, etc',
- 'The Corsair, a tale',
  'Poems ... With notes [With a portrait.]',
- 'Report of the Librarian for the year 1898 (1899, 1901, 1909)',
- "The World of Thought. A novel. By the author of 'Before I began to speak.'",
- 'Amleto; tragedia ... recata in versi italiani da M. Leoni, etc']

Whilst using titles alone, is obviously insufficient to integrate bias in this collection it gives some insight into the topics covered by books in the corpus. Further looking into the tiles highlight some particular types of bias we might find in the collection. This should in no way be considered an exhaustive list.

#### Colonialism

We can see even in the above random sample of titles examples of colonial attitudes. We can try and interrogate this further by searching for the name of countries which were part of the British Empire at the time many of these books were published.

Searching for the string `India` in the titles and randomly sampling 10 titles returns:

- "Travels in India in the Seventeenth Century: by Sir Thomas Roe and Dr. John Fryer. Reprinted from the 'Calcutta Weekly Englishman.'",
- 'A Winter in India and Malaysia among the Methodist Missions',
- "The Tourist's Guide to all the principal stations on the railways of Northern India [By W. W.] ... Fifth edition",
- 'Records of Sport and Military Life in Western India ... With an introduction by ... G. B. Malleson',
- "Lakhmi, the Rájpút's Bride. A tale of Gujarát in Western India [A poem.]",
- 'The West India Commonplace Book: compiled from parliamentary and official documents; shewing the interest of Great Britain in its Sugar Colonies',
- "From Tonkin to India : by the sources of the Irawadi, January '95-January '96",
- 'Case of the Ameers of Sinde : speeches of Mr. John Sullivan, and Captain William Eastwick, at a special court held at the India House, ... 26th January, 1844',
- 'The Andaman Islands; their colonization, etc. A correspondence addressed to the India Office',
- 'Ancient India as described by Ptolemy; being a translation of the chapters which describe India and Eastern Asia in the treatise on Geography written by Klaudios Ptolemaios ... with introduction, commentary, map of India according to Ptolemy, and ... index, by J. W. McCrindle']

Searching form the string `Africa` in the titles and randomly sampling 10 titles returns:

- ['De Benguella ás Terras de Iácca. Descripção de uma viagem na Africa Central e Occidental ... Expedição organisada nos annos de 1877-1880. Edição illustrada',
- 'To the New Geographical Society of Edinburgh [An address on Africa by H. M. Stanley.]',
- 'Diamonds and Gold in South Africa ... With maps, etc',
- 'Missionary Travels and Researches in South Africa ... With notes by F. S. Arnot. With map and illustrations. New edition',
- 'A Narrative of a Visit to the Mauritius and South Africa ... Illustrated by two maps, sixteen etchings and twenty-eight wood-cuts',
- 'Side Lights on South Africa ... With a map, etc',
- 'My Second Journey through Equatorial Africa ... in ... 1886 and 1887 ... Translated ... by M. J. A. Bergmann. With a map ... and ... illustrations, etc',
- 'Missionary Travels and Researches in South Africa ... With portrait and fullpage illustrations',
- '[African sketches.] Narrative of a residence in South Africa ... A new edition. To which is prefixed a biographical sketch of the author by J. Conder',
- 'Lake Ngami; or, Explorations and discoveries during four years wandering in the wilds of South Western Africa ... With a map, and numerous illustrations, etc']

Whilst this dataset doesn't include the underlying text it is important to consider the potential attitudes represented in the title of the books, or the full text if you are using this dataset in conjunction with the full text.

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The books are licensed under the [CC Public Domain Mark 1.0](https://creativecommons.org/publicdomain/mark/1.0/) license.

### Citation Information

```bibtex
@misc{british library_genre, 
title={ 19th Century Books - metadata with additional crowdsourced annotations}, 
url={https://doi.org/10.23636/BKHQ-0312},
author={{British Library} and  Morris, Victoria and van Strien, Daniel and Tolfo, Giorgia and Afric, Lora and Robertson, Stewart and Tiney, Patricia and Dogterom, Annelies and Wollner, Ildi},
year={2021}}
```

### Contributions

Thanks to [@davanstrien](https://github.com/davanstrien) for adding this dataset.
