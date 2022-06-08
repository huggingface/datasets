---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- es
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 100M<n<1B
- 10K<n<100K
- 10M<n<100M
- 1M<n<10M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-pretraining-language-models
paperswithcode_id: null
pretty_name: The Large Spanish Corpus
configs:
- DGT
- DOGC
- ECB
- EMEA
- EUBookShop
- Europarl
- GlobalVoices
- JRC
- NewsCommentary11
- OpenSubtitles2018
- ParaCrawl
- TED
- UN
- all_wikis
- combined
- multiUN
---

# Dataset Card for The Large Spanish Corpus

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

- **Homepage:** [https://github.com/josecannete/spanish-corpora](https://github.com/josecannete/spanish-corpora)
- **Repository:** [https://github.com/josecannete/spanish-corpora](https://github.com/josecannete/spanish-corpora)
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** [José Cañete](mailto:jose.canete@ug.uchile.cl) (corpus creator) or [Lewis Tunstall](mailto:lewis.c.tunstall@gmail.com) (corpus submitter)

### Dataset Summary

The Large Spanish Corpus is a compilation of 15 unlabelled Spanish corpora spanning Wikipedia to European parliament notes. Each config contains the data corresponding to a different corpus. For example, `all_wiki` only includes examples from Spanish Wikipedia:

```python
from datasets import load_dataset
all_wiki = load_dataset('large_spanish_corpus', name='all_wiki')
```

By default, the config is set to "combined" which loads all the corpora.



### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Spanish

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

The following is taken from the corpus' source repsository:

* Spanish Wikis: Which include Wikipedia, Wikinews, Wikiquotes and more. These were first processed with wikiextractor (https://github.com/josecannete/wikiextractorforBERT) using the wikis dump of 20/04/2019.

* ParaCrawl: Spanish portion of ParaCrawl (http://opus.nlpl.eu/ParaCrawl.php)

* EUBookshop: Spanish portion of EUBookshop (http://opus.nlpl.eu/EUbookshop.php)

* MultiUN: Spanish portion of MultiUN (http://opus.nlpl.eu/MultiUN.php)

* OpenSubtitles: Spanish portion of OpenSubtitles2018 (http://opus.nlpl.eu/OpenSubtitles-v2018.php)

* DGC: Spanish portion of DGT (http://opus.nlpl.eu/DGT.php)

* DOGC: Spanish portion of DOGC (http://opus.nlpl.eu/DOGC.php)

* ECB: Spanish portion of ECB (http://opus.nlpl.eu/ECB.php)

* EMEA: Spanish portion of EMEA (http://opus.nlpl.eu/EMEA.php)

* Europarl: Spanish portion of Europarl (http://opus.nlpl.eu/Europarl.php)

* GlobalVoices: Spanish portion of GlobalVoices (http://opus.nlpl.eu/GlobalVoices.php)

* JRC: Spanish portion of JRC (http://opus.nlpl.eu/JRC-Acquis.php)

* News-Commentary11: Spanish portion of NCv11 (http://opus.nlpl.eu/News-Commentary-v11.php)

* TED: Spanish portion of TED (http://opus.nlpl.eu/TED2013.php)

* UN: Spanish portion of UN (http://opus.nlpl.eu/UN.php)

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

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

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@lewtun](https://github.com/lewtun) for adding this dataset.
