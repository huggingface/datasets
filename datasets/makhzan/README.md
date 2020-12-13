annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ur
licenses:
- other-my-license
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling

# Dataset Card for makhzan

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** https://matnsaz.net/en/makhzan
- **Repository:** https://github.com/zeerakahmed/makhzan
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** Zeerak Ahmed

### Dataset Summary

An Urdu text corpus for machine learning, natural language processing and linguistic analysis.


### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

[Needs More Information]

## Dataset Structure

### Data Instances

```

```

### Data Fields
```file_id (str)```: Document file_id corresponding to filename in repository.

```metadata(str)```: XML formatted string containing metadata on the document such as the document's title, information about the author and publication, as well as other potentially useful facts such as the number of Urdu words in the document and whether the document contains text in any other languages.

```title (str)```: Title of the document.

```num-words (int)```: Number of words in document.

```contains-non-urdu-languages (str)```: ```Yes``` if document contains words other than urdu, ```No``` otherwise.

```document_body```: XML formatted body of the document. Details below:

The document is divided into ```<section>``` elements. In general the rule is that a clear visual demarkation in the original text (such as a page break, or a horizontal rule) is used to indicate a section break. A heading does not automatically create a new section.

Each paragraph is a ```<p>``` element.

Headings are wrapped in an ```<heading>``` element.

Blockquotes are wrapped in a ```<blockquote>``` element. Blockquotes may themselves contain other elements.

Lists are wrapped in an ```<list>```. Individual items in each list are wrapped in an ```<li>``` element.

Poetic verses are wrapped in a ```<verse>``` element. Each verse is on a separate line but is not wrapped in an individual element.

Tables are wrapped in a ```<table>``` element. A table is divided into rows marked by ```<tr>``` and columns marked by ```<td>```.

Text not in the Urdu language is wrapped in an ```<annotation>``` tag (more below).

```<p>, <heading>, <li>, <td>``` and ```<annotation>``` tags are inline with the text (i.e. there is no new line character before and after the tag). Other tags have a new line after the opening and before the closing tag.

Due to the use of XML syntax, ```<```, ```>``` and ```&``` characters have been escaped as ```&lt```;, ```&gt```;, and ```&amp```; respectively. This includes the use of these characters in URLs inside metadata.

### Data Splits

All the data is in one split ```train```
## Dataset Creation

### Curation Rationale

All text in this repository has been selected for quality of language, upholding high editorial standards. Given the poor quality of most published Urdu text in digital form, this selection criteria allows the use of this text for natural language processing, and machine learning applications without the need to address fundamental quality issues in the text.

We have made efforts to ensure this text is as broadly representative as possible. Specifically we have attempted to select for as many authors as possible, and diversity in the gender of the author, as well as years and city of publication. This effort is imperfect, and we appreciate any attempts at pointing us to resources that can help diversify this text further.

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?
Makhzan has been started with generous initial donations of text from two renowned journals  Bunyad, from the Gurmani Center of Literature and Languages at the Lahore University of Management Sciences (LUMS), and Ishraq, from the Al-Mawrid Institute. This choice of sources allowed us to get a diversity of voices even in a small initial corpus, while ensuring the highest editorial standards available in published Urdu text. As a result your models can also maintain high linguistic standards.

### Annotations

#### Annotation process
Text is structured and annotated using XML syntax. The ontology of elements used is loosely based around HTML, with simplifications made when HTML's specificity is not needed, and additions made to express common occurences in this corpus that would be useful for linguistic analysis. The semantic tagging of text is editorial in nature, which is to say that another person semantically tagging the text may do so differently. Effort has been made however to ensure consistency, and to retain the original meaning of the text while making it easy to parse through linguistically different pieces of text for analysis.


Annotations have been made inline using an ```<annotation>``` element.
A language (lang) attribute is added to the ```<annotation>``` element to indicate text in other languages (such as quoted text or technical vocabulary presented in other languages and scripts). The attribute value a two-character ISO 639-1 code. So the resultant annotation for an Arabic quote for example, will be ```<annotation lang="ar"></annotation>```.
A type (type) attributed is added to indicate text that is not in a language per se but is not Urdu text. URLs for example are wrapped in an ```<annotation type="url">``` tag.


#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

A few of the files do not have valid XML and cannot be loaded. This issue is tracked [here](https://github.com/zeerakahmed/makhzan/issues/28)

## Additional Information

### Dataset Curators

Zeerak Ahmed

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]
