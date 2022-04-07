---
pretty_name: ATOMIC
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- other-structured-to-text
paperswithcode_id: atomic
---

# Dataset Card for An Atlas of Machine Commonsense for If-Then Reasoning - Atomic Common Sense Dataset

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
https://homes.cs.washington.edu/~msap/atomic/
- **Repository:**
https://homes.cs.washington.edu/~msap/atomic/
- **Paper:**
Maarten Sap, Ronan LeBras, Emily Allaway, Chandra Bhagavatula, Nicholas Lourie, Hannah Rashkin, Brendan Roof, Noah A. Smith & Yejin Choi (2019). ATOMIC: An Atlas of Machine Commonsense for If-Then Reasoning. AAAI

### Dataset Summary

This dataset provides the template sentences and
relationships defined in the ATOMIC common sense dataset. There are
three splits - train, test, and dev.

From the authors.

Disclaimer/Content warning: the events in atomic have been
automatically extracted from blogs, stories and books written at
various times. The events might depict violent or problematic actions,
which we left in the corpus for the sake of learning the (probably
negative but still important) commonsense implications associated with
the events. We removed a small set of truly out-dated events, but
might have missed some so please email us (msap@cs.washington.edu) if
you have any concerns.


For more information, see: https://homes.cs.washington.edu/~msap/atomic/

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
en

## Dataset Structure

### Data Instances

Here is one example from the atomic dataset:


`` 
{'event': "PersonX uses PersonX's ___ to obtain", 'oEffect': [], 'oReact': ['annoyed', 'angry', 'worried'], 'oWant': [], 'prefix': ['uses', 'obtain'], 'split': 'trn', 'xAttr': [], 'xEffect': [], 'xIntent': ['to have an advantage', 'to fulfill a desire', 'to get out of trouble'], 'xNeed': [], 'xReact': ['pleased', 'smug', 'excited'], 'xWant': []}
``


### Data Fields

Notes from the authors:

* event: just a string representation of the event.
* oEffect,oReact,oWant,xAttr,xEffect,xIntent,xNeed,xReact,xWant: annotations for each of the dimensions, stored in a json-dumped string.
  Note: "none" means the worker explicitly responded with the empty response, whereas [] means the worker did not annotate this dimension.
* prefix: json-dumped string that represents the prefix of content words (used to make a better trn/dev/tst split).
* split: string rep of which split the event belongs to.

### Data Splits

The atomic dataset has three splits: test, train and dev of the form:

## Dataset Creation

### Curation Rationale

This dataset was gathered and created over to assist in common sense reasoning.

### Source Data

#### Initial Data Collection and Normalization

See the reaserch paper and website for more detail. The dataset was
created by the University of Washington using crowd sourced data


#### Who are the source language producers?

The Atomic authors and crowd source.

### Annotations

#### Annotation process

Human annotations directed by forms.

#### Who are the annotators?

Human annotations.

### Personal and Sensitive Information

Unkown, but likely none.

## Considerations for Using the Data

### Social Impact of Dataset

The goal for the work is to help machines understand common sense.

### Discussion of Biases

Since the data is human annotators, there is likely to be baised. From the authors:


Disclaimer/Content warning: the events in atomic have been automatically extracted from blogs, stories and books written at various times. The events might depict violent or problematic actions, which we left in the corpus for the sake of learning the (probably negative but still important) commonsense implications associated with the events. We removed a small set of truly out-dated events, but might have missed some so please email us (msap@cs.washington.edu) if you have any concerns.


### Other Known Limitations

While there are many relationships, the data is quite sparse. Also, each item of the dataset could be expanded into multiple sentences along the vsrious dimensions, oEffect, oRect, etc.

For example, given event: "PersonX uses PersonX's ___ to obtain" and dimension oReact: "annoyed", this could be transformed into an entry:

"PersonX uses PersonX's ___ to obtain => PersonY is annoyed"

## Additional Information

### Dataset Curators

The authors of Aotmic at The University of Washington

### Licensing Information

The Creative Commons Attribution 4.0 International License. https://creativecommons.org/licenses/by/4.0/

### Citation Information

@article{Sap2019ATOMICAA,
  title={ATOMIC: An Atlas of Machine Commonsense for If-Then Reasoning},
  author={Maarten Sap and Ronan Le Bras and Emily Allaway and Chandra Bhagavatula and Nicholas Lourie and Hannah Rashkin and Brendan Roof and Noah A. Smith and Yejin Choi},
  journal={ArXiv},
  year={2019},
  volume={abs/1811.00146}
}

### Contributions

Thanks to [@ontocord](https://github.com/ontocord) for adding this dataset.