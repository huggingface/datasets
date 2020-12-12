---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- conditional-text-generation
- text-retrieval
task_ids:
- entity-linking-retrieval
- fact-checking-retrieval
- other-stuctured-to-text
---

# Dataset Card for Never Ending Language Learning (NELL)

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

- **Homepage:**
http://rtw.ml.cmu.edu/rtw/
- **Repository:**
http://rtw.ml.cmu.edu/rtw/
- **Paper:**
Never-Ending Learning.
T. Mitchell, W. Cohen, E. Hruschka, P. Talukdar, J. Betteridge, A. Carlson, B. Dalvi, M. Gardner, B. Kisiel, J. Krishnamurthy, N. Lao, K. Mazaitis, T. Mohamed, N. Nakashole, E. Platanios, A. Ritter, M. Samadi, B. Settles, R. Wang, D. Wijaya, A. Gupta, X. Chen, A. Saparov, M. Greaves, J. Welling. In Proceedings of the Conference on Artificial Intelligence (AAAI), 2015

### Dataset Summary

This dataset provides version 1115 of the belief
extracted by CMU's Never Ending Language Learner (NELL) and version
1110 of the candidate belief extracted by NELL. See
http://rtw.ml.cmu.edu/rtw/overview.  NELL is an open information
extraction system that attempts to read the Clueweb09 of 500 million
web pages (http://boston.lti.cs.cmu.edu/Data/clueweb09/) and general
web searches.

The dataset has 4 configurations: nell_belief, nell_candidate,
nell_belief_sentences, and nell_candidate_sentences. nell_belief is
certainties of belief are lower. The two sentences config extracts the
CPL sentence patterns filled with the applicable 'best' literal string
for the entities filled into the sentence patterns. And also provides
sentences found using web searches containing the entities and
relationships.

There are roughly 21M entries for nell_belief_sentences, and 100M
sentences for nell_candidate_sentences.

From the NELL website:

- **Research Goal**
To build a never-ending machine learning system that acquires the ability to extract structured information from unstructured web pages. If successful, this will result in a knowledge base (i.e., a relational database) of structured information that mirrors the content of the Web. We call this system NELL (Never-Ending Language Learner).

- **Approach**
The inputs to NELL include (1) an initial ontology defining hundreds of categories (e.g., person, sportsTeam, fruit, emotion) and relations (e.g., playsOnTeam(athlete,sportsTeam), playsInstrument(musician,instrument)) that NELL is expected to read about, and (2) 10 to 15 seed examples of each category and relation.

Given these inputs, plus a collection of 500 million web pages and access to the remainder of the web through search engine APIs, NELL runs 24 hours per day, continuously, to perform two ongoing tasks:

Extract new instances of categories and relations. In other words, find noun phrases that represent new examples of the input categories (e.g., "Barack Obama" is a person and politician), and find pairs of noun phrases that correspond to instances of the input relations (e.g., the pair "Jason Giambi" and "Yankees" is an instance of the playsOnTeam relation). These new instances are added to the growing knowledge base of structured beliefs.
Learn to read better than yesterday. NELL uses a variety of methods to extract beliefs from the web. These are retrained, using the growing knowledge base as a self-supervised collection of training examples. The result is a semi-supervised learning method that couples the training of hundreds of different extraction methods for a wide range of categories and relations. Much of NELL’s current success is due to its algorithm for coupling the simultaneous training of many extraction methods.

For more information, see: http://rtw.ml.cmu.edu/rtw/resources

### Languages
en, and perhaps some others

## Dataset Structure

### Data Instances

There are four configurations for the dataset: nell_belief, nell_candidate, nell_belief_sentences, nell_candidate_sentences. 

nell_belief and nell_candidate defines:

``
{
	'entity': ...,
	'relation': ...,
	'value': ...,
	'iteration_of_promotion': ...,o
	'probability': ...,
	'entity_literal_strings': ...,
	'value_literal_strings': ...
	'best_entity_literal_string': ...
	'best_value_literal_string': ...
	'categories_for_entity': ...
	'categories_for_value': ...
	'candidate_source': ...
}
``

nell_belief_sentences, nell_candidate_sentences defines:

``
{
	'entity': ...,
	'relation': ...,
	'value': ...,
	'sentence': ...,
	'probability': ...,
	'url': ...
	'count': ...
	'sentence_type': ...
}
``

### Data Fields

For nell_belief and nell_canddiate configurations. From http://rtw.ml.cmu.edu/rtw/faq:
* entity: The Entity part of the (Entity, Relation, Value) tripple. Note that this will be the name of a concept and is not the literal string of characters seen by NELL from some text source, nor does it indicate the category membership of that concept
* relation: The Relation part of the (Entity, Relation, Value) tripple. In the case of a category instance, this will be "generalizations". In the case of a relation instance, this will be the name of the relation.
* value: The Value part of the (Entity, Relation, Value) tripple. In the case of a category instance, this will be the name of the category. In the case of a relation instance, this will be another concept (like Entity).
* iteration_of_promotion: The point in NELL's life at which this category or relation instance was promoted to one that NELL beleives to be true. This is a non-negative integer indicating the number of iterations of bootstrapping NELL had gone through.
* probability: A confidence score for the belief. Note that NELL's scores are not actually probabilistic at this time.
* source: A summary of the provenance for the belief indicating the set of learning subcomponents (CPL, SEAL, etc.) that had submitted this belief as being potentially true.
* entity_literal_strings: The set of actual textual strings that NELL has read that it believes can refer to the concept indicated in the Entity column.
* value_literal_strings: For relations, the set of actual textual strings that NELL has read that it believes can refer to the concept indicated in the Value column. For categories, this should be empty but may contain something spurious.
* best_entity_literal_string: Of the set of strings in the Entity literalStrings, column, which one string can best be used to describe the concept.
* best_value_literal_string: Same thing, but for Value literalStrings.
* categories_for_entity: The full set of categories (which may be empty) to which NELL belives the concept indicated in the Entity column to belong.
* categories_for_value: For relations, the full set of categories (which may be empty) to which NELL believes the concept indicated in the Value column to belong. For categories, this should be empty but may contain something spurious.
* candidate_source: A free-form amalgamation of more specific provenance information describing the justification(s) NELL has for possibly believing this category or relation instance.

For the nell_belief_sentences and nell_candidate_sentences, we have extracted the underlying sentences, sentence count and URLs and provided a shortened version of the entity, relation and value field by removing the string "concept:" and "candidate:". There are two types of sentences, 'CPL' and 'OE', which are generated by two of the modules of NELL, pattern matching and open web searching, respectively. There may be duplicates. The configuration is as follows:
* entity: The Entity part of the (Entity, Relation, Value) tripple. Note that this will be the name of a concept and is not the literal string of characters seen by NELL from some text source, nor does it indicate the category membership of that concept
* relation: The Relation part of the (Entity, Relation, Value) tripple. In the case of a category instance, this will be "generalizations". In the case of a relation instance, this will be the name of the relation.
* value: The Value part of the (Entity, Relation, Value) tripple. In the case of a category instance, this will be the name of the category. In the case of a relation instance, this will be another concept (like Entity).
* probability: A confidence score for the belief. Note that NELL's scores are not actually probabilistic at this time.
* sentence: the raw sentence. For 'CPL' type sentences, there are "[[" "]]" arounds the entity and value. For 'OE' type sentences, there are no "[[" and "]]".
* url: the url if there is one from which this sentence was extracted
* count: the count for this sentence
* sentence_type: either 'CPL' or 'OE'

### Data Splits

There are no splits. 

## Dataset Creation

### Curation Rationale

This dataset was gathered and created over many years of running the NELL system on web data.

### Source Data

#### Initial Data Collection and Normalization

See the research paper on NELL. NELL searches a subset of the web
(Clueweb09) and the open web using various open information extraction
algorithms, including pattern matching.

#### Who are the source language producers?

The NELL authors at Carnegie Mellon Univiersty and data from Cluebweb09 and the open web. 

### Annotations

#### Annotation process

The various open information extraction modules of NELL.

#### Who are the annotators?

Machine annotated.

### Personal and Sensitive Information

Unkown, but likely there are names of famous individuals.

## Considerations for Using the Data

### Social Impact of Dataset

The goal for the work is to help machines learn to read and understand the web.

### Discussion of Biases

Since the data is gathered from the web, there is likely to be biased text and relationships.

### Other Known Limitations

The relationships and concepts gathered from NELL are not 100% accurate, and there could be errors (maybe as high as 30% error). 
See https://en.wikipedia.org/wiki/Never-Ending_Language_Learning

We did not 'tag' the entity and value in the 'OE' sentences, and this might be an extension in the future.

## Additional Information

### Dataset Curators

The authors of NELL at Carnegie Mellon Univeristy

### Licensing Information

There does not appear to be a license on http://rtw.ml.cmu.edu/rtw/resources. The data is made available by CMU on the web. 

### Citation Information

Never-Ending Learning.
T. Mitchell, W. Cohen, E. Hruschka, P. Talukdar, J. Betteridge, A. Carlson, B. Dalvi, M. Gardner, B. Kisiel, J. Krishnamurthy, N. Lao, K. Mazaitis, T. Mohamed, N. Nakashole, E. Platanios, A. Ritter, M. Samadi, B. Settles, R. Wang, D. Wijaya, A. Gupta, X. Chen, A. Saparov, M. Greaves, J. Welling. In Proceedings of the Conference on Artificial Intelligence (AAAI), 2015


