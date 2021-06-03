---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- found
languages:
- de
- en
- es
- fr
- it
- ja
- nl
- pt
- ru
- zh
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
  conceptnet5:
  - 10M<n<100M
  omcs_sentences_free:
  - 100K<n<1M
  omcs_sentences_more:
  - 1M<n<10M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: conceptnet
---

# Dataset Card for Conceptnet5

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

- **Homepage:**
https://github.com/commonsense/conceptnet5/wiki
- **Repository:**
https://github.com/commonsense/conceptnet5/wiki
- **Paper:**
Robyn Speer, Joshua Chin, and Catherine Havasi. 2017. "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 31.o

### Dataset Summary

ConceptNet is a multilingual knowledge base, representing words and
phrases that people use and the common-sense relationships between
them. The knowledge in ConceptNet is collected from a variety of
resources, including crowd-sourced resources (such as Wiktionary and
Open Mind Common Sense), games with a purpose (such as Verbosity and
nadya.jp), and expert-created resources (such as WordNet and JMDict).

You can browse what ConceptNet knows at http://conceptnet.io.

This dataset is designed to provide training data
for common sense relationships pulls together from various sources.

The dataset is multi-lingual. See langauge codes and language info
here: https://github.com/commonsense/conceptnet5/wiki/Languages


This dataset provides an interface for the conceptnet5 csv file, and
some (but not all) of the raw text data used to build conceptnet5:
omcsnet_sentences_free.txt, and omcsnet_sentences_more.txt.

One use of this dataset would be to learn to extract the conceptnet
relationship from the omcsnet sentences.

Conceptnet5 has 34,074,917 relationships. Of those relationships,
there are 2,176,099 surface text sentences related to those 2M
entries.

omcsnet_sentences_free has 898,161 lines. omcsnet_sentences_more has
2,001,736 lines.

Original downloads are available here
https://github.com/commonsense/conceptnet5/wiki/Downloads. For more
information, see: https://github.com/commonsense/conceptnet5/wiki

The omcsnet data comes with the following warning from the authors of
the above site: 

Remember: this data comes from various forms of
crowdsourcing. Sentences in these files are not necessarily true,
useful, or appropriate.

### Languages
en, fr, it, de, es, ru, pt, ja, nl, zh and others

## Dataset Structure

### Data Instances

There are three configurations for the dataset: conceptnet5, omcs_sentences_free, omcs_sentences_more. 

Conceptnet5 defines:

``
{
	'sentence': ...,
	'full_rel': ...,
	'rel': ...,
	'arg1': ...,
	'arg2': ...,
	'lang': ...,
	'extra_info': ...
	'weight': ...
}
``

The omcs text defines:
``
{
	'sentence': ...,
	'raw_data': ...
	'weight': ...
}
``

### Data Fields

For conceptnet5 configurations:
* full_rel: the full relationship. e.g., /a/[/r/Antonym/,/c/en/able/,/c/en/cane/] 
* rel: the binary relationship. e.g., /r/Antonym      
* arg1: the first argument to the binary relationship. e.g., /c/en/able
* arg2: the second argument to the binary relationship. e.g., /c/en/cane      
* lang: the language code. e.g., en, fr, etc. If the arg1 and arg2 are two different languages, then the form os lang1/lang2.
* extra_info: a string that includes json data that has the dataset name, license type (mostly cc-4.0), contributor, etc. e.g., : {"dataset": "/d/verbosity", "license": "cc:by/4.0", "sources": [{"contributor": "/s/resource/verbosity"}], "surfaceEnd": "cane", "surfaceStart": "able", "surfaceText": "[[able]] is the opposite of [[cane]]", "weight": 0.299}
* sentence: the sentence from which the relationship was extracted, if one exists, with brackets around the arg1 and arg2. e.g., [[able]] is the opposite of [[cane]]
* weight: the weight assigned by the curators or automatically to the relationship, between 1.0-0.0, higher being more certain. 

For the omcs text configurations:

* sentence: the raw sentence
* raw_data: the raw tab seperated data of the form, id, text, curator_id, created_on, lanugage_id, activity_id, and score. Most of this information was tied to older systems for entering the data os was not partsed into fields for the dataset. e.g., 1237278 someone can be at catch 10805   2006-11-14 17:56:49.70872-05    en 27      1
* lang: the language code

### Data Splits

There are no splits. 

## Dataset Creation

### Curation Rationale

This dataset was gathered and created over many years for research in common sense reasoning. 

### Source Data

#### Initial Data Collection and Normalization

Started as the Open Mind Common Sense project at MIT Media Lab in 1999. See https://en.wikipedia.org/wiki/Open_Mind_Common_Sense

#### Who are the source language producers?

Crowd Sourced

### Annotations

#### Annotation process

Crowd Source template text, games, etc. 

#### Who are the annotators?

Crowd sourced.

### Personal and Sensitive Information

Unkown, but likely there are names of famous individuals.

## Considerations for Using the Data

### Social Impact of Dataset

The goal for the work is to help machines understand common sense.

### Discussion of Biases

See the website and paper for efforts to minimize data bias, but
please note that omcs_sentences_free, omcs_sentences_more are raw data
entered by users and may very well have biased data.


### Other Known Limitations

While the relationship dataset is large, the amount of actual sentences is limited.

## Additional Information

### Dataset Curators

The authors of https://github.com/commonsense/conceptnet5/wiki and Luminoso. 

### Licensing Information

This work includes data from ConceptNet 5, which was compiled by the
Commonsense Computing Initiative. ConceptNet 5 is freely available under
the Creative Commons Attribution-ShareAlike license (CC BY SA 3.0) from
http://conceptnet.io.

The included data was created by contributors to Commonsense Computing
projects, contributors to Wikimedia projects, DBPedia, OpenCyc, Games
with a Purpose, Princeton University's WordNet, Francis Bond's Open
Multilingual WordNet, and Jim Breen's JMDict.
Credits and acknowledgements
ConceptNet has been developed by:

The MIT Media Lab, through various groups at different times:

Commonsense Computing
Software Agents
Digital Intuition
The Commonsense Computing Initiative, a worldwide collaboration with contributions from:

National Taiwan University
Universidade Federal de São Carlos
Hokkaido University
Tilburg University
Nihon Unisys Labs
Dentsu Inc.
Kyoto University
Yahoo Research Japan
Luminoso Technologies, Inc.

Significant amounts of data were imported from:

WordNet, a project of Princeton University
Open Multilingual WordNet, compiled by Francis Bond and Kyonghee Paik
Wikipedia and Wiktionary, collaborative projects of the Wikimedia Foundation
Luis von Ahn's "Games with a Purpose"
JMDict, compiled by Jim Breen
CC-CEDict, by MDBG
The Unicode CLDR
DBPedia
Here is a short, incomplete list of people who have made significant contributions to the development of ConceptNet as a data resource, roughly in order of appearance:

Push Singh
Catherine Havasi
Hugo Liu
Hyemin Chung
Robyn Speer
Ken Arnold
Yen-Ling Kuo
Joshua Chin
Joanna Lowry-Duda
Robert Beaudoin
Naoki Otani
Vanya Cohen
Licenses for included resources
Commonsense Computing
The Commonsense Computing project originated at the MIT Media Lab and expanded worldwide. Tens of thousands of contributors have taken some time to teach facts to computers. Their pseudonyms can be found in the "sources" list found in ConceptNet's raw data and in its API.

Games with a Purpose
Data collected from Verbosity, one of the CMU "Games with a Purpose", is used and released under ConceptNet's license, by permission from Luis von Ahn and Harshit Surana.

Verbosity players are anonymous, so in the "sources" list, data from Verbosity is simply credited to the pseudonym "verbosity".

Wikimedia projects
ConceptNet uses data directly from Wiktionary, the free dictionary. It also uses data from Wikipedia, the free encyclopedia via DBPedia.

Wiktionary and Wikipedia are collaborative projects, authored by their respective online communities. They are currently released under the Creative Commons Attribution-ShareAlike license.

Wikimedia encourages giving attribution by providing links to the hosted pages that the data came from, and DBPedia asks for the same thing in turn. In addition to crediting the assertions that came from Wiktionary and DBPedia, we also provide "ExternalURL" edges pointing to the page that they came from. For example, the term /c/de/sprache has an ExternalURL link pointing to http://en.wiktionary.org/wiki/Sprache. Its list of individual contributors can be seen by following its "History" link.

The URLs of links to DBPedia are the same as the resource names that DBPedia uses, encouraging interoperability with their linked data.

WordNet
WordNet is available under an unencumbered license: see http://wordnet.princeton.edu/wordnet/license/. Its text is reproduced below:

WordNet Release 3.0

This software and database is being provided to you, the LICENSEE, by Princeton University under the following license. By obtaining, using and/or copying this software and database, you agree that you have read, understood, and will comply with these terms and conditions.:

Permission to use, copy, modify and distribute this software and database and its documentation for any purpose and without fee or royalty is hereby granted, provided that you agree to comply with the following copyright notice and statements, including the disclaimer, and that the same appear on ALL copies of the software, database and documentation, including modifications that you make for internal use or for distribution.

WordNet 3.0 Copyright 2006 by Princeton University. All rights reserved.

THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT- ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

The name of Princeton University or Princeton may not be used in advertising or publicity pertaining to distribution of the software and/or database. Title to copyright in this software, database and any associated documentation shall at all times remain with Princeton University and LICENSEE agrees to preserve same.

Open Multilingual WordNet
Open Multilingual WordNet was compiled by Francis Bond, Kyonghee Paik, and Ryan Foster, from data provided by many multilingual WordNet projects. Here is the complete list of references to the projects that created the data.


### Citation Information

Robyn Speer, Joshua Chin, and Catherine Havasi. 2017. "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 31.

### Contributions

Thanks to [@ontocord](https://github.com/ontocord) for adding this dataset.