---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
language:
- es
license:
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
dataset_info:
- config_name: JRC
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 380895504
    num_examples: 3410620
  download_size: 4099166669
  dataset_size: 380895504
- config_name: EMEA
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 100259598
    num_examples: 1221233
  download_size: 4099166669
  dataset_size: 100259598
- config_name: GlobalVoices
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 114435784
    num_examples: 897075
  download_size: 4099166669
  dataset_size: 114435784
- config_name: ECB
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 336285757
    num_examples: 1875738
  download_size: 4099166669
  dataset_size: 336285757
- config_name: DOGC
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 898279656
    num_examples: 10917053
  download_size: 4099166669
  dataset_size: 898279656
- config_name: all_wikis
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 3782280549
    num_examples: 28109484
  download_size: 4099166669
  dataset_size: 3782280549
- config_name: TED
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 15858148
    num_examples: 157910
  download_size: 4099166669
  dataset_size: 15858148
- config_name: multiUN
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 2327269369
    num_examples: 13127490
  download_size: 4099166669
  dataset_size: 2327269369
- config_name: Europarl
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 359897865
    num_examples: 2174141
  download_size: 4099166669
  dataset_size: 359897865
- config_name: NewsCommentary11
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 48350573
    num_examples: 288771
  download_size: 4099166669
  dataset_size: 48350573
- config_name: UN
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 23654590
    num_examples: 74067
  download_size: 4099166669
  dataset_size: 23654590
- config_name: EUBookShop
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1326861077
    num_examples: 8214959
  download_size: 4099166669
  dataset_size: 1326861077
- config_name: ParaCrawl
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 1840430234
    num_examples: 15510649
  download_size: 4099166669
  dataset_size: 1840430234
- config_name: OpenSubtitles2018
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 7477281776
    num_examples: 213508602
  download_size: 4099166669
  dataset_size: 7477281776
- config_name: DGT
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 396217351
    num_examples: 3168368
  download_size: 4099166669
  dataset_size: 396217351
- config_name: combined
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 19428257807
    num_examples: 302656160
  download_size: 4099166669
  dataset_size: 19428257807
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