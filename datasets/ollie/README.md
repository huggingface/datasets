---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- other-university-of-washington-academic
multilinguality:
- monolingual
size_categories:
  ollie_lemmagrep:
  - 10M<n<100M
  ollie_patterned:
  - 1M<n<10M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-structured-to-text
- other-other-relation-extraction
paperswithcode_id: null
pretty_name: Ollie
---

# Dataset Card for Ollie

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

- **Homepage:** [Ollie](https://knowitall.github.io/ollie/)
- **Repository:** [Github](https://github.com/knowitall/ollie)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/D12-1048/)

### Dataset Summary

The Ollie dataset includes two configs for the data
used to train the Ollie informatation extraction algorithm, for 18M
sentences and 3M sentences respectively. 

This data is for academic use only. From the authors:

Ollie is a program that automatically identifies and extracts binary
relationships from English sentences. Ollie is designed for Web-scale
information extraction, where target relations are not specified in
advance.

Ollie is our second-generation information extraction system . Whereas
ReVerb operates on flat sequences of tokens, Ollie works with the
tree-like (graph with only small cycles) representation using
Stanford's compression of the dependencies. This allows Ollie to
capture expression that ReVerb misses, such as long-range relations.

Ollie also captures context that modifies a binary relation. Presently
Ollie handles attribution (He said/she believes) and enabling
conditions (if X then).

More information is available at the Ollie homepage:
https://knowitall.github.io/ollie/

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
en

## Dataset Structure

### Data Instances

There are two configurations for the dataset: ollie_lemmagrep which
are 18M sentences from web searches for a subset of the Reverb
relationships (110,000 relationships), and the 3M sentences for
ollie_patterned which is a subset of the ollie_lemmagrep dataset
derived from patterns according to the Ollie paper.

An example of an ollie_lemmagrep record:

``
{'arg1': 'adobe reader',
 'arg2': 'pdf',
 'chunk': 'B-NP I-NP I-NP I-NP B-PP B-NP I-NP B-VP B-PP B-NP I-NP O B-VP B-NP I-NP I-NP I-NP B-VP I-VP I-VP O',
 'pos': 'JJ NNS CC NNS IN PRP$ NN VBP IN NNP NN CC VB DT NNP NNP NNP TO VB VBN .',
 'rel': 'be require to view',
 'search_query': 'require reader pdf adobe view',
 'sentence': 'Many documents and reports on our site are in PDF format and require the Adobe Acrobat Reader to be viewed .',
 'sentence_cnt': '9',
 'words': 'many,document,and,report,on,our,site,be,in,pdf,format,and,require,the,adobe,acrobat,reader,to,be,view'}
``

An example of an ollie_patterned record:
``
{'arg1': 'english',
 'arg2': 'internet',
 'parse': '(in_IN_6), advmod(important_JJ_4, most_RBS_3); nsubj(language_NN_5, English_NNP_0); cop(language_NN_5, being_VBG_1); det(language_NN_5, the_DT_2); amod(language_NN_5, important_JJ_4); prep_in(language_NN_5, era_NN_9); punct(language_NN_5, ,_,_10); conj(language_NN_5, education_NN_12); det(era_NN_9, the_DT_7); nn(era_NN_9, Internet_NNP_8); amod(education_NN_12, English_JJ_11); nsubjpass(enriched_VBN_15, language_NN_5); aux(enriched_VBN_15, should_MD_13); auxpass(enriched_VBN_15, be_VB_14); punct(enriched_VBN_15, ._._16)',
 'pattern': '{arg1} <nsubj< {rel:NN} >prep_in> {slot0:NN} >nn> {arg2}',
 'rel': 'be language of',
 'search_query': 'english language internet',
 'sentence': 'English being the most important language in the Internet era , English education should be enriched .',
 'slot0': 'era'}
``


### Data Fields

For ollie_lemmagrep:
* rel: the relationship phrase/verb phrase. This may be empty, which represents the "be" relationship.
* arg1: the first argument in the relationship
* arg2: the second argument in the relationship.
* chunk: a tag of each token in the sentence, showing the pos chunks
* pos: part of speech tagging of the sentence
* sentence: the sentence
* sentence_cnt: the number of copies of this sentence encountered
* search_query: a combintion of rel, arg1, arg2
* words: the lemma of the words of the sentence separated by commas

For ollie_patterned:
* rel: the relationship phrase/verb phrase.
* arg1: the first argument in the relationship
* arg2: the second argument in the relationship.
* slot0: the third argument in the relationship, which might be empty.
* pattern: a parse pattern for the relationship
* parse: a dependency parse forthe sentence
* search_query: a combintion of rel, arg1, arg2
* sentence: the senence

### Data Splits

There are no splits. 

## Dataset Creation

### Curation Rationale

This dataset was created as part of research on open information extraction.

### Source Data

#### Initial Data Collection and Normalization

See the research paper on OLlie. The training data is extracted from web pages (Cluebweb09).  

#### Who are the source language producers?

The Ollie authors at the Univeristy of Washington and data from Cluebweb09 and the open web. 

### Annotations

#### Annotation process

The various parsers and code from the Ollie alogrithm.

#### Who are the annotators?

Machine annotated.

### Personal and Sensitive Information

Unkown, but likely there are names of famous individuals.

## Considerations for Using the Data

### Social Impact of Dataset

The goal for the work is to help machines learn to extract information form open domains.

### Discussion of Biases

Since the data is gathered from the web, there is likely to be biased text and relationships.

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The authors of Ollie at The University of Washington

### Licensing Information

The University of Washington academic license: https://raw.githubusercontent.com/knowitall/ollie/master/LICENSE


### Citation Information

```
@inproceedings{ollie-emnlp12,
  author = {Mausam and Michael Schmitz and Robert Bart and Stephen Soderland and Oren Etzioni},
  title = {Open Language Learning for Information Extraction},
  booktitle = {Proceedings of Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP-CONLL)},
  year = {2012}
}
```

### Contributions

Thanks to [@ontocord](https://github.com/ontocord) for adding this dataset.