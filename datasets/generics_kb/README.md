---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
  generics_kb:
  - 1M<n<10M
  generics_kb_best:
  - 1M<n<10M
  generics_kb_simplewiki:
  - 10K<n<100K
  generics_kb_waterloo:
  - 1M<n<10M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-knowledge-base
paperswithcode_id: genericskb
---

# Dataset Card for Generics KB

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

- **Homepage:** [Homepage](https://allenai.org/data/genericskb)
- **Repository:** [Repository](https://drive.google.com/drive/folders/1vqfVXhJXJWuiiXbUa4rZjOgQoJvwZUoT)
- **Paper:** [Paper](https://arxiv.org/pdf/2005.00660.pdf)
- **Point of Contact:**[Sumithra Bhakthavatsalam](sumithrab@allenai.org)
                        [Chloe Anastasiades](chloea@allenai.org)
                        [Peter Clark](peterc@allenai.org)
                        Alternatively email_at info@allenai.org


### Dataset Summary

Dataset contains a large (3.5M+ sentence) knowledge base of *generic sentences*.  This is the first large resource to contain *naturally occurring* generic sentences, rich in high-quality, general, semantically complete statements. All GenericsKB sentences are annotated with their topical term, surrounding context (sentences), and a (learned) confidence. We also release GenericsKB-Best (1M+ sentences), containing the best-quality generics in GenericsKB augmented with selected, synthesized generics from WordNet and ConceptNet. This demonstrates that GenericsKB can be a useful resource for NLP applications, as well as providing data for linguistic studies of generics and their semantics.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

The GENERICSKB contains 3,433,000 sentences. GENERICS-KB-BEST comprises of GENERICSKB generics with a score > 0.234, augmented with short generics synthesized from three other resources for all the terms (generic categories) in GENERICSKB- BEST. GENERICSKB-BEST contains 1,020,868 generics (774,621 from GENERICSKB plus 246,247 synthesized).
SimpleWikipedia is a filtered scrape of SimpleWikipedia pages (simple.wikipedia.org). The Waterloo corpus is 280GB of English plain text, gathered by Charles Clarke (Univ. Waterloo) using a webcrawler in 2001 from .edu domains.

###### Sample SimpleWikipedia/ Waterloo config look like this
```
{'source_name': 'SimpleWikipedia', 'sentence': 'Sepsis happens when the bacterium enters the blood and make it form tiny clots.', 'sentences_before': [], 'sentences_after': [], 'concept_name': 'sepsis', 'quantifiers': {}, 'id': 'SimpleWikipedia--tmp-sw-rs1-with-bug-fixes-initialprocessing-inputs-articles-with-clean-sentences-jsonl-c27816b298e1e0b5326916ee4e2fd0f1603caa77-100-Bubonic-plague--Different-kinds-of-the-same-disease--Septicemic-plague-0-0-039fbe9c11adde4ff9a829376ca7e0ed-1560874903-47882-/Users/chloea/Documents/aristo/commonsense/kbs/simplewikipedia/commonsense-filtered-good-rs1.jsonl-1f33b1e84018a2b1bfdf446f9a6491568b5585da-1561086091.8220549', 'bert_score': 0.8396177887916565}
```
###### Sample instance for Generics KB datasets look like this:
```
{'source': 'Waterloo', 'term': 'aardvark', 'quantifier_frequency': '', 'quantifier_number': '', 'generic_sentence': 'Aardvarks are very gentle animals.', 'score': '0.36080607771873474'}
{'source': 'TupleKB', 'term': 'aardvark', 'quantifier_frequency': '', 'quantifier_number': '', 'generic_sentence': 'Aardvarks dig burrows.', 'score': '1.0'}
```
### Data Fields

The fields in GenericsKB-Best.tsv and GenericsKB.tsv are as follows:
- `SOURCE`: denotes the source of the generic
- `TERM`: denotes the category that is the topic of the generic.
- `GENERIC SENTENCE`: is the sentence itself.
- `SCORE`: Is the BERT-trained score, measuring the degree to which the generic represents a "useful, general truth" about the world (as judged by crowdworkers). Score ranges from 0 (worst) to 1 (best). Sentences with scores below 0.23 (corresponding to an "unsure" vote by crowdworkers) are in GenericsKB, but are not part of GenericsKB-Best due to their unreliability.
- `QUANTIFIER_FREQUENCY`:For generics with explicit quantifiers (all, most, etc.) the quantifier is listed - Frequency contains values  such as 'usually', 'often', 'frequently'
- `QUANTIFIER_NUMBER`: For generics with explicit quantifiers (all, most, etc.) with values such as 'all'|'any'|'most'|'much'|'some' etc...

The SimpleWiki/Waterloo generics from GenericsKB.tsv, but expanded to also include their surrounding context (before/after sentences). The Waterloo generics are the majority of GenericsKB. This zip file is 1.4GB expanding to 5.5GB.
There is a json representation for every generic statement in the Generics KB. The generic statement is stored under the `sentence` field within the `knowledge` object. There is also a `bert_score` associated with each sentence which is the BERT-based classifier's score for the 'genericness' of the statement. This score is meant to reflect how much generalized world knowledge/commonsense the statement captures vs only being contextually meaningful.
Detailed description of each of the fields:

- `source_name`: The name of the corpus the generic statement was picked from.
- `sentence`: The generic sentence.
- `sentences_before`: Provides context information surrounding the generic statement from the original corpus.Up to five sentences preceding the generic sentence in the original corpus.
- `sentences_after`: Up to five sentences following the generic sentence in the original corpus.
- `concept_name`: A concept that is the subject of the generic statement.
- `quantifiers`: The quantifiers for the key concept of the generic statement. There can be multiple quantifiers to allow for statements such as "All bats sometimes fly", where 'all' and 'sometimes' are both quantifiers reflecting number and frequency respectively. 
- `id`: Unique identifier for a generic statement in the kb.
- `bert_score`: Score for the generic statement from the BERT-based generics classifier.
<br>**Additional fields that apply only to SimpleWiki dataset**
    - `headings`: A breadcrumb of section/subsection headings from the top down to the location of the generic statement in the corpus. It applies to SimpleWikipedia which has a hierarchical structure.
    - `categories`:The listed categories under which the source article falls. Applies to SimpleWikipedia.


### Data Splits

There are no splits. 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Data was crawled. SimpleWikipedia is a filtered scrape of SimpleWikipedia pages (simple.wikipedia.org). The Waterloo corpus is 280GB of English plain text, gathered by Charles Clarke (Univ. Waterloo) using a webcrawler in 2001 from .edu domains.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

Bert was used to decide whether the sentence is useful or not. Every sentence has a bert score.

#### Who are the annotators?

No annotations were made. 

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The GenericsKB is available under the Creative Commons - Attribution 4.0 International - licence.

As an informal summary, from https://creativecommons.org/licenses/by/4.0/, you are free to:

	Share ― copy and redistribute the material in any medium or format
	Adapt ― remix, transform, and build upon the material for any purpose, even commercially.

under the following terms:

	Attribution ― You must give appropriate credit, provide a link to the license, and
		indicate if changes were made. You may do so in any reasonable manner,
		but not in any way that suggests the licensor endorses you or your use.
	No additional restrictions ― You may not apply legal terms or technological measures
		that legally restrict others from doing anything the license permits.

For details, see https://creativecommons.org/licenses/by/4.0/ or the or the included
file "Creative Commons ― Attribution 4.0 International ― CC BY 4.0.pdf" in this folder.

### Citation Information
```
@InProceedings{huggingface:dataset,
title = {GenericsKB: A Knowledge Base of Generic Statements},
authors={Sumithra Bhakthavatsalam, Chloe Anastasiades, Peter Clark},
year={2020},
publisher = {Allen Institute for AI},
}
```

### Contributions

Thanks to [@bpatidar](https://github.com/bpatidar) for adding this dataset.